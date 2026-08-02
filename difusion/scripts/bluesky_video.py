#!/usr/bin/env python3
"""Prepara y publica una respuesta Bluesky con video.

El caso que motivo este script fue una respuesta al post
https://bsky.app/profile/labra.bsky.social/post/3ms2hcchhwr25 con el video
assets/videos/catastro-sii-visor.mp4, el texto:

Lo llevé a un visor para recorrer 346 comunas y ver cómo cambia la lectura territorial según el denominador: hogares, personas o superficie.

Adelanto 😒: en varias comunas la cobertura del SII frente al Censo 2024 es baja y, suavemente, discutible.

3cucharadas.cl/catastro_sii_brecha/

Alt text usado en esa publicacion:

Recorrido por el visor del Catastro SII: los indicadores nacionales, la elección de una comuna en el gráfico de burbujas, el mapa bivariado de unidades vecinales y el laboratorio de denominadores.

Ejemplo reproducible para ese caso:

  python difusion/scripts/bluesky_video.py prepare \
    --video assets/videos/catastro-sii-visor.mp4 \
    --root-uri at://did:plc:v2tiac7n52wcyoz6vkfjajob/app.bsky.feed.post/3ms2hcchhwr25 \
    --root-url https://bsky.app/profile/labra.bsky.social/post/3ms2hcchhwr25 \
    --root-author-handle labra.bsky.social \
    --text-file /tmp/bluesky-text.txt \
    --alt-file /tmp/bluesky-alt.txt \
    --link 3cucharadas.cl/catastro_sii_brecha/=https://3cucharadas.cl/catastro_sii_brecha/ \
    --state difusion/state/bluesky-video-catastro-sii-visor.json \
    --live

  python difusion/scripts/bluesky_video.py publish ... --live
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DIFUSION_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = DIFUSION_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

# El import va despues del sys.path.insert a proposito: el paquete no es
# importable hasta que esa ruta entra en sys.path. De ahi el E402 silenciado.
from cucharadas_difusion.networks import (  # noqa: E402
    BlueskyClient,
    PublishError,
    load_secrets,
)

DEFAULT_VIDEO_SERVICE = "https://video.bsky.app"
VIDEO_SERVICE_AUTH_LXM = "com.atproto.repo.uploadBlob"
MAX_VIDEO_BYTES = 50_000_000
MAX_DURATION_SECONDS = 180.0
MAX_TEXT_CHARS = 300
MAX_ALT_CHARS = 1_000


class StepError(RuntimeError):
    pass


@dataclass(frozen=True)
class LinkFacetSpec:
    text: str
    uri: str


@dataclass(frozen=True)
class Config:
    video_path: Path
    text: str
    alt_text: str
    root_uri: str
    root_url: str | None
    state_path: Path
    secrets_path: Path | None
    expected_handle: str | None
    root_author_handle: str | None
    video_service: str
    links: tuple[LinkFacetSpec, ...]
    aspect_ratio: tuple[int, int] | None
    require_silent: bool
    max_video_bytes: int
    max_duration_seconds: float
    max_text_chars: int
    max_alt_chars: int


@dataclass(frozen=True)
class VideoInfo:
    metadata: dict[str, Any]
    sha256: str
    size_bytes: int
    duration_seconds: float
    width: int
    height: int
    aspect_width: int
    aspect_height: int


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def status(step: str, detail: str) -> None:
    print(f"{step}: {detail}", flush=True)


def resolve_cli_path(value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (Path.cwd() / path).resolve()


def default_state_path(video_path: Path, root_uri: str) -> Path:
    root_key = root_uri.rstrip("/").rsplit("/", 1)[-1] or "root"
    raw = f"{video_path.stem}-{root_key}".lower()
    slug = re.sub(r"[^a-z0-9._-]+", "-", raw).strip("-")[:96] or "video"
    return DIFUSION_ROOT / "state" / f"bluesky-video-{slug}.json"


def read_text_arg(value: str | None, file_value: str | None, label: str) -> str:
    if value is not None:
        return value
    if file_value is None:
        raise StepError(f"Falta --{label} o --{label}-file")
    return resolve_cli_path(file_value).read_text(encoding="utf-8").strip()


def parse_link(value: str) -> LinkFacetSpec:
    if "=" not in value:
        raise argparse.ArgumentTypeError("usa TEXTO=URL")
    text, uri = value.split("=", 1)
    text = text.strip()
    uri = uri.strip()
    if not text or not uri:
        raise argparse.ArgumentTypeError("TEXTO y URL no pueden estar vacios")
    if "://" not in uri:
        uri = f"https://{uri}"
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("URL debe ser http(s)")
    return LinkFacetSpec(text=text, uri=uri)


def parse_aspect(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"([1-9][0-9]*)x([1-9][0-9]*)", value)
    if not match:
        raise argparse.ArgumentTypeError("usa WIDTHxHEIGHT, por ejemplo 1920x1080")
    return int(match.group(1)), int(match.group(2))


def config_from_args(args: argparse.Namespace) -> Config:
    video_path = resolve_cli_path(args.video)
    state_path = resolve_cli_path(args.state) if args.state else default_state_path(video_path, args.root_uri)
    return Config(
        video_path=video_path,
        text=read_text_arg(args.text, args.text_file, "text"),
        alt_text=read_text_arg(args.alt, args.alt_file, "alt"),
        root_uri=args.root_uri,
        root_url=args.root_url,
        state_path=state_path,
        secrets_path=resolve_cli_path(args.secrets) if args.secrets else None,
        expected_handle=args.expected_handle,
        root_author_handle=args.root_author_handle,
        video_service=args.video_service.rstrip("/"),
        links=tuple(args.links or ()),
        aspect_ratio=args.aspect,
        require_silent=args.require_silent,
        max_video_bytes=args.max_video_bytes,
        max_duration_seconds=args.max_duration_seconds,
        max_text_chars=args.max_text_chars,
        max_alt_chars=args.max_alt_chars,
    )


def read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise StepError(f"Estado invalido en {path}")
    return value


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    tmp.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ffprobe(path: Path) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration,size:stream=index,codec_type,codec_name,width,height",
                "-of",
                "json",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise StepError("No se encontro ffprobe para validar el video") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip().splitlines()[0] if exc.stderr.strip() else "sin detalle"
        raise StepError(f"ffprobe fallo: {detail[:240]}") from exc
    return json.loads(completed.stdout)


def validate_inputs(config: Config) -> VideoInfo:
    if not config.text:
        raise StepError("El texto esta vacio")
    if len(config.text) > config.max_text_chars:
        raise StepError(f"El texto tiene {len(config.text)} caracteres y supera {config.max_text_chars}")
    if not config.alt_text:
        raise StepError("El alt text esta vacio")
    if len(config.alt_text) > config.max_alt_chars:
        raise StepError(f"El alt text tiene {len(config.alt_text)} caracteres y supera {config.max_alt_chars}")
    if not config.root_uri.startswith("at://"):
        raise StepError("--root-uri debe ser una URI AT, por ejemplo at://did:.../app.bsky.feed.post/...")
    if not config.video_path.exists():
        raise StepError(f"No existe el video: {config.video_path}")

    video_size = config.video_path.stat().st_size
    if video_size > config.max_video_bytes:
        raise StepError(f"El video pesa {video_size} bytes y supera {config.max_video_bytes}")

    metadata = ffprobe(config.video_path)
    streams = metadata.get("streams") or []
    video_streams = [item for item in streams if item.get("codec_type") == "video"]
    audio_streams = [item for item in streams if item.get("codec_type") == "audio"]
    if len(video_streams) != 1:
        raise StepError(f"Se esperaba 1 stream de video y hay {len(video_streams)}")
    if config.require_silent and audio_streams:
        raise StepError("El video contiene pista de audio, pero --require-silent exige video silente")

    stream = video_streams[0]
    if stream.get("codec_name") != "h264":
        raise StepError(f"Codec inesperado: {stream.get('codec_name')}; Bluesky espera H.264 en MP4")
    width = int(stream.get("width") or 0)
    height = int(stream.get("height") or 0)
    if width <= 0 or height <= 0:
        raise StepError("ffprobe no devolvio dimensiones de video validas")

    duration = float((metadata.get("format") or {}).get("duration") or 0)
    if duration > config.max_duration_seconds:
        raise StepError(f"El video dura {duration:.2f}s y supera {config.max_duration_seconds:.0f}s")

    aspect_width, aspect_height = config.aspect_ratio or (width, height)
    return VideoInfo(
        metadata=metadata,
        sha256=sha256_file(config.video_path),
        size_bytes=video_size,
        duration_seconds=duration,
        width=width,
        height=height,
        aspect_width=aspect_width,
        aspect_height=aspect_height,
    )


def redacted_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def redact(text: str, secrets: dict[str, str] | None = None) -> str:
    safe = text
    for key in ("BSKY_APP_PASSWORD", "MASTODON_TOKEN"):
        value = (secrets or {}).get(key, "")
        if value:
            safe = safe.replace(value, "[REDACTED]")
    return safe[:500]


def http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    request = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise StepError(f"HTTP {exc.code} en {method} {redacted_url(url)}") from exc
    except urllib.error.URLError as exc:
        raise StepError(f"Error de red en {method} {redacted_url(url)}: {exc.reason}") from exc

    try:
        payload = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise StepError(f"Respuesta no JSON en {method} {redacted_url(url)}") from exc
    if not isinstance(payload, dict):
        raise StepError(f"Respuesta JSON inesperada en {method} {redacted_url(url)}")
    return payload


def authenticate(config: Config) -> Any:
    secrets = load_secrets(config.secrets_path)
    try:
        client = BlueskyClient(secrets)._client()
    except Exception as exc:
        raise StepError(redact(f"No se pudo autenticar en Bluesky: {type(exc).__name__}", secrets)) from exc
    expected_handle = config.expected_handle or secrets.get("BSKY_HANDLE")
    if expected_handle:
        actual_handle = str(getattr(client.me, "handle", ""))
        if actual_handle != expected_handle:
            raise StepError("Login Bluesky no coincide con el handle esperado")
    return client


def pds_audience(client: Any) -> str:
    session = getattr(client, "_session", None)
    pds_endpoint = str(getattr(session, "pds_endpoint", "") or getattr(client, "_base_url", ""))
    parsed = urllib.parse.urlparse(pds_endpoint)
    host = parsed.hostname
    if not host:
        raise StepError("No se pudo determinar el host PDS de la sesion Bluesky")
    return f"did:web:{host}"


def get_service_token(client: Any) -> str:
    response = client.com.atproto.server.get_service_auth(
        {
            "aud": pds_audience(client),
            "lxm": VIDEO_SERVICE_AUTH_LXM,
            "exp": int(time.time()) + 30 * 60,
        }
    )
    token = str(getattr(response, "token", ""))
    if not token:
        raise StepError("getServiceAuth no devolvio token")
    return token


def extract_job_status(payload: dict[str, Any]) -> dict[str, Any]:
    job = payload.get("jobStatus") or payload.get("job_status") or payload
    if not isinstance(job, dict):
        raise StepError("Respuesta de job invalida")
    return job


def job_id(job: dict[str, Any]) -> str:
    value = str(job.get("jobId") or job.get("job_id") or "")
    if not value:
        raise StepError("Job sin jobId")
    return value


def job_state(job: dict[str, Any]) -> str:
    return str(job.get("state") or "")


def upload_video(client: Any, config: Config) -> dict[str, Any]:
    # Client.send_video de atproto no sirve para este caso: en la version usada
    # intenta llamar upload_blob contra el PDS. Bluesky exige pasar por el
    # servicio de video: getServiceAuth -> uploadVideo -> polling getJobStatus.
    token = get_service_token(client)
    params = urllib.parse.urlencode(
        {
            "did": str(client.me.did),
            "name": config.video_path.name,
        }
    )
    url = f"{config.video_service}/xrpc/app.bsky.video.uploadVideo?{params}"
    data = config.video_path.read_bytes()
    payload = http_json(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "video/mp4",
            "Content-Length": str(len(data)),
        },
        data=data,
        timeout=180,
    )
    return extract_job_status(payload)


def poll_job(
    job: dict[str, Any],
    config: Config,
    *,
    interval_seconds: float = 5.0,
    timeout_seconds: float = 600.0,
) -> dict[str, Any]:
    current = job
    deadline = time.monotonic() + timeout_seconds
    while True:
        state = job_state(current)
        blob = current.get("blob")
        progress = current.get("progress")
        detail = state if progress is None else f"{state} ({progress}%)"
        status("poll", detail)
        if blob:
            return current
        if state == "JOB_STATE_FAILED":
            raise StepError(f"Procesamiento de video fallo para job {job_id(current)}")
        if time.monotonic() >= deadline:
            raise StepError(f"Timeout esperando job {job_id(current)}")
        time.sleep(interval_seconds)
        params = urllib.parse.urlencode({"jobId": job_id(current)})
        payload = http_json(
            "GET",
            f"{config.video_service}/xrpc/app.bsky.video.getJobStatus?{params}",
            timeout=60,
        )
        current = extract_job_status(payload)


def get_root_ref(client: Any, config: Config) -> Any:
    from atproto import models

    response = client.app.bsky.feed.get_posts({"uris": [config.root_uri]})
    posts = list(getattr(response, "posts", []) or [])
    if not posts:
        raise StepError("No se pudo recuperar el post raiz")
    root = posts[0]
    if config.root_author_handle:
        root_author = getattr(getattr(root, "author", None), "handle", "")
        if root_author != config.root_author_handle:
            raise StepError("El post raiz no pertenece al handle esperado")
    root_did = getattr(getattr(root, "author", None), "did", "")
    if root_did and not config.root_uri.startswith(f"at://{root_did}/"):
        raise StepError("El DID del post raiz no coincide con la URI")
    return models.ComAtprotoRepoStrongRef.Main(cid=str(root.cid), uri=config.root_uri)


def link_facets(config: Config) -> list[Any]:
    from atproto import models

    facets: list[Any] = []
    for spec in config.links:
        start = config.text.find(spec.text)
        if start < 0:
            raise StepError(f"El texto no contiene el fragmento facetado: {spec.text!r}")
        end = start + len(spec.text)
        byte_start = len(config.text[:start].encode("utf-8"))
        byte_end = len(config.text[:end].encode("utf-8"))
        facets.append(
            models.AppBskyRichtextFacet.Main(
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byte_start=byte_start,
                    byte_end=byte_end,
                ),
                features=[
                    models.AppBskyRichtextFacet.Link(
                        uri=spec.uri,
                    )
                ],
            )
        )
    return facets


def ensure_state_for_request(state: dict[str, Any], config: Config) -> None:
    state_root = state.get("root_uri")
    if state_root and state_root != config.root_uri:
        raise StepError("El estado preparado corresponde a otro root_uri")
    if state.get("published_uri"):
        raise StepError("El estado ya registra un published_uri; no se publica duplicado")


def prepared_blob(state: dict[str, Any], config: Config, expected_sha256: str) -> dict[str, Any]:
    ensure_state_for_request(state, config)
    if state.get("video_sha256") != expected_sha256:
        raise StepError("El estado preparado no corresponde al SHA-256 del video actual")
    blob = state.get("blob")
    if not isinstance(blob, dict):
        raise StepError(f"El estado no tiene BlobRef preparado: {config.state_path}")
    return blob


def dry_run_prepare(config: Config, info: VideoInfo, state: dict[str, Any]) -> int:
    ensure_state_for_request(state, config)
    summary = {
        "status": "dry_run",
        "command": "prepare",
        "state_path": str(config.state_path),
        "video_sha256": info.sha256,
        "video_size_bytes": info.size_bytes,
        "duration_seconds": round(info.duration_seconds, 3),
        "aspect_ratio": {"width": info.aspect_width, "height": info.aspect_height},
        "text_chars": len(config.text),
        "alt_chars": len(config.alt_text),
        "would": [
            "authenticate_bluesky",
            "get_reply_root_cid",
            "getServiceAuth",
            "uploadVideo",
            "poll_getJobStatus",
            "write_blobref_state",
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def prepare(args: argparse.Namespace) -> int:
    config = config_from_args(args)
    info = validate_inputs(config)
    state = read_state(config.state_path)
    if not args.live:
        return dry_run_prepare(config, info, state)

    ensure_state_for_request(state, config)
    if state.get("blob") and state.get("video_sha256") == info.sha256:
        status("upload", "estado existente con BlobRef; no se repite la subida")
        return 0

    client = authenticate(config)
    status("auth", "login OK")
    root_ref = get_root_ref(client, config)
    status("root", f"CID recuperado: {root_ref.cid}")

    status("upload", "subiendo video al servicio de Bluesky")
    uploaded_job = upload_video(client, config)
    status("upload", f"jobId={job_id(uploaded_job)} state={job_state(uploaded_job)}")
    completed_job = poll_job(uploaded_job, config)
    blob = completed_job.get("blob")
    if not isinstance(blob, dict):
        raise StepError("Job completado sin BlobRef")

    state = {
        "prepared_at": now_iso(),
        "root_uri": config.root_uri,
        "root_url": config.root_url,
        "root_cid": str(root_ref.cid),
        "video_path": str(config.video_path),
        "video_sha256": info.sha256,
        "video_size_bytes": info.size_bytes,
        "video_metadata": info.metadata,
        "job_id": job_id(completed_job),
        "job_state": job_state(completed_job),
        "blob": blob,
        "text_sha256": hashlib.sha256(config.text.encode("utf-8")).hexdigest(),
        "alt_sha256": hashlib.sha256(config.alt_text.encode("utf-8")).hexdigest(),
        "text_chars": len(config.text),
        "alt_chars": len(config.alt_text),
        "aspect_width": info.aspect_width,
        "aspect_height": info.aspect_height,
    }
    write_state(config.state_path, state)
    status("prepare", f"BlobRef listo y guardado en {config.state_path}")
    return 0


def dry_run_publish(config: Config, info: VideoInfo, state: dict[str, Any]) -> int:
    already_published = bool(state.get("published_uri"))
    state_ready = (
        not already_published
        and state.get("root_uri") in {None, config.root_uri}
        and state.get("video_sha256") == info.sha256
        and isinstance(state.get("blob"), dict)
    )
    summary = {
        "status": "dry_run",
        "command": "publish",
        "state_path": str(config.state_path),
        "state_ready": state_ready,
        "already_published": already_published,
        "text_chars": len(config.text),
        "alt_chars": len(config.alt_text),
        "would": ["authenticate_bluesky", "get_reply_root_cid", "create_reply_with_video_embed", "verify_post"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def publish(args: argparse.Namespace) -> int:
    config = config_from_args(args)
    info = validate_inputs(config)
    state = read_state(config.state_path)
    if not args.live:
        return dry_run_publish(config, info, state)

    blob = prepared_blob(state, config, info.sha256)
    client = authenticate(config)
    status("auth", "login OK")
    root_ref = get_root_ref(client, config)
    state["root_cid"] = str(root_ref.cid)
    status("root", f"CID recuperado: {root_ref.cid}")

    from atproto import models

    # El embed consume el BlobRef devuelto por el servicio de video. Enviar el
    # archivo directo con upload_blob/send_video no produce el asset procesado.
    reply_ref = models.AppBskyFeedPost.ReplyRef(root=root_ref, parent=root_ref)
    embed = models.AppBskyEmbedVideo.Main(
        video=blob,
        alt=config.alt_text,
        aspect_ratio=models.AppBskyEmbedDefs.AspectRatio(width=info.aspect_width, height=info.aspect_height),
    )
    status("publish", "creando respuesta con video en Bluesky")
    created = client.send_post(
        text=config.text,
        reply_to=reply_ref,
        embed=embed,
        langs=["es"],
        facets=link_facets(config),
    )
    published_uri = str(created.uri)
    published_cid = str(created.cid)
    handle = str(getattr(client.me, "handle", ""))
    published_url = f"https://bsky.app/profile/{handle}/post/{published_uri.rsplit('/', 1)[-1]}"
    state.update(
        {
            "published_at": now_iso(),
            "published_uri": published_uri,
            "published_cid": published_cid,
            "published_url": published_url,
        }
    )
    write_state(config.state_path, state)
    status("publish", f"creado: {published_url}")

    try:
        verify_post(client, config, published_uri, info)
    except Exception as exc:  # noqa: BLE001 - el post ya existe; propagar invitaria a reintentar y duplicar
        status("verify", f"fallo despues de crear el post; no reintentar publicacion. Detalle: {type(exc).__name__}")
        return 2
    status("verify", "post recuperado y campos criticos confirmados")
    return 0


def model_to_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, dict):
        return value
    raise StepError(f"No se pudo convertir a dict: {type(value).__name__}")


def verify_post(client: Any, config: Config, published_uri: str, info: VideoInfo) -> None:
    for _ in range(5):
        response = client.app.bsky.feed.get_posts({"uris": [published_uri]})
        posts = list(getattr(response, "posts", []) or [])
        if posts:
            post = posts[0]
            record = model_to_dict(getattr(post, "record", {}))
            reply = record.get("reply") or {}
            embed = record.get("embed") or {}
            failures: list[str] = []
            if record.get("text") != config.text:
                failures.append("text")
            if (record.get("langs") or []) != ["es"]:
                failures.append("langs")
            if (reply.get("root") or {}).get("uri") != config.root_uri:
                failures.append("reply.root")
            if (reply.get("parent") or {}).get("uri") != config.root_uri:
                failures.append("reply.parent")
            if embed.get("$type") != "app.bsky.embed.video":
                failures.append("embed.type")
            if embed.get("alt") != config.alt_text:
                failures.append("embed.alt")
            if (embed.get("aspectRatio") or {}).get("width") != info.aspect_width:
                failures.append("aspectRatio.width")
            if (embed.get("aspectRatio") or {}).get("height") != info.aspect_height:
                failures.append("aspectRatio.height")
            if failures:
                raise StepError("verificacion incompleta: " + ", ".join(failures))
            return
        time.sleep(3)
    raise StepError("Bluesky no devolvio el post creado")


def add_common_post_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--video", required=True, help="Ruta del video MP4 a adjuntar")
    text_group = parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument("--text", help="Texto del post")
    text_group.add_argument("--text-file", help="Archivo UTF-8 con el texto del post")
    alt_group = parser.add_mutually_exclusive_group(required=True)
    alt_group.add_argument("--alt", help="Alt text del video")
    alt_group.add_argument("--alt-file", help="Archivo UTF-8 con el alt text del video")
    parser.add_argument("--root-uri", required=True, help="URI AT del post al que se responde")
    parser.add_argument("--root-url", help="URL web del post raiz; solo se guarda en estado")
    parser.add_argument("--state", help="Estado JSON local; por defecto se deriva de video y root-uri")
    parser.add_argument("--secrets", help="Sobrescribe ~/.config/3cucharadas-difusion/secrets.env")
    parser.add_argument("--expected-handle", help="Handle esperado para el login; por defecto BSKY_HANDLE")
    parser.add_argument("--root-author-handle", help="Valida que el post raiz pertenezca a este handle")
    parser.add_argument(
        "--link",
        action="append",
        type=parse_link,
        dest="links",
        metavar="TEXTO=URL",
        help="Agrega un facet de link sobre la primera aparicion de TEXTO; repetible",
    )
    parser.add_argument("--aspect", type=parse_aspect, help="Aspect ratio del embed, por ejemplo 1920x1080")
    parser.add_argument("--video-service", default=DEFAULT_VIDEO_SERVICE, help=argparse.SUPPRESS)
    parser.add_argument("--require-silent", action="store_true", help="Falla si el video trae pista de audio")
    parser.add_argument("--max-video-bytes", type=int, default=MAX_VIDEO_BYTES, help=argparse.SUPPRESS)
    parser.add_argument("--max-duration-seconds", type=float, default=MAX_DURATION_SECONDS, help=argparse.SUPPRESS)
    parser.add_argument("--max-text-chars", type=int, default=MAX_TEXT_CHARS, help=argparse.SUPPRESS)
    parser.add_argument("--max-alt-chars", type=int, default=MAX_ALT_CHARS, help=argparse.SUPPRESS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepara y publica una respuesta Bluesky con video procesado.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Dry-run por defecto: prepare valida sin autenticar/subir y publish simula sin crear posts. "
            "Usa --live solo cuando quieras escribir en Bluesky."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Dry-run por defecto; --live sube video y guarda BlobRef")
    add_common_post_args(prepare_parser)
    prepare_parser.add_argument("--live", action="store_true", help="Autentica, sube el video y guarda estado")
    prepare_parser.set_defaults(func=prepare)

    publish_parser = subparsers.add_parser("publish", help="Dry-run por defecto; --live crea el post irreversible")
    add_common_post_args(publish_parser)
    publish_parser.add_argument("--live", action="store_true", help="Crea el post real en Bluesky")
    publish_parser.set_defaults(func=publish)

    state_parser = subparsers.add_parser("show-state", help="Muestra estado local sin secretos")
    state_parser.add_argument("--state", required=True, help="Estado JSON local a mostrar")
    state_parser.set_defaults(func=show_state)
    return parser


def show_state(args: argparse.Namespace) -> int:
    print(json.dumps(read_state(resolve_cli_path(args.state)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (PublishError, StepError, OSError, ValueError) as exc:
        print(f"ERROR: {redact(str(exc))}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
