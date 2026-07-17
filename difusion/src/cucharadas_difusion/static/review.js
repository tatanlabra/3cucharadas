"use strict";

const token = new URLSearchParams(window.location.hash.slice(1)).get("token") || "";
const authHeaders = {"X-Review-Token": token, "Content-Type": "application/json"};
const template = document.querySelector("#message-template");
const statusNode = document.querySelector("#global-status");
const publishButton = document.querySelector("#publish");
const resultsNode = document.querySelector("#results");
const stepLabels = {
  mastodon_es: "Mastodon ES · raíz",
  mastodon_en: "Mastodon EN · autorrespuesta",
  bluesky_es: "Bluesky ES · raíz",
  bluesky_en: "Bluesky EN · autorrespuesta",
  verification: "Verificación pública",
};
let draft = null;
let publishing = false;
let saveTimer = null;
let saveChain = Promise.resolve();

function setStatus(text, kind = "") {
  statusNode.textContent = text;
  statusNode.className = `status ${kind}`.trim();
}

function terminalDraft() {
  return Boolean(draft && ["published", "published_verified", "published_unverified"].includes(draft.status));
}

function graphemes(text) {
  if (typeof Intl.Segmenter === "function") {
    return [...new Intl.Segmenter(undefined, {granularity: "grapheme"}).segment(text)].length;
  }
  return Array.from(text).length;
}

function hashtags(text) {
  return text.match(/#[\p{L}\p{N}_-]+/gu) || [];
}

async function api(path, options = {}) {
  const response = await fetch(path, {...options, headers: {...authHeaders, ...(options.headers || {})}});
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail || body);
    throw new Error(detail || `HTTP ${response.status}`);
  }
  return body;
}

function account(network) {
  return network === "mastodon" ? "@asiole@mastodon.social" : "labra.bsky.social";
}

function deriveLocal() {
  for (const network of ["mastodon", "bluesky"]) {
    for (const lang of ["es", "en"]) {
      const base = (draft.base_copy[lang] || "").trim();
      draft.messages[network][lang].text = network === "mastodon" && base
        ? `${base} ${draft.messages[network][lang].target_url}`
        : base;
    }
  }
}

function ensureCard(network, lang) {
  const container = document.querySelector(`#card-${network}-${lang}`);
  if (!container.hasChildNodes()) {
    container.append(template.content.cloneNode(true));
    container.querySelector(".copy").addEventListener("click", async () => {
      await navigator.clipboard.writeText(draft.messages[network][lang].text);
      setStatus("Texto derivado copiado", "ok");
    });
  }
  return container;
}

function updateCounter(container, network, text) {
  const count = graphemes(text);
  const limit = draft.limits[network];
  const node = container.querySelector(".counter");
  node.textContent = `${count}/${limit}`;
  node.classList.toggle("invalid", count > limit);
}

function renderCard(network, lang) {
  const container = ensureCard(network, lang);
  const message = draft.messages[network][lang];
  const post = draft.posts[lang];
  container.querySelector(".derived-text").textContent = message.text;
  container.querySelector(".account").textContent = account(network);
  container.querySelector(".language").textContent = lang;
  container.querySelector(".role").textContent = message.role === "root" ? "raíz" : "respuesta";
  updateCounter(container, network, message.text);
  container.querySelector(".hashtag-row").textContent = hashtags(message.text).join("  ");
  const warnings = container.querySelector(".warnings");
  warnings.replaceChildren();
  for (const warning of message.warnings || []) {
    const line = document.createElement("div");
    line.textContent = warning.replace(/^error:\s*/, "");
    if (warning.startsWith("error:")) line.className = "error";
    warnings.append(line);
  }
  const card = container.querySelector(".link-card");
  card.href = message.target_url;
  const image = card.querySelector("img");
  image.src = post.image_url;
  image.alt = `Vista previa: ${post.title}`;
  card.querySelector(".link-title").textContent = post.title;
  card.querySelector(".link-description").textContent = post.description;
  card.querySelector(".link-url").textContent = message.target_url;
  container.querySelector(".canonical").href = post.canonical_url;
}

function hasErrors() {
  return ["mastodon", "bluesky"].some(network =>
    ["es", "en"].some(lang =>
      (draft.messages[network][lang].warnings || []).some(item => item.startsWith("error:"))
    )
  );
}

function updatePublishState() {
  publishButton.disabled = !draft || publishing || terminalDraft() || hasErrors()
    || !draft.approvals.mastodon || !draft.approvals.bluesky;
  for (const network of ["mastodon", "bluesky"]) {
    document.querySelector(`#approve-${network}`).disabled = publishing || terminalDraft();
  }
  for (const lang of ["es", "en"]) {
    document.querySelector(`#base-${lang}`).disabled = publishing || terminalDraft();
    document.querySelector(`#regenerate-${lang}`).disabled = publishing || terminalDraft();
  }
}

function render() {
  document.querySelector("#page-title").textContent = draft.posts.es.title;
  document.querySelector("#page-meta").textContent =
    `ref: ${draft.ref} · proveedor: ${draft.provider} · revisión ${draft.draft_revision} · ${draft.status}`;
  for (const lang of ["es", "en"]) {
    const editor = document.querySelector(`#base-${lang}`);
    if (document.activeElement !== editor) editor.value = draft.base_copy[lang] || "";
  }
  for (const network of ["mastodon", "bluesky"]) {
    for (const lang of ["es", "en"]) renderCard(network, lang);
    document.querySelector(`#approve-${network}`).checked = Boolean(draft.approvals[network]);
  }
  updatePublishState();
}

function collectPayload() {
  return {
    expected_revision: draft.draft_revision,
    approvals: {...draft.approvals},
    base_copy: {...draft.base_copy},
  };
}

function queueSave(showStatus = true) {
  if (terminalDraft() || publishing) return Promise.resolve(draft);
  saveChain = saveChain.catch(() => {}).then(async () => {
    if (showStatus) setStatus("Guardando…");
    draft = await api("/api/draft", {method: "PUT", body: JSON.stringify(collectPayload())});
    render();
    if (showStatus) setStatus("Borrador guardado", "ok");
    return draft;
  }).catch(error => {
    setStatus(error.message, "error");
    throw error;
  });
  return saveChain;
}

function baseChanged(lang, value) {
  draft.base_copy[lang] = value;
  deriveLocal();
  draft.approvals.mastodon = false;
  draft.approvals.bluesky = false;
  for (const network of ["mastodon", "bluesky"]) {
    document.querySelector(`#approve-${network}`).checked = false;
    for (const messageLang of ["es", "en"]) renderCard(network, messageLang);
  }
  updatePublishState();
  window.clearTimeout(saveTimer);
  saveTimer = window.setTimeout(() => queueSave(false), 800);
}

for (const lang of ["es", "en"]) {
  document.querySelector(`#base-${lang}`).addEventListener("input", event => baseChanged(lang, event.target.value));
  document.querySelector(`#regenerate-${lang}`).addEventListener("click", async () => {
    try {
      await queueSave(false);
      setStatus(`Regenerando mensaje base ${lang.toUpperCase()}…`);
      draft = await api(`/api/regenerate/${lang}`, {
        method: "POST",
        body: JSON.stringify({expected_revision: draft.draft_revision}),
      });
      render();
      setStatus("Mensaje regenerado; ambas redes requieren nueva aprobación", "ok");
    } catch (error) {
      setStatus(error.message, "error");
    }
  });
}

for (const network of ["mastodon", "bluesky"]) {
  document.querySelector(`#approve-${network}`).addEventListener("change", event => {
    draft.approvals[network] = event.target.checked;
    queueSave(true).catch(() => {});
  });
}

document.querySelector("#save").addEventListener("click", () => queueSave(true).catch(() => {}));

function renderProgress(job) {
  resultsNode.hidden = false;
  resultsNode.replaceChildren();
  const heading = document.createElement("strong");
  heading.textContent = job.state === "done" ? `Resultado: ${job.status}` : "Publicación en curso";
  resultsNode.append(heading);
  const list = document.createElement("ol");
  list.className = "progress-list";
  for (const [step, label] of Object.entries(stepLabels)) {
    const value = job.steps[step] || {status: "pending", detail: "", url: ""};
    const item = document.createElement("li");
    item.className = `progress-${value.status}`;
    const marker = {pending: "○", in_progress: "…", success: "✓", skipped: "↷", failed: "✕"}[value.status] || "○";
    item.append(`${marker} ${label}`);
    if (value.detail) item.append(` — ${value.detail}`);
    if (value.url) {
      const link = document.createElement("a");
      link.href = value.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = " abrir";
      item.append(link);
    }
    list.append(item);
  }
  resultsNode.append(list);
  if (job.error) {
    const error = document.createElement("p");
    error.className = "error";
    error.textContent = job.error;
    resultsNode.append(error);
  }
}

async function monitorJob(job) {
  let current = job;
  while (current.state !== "done") {
    renderProgress(current);
    await new Promise(resolve => window.setTimeout(resolve, 500));
    current = await api(`/api/publish/${current.job_id}`);
  }
  renderProgress(current);
  draft = await api("/api/draft");
  publishing = false;
  render();
  if (current.status === "published_verified") {
    setStatus("Publicado y verificado", "ok");
  } else {
    setStatus(current.error || current.status, "error");
  }
}

publishButton.addEventListener("click", async () => {
  try {
    await queueSave(false);
    const confirmation = window.prompt(`Escribe PUBLICAR ${draft.ref} para publicar las cuatro piezas:`);
    if (confirmation === null) return;
    publishing = true;
    updatePublishState();
    setStatus("Iniciando publicación…");
    const job = await api("/api/publish", {
      method: "POST",
      body: JSON.stringify({expected_revision: draft.draft_revision, confirmation}),
    });
    await monitorJob(job);
  } catch (error) {
    publishing = false;
    updatePublishState();
    setStatus(error.message, "error");
  }
});

document.querySelector("#close").addEventListener("click", async () => {
  try {
    if (!terminalDraft()) await queueSave(false);
    await api("/api/close", {method: "POST", body: "{}"});
    document.body.replaceChildren(Object.assign(document.createElement("main"), {
      textContent: "Estado guardado. Puedes cerrar esta pestaña.",
    }));
  } catch (error) {
    setStatus(error.message, "error");
  }
});

window.addEventListener("pagehide", () => {
  if (!draft || terminalDraft() || publishing) return;
  fetch("/api/draft", {
    method: "PUT",
    headers: authHeaders,
    body: JSON.stringify(collectPayload()),
    keepalive: true,
  }).catch(() => {});
});

(async () => {
  if (!token) {
    setStatus("Falta token local de revisión", "error");
    return;
  }
  try {
    draft = await api("/api/draft");
    render();
    setStatus(terminalDraft() ? draft.status : "Borrador listo", terminalDraft() ? "ok" : "ok");
  } catch (error) {
    setStatus(error.message, "error");
  }
})();
