#!/usr/bin/env node

/**
 * Reproducible 10-second social-video capture for the public penta-agent graph.
 *
 * The canonical viewer is never edited. A localhost-only server exposes the
 * ForceGraph instance in memory, Playwright renders a deterministic camera
 * path at 4K (DPR 2), and FFmpeg downsamples/encodes upload-ready candidates.
 */

import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { createReadStream, createWriteStream } from "node:fs";
import {
  access,
  copyFile,
  mkdir,
  mkdtemp,
  readFile,
  rename,
  stat,
  writeFile,
} from "node:fs/promises";
import http from "node:http";
import { tmpdir } from "node:os";
import { dirname, extname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(SCRIPT_DIR, "..");
const WORKSPACE_ROOT = resolve(REPO_ROOT, "../..");
const VIEWER_RELATIVE = "assets/visualizations/penta-rag-knowledge-graph/index.html";
const GRAPH_RELATIVE = "assets/data/rag_knowledge_graph/public-graph.json";
const DEFAULT_OUTPUT = resolve(
  REPO_ROOT,
  "assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-linkedin-x.mp4",
);
const PLAYWRIGHT_ENTRY = resolve(
  WORKSPACE_ROOT,
  "penta-agent/tools/playwright-local-mcp/node_modules/playwright/index.js",
);
const GRAPH_ANCHOR = "const Graph = ForceGraph3D";
const GRAPH_REPLACEMENT =
  "GRAPH.nodes.forEach(node => { node.fx = node.x; node.fy = node.y; node.fz = node.z; });\n" +
  "const Graph = window.__captureGraph = ForceGraph3D";
const SOURCE_PUBLIC_URL =
  "https://3cucharadas.cl/assets/visualizations/penta-rag-knowledge-graph/index.html";

const FPS = 30;
const FRAME_COUNT = 300;
const VIEWPORT = { width: 1920, height: 1080 };
const DEVICE_SCALE_FACTOR = 2;
const PHYSICAL_FRAME = { width: 3840, height: 2160 };
const FOCUS_STRENGTH = 1;
const MIN_RADIUS_SCALE = 0.12;
const START_POSITION = { x: 0, y: 0, z: 3600 };
const START_TARGET = { x: 0, y: 0, z: 0 };
const CRF_CANDIDATES = [14, 16, 18];
const QUALITY_THRESHOLDS = { vmaf: 97, ssim: 0.995, psnr: 42 };
const CROSS_SESSION_SSIM_MIN = 0.9999;
const LAYOUT_ANCHOR = 'Graph.d3Force("charge").strength(-95);';
const LAYOUT_REPLACEMENT = `${LAYOUT_ANCHOR}
Graph.warmupTicks(180).cooldownTicks(0).onEngineStop(() => {
  Graph.graphData().nodes.forEach(n => { n.fx=n.x; n.fy=n.y; n.fz=n.z; });
  window.__captureLayoutReady = true;
});`;

const MIME_TYPES = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
};

function parseArgs(argv) {
  const options = {
    output: DEFAULT_OUTPUT,
    scratch: null,
    resumeScratch: null,
    checkResumeOnly: false,
    overwrite: false,
    selfTest: false,
    preview: false,
    encodeOnly: false,
    verify: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--output") options.output = resolve(argv[++index]);
    else if (argument === "--scratch") options.scratch = resolve(argv[++index]);
    else if (argument === "--resume-scratch") options.resumeScratch = resolve(argv[++index]);
    else if (argument === "--check-resume-only") options.checkResumeOnly = true;
    else if (argument === "--overwrite") options.overwrite = true;
    else if (argument === "--self-test") options.selfTest = true;
    else if (argument === "--preview") options.preview = true;
    else if (argument === "--encode-only") options.encodeOnly = true;
    else if (argument === "--verify") options.verify = resolve(argv[++index]);
    else if (argument === "--help") {
      console.log(`Usage: node ${relative(process.cwd(), fileURLToPath(import.meta.url))} [options]\n\n` +
        "  --output PATH    Final MP4 path\n" +
        "  --scratch PATH   New/empty scratch directory (kept for human review)\n" +
        "  --resume-scratch PATH  Reuse a completed 4K frame sequence after validating frame 0\n" +
        "  --check-resume-only  Stop after the independent frame-0 reproducibility check\n" +
        "  --overwrite      Replace an existing final MP4 and manifest\n" +
        "  --self-test      Exercise fail-closed invariants without opening a browser");
      console.log("  --preview        Capture five keyframes only; no MP4\n" +
        "  --encode-only    Encode verified saved frames; requires --resume-scratch\n" +
        "  --verify PATH    Audit an existing 10s/1080p/30fps delivery; no writes");
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  return options;
}

function sha256Buffer(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

async function sha256File(path) {
  return await new Promise((resolvePromise, rejectPromise) => {
    const hash = createHash("sha256");
    createReadStream(path)
      .on("error", rejectPromise)
      .on("data", (chunk) => hash.update(chunk))
      .on("end", () => resolvePromise(hash.digest("hex")));
  });
}

function injectCaptureHook(html) {
  const occurrences = html.split(GRAPH_ANCHOR).length - 1;
  if (occurrences !== 1) {
    throw new Error(`Capture hook requires exactly one Graph anchor; found ${occurrences}`);
  }
  const hooked = html.replace(GRAPH_ANCHOR, GRAPH_REPLACEMENT);
  if (html === GRAPH_ANCHOR) return hooked; // Unit fixture, not a viewer.
  const layoutOccurrences = html.split(LAYOUT_ANCHOR).length - 1;
  if (layoutOccurrences !== 1) throw new Error(`Layout hook requires one anchor; found ${layoutOccurrences}`);
  return hooked.replace(LAYOUT_ANCHOR, LAYOUT_REPLACEMENT);
}

function envelope(t) {
  return Math.sin(Math.PI * t) ** 2;
}

function cameraPose(t, startPosition, startTarget, focusNode) {
  const amount = envelope(t);
  const target = {
    x: startTarget.x + (focusNode.x - startTarget.x) * FOCUS_STRENGTH * amount,
    y: startTarget.y + (focusNode.y - startTarget.y) * FOCUS_STRENGTH * amount,
    z: startTarget.z + (focusNode.z - startTarget.z) * FOCUS_STRENGTH * amount,
  };
  const vector = {
    x: startPosition.x - startTarget.x,
    y: startPosition.y - startTarget.y,
    z: startPosition.z - startTarget.z,
  };
  const angle = 2 * Math.PI * t;
  const cosine = Math.cos(angle);
  const sine = Math.sin(angle);
  const scale = MIN_RADIUS_SCALE ** amount;
  const rotated = {
    x: (vector.x * cosine + vector.z * sine) * scale,
    y: vector.y * scale,
    z: (-vector.x * sine + vector.z * cosine) * scale,
  };
  return {
    position: {
      x: target.x + rotated.x,
      y: target.y + rotated.y,
      z: target.z + rotated.z,
    },
    target,
    radiusScale: scale,
    focusEnvelope: amount,
  };
}

function maximumCoordinateDelta(left, right) {
  return Math.max(
    Math.abs(left.x - right.x),
    Math.abs(left.y - right.y),
    Math.abs(left.z - right.z),
  );
}

function assertCaptureStateMatches(actual, expected) {
  const cameraDelta = Math.max(
    maximumCoordinateDelta(actual.startPosition, expected.startPosition),
    maximumCoordinateDelta(actual.startTarget, expected.startTarget),
    maximumCoordinateDelta(actual.focusNode, expected.focusNode),
  );
  if (!Number.isFinite(cameraDelta) || cameraDelta > 1e-9) {
    throw new Error(`Capture state drift ${cameraDelta} exceeds 1e-9`);
  }
  assert.equal(actual.layoutSha256, expected.layoutSha256, "Full graph layout drift");
  assert.deepEqual(actual.framebuffer, expected.framebuffer, "WebGL framebuffer drift");
  return cameraDelta;
}

function runSelfTest() {
  const expectedFailures = [];
  for (const [name, malformed] of [
    ["missing-anchor", "<html></html>"],
    ["duplicate-anchor", `${GRAPH_ANCHOR}\n${GRAPH_ANCHOR}`],
  ]) {
    assert.throws(() => injectCaptureHook(malformed), /exactly one Graph anchor/);
    expectedFailures.push(name);
    console.log(`[expected-red] ${name}: rejected`);
  }
  assert.equal(injectCaptureHook(GRAPH_ANCHOR), GRAPH_REPLACEMENT);
  const position = { x: 30, y: 12, z: 90 };
  const target = { x: 1, y: 2, z: 3 };
  const focus = { x: -104, y: 1.2, z: -13.5 };
  const start = cameraPose(0, position, target, focus);
  const finish = cameraPose(1, position, target, focus);
  const middle = cameraPose(0.5, position, target, focus);
  assert.ok(maximumCoordinateDelta(start.position, finish.position) < 1e-10);
  assert.ok(maximumCoordinateDelta(start.target, finish.target) < 1e-10);
  assert.ok(Math.abs(middle.radiusScale - MIN_RADIUS_SCALE) < 1e-12);
  assert.ok(START_POSITION.z * MIN_RADIUS_SCALE <= 500, "Zoom must reach the corpus core");
  assert.equal(FOCUS_STRENGTH, 1, "Zoom must reach its target");
  const state = {startPosition:position,startTarget:target,focusNode:focus,layoutSha256:"a",framebuffer:PHYSICAL_FRAME};
  assert.throws(() => assertCaptureStateMatches({...state,layoutSha256:"b"},state), /Full graph layout drift/);
  assert.throws(() => assertCaptureStateMatches({...state,startPosition:{x:NaN,y:0,z:0}},state), /Capture state drift/);
  assert.equal(assertCaptureStateMatches(state,state),0);
  console.log("[expected-red] changed layout and NaN camera: rejected; valid state: green");
  assert.deepEqual(expectedFailures, ["missing-anchor", "duplicate-anchor"]);
  console.log("[green] capture hook and seamless camera-path invariants passed");
}

async function ensureNewScratch(path) {
  if (!path) return await mkdtemp(join(tmpdir(), "penta-rag-video-"));
  try {
    await access(path);
    const entries = await import("node:fs/promises").then(({ readdir }) => readdir(path));
    if (entries.length > 0) throw new Error(`Scratch directory is not empty: ${path}`);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
    await mkdir(path, { recursive: true });
  }
  return path;
}

async function pathExists(path) {
  try {
    await access(path);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

function serverPath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?")[0]);
  const candidate = resolve(REPO_ROOT, `.${decoded}`);
  const rootPrefix = `${REPO_ROOT}${sep}`;
  if (candidate !== REPO_ROOT && !candidate.startsWith(rootPrefix)) return null;
  return candidate;
}

async function startLocalServer(injectedViewer) {
  const viewerRoute = `/${VIEWER_RELATIVE}`;
  const server = http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url ?? "/", "http://127.0.0.1");
      let pathname = url.pathname;
      if (pathname.endsWith("/")) pathname += "index.html";
      if (pathname === viewerRoute) {
        response.writeHead(200, {
          "Cache-Control": "no-store",
          "Content-Type": MIME_TYPES[".html"],
        });
        response.end(injectedViewer);
        return;
      }
      // The viewer is self-contained. Never expose the surrounding repository.
      response.writeHead(pathname === "/favicon.ico" ? 204 : 404);
      response.end();
    } catch (error) {
      response.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      response.end(String(error));
    }
  });
  await new Promise((resolvePromise, rejectPromise) => {
    server.once("error", rejectPromise);
    server.listen(0, "127.0.0.1", resolvePromise);
  });
  const address = server.address();
  assert.equal(typeof address, "object");
  return {
    origin: `http://127.0.0.1:${address.port}`,
    close: () => new Promise((resolvePromise, rejectPromise) =>
      server.close((error) => error ? rejectPromise(error) : resolvePromise())),
  };
}

async function pngDimensions(path) {
  const file = await readFile(path);
  assert.equal(file.subarray(1, 4).toString("ascii"), "PNG");
  return { width: file.readUInt32BE(16), height: file.readUInt32BE(20) };
}

async function run(command, args, options = {}) {
  const printable = [command, ...args].map((part) => /\s/.test(part) ? JSON.stringify(part) : part).join(" ");
  if (!options.quiet) console.log(`$ ${printable}`);
  return await new Promise((resolvePromise, rejectPromise) => {
    const child = spawn(command, args, {
      cwd: options.cwd,
      env: { ...process.env, ...options.env },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
      if (options.stream) process.stdout.write(chunk);
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
      if (options.stream) process.stderr.write(chunk);
    });
    child.once("error", rejectPromise);
    child.once("close", (code) => {
      if (code === 0) resolvePromise({ stdout, stderr, printable });
      else rejectPromise(new Error(`${command} exited ${code}\n${stderr.slice(-5000)}`));
    });
  });
}

async function captureFrames({ scratch, viewerHtml, resume = false, preview = false }) {
  const playwrightModule = await import(pathToFileURL(PLAYWRIGHT_ENTRY).href);
  const chromium = playwrightModule.chromium ?? playwrightModule.default?.chromium;
  if (!chromium) throw new Error(`Playwright Chromium API is unavailable at ${PLAYWRIGHT_ENTRY}`);
  const local = await startLocalServer(injectCaptureHook(viewerHtml));
  const framesDir = join(scratch, "frames-4k");
  await mkdir(framesDir, { recursive: true });
  let browser;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const context = await browser.newContext({
      viewport: VIEWPORT,
      deviceScaleFactor: DEVICE_SCALE_FACTOR,
      colorScheme: "dark",
      locale: "es-CL",
      timezoneId: "America/Santiago",
      reducedMotion: "reduce",
    });
    await context.route("**/*", async (route) => {
      const requested = route.request().url();
      if (new URL(requested).origin === local.origin || requested.startsWith("data:") || requested.startsWith("blob:")) {
        await route.continue();
      } else {
        await route.abort("blockedbyclient");
      }
    });
    const page = await context.newPage();
    await page.addInitScript(() => {
      // Fixed layout initialization, including the nodes without source coordinates.
      let seed = 20260906;
      Math.random = () => ((seed = Math.imul(1664525, seed) + 1013904223 >>> 0) / 4294967296);
    });
    const consoleErrors = [];
    page.on("pageerror", (error) => consoleErrors.push(String(error)));
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    await page.goto(`${local.origin}/${VIEWER_RELATIVE}`, { waitUntil: "load" });
    await page.waitForFunction(
      () => {
        const graph = window.__captureGraph;
        return graph && window.__captureLayoutReady && graph.graphData().nodes.every(
          n => [n.x,n.y,n.z].every(Number.isFinite));
      },
      null,
      { timeout: 30_000 },
    );
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(6_200);
    await page.evaluate(() => window.__captureGraph.linkDirectionalParticles(0));
    await page.waitForTimeout(150);

    const state = await page.evaluate(({ startPosition, startTarget, pixelRatio }) => {
      const graph = window.__captureGraph;
      graph.pauseAnimation();
      graph.linkDirectionalParticles(0);
      const controls = graph.controls();
      controls.autoRotate = false;
      controls.enableDamping = false;
      controls.enabled = false;
      document.documentElement.style.cursor = "none";
      document.body.style.cursor = "none";
      const camera = graph.camera();
      camera.position.set(startPosition.x, startPosition.y, startPosition.z);
      controls.target.set(startTarget.x, startTarget.y, startTarget.z);
      camera.lookAt(startTarget.x, startTarget.y, startTarget.z);
      camera.updateMatrixWorld(true);
      camera.updateProjectionMatrix();
      const renderer = graph.renderer();
      renderer.setPixelRatio(pixelRatio);
      renderer.render(graph.scene(), camera);
      const nodes = graph.graphData().nodes;
      // Published corpus coordinates are centered at the origin; do not target an edge node.
      const focus = {id:"corpus-center",x:0,y:0,z:0};
      const gl = renderer.getContext();
      const captureState = {
        startPosition: { x: camera.position.x, y: camera.position.y, z: camera.position.z },
        startTarget: { x: controls.target.x, y: controls.target.y, z: controls.target.z },
        focusNode: focus,
        layout: nodes.map(n => ({id:n.id,x:n.x,y:n.y,z:n.z})),
        framebuffer: {width:gl.drawingBufferWidth,height:gl.drawingBufferHeight},
      };
      window.__captureState = captureState;
      return captureState;
    }, { startPosition: START_POSITION, startTarget: START_TARGET, pixelRatio: DEVICE_SCALE_FACTOR });
    state.layoutSha256 = sha256Buffer(Buffer.from(JSON.stringify(state.layout)));
    assert.deepEqual(state.framebuffer, PHYSICAL_FRAME, "Native WebGL capture must be 4K");
    if (!resume) await writeFile(join(scratch, "capture-state.json"), JSON.stringify(state, null, 2));

    const renderPose = async (t) => {
      const pose = cameraPose(t, state.startPosition, state.startTarget, state.focusNode);
      await page.evaluate(({ position, target }) => {
        const graph = window.__captureGraph;
        const camera = graph.camera();
        const controls = graph.controls();
        camera.position.set(position.x, position.y, position.z);
        controls.target.set(target.x, target.y, target.z);
        camera.lookAt(target.x, target.y, target.z);
        camera.updateMatrixWorld(true);
        camera.updateProjectionMatrix();
        graph.renderer().render(graph.scene(), camera);
      }, pose);
    };

    let resumeStartFrame = null;
    if (resume) {
      resumeStartFrame = join(scratch, "resume-start-4k.png");
      await renderPose(0);
      await page.screenshot({ path: resumeStartFrame, type: "png", animations: "disabled" });
    } else {
      const indices = preview ? [0,75,150,225,299] : Array.from({length:FRAME_COUNT}, (_,i)=>i);
      for (const frame of indices) {
        await renderPose(frame / FRAME_COUNT);
        const path = join(framesDir, `frame-${String(frame).padStart(4, "0")}.png`);
        await page.screenshot({ path, type: "png", animations: "disabled" });
        if (frame % FPS === 0 || frame === FRAME_COUNT - 1) {
          console.log(`[capture] ${frame + 1}/${FRAME_COUNT} frames`);
        }
      }
    }
    const closeFrame = join(scratch, "loop-close-4k.png");
    if (!resume) {
      await renderPose(1);
      await page.screenshot({ path: closeFrame, type: "png", animations: "disabled" });
    }
    await context.close();
    if (consoleErrors.length > 0) {
      throw new Error(`Browser console errors: ${consoleErrors.join(" | ")}`);
    }
    return {
      framesDir,
      closeFrame,
      state,
      resumeStartFrame,
      chromiumVersion: browser.version(),
    };
  } finally {
    if (browser) await browser.close();
    await local.close();
  }
}

function parseFinite(regex, text, label) {
  const match = text.match(regex);
  if (!match) throw new Error(`Could not parse ${label} from FFmpeg output`);
  const value = Number(match[1]);
  if (!Number.isFinite(value)) throw new Error(`${label} is not finite: ${match[1]}`);
  return value;
}

async function compareImages(first, second) {
  const { stderr } = await run("ffmpeg", [
    "-hide_banner", "-nostats", "-i", first, "-i", second,
    "-lavfi", "[0:v][1:v]ssim", "-f", "null", "-",
  ], { quiet: true });
  return parseFinite(/All:([0-9.]+)/, stderr, "loop SSIM");
}

async function measureQuality(candidate, reference, scratch, label) {
  const vmafLog = `${label}-vmaf.json`;
  await run("ffmpeg", [
    "-hide_banner", "-nostats", "-i", candidate, "-i", reference,
    "-lavfi", `[0:v]fps=${FPS},settb=AVTB,setpts=N/(${FPS}*TB)[dist];[1:v]fps=${FPS},settb=AVTB,setpts=N/(${FPS}*TB)[ref];[dist][ref]libvmaf=log_fmt=json:log_path=${vmafLog}`,
    "-f", "null", "-",
  ], { cwd: scratch, quiet: true });
  const vmafJson = JSON.parse(await readFile(join(scratch, vmafLog), "utf8"));
  const vmaf = Number(vmafJson?.pooled_metrics?.vmaf?.mean);
  const ssimResult = await run("ffmpeg", [
    "-hide_banner", "-nostats", "-i", candidate, "-i", reference,
    "-lavfi", `[0:v]fps=${FPS},settb=AVTB,setpts=N/(${FPS}*TB)[dist];[1:v]fps=${FPS},settb=AVTB,setpts=N/(${FPS}*TB)[ref];[dist][ref]ssim`, "-f", "null", "-",
  ], { quiet: true });
  const psnrResult = await run("ffmpeg", [
    "-hide_banner", "-nostats", "-i", candidate, "-i", reference,
    "-lavfi", `[0:v]fps=${FPS},settb=AVTB,setpts=N/(${FPS}*TB)[dist];[1:v]fps=${FPS},settb=AVTB,setpts=N/(${FPS}*TB)[ref];[dist][ref]psnr`, "-f", "null", "-",
  ], { quiet: true });
  const ssim = parseFinite(/All:([0-9.]+)/, ssimResult.stderr, "SSIM");
  const psnr = parseFinite(/average:([0-9.]+)/, psnrResult.stderr, "PSNR");
  return {
    vmaf,
    ssim,
    psnr,
    passes:
      vmaf >= QUALITY_THRESHOLDS.vmaf &&
      ssim >= QUALITY_THRESHOLDS.ssim &&
      psnr >= QUALITY_THRESHOLDS.psnr,
  };
}

async function probeVideo(path) {
  const result = await run("ffprobe", [
    "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", path,
  ], { quiet: true });
  return JSON.parse(result.stdout);
}

async function peakRollingBitrate(path) {
  const result = await run("ffprobe", [
    "-v", "error", "-select_streams", "v:0", "-show_packets",
    "-show_entries", "packet=pts_time,size", "-of", "json", path,
  ], { quiet: true });
  const packets = JSON.parse(result.stdout).packets
    .map((packet) => ({ time: Number(packet.pts_time), bytes: Number(packet.size) }))
    .filter((packet) => Number.isFinite(packet.time) && Number.isFinite(packet.bytes))
    .sort((a,b) => a.time-b.time);
  let start = 0;
  let bytes = 0;
  let maximum = 0;
  for (let end = 0; end < packets.length; end += 1) {
    bytes += packets[end].bytes;
    while (packets[end].time - packets[start].time >= 1 && start < end) {
      bytes -= packets[start].bytes;
      start += 1;
    }
    maximum = Math.max(maximum, bytes * 8);
  }
  return maximum;
}

async function decodedFrameAudit(path) {
  const hashes = await run("ffmpeg", [
    "-hide_banner", "-loglevel", "error", "-i", path, "-f", "framemd5", "-",
  ], { quiet: true });
  const values = hashes.stdout
    .split("\n")
    .filter((line) => line && !line.startsWith("#"))
    .map((line) => line.split(",").at(-1).trim());
  let maximumIdenticalRun = 1;
  let currentRun = 1;
  for (let index = 1; index < values.length; index += 1) {
    if (values[index] === values[index - 1]) currentRun += 1;
    else currentRun = 1;
    maximumIdenticalRun = Math.max(maximumIdenticalRun, currentRun);
  }
  const detector = await run("ffmpeg", [
    "-hide_banner", "-nostats", "-i", path,
    "-vf", "blackdetect=d=0.2:pix_th=0.01:pic_th=0.98,freezedetect=n=0.001:d=0.4",
    "-an", "-f", "null", "-",
  ], { quiet: true });
  return {
    framesDecoded: values.length,
    uniqueDecodedFrames: new Set(values).size,
    maximumIdenticalRun,
    blackIntervals: (detector.stderr.match(/black_start:/g) ?? []).length,
    freezeIntervals: (detector.stderr.match(/freeze_start:/g) ?? []).length,
  };
}

async function verifyDelivery(path) {
  const probe = await probeVideo(path);
  assert.equal(probe.streams.length, 1, "Expected one video stream and no audio");
  const video = probe.streams[0];
  for (const [key,value] of Object.entries({codec_name:"h264",width:1920,height:1080,
    pix_fmt:"yuv420p",avg_frame_rate:"30/1",color_range:"tv",color_space:"bt709",
    color_transfer:"bt709",color_primaries:"bt709"})) assert.equal(video[key],value,key);
  assert.equal(Number(video.nb_read_frames),FRAME_COUNT,"Frame count");
  const duration = Number(probe.format.duration);
  assert.ok(Math.abs(duration-10)<=0.02,"Duration must be 10 seconds");
  assert.ok(Number(probe.format.size)<512_000_000,"Upload size");
  const packetResult = await run("ffprobe", ["-v","error","-select_streams","v:0","-show_packets",
    "-show_entries","packet=pts_time","-of","json",path],{quiet:true});
  const times=JSON.parse(packetResult.stdout).packets.map(p=>Number(p.pts_time)).sort((a,b)=>a-b);
  assert.equal(times.length,FRAME_COUNT);
  assert.ok(times.every((t,i)=>Number.isFinite(t)&&Math.abs(t-i/FPS)<0.00001),"CFR timestamps");
  const buffer=await readFile(path);
  const atoms=[];
  for(let offset=0;offset+8<=buffer.length;) {
    let size=buffer.readUInt32BE(offset);
    if(size===1) size=Number(buffer.readBigUInt64BE(offset+8));
    if(size===0) size=buffer.length-offset;
    assert.ok(size>=8&&offset+size<=buffer.length,"Invalid MP4 atom");
    atoms.push(buffer.toString("ascii",offset+4,offset+8));
    offset+=size;
  }
  assert.ok(atoms.includes("moov")&&atoms.includes("mdat")&&atoms.indexOf("moov")<atoms.indexOf("mdat"),"faststart");
  const peakOneSecondBitrate=await peakRollingBitrate(path);
  assert.ok(peakOneSecondBitrate<=25_000_000,"Peak bitrate");
  const decoded=await decodedFrameAudit(path);
  assert.ok(decoded.uniqueDecodedFrames>=295&&decoded.maximumIdenticalRun<=1,"Motion frames");
  assert.equal(decoded.blackIntervals,0,"Black interval");
  assert.equal(decoded.freezeIntervals,0,"Frozen interval");
  return {probe,duration,peakOneSecondBitrate,decoded,cfr:true,faststart:true};
}

async function frameReceipt(framesDir) {
  const entries=[];
  for(let i=0;i<FRAME_COUNT;i++) {
    const name=`frame-${String(i).padStart(4,"0")}.png`;
    assert.deepEqual(await pngDimensions(join(framesDir,name)),PHYSICAL_FRAME,name);
    entries.push({name,sha256:await sha256File(join(framesDir,name))});
  }
  return entries;
}

async function encodeAndValidate({ scratch, framesDir, closeFrame, output }) {
  const framePattern = join(framesDir, "frame-%04d.png");
  const firstFrame = join(framesDir, "frame-0000.png");
  const reference = join(scratch, "reference-1080p-ffv1.mkv");
  const contactSheet = join(scratch, "contact-sheet-final.jpg");
  const scaleFilter = "scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p";
  const colorArgs = [
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
  ];
  const h264ColorArgs = [
    ...colorArgs,
    "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709:fullrange=off",
  ];
  await run("ffmpeg", [
    "-hide_banner", "-y", "-framerate", String(FPS), "-i", framePattern,
    "-frames:v", String(FRAME_COUNT), "-vf", scaleFilter,
    "-c:v", "ffv1", "-level", "3", "-g", "1", "-slicecrc", "1", ...colorArgs, reference,
  ], { stream: true });

  const candidates = [];
  for (const crf of CRF_CANDIDATES) {
    const candidate = join(scratch, `candidate-crf${crf}.mp4`);
    const encodeArgs = [
      "-hide_banner", "-y", "-i", reference,
      "-frames:v", String(FRAME_COUNT),
      "-c:v", "libx264", "-preset", "slow", "-crf", String(crf),
      "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p",
      "-r", String(FPS), "-g", "60", "-keyint_min", "60", "-sc_threshold", "0",
      "-maxrate", "20M", "-bufsize", "40M", "-movflags", "+faststart", "-an",
      ...h264ColorArgs, candidate,
    ];
    await run("ffmpeg", encodeArgs, { stream: true });
    const quality = await measureQuality(candidate, reference, scratch, `crf${crf}`);
    candidates.push({
      crf,
      path: candidate,
      bytes: (await stat(candidate)).size,
      encodeCommand: ["ffmpeg", ...encodeArgs].join(" "),
      ...quality,
    });
    console.log(`[quality] CRF ${crf}: VMAF=${quality.vmaf.toFixed(3)} SSIM=${quality.ssim.toFixed(6)} PSNR=${quality.psnr.toFixed(3)} pass=${quality.passes}`);
  }
  const passing = candidates.filter((candidate) => candidate.passes).sort((a, b) => a.bytes - b.bytes);
  if (passing.length === 0) throw new Error("No encode candidate passed the quality thresholds");
  const selected = passing[0];

  const loopSsim = await compareImages(firstFrame, closeFrame);
  if (loopSsim < 0.9999) throw new Error(`Loop closure SSIM ${loopSsim} is below 0.9999`);
  const {probe,duration,peakOneSecondBitrate,decoded}=await verifyDelivery(selected.path);

  await run("ffmpeg", [
    "-hide_banner", "-y", "-i", selected.path,
    "-vf", "fps=1,scale=640:-1:flags=lanczos,tile=5x2:padding=4:margin=4:color=0x16161e",
    "-frames:v", "1", "-q:v", "2", contactSheet,
  ], { quiet: true });
  await mkdir(dirname(output), { recursive: true });
  const partial = `${output}.partial-${process.pid}`;
  await copyFile(selected.path, partial);
  await rename(partial, output);
  return {
    candidates,
    selected,
    reference,
    contactSheet,
    loopSsim,
    probe,
    duration,
    peakOneSecondBitrate,
    decoded,
  };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.selfTest) {
    runSelfTest();
    return;
  }
  if (options.verify) {
    const audit=await verifyDelivery(options.verify);
    console.log(JSON.stringify({status:"pass",path:options.verify,sha256:await sha256File(options.verify),
      bytes:(await stat(options.verify)).size,...audit},null,2));
    return;
  }
  const output = options.output;
  assert.ok(/\.mp4$/i.test(output),"Output must end in .mp4");
  const manifestPath = output.replace(/\.mp4$/i, ".json");
  if (options.checkResumeOnly && !options.resumeScratch) {
    throw new Error("--check-resume-only requires --resume-scratch");
  }
  if (!options.preview && !options.checkResumeOnly && !options.overwrite && ((await pathExists(output)) || (await pathExists(manifestPath)))) {
    throw new Error(`Output or manifest already exists; use --overwrite: ${output}`);
  }
  if (options.scratch && options.resumeScratch) {
    throw new Error("Use either --scratch or --resume-scratch, not both");
  }
  if(options.encodeOnly&&!options.resumeScratch) throw new Error("--encode-only requires --resume-scratch");
  const scratch = options.resumeScratch ?? await ensureNewScratch(options.scratch);
  if (options.resumeScratch && !(await pathExists(scratch))) {
    throw new Error(`Resume scratch does not exist: ${scratch}`);
  }
  const viewerPath = resolve(REPO_ROOT, VIEWER_RELATIVE);
  const graphPath = resolve(REPO_ROOT, GRAPH_RELATIVE);
  const [viewerBuffer, graphBuffer] = await Promise.all([readFile(viewerPath), readFile(graphPath)]);
  const viewerHtml = viewerBuffer.toString("utf8");
  injectCaptureHook(viewerHtml);
  console.log(`[scratch] ${scratch}`);
  console.log(`[source] ${viewerPath}`);

  const capture = options.encodeOnly ? JSON.parse(await readFile(join(scratch,"capture-receipt.json"),"utf8"))
    : await captureFrames({ scratch, viewerHtml, resume: Boolean(options.resumeScratch), preview:options.preview });
  let resumeSsim = null;
  let replayStateDelta = null;
  if(options.encodeOnly) {
    assert.equal(capture.sourceSha256,sha256Buffer(viewerBuffer),"Source changed since capture");
    assert.equal(capture.scriptSha256,await sha256File(fileURLToPath(import.meta.url)),"Recipe changed since capture");
    assert.deepEqual(await frameReceipt(capture.framesDir),capture.frameHashes,"Saved frame integrity");
    resumeSsim=capture.replaySsim;
    replayStateDelta=0;
  } else if (options.resumeScratch) {
    for (const required of [
      join(capture.framesDir, "frame-0000.png"),
      join(capture.framesDir, "frame-0299.png"),
      capture.closeFrame,
    ]) {
      if (!(await pathExists(required))) throw new Error(`Resume input is missing: ${required}`);
    }
    resumeSsim = await compareImages(
      join(capture.framesDir, "frame-0000.png"),
      capture.resumeStartFrame,
    );
    const statePath = join(scratch, "capture-state.json");
    if (!(await pathExists(statePath))) {
      throw new Error(`Resume state is missing: ${statePath}`);
    }
    const expectedState = JSON.parse(await readFile(statePath, "utf8"));
    replayStateDelta = assertCaptureStateMatches(capture.state, expectedState);
    console.log(`[resume-state] layout=${capture.state.layoutSha256}`);
    if (resumeSsim < CROSS_SESSION_SSIM_MIN) {
      throw new Error(`Resume frame-0 SSIM ${resumeSsim} is below ${CROSS_SESSION_SSIM_MIN}; recapture required`);
    }
    console.log(`[green] resume frame-0 SSIM=${resumeSsim.toFixed(6)}`);
  } else {
    const statePath = join(scratch, "capture-state.json");
    await writeFile(statePath, `${JSON.stringify(capture.state, null, 2)}\n`);
    const replay = await captureFrames({ scratch, viewerHtml, resume: true });
    replayStateDelta = assertCaptureStateMatches(replay.state, capture.state);
    resumeSsim = await compareImages(
      join(capture.framesDir, "frame-0000.png"),
      replay.resumeStartFrame,
    );
    if (resumeSsim < CROSS_SESSION_SSIM_MIN) {
      throw new Error(`Independent frame-0 SSIM ${resumeSsim} is below ${CROSS_SESSION_SSIM_MIN}`);
    }
    console.log(`[green] independent replay: state delta=${replayStateDelta} SSIM=${resumeSsim.toFixed(6)}`);
  }
  if(options.preview) {
    console.log(`[green] preview: ${capture.framesDir}; all ${capture.state.layout.length} nodes fixed; framebuffer=${JSON.stringify(capture.state.framebuffer)}; replay SSIM=${resumeSsim}`);
    return;
  }
  const firstDimensions = await pngDimensions(join(capture.framesDir, "frame-0000.png"));
  const lastDimensions = await pngDimensions(join(capture.framesDir, "frame-0299.png"));
  assert.deepEqual(firstDimensions, PHYSICAL_FRAME);
  assert.deepEqual(lastDimensions, PHYSICAL_FRAME);
  if (options.checkResumeOnly) {
    console.log(`[green] deterministic replay gate passed: SSIM=${resumeSsim.toFixed(6)}`);
    return;
  }
  if(!options.encodeOnly) {
    capture.frameHashes=await frameReceipt(capture.framesDir);
    capture.sourceSha256=sha256Buffer(viewerBuffer);
    capture.scriptSha256=await sha256File(fileURLToPath(import.meta.url));
    capture.replaySsim=resumeSsim;
    await writeFile(join(scratch,"capture-receipt.json"),JSON.stringify(capture,null,2));
  }
  const encoding = await encodeAndValidate({
    scratch,
    framesDir: capture.framesDir,
    closeFrame: capture.closeFrame,
    output,
  });

  const ffmpegVersion = (await run("ffmpeg", ["-version"], { quiet: true })).stdout.split("\n")[0];
  const ffprobeVersion = (await run("ffprobe", ["-version"], { quiet: true })).stdout.split("\n")[0];
  const finalSha256 = await sha256File(output);
  const manifest = {
    schemaVersion: 1,
    createdAt: new Date().toISOString(),
    status: "centered_zoom_technical_pass",
    source: {
      publicUrl: SOURCE_PUBLIC_URL,
      localViewer: relative(REPO_ROOT, viewerPath),
      localGraph: relative(REPO_ROOT, graphPath),
      viewerSha256: sha256Buffer(viewerBuffer),
      graphSha256: sha256Buffer(graphBuffer),
      runtimeAdapter: {
        persistedToViewer: false,
        anchor: GRAPH_ANCHOR,
        replacement: GRAPH_REPLACEMENT,
        layoutReplacement: LAYOUT_REPLACEMENT,
      },
    },
    motion: {
      durationSeconds: FRAME_COUNT / FPS,
      fps: FPS,
      frameCount: FRAME_COUNT,
      sample: "t = frame_index / 300; frame 300 is validation-only and not encoded",
      orbitRadians: "2*pi*t",
      focusEnvelope: "sin(pi*t)^2",
      focusNode: capture.state.focusNode,
      focusStrength: FOCUS_STRENGTH,
      minimumRadiusScale: MIN_RADIUS_SCALE,
      radiusInterpolation: "minimumRadiusScale ** sin(pi*t)^2",
      closestDistance: START_POSITION.z * MIN_RADIUS_SCALE,
      startPosition: capture.state.startPosition,
      startTarget: capture.state.startTarget,
    },
    capture: {
      cssViewport: VIEWPORT,
      deviceScaleFactor: DEVICE_SCALE_FACTOR,
      physicalFrame: PHYSICAL_FRAME,
      framebuffer: capture.state.framebuffer,
      layoutSha256: capture.state.layoutSha256,
      layout: capture.state.layout,
      recipeSha256: capture.scriptSha256,
      frameHashes: capture.frameHashes,
      frameFormat: "PNG",
      scratch,
      framesDirectory: capture.framesDir,
      losslessReference: encoding.reference,
      contactSheet: encoding.contactSheet,
    },
    delivery: {
      path: relative(REPO_ROOT, output),
      sha256: finalSha256,
      bytes: (await stat(output)).size,
      container: "MP4",
      codec: "H.264 High@4.1",
      pixelFormat: "yuv420p",
      dimensions: { width: 1920, height: 1080 },
      fps: FPS,
      audio: false,
      color: "BT.709 limited range",
      gopFrames: 60,
      maxrate: "20M",
      bufsize: "40M",
      faststart: true,
      selectedCrf: encoding.selected.crf,
    },
    quality: {
      thresholds: QUALITY_THRESHOLDS,
      candidates: encoding.candidates.map(({ path, ...candidate }) => ({
        ...candidate,
        scratchFile: path,
      })),
      loopClosureSsim4k: encoding.loopSsim,
      independentReplay: {
        stateMaximumCoordinateDelta: replayStateDelta,
        frame0Ssim4k: resumeSsim,
        minimumFrame0Ssim4k: CROSS_SESSION_SSIM_MIN,
      },
      durationSeconds: encoding.duration,
      peakRollingOneSecondBitrate: encoding.peakOneSecondBitrate,
      decodedFrameAudit: encoding.decoded,
      technicalGate: "pass",
      cfrTimestamps: "pass",
      faststartAtoms: "pass",
      humanVisualGate: "pending",
    },
    compatibilityTarget: {
      linkedin: "MP4; 1920x1080; 30 fps; <=30 Mbps",
      x: "MP4; 1920x1080; 30 fps; <=25 Mbps",
    },
    environment: {
      node: process.version,
      playwright: "1.63.0-alpha-2026-08-05",
      chromium: capture.chromiumVersion,
      ffmpeg: ffmpegVersion,
      ffprobe: ffprobeVersion,
    },
  };
  const manifestPartial = `${manifestPath}.partial-${process.pid}`;
  await writeFile(manifestPartial, `${JSON.stringify(manifest, null, 2)}\n`);
  await rename(manifestPartial, manifestPath);
  console.log(`[green] final: ${output}`);
  console.log(`[green] manifest: ${manifestPath}`);
  console.log(`[review] contact sheet: ${encoding.contactSheet}`);
  console.log(`[review] scratch retained until human approval: ${scratch}`);
}

main().catch((error) => {
  console.error(`[fatal] ${error.stack ?? error}`);
  process.exitCode = 1;
});
