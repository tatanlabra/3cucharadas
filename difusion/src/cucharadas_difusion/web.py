from __future__ import annotations

import asyncio
import secrets
import socket
import threading
import time
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from .desktop import notify_ready, notify_status, open_url
from .networks import Publisher
from .posts import PostError, derive_messages, public_prompt_context, update_draft_from_ui, validate_draft
from .providers import generate_copies
from .storage import StaleRevisionError, Storage
from .verification import verify_publication

PACKAGE_ROOT = Path(__file__).parent
PUBLISH_STEPS = ("mastodon_es", "mastodon_en", "bluesky_es", "bluesky_en", "verification")


def create_app(ref: str, storage: Storage, session_token: str) -> FastAPI:
    app = FastAPI(title="3cucharadas-difusion", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.last_activity = time.monotonic()
    app.state.server = None
    app.state.jobs = {}
    app.state.active_job = None
    app.state.jobs_lock = threading.Lock()

    def job_snapshot(job_id: str) -> dict[str, Any]:
        with app.state.jobs_lock:
            job = app.state.jobs.get(job_id)
            if job is None:
                raise HTTPException(status_code=404, detail="Job no encontrado")
            return {
                **job,
                "steps": {name: dict(value) for name, value in job["steps"].items()},
                "results": [dict(value) for value in job.get("results", [])],
            }

    def update_job(job_id: str, **changes: Any) -> None:
        with app.state.jobs_lock:
            app.state.jobs[job_id].update(changes)

    def report(job_id: str, step: str, status: str, detail: str = "", url: str = "") -> None:
        with app.state.jobs_lock:
            if step not in app.state.jobs[job_id]["steps"]:
                return
            app.state.jobs[job_id]["steps"][step] = {
                "status": status,
                "detail": detail,
                "url": url,
            }

    def run_publish_job(job_id: str) -> None:
        callback = lambda step, status, detail, url: report(job_id, step, status, detail, url)
        try:
            current = storage.load_draft(ref)
            results = Publisher(storage).publish(current, live=True, progress=callback)
            update_job(job_id, results=[item.to_dict() for item in results])
            if all(item.status in {"published", "skipped"} for item in results):
                verification = verify_publication(storage, ref, progress=callback)
                final_status = verification["status"]
                update_job(job_id, verification=verification)
            else:
                final_status = storage.load_draft(ref).status
                report(job_id, "verification", "skipped", "publicacion incompleta", "")
            refreshed = storage.load_draft(ref)
            update_job(
                job_id,
                status=final_status,
                state="done",
                draft_revision=refreshed.draft_revision,
            )
            notify_status(ref, final_status)
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"[:500]
            update_job(job_id, status="failed", state="done", error=detail)
            notify_status(ref, "failed", detail[:120])
        finally:
            with app.state.jobs_lock:
                if app.state.active_job == job_id:
                    app.state.active_job = None

    @app.middleware("http")
    async def security_headers(request: Request, call_next: Any) -> Any:
        app.state.last_activity = time.monotonic()
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' https:; style-src 'self'; "
            "script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cache-Control"] = "no-store"
        return response

    def authorize(request: Request) -> None:
        provided = request.headers.get("X-Review-Token", "")
        if not secrets.compare_digest(provided, session_token):
            raise HTTPException(status_code=403, detail="Token de revision invalido")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return (PACKAGE_ROOT / "templates" / "review.html").read_text(encoding="utf-8")

    @app.get("/assets/{name}")
    async def asset(name: str) -> FileResponse:
        if name not in {"review.css", "review.js"}:
            raise HTTPException(status_code=404)
        return FileResponse(PACKAGE_ROOT / "static" / name)

    @app.get("/api/draft")
    async def get_draft(request: Request) -> dict[str, Any]:
        authorize(request)
        draft = storage.load_draft(ref)
        validate_draft(draft)
        return draft.to_dict()

    @app.put("/api/draft")
    async def save_draft(request: Request) -> JSONResponse:
        authorize(request)
        raw = await request.json()
        expected = int(raw.get("expected_revision", -1))
        draft = storage.load_draft(ref)
        if draft.draft_revision != expected:
            raise HTTPException(status_code=409, detail="El borrador cambio en otra sesion")
        try:
            update_draft_from_ui(draft, raw)
            saved = storage.save_draft(draft, expected_revision=expected)
        except (PostError, StaleRevisionError) as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        storage.append_event({"event": "draft_saved", "ref": ref, "revision": saved.draft_revision})
        return JSONResponse(saved.to_dict())

    @app.post("/api/regenerate/{lang}")
    async def regenerate(lang: str, request: Request) -> JSONResponse:
        authorize(request)
        if lang not in {"es", "en"}:
            raise HTTPException(status_code=404)
        raw = await request.json()
        expected = int(raw.get("expected_revision", -1))
        draft = storage.load_draft(ref)
        if draft.draft_revision != expected:
            raise HTTPException(status_code=409, detail="El borrador cambio en otra sesion")
        outcome = generate_copies(public_prompt_context(draft.posts), "auto")
        if outcome.payload is None:
            raise HTTPException(status_code=503, detail={"message": "Proveedores no disponibles", "attempts": outcome.attempts})
        if draft.status in {"published", "published_verified", "published_unverified"}:
            raise HTTPException(status_code=409, detail="Una publicacion finalizada es de solo lectura")
        draft.base_copy[lang] = str(outcome.payload[lang]).strip()
        derive_messages(draft)
        for network in ("mastodon", "bluesky"):
            draft.approvals[network] = False
            for message_lang in ("es", "en"):
                draft.messages[network][message_lang].approved = False
        draft.provider = outcome.provider
        draft.provider_attempts.extend(outcome.attempts)
        validate_draft(draft)
        saved = storage.save_draft(draft, expected_revision=expected)
        return JSONResponse(saved.to_dict())

    @app.post("/api/publish")
    async def publish(request: Request) -> JSONResponse:
        authorize(request)
        raw = await request.json()
        expected = int(raw.get("expected_revision", -1))
        draft = storage.load_draft(ref)
        if draft.draft_revision != expected:
            raise HTTPException(status_code=409, detail="El borrador cambio en otra sesion")
        if raw.get("confirmation") != f"PUBLICAR {ref}":
            raise HTTPException(status_code=400, detail="Confirmacion escrita incorrecta")
        errors = validate_draft(draft)
        if errors:
            raise HTTPException(status_code=400, detail="Borrador invalido: " + "; ".join(errors))
        if not all(draft.approvals.get(network) for network in ("mastodon", "bluesky")):
            raise HTTPException(status_code=400, detail="Debes aprobar ambas cadenas")
        if draft.status in {"published", "published_verified", "published_unverified"}:
            raise HTTPException(status_code=409, detail="Esta revision ya fue publicada; usa verify")
        with app.state.jobs_lock:
            if app.state.active_job is not None:
                raise HTTPException(status_code=409, detail="Ya hay una publicacion en curso")
            job_id = secrets.token_urlsafe(12)
            app.state.jobs[job_id] = {
                "job_id": job_id,
                "state": "running",
                "status": "publishing",
                "draft_revision": draft.draft_revision,
                "steps": {
                    step: {"status": "pending", "detail": "", "url": ""}
                    for step in PUBLISH_STEPS
                },
                "results": [],
                "verification": None,
                "error": "",
            }
            app.state.active_job = job_id
        threading.Thread(target=run_publish_job, args=(job_id,), daemon=True).start()
        return JSONResponse(job_snapshot(job_id), status_code=202)

    @app.get("/api/publish/{job_id}")
    async def publish_status(job_id: str, request: Request) -> JSONResponse:
        authorize(request)
        return JSONResponse(job_snapshot(job_id))

    @app.post("/api/close")
    async def close(request: Request, background_tasks: BackgroundTasks) -> dict[str, bool]:
        authorize(request)
        if app.state.active_job is not None:
            raise HTTPException(status_code=409, detail="Espera a que termine la publicacion")

        async def stop() -> None:
            await asyncio.sleep(0.2)
            if app.state.server is not None:
                app.state.server.should_exit = True

        background_tasks.add_task(stop)
        return {"closing": True}

    @app.exception_handler(StaleRevisionError)
    async def stale_handler(_: Request, exc: StaleRevisionError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=409)

    return app


def run_review(
    ref: str,
    storage: Storage,
    *,
    open_browser: bool = True,
    inactivity_seconds: int = 1800,
) -> None:
    token = secrets.token_urlsafe(32)
    app = create_app(ref, storage, token)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 0))
    sock.listen(2048)
    port = int(sock.getsockname()[1])
    url = f"http://127.0.0.1:{port}/#token={token}"
    config = uvicorn.Config(app, log_level="warning", access_log=False)
    server = uvicorn.Server(config)
    app.state.server = server

    def idle_watch() -> None:
        while not server.should_exit:
            time.sleep(5)
            if time.monotonic() - app.state.last_activity >= inactivity_seconds:
                server.should_exit = True

    threading.Thread(target=idle_watch, daemon=True).start()
    print(f"Revision local: {url}", flush=True)
    if open_browser:
        open_url(url)
    notify_ready(ref, url)
    try:
        server.run(sockets=[sock])
    finally:
        sock.close()
