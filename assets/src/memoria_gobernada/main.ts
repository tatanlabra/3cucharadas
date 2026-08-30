import {
  BufferAttribute,
  BufferGeometry,
  IcosahedronGeometry,
  Line,
  LineBasicMaterial,
  Mesh,
  MeshBasicMaterial,
  PerspectiveCamera,
  Points,
  PointsMaterial,
  Raycaster,
  Scene,
  Vector2,
  Vector3,
  WebGLRenderer
} from "three";
import "./styles.scss";
import { GraphNode, palette, positionFor } from "./layout";

type GraphLink = { source: string; target: string; kind: string };
type GraphData = { nodes: GraphNode[]; links: GraphLink[] };

const host = document.getElementById("memory-observatory");
const status = document.getElementById("memory-observatory-status");
const detail = document.getElementById("memory-observatory-detail");
const reset = document.getElementById("memory-observatory-reset") as HTMLButtonElement | null;
const isEnglish = document.documentElement.lang.toLowerCase().startsWith("en");
const copy = isEnglish
  ? {
      fallbackWebGl: "Your browser does not expose WebGL; the accessible table preserves the demonstration’s content.",
      loadingFailed: "The narrative and table remain available; the 3D view could not start.",
      ready: "3D view active. Drag to orbit, use the wheel to zoom, and select a node to inspect its provenance.",
      reset: "View reset.",
    }
  : {
      fallbackWebGl: "Tu navegador no expone WebGL; la tabla accesible conserva el contenido de la demostración.",
      loadingFailed: "El relato y la tabla siguen disponibles; no fue posible iniciar la vista 3D.",
      ready: "Vista 3D activa. Arrastra para orbitar, usa la rueda para acercar y selecciona un nodo para leer su procedencia.",
      reset: "Vista reencuadrada.",
    };

const englishNodePresentation: Record<string, { label: string; status: string; provenance: string }> = {
  rag_curated_context: { label: "Curated operational memory", status: "current", provenance: "sanitized canonical ledger" },
  mail_local_pilot: { label: "Aggregated personal-mail pilot", status: "reviewed local aggregate", provenance: "12,072 unique messages; authorized local inventory without a public corpus" },
  thesis_provenance: { label: "Thesis provenance and contracts", status: "authorized metadata", provenance: "approved provenance contract" },
  memory_projection: { label: "Governed public projection", status: "derived", provenance: "deterministic public export" },
};

function message(text: string): void {
  if (status) status.textContent = text;
}

function describe(node: GraphNode): void {
  if (!detail) return;
  const presentation = isEnglish ? englishNodePresentation[node.id] : undefined;
  detail.innerHTML = "";
  const title = document.createElement("strong");
  title.textContent = presentation?.label ?? node.label;
  const body = document.createElement("span");
  body.textContent = `${node.source_kind} · ${presentation?.status ?? node.status} · ${presentation?.provenance ?? node.provenance}`;
  detail.append(title, body);
}

function hasWebGL(): boolean {
  try {
    const canvas = document.createElement("canvas");
    return Boolean(window.WebGLRenderingContext && canvas.getContext("webgl"));
  } catch {
    return false;
  }
}

async function start(): Promise<void> {
  if (!(host instanceof HTMLElement) || !hasWebGL()) {
    if (host) host.dataset.state = "fallback";
    message(copy.fallbackWebGl);
    return;
  }
  const graphUrl = host.dataset.graphUrl;
  if (!graphUrl) throw new Error("missing graph data URL");
  const response = await fetch(graphUrl, { credentials: "same-origin" });
  if (!response.ok) throw new Error("graph data unavailable");
  const graph = await response.json() as GraphData;
  if (!Array.isArray(graph.nodes) || !Array.isArray(graph.links)) throw new Error("invalid graph data");

  const scene = new Scene();
  const camera = new PerspectiveCamera(40, 1, 0.1, 100);
  const initialCamera = new Vector3(0, 0.5, 8.2);
  camera.position.copy(initialCamera);
  const renderer = new WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.domElement.setAttribute("aria-hidden", "true");
  host.prepend(renderer.domElement);

  const starGeometry = new BufferGeometry();
  const stars = new Float32Array(240 * 3);
  for (let index = 0; index < stars.length; index += 3) {
    const seed = index / 3;
    stars[index] = ((seed * 37) % 29) / 2.7 - 5.3;
    stars[index + 1] = ((seed * 17) % 23) / 3.2 - 3.4;
    stars[index + 2] = ((seed * 13) % 31) / 3 - 5.2;
  }
  starGeometry.setAttribute("position", new BufferAttribute(stars, 3));
  scene.add(new Points(starGeometry, new PointsMaterial({ color: "#d8f7ff", size: 0.022, transparent: true, opacity: 0.72 })));

  const positions = new Map<string, { x: number; y: number; z: number }>();
  const selectable: Array<{ userData: { node: GraphNode } }> = [];
  const nodes = graph.nodes.map((node, index) => ({ node, position: new Vector3(...positionFor(node, index)) }));
  for (const entry of nodes) positions.set(entry.node.id, entry.position);
  for (const link of graph.links) {
    const source = positions.get(link.source);
    const target = positions.get(link.target);
    if (!source || !target) continue;
    const geometry = new BufferGeometry().setFromPoints([source, target]);
    scene.add(new Line(geometry, new LineBasicMaterial({ color: "#7193a8", transparent: true, opacity: 0.58 })));
  }
  for (const { node, position } of nodes) {
    const mesh = new Mesh(
      new IcosahedronGeometry(node.id === "memory_projection" ? 0.31 : 0.2, 3),
      new MeshBasicMaterial({ color: palette[node.source_kind], transparent: true, opacity: 0.94 })
    );
    mesh.position.copy(position);
    mesh.userData.node = node;
    selectable.push(mesh);
    scene.add(mesh);
  }

  let yaw = 0;
  let pitch = 0;
  let distance = initialCamera.length();
  let dragging = false;
  let last = { x: 0, y: 0 };
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const raycaster = new Raycaster();
  const pointer = new Vector2();

  const resize = (): void => {
    const width = Math.max(host.clientWidth, 280);
    const height = Math.max(Math.min(width * 0.62, 510), 320);
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  };
  const placeCamera = (): void => {
    camera.position.set(
      distance * Math.sin(yaw) * Math.cos(pitch),
      distance * Math.sin(pitch) + 0.35,
      distance * Math.cos(yaw) * Math.cos(pitch)
    );
    camera.lookAt(0, 0, 0);
  };
  const render = (): void => {
    placeCamera();
    renderer.render(scene, camera);
  };
  resize();
  render();
  new ResizeObserver(resize).observe(host);
  host.dataset.state = "ready";
  message(copy.ready);

  renderer.domElement.addEventListener("pointerdown", (event: PointerEvent) => {
    dragging = true;
    last = { x: event.clientX, y: event.clientY };
    renderer.domElement.setPointerCapture(event.pointerId);
  });
  renderer.domElement.addEventListener("pointermove", (event: PointerEvent) => {
    if (!dragging) return;
    yaw += (event.clientX - last.x) * 0.008;
    pitch = Math.max(-0.7, Math.min(0.7, pitch + (event.clientY - last.y) * 0.006));
    last = { x: event.clientX, y: event.clientY };
    render();
  });
  renderer.domElement.addEventListener("pointerup", (event: PointerEvent) => {
    const moved = Math.abs(event.clientX - last.x) + Math.abs(event.clientY - last.y);
    dragging = false;
    if (moved > 5) return;
    const bounds = renderer.domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - bounds.left) / bounds.width) * 2 - 1;
    pointer.y = -((event.clientY - bounds.top) / bounds.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const selected = raycaster.intersectObjects(selectable, false)[0];
    if (selected) describe(selected.object.userData.node as GraphNode);
  });
  renderer.domElement.addEventListener("wheel", (event: WheelEvent) => {
    event.preventDefault();
    distance = Math.max(4.5, Math.min(12, distance + event.deltaY * 0.008));
    render();
  }, { passive: false });
  reset?.addEventListener("click", () => {
    yaw = 0;
    pitch = 0;
    distance = initialCamera.length();
    render();
    message(copy.reset);
  });
  if (!reducedMotion) {
    const animate = (): void => {
      scene.rotation.y += 0.0011;
      renderer.render(scene, camera);
      window.requestAnimationFrame(animate);
    };
    window.requestAnimationFrame(animate);
  }
}

start().catch(() => {
  if (host) host.dataset.state = "fallback";
  message(copy.loadingFailed);
});
