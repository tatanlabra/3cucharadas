const socket = new WebSocket(process.argv[2]);
let seq = 0, sessionId;
const pending = new Map();
const send = (method, params = {}, session = sessionId) => new Promise((resolve, reject) => {
  const id = ++seq; pending.set(id, { resolve, reject });
  socket.send(JSON.stringify({ id, method, params, ...(session ? { sessionId: session } : {}) }));
});
socket.addEventListener('message', ({ data }) => {
  const e = JSON.parse(data); if (!e.id) return;
  const p = pending.get(e.id); pending.delete(e.id);
  e.error ? p?.reject(e.error) : p?.resolve(e.result);
});
await new Promise(r => socket.addEventListener('open', r, { once: true }));
const { targetInfos } = await send('Target.getTargets', {}, null);
const page = targetInfos.find(t => t.type === 'page');
({ sessionId } = await send('Target.attachToTarget', { targetId: page.targetId, flatten: true }, null));
await send('Page.enable');
await send('Page.bringToFront');
await send('Page.addScriptToEvaluateOnNewDocument', { source: `(() => {
  const state = kind => ({ kind, ms: performance.now(), visibility: document.visibilityState, focus: document.hasFocus() });
  const events = window.__foregroundTrace = [state('init')];
  for (const name of ['focus','blur','load']) window.addEventListener(name, () => events.push(state(name)));
  for (const name of ['visibilitychange','DOMContentLoaded']) document.addEventListener(name, () => events.push(state(name)));
})();` });
const before = await send('Runtime.evaluate', { expression: `new Promise(resolve => { const frames=[]; const next=ms=>{frames.push(ms); if(frames.length<10)requestAnimationFrame(next); else resolve({visibility:document.visibilityState,focus:document.hasFocus(),frames})};requestAnimationFrame(next) })`, awaitPromise: true, returnByValue: true });
console.log(JSON.stringify(before.result.value));
socket.close();
