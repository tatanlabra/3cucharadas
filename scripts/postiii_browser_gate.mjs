#!/usr/bin/env node

/**
 * Fail-closed static and local-preview checks for Post III's browser gate.
 *
 * This script intentionally does not claim Safari 16 or Firefox 104 support:
 * those are human-platform gates described in postiii_browser_gate.md.
 */

import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { spawnSync } from "node:child_process";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const postPath = resolve(repoRoot, "_drafts/2026-08-28-multiagente-penta-agent-memoria-gobernada-poc.md");
const viewerPath = resolve(repoRoot, "assets/visualizations/penta-rag-knowledge-graph/index.html");
const viewerReadmePath = resolve(repoRoot, "assets/visualizations/penta-rag-knowledge-graph/README.md");
const graphPath = resolve(repoRoot, "assets/data/rag_knowledge_graph/public-graph.json");
const graphGeneratorPath = resolve(repoRoot, "scripts/penta_rag_graph/build_graph.py");
const graphTemplatePath = resolve(repoRoot, "scripts/penta_rag_graph/rag-graph.template.html");
const graphVendorPath = resolve(repoRoot, "scripts/penta_rag_graph/vendor/3d-force-graph.min.js");
const graphLicensePath = resolve(repoRoot, "scripts/penta_rag_graph/LICENSE-3d-force-graph.txt");
const defaultPreviewOrigin = "http://127.0.0.1:4004";
const postRoute = "/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/";
const viewerRoute = "/assets/visualizations/penta-rag-knowledge-graph/";
const expectedTaskFamilies = [
  "Coordinar agentes y decisiones",
  "Investigar y analizar datos",
  "Probar y verificar",
  "Versionar y comparar cambios",
  "Editar y comunicar",
  "Operar herramientas y servicios",
  "Leer y rastrear evidencia",
  "Ejecutar y automatizar",
];

const checks = [];

function check(name, condition, detail) {
  checks.push({ name, ok: Boolean(condition), detail });
}

function escaped(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function hasAll(text, values) {
  return values.every((value) => text.includes(value));
}

async function checkStaticSources() {
  const [post, viewer, readme, graphText, generator, template, vendor, license] = await Promise.all([
    readFile(postPath, "utf8"),
    readFile(viewerPath, "utf8"),
    readFile(viewerReadmePath, "utf8"),
    readFile(graphPath, "utf8"),
    readFile(graphGeneratorPath, "utf8"),
    readFile(graphTemplatePath, "utf8"),
    readFile(graphVendorPath, "utf8"),
    readFile(graphLicensePath, "utf8"),
  ]);
  const graph = JSON.parse(graphText);
  const normalizedReadme = readme.replace(/\s+/g, " ");

  check(
    "draft-has-public-safety-boundary",
    post.includes("Borrador ejecutable y local") &&
      post.includes("no contiene cuerpos de correo, adjuntos, direcciones, rutas absolutas, tokens ni credenciales") &&
      /\*\*No\*\*\s+están como nodos de contenido\./.test(post),
    "The post must keep the public projection and privacy boundary visible."
  );
  check(
    "post-keeps-textual-alternative",
    hasAll(post, [
      "**Tabla 1** — Alternativa textual y límites de la proyección",
      "Tipos de tarea",
      "Aristas semánticas",
      "Correo y tesis",
      "Similitud operacional, no causalidad.",
    ]),
    "The post, not the canvas, is the required readable alternative."
  );
  check(
    "embed-is-labeled-and-contained",
    /<iframe[^>]+title="Mapa 3D navegable de tipos de trabajo y estrategias de penta-agent"[^>]+sandbox="allow-scripts"[^>]+referrerpolicy="no-referrer"/.test(post),
    "The embedded viewer needs a descriptive title and the current containment attributes."
  );
  check(
    "full-viewer-link-is-safe",
    /target="_blank"\s+rel="noopener"/.test(post),
    "Opening the full viewer must preserve noopener."
  );
  check(
    "viewer-exposes-human-purpose-before-canvas",
    hasAll(viewer, [
      'id="viewer-main" aria-labelledby="graph-title"',
      'id="graph" role="region" aria-label="Grafo 3D de estrategias de trabajo.',
      'id="graph-instructions"',
      "Cada punto es una forma reutilizable de trabajar.",
      "La cercanía visual es similitud de trazas, no causalidad ni afinidad humana.",
    ]),
    "The viewer must explain what it represents and what proximity does not mean."
  );
  check(
    "viewer-has-keyboard-addressable-controls",
    hasAll(viewer, [
      'id="taskFilter"',
      'id="projectFilter"',
      'id="search"',
      'id="resetView"',
      'role="tablist" aria-label="Perspectiva del grafo"',
      'aria-pressed="${taskFilter===t.id}"',
      "Ver todos los tipos de tarea",
    ]),
    "The task/category workflow must remain operable without dragging the graph."
  );
  check(
    "viewer-keeps-all-reading-tabs",
    ["Tareas", "Temas", "Proy", "Libs", "Errores", "Mejora"].every((label) =>
      new RegExp(`<button[^>]+role="tab"[^>]*>${escaped(label)}</button>`).test(viewer)
    ),
    "All six explanatory tabs are required for the guided reading path."
  );
  check(
    "viewer-has-a-webgl-text-fallback",
    hasAll(viewer, [
      "function renderGraphFallback()",
      'host.classList.add("graph-fallback")',
      'host.setAttribute("aria-label","Resumen textual del mapa de trabajo; la vista 3D no está disponible")',
      'element("h2","La proyección 3D no pudo iniciarse")',
      "estrategias en el corte",
      "relaciones semánticas derivadas",
      "relaciones estructurales",
      "Qué tipo de trabajo representa el corte",
    ]),
    "The direct viewer must retain a readable fallback when WebGL cannot start."
  );
  check(
    "viewer-readme-keeps-regeneration-and-sanitization-contract",
    hasAll(normalizedReadme, [
      "--sanitize",
      "elimina rutas absolutas",
      "no contiene cuerpos de correo",
      "no carga un CDN ni consulta Qdrant desde el navegador",
      "--check-public",
    ]),
    "The generation contract must remain adjacent to the public viewer."
  );
  check(
    "viewer-source-is-versioned-and-checkable",
    hasAll(generator, [
      "--sanitize",
      "--render-public",
      "--check-public",
      "PUBLIC_GRAPH",
      "PUBLIC_HTML",
      "current != rendered",
    ]) &&
      template.includes("/*__VENDOR_JS__*/") &&
      vendor.startsWith("// Version 1.80.0 3d-force-graph") &&
      hasAll(license, ["MIT License", "Copyright (c) 2017 Vasco Asturiano"]),
    "The public graph needs versioned source, an offline vendor and a reproducibility check."
  );
  check(
    "public-graph-has-a-nonempty-derived-cut",
    Number.isInteger(graph?.meta?.points_indexed) && graph.meta.points_indexed > 0 &&
      Number.isInteger(graph?.meta?.nodes) && graph.meta.nodes > 0 &&
      Array.isArray(graph?.nodes) && graph.nodes.length === graph.meta.nodes &&
      Array.isArray(graph?.links) && graph.links.length > 0,
    "The static viewer must be backed by a nonempty public graph with matching node metadata."
  );
  check(
    "public-graph-backs-the-eight-fallback-families",
    graph?.meta?.task_families?.length === expectedTaskFamilies.length &&
      expectedTaskFamilies.every((label) => graph.meta.task_families.some((family) =>
        family.label === label && Number.isInteger(family.strategies) && family.strategies > 0
      )) &&
      Number.isInteger(graph.meta.semantic_edges) && graph.meta.semantic_edges > 0 &&
      Number.isInteger(graph.meta.structural_edges) && graph.meta.structural_edges > 0,
    "The fallback needs eight nonempty public task families and its derived metrics."
  );
}

async function checkPreview(origin) {
  const parsed = new URL(origin);
  if (parsed.origin !== defaultPreviewOrigin) {
    throw new Error(`--probe only permits ${defaultPreviewOrigin}; received ${parsed.origin}`);
  }

  for (const [name, route, expected] of [
    ["preview-post", postRoute, ["Multiagentes en 3 cucharadas III", "Mapa de trabajo aprendido por penta-agent", "Alternativa textual y límites de la proyección"]],
    ["preview-viewer", viewerRoute, ["Mapa de trabajo aprendido", 'id="taskFilter"', 'role="tablist"']],
  ]) {
    const response = await fetch(new URL(route, parsed));
    const body = await response.text();
    check(
      name,
      response.status === 200 && hasAll(body, expected),
      `${new URL(route, parsed)} must return 200 with the expected rendered content.`
    );
  }
}

function runAgentBrowser(args) {
  const result = spawnSync("agent-browser", args, {
    encoding: "utf8",
    timeout: 30_000,
  });
  const output = `${result.stdout ?? ""}${result.stderr ?? ""}`;
  if (result.error) {
    throw new Error(`agent-browser could not run: ${result.error.message}`);
  }
  if (result.status !== 0) {
    throw new Error(`agent-browser ${args.at(-1)} failed: ${output.trim()}`);
  }
  return output;
}

async function checkWebglFallback(origin) {
  const parsed = new URL(origin);
  if (parsed.origin !== defaultPreviewOrigin) {
    throw new Error(`--probe-webgl-fallback only permits ${defaultPreviewOrigin}; received ${parsed.origin}`);
  }

  const session = `postiii-gate-webgl-fallback-${process.pid}`;
  const scratch = await mkdtemp(join(tmpdir(), "postiii-webgl-fallback-"));
  const initScript = join(scratch, "disable-webgl.js");
  const viewerUrl = new URL(viewerRoute, parsed).toString();
  const expectedFamiliesJson = JSON.stringify(expectedTaskFamilies);
  const probeExpression = `(() => {
    const fallback = document.querySelector('#graph.graph-fallback');
    const text = fallback?.innerText || '';
    const labels = [...document.querySelectorAll('#graph.graph-fallback h4')].map((node) => node.textContent.trim());
    const expected = ${expectedFamiliesJson};
    const metricLabels = ['estrategias en el corte', 'relaciones semánticas derivadas', 'relaciones estructurales', 'tipos de tarea'];
    const metricText = [...document.querySelectorAll('#graph.graph-fallback .graph-fallback__metric')].map((node) => node.innerText).join(' ');
    const ok = !document.querySelector('#graph canvas') &&
      fallback?.getAttribute('role') === 'region' &&
      fallback?.getAttribute('aria-label') === 'Resumen textual del mapa de trabajo; la vista 3D no está disponible' &&
      text.includes('La proyección 3D no pudo iniciarse') &&
      metricLabels.every((label) => metricText.includes(label)) &&
      expected.every((label) => labels.includes(label));
    return ok ? 'POSTIII_WEBGL_FALLBACK_PASS' : 'POSTIII_WEBGL_FALLBACK_FAIL';
  })()`;

  try {
    await writeFile(initScript, `(() => {
  const original = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function(type, ...args) {
    if (["webgl", "webgl2", "experimental-webgl"].includes(String(type).toLowerCase())) return null;
    return original.call(this, type, ...args);
  };
})();\n`, "utf8");
    runAgentBrowser(["--session", session, "open", viewerUrl, "--headless", "--init-script", initScript]);
    runAgentBrowser(["--session", session, "wait", "--load", "networkidle"]);
    const result = runAgentBrowser(["--session", session, "eval", probeExpression]);
    check(
      "preview-webgl-fallback",
      result.includes("POSTIII_WEBGL_FALLBACK_PASS"),
      "The local Chromium simulation found the labeled fallback, four metrics, and all eight families. This is not Safari or Firefox evidence."
    );
  } catch (error) {
    check(
      "preview-webgl-fallback",
      false,
      `The local WebGL-off simulation could not prove the fallback: ${error.message}`
    );
  } finally {
    try {
      runAgentBrowser(["--session", session, "close"]);
    } catch {
      // The test result already records any failed browser action; cleanup is best-effort.
    }
    await rm(scratch, { recursive: true, force: true });
  }
}

function printManualProtocol() {
  console.log(`\nHuman-platform gate: read scripts/postiii_browser_gate.md\n`);
}

async function main() {
  const args = new Set(process.argv.slice(2));
  const unknown = [...args].filter((arg) => !["--probe", "--probe-webgl-fallback", "--manual"].includes(arg));
  if (unknown.length) {
    throw new Error(`Unknown argument(s): ${unknown.join(", ")}`);
  }

  await checkStaticSources();
  if (args.has("--probe")) {
    await checkPreview(defaultPreviewOrigin);
  }
  if (args.has("--probe-webgl-fallback")) {
    await checkWebglFallback(defaultPreviewOrigin);
  }

  for (const result of checks) {
    console.log(`${result.ok ? "PASS" : "FAIL"} ${result.name}: ${result.detail}`);
  }
  const failures = checks.filter((result) => !result.ok);
  if (args.has("--manual")) {
    printManualProtocol();
  }
  if (failures.length) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(`FAIL postiii-browser-gate: ${error.message}`);
  process.exitCode = 1;
});
