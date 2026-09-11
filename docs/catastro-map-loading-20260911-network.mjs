import { writeFileSync } from 'node:fs';
const socket = new WebSocket(process.argv[2]);
let sequence = 0;
const pending = new Map();
const events = [];
const urls = new Map();
let sessionId;
const send = (method, params = {}, session = sessionId) => new Promise((resolve, reject) => {
  const id = ++sequence;
  pending.set(id, { resolve, reject });
  socket.send(JSON.stringify({ id, method, params, ...(session ? { sessionId: session } : {}) }));
});
socket.addEventListener('message', ({ data }) => {
  const event = JSON.parse(data);
  if (event.id) {
    const target = pending.get(event.id);
    pending.delete(event.id);
    return event.error ? target?.reject(event.error) : target?.resolve(event.result);
  }
  const params = event.params ?? {};
  if (event.method === 'Network.requestWillBeSent') urls.set(params.requestId, params.request.url);
  const url = urls.get(params.requestId);
  if (!url || !/tiles\.3cucharadas|tile\.openstreetmap|local\/manifest/.test(url)) return;
  if (event.method === 'Network.requestWillBeSent') events.push({ event: 'request', url, timestamp: params.timestamp });
  if (event.method === 'Network.loadingFailed') events.push({ event: 'failed', url, timestamp: params.timestamp, errorText: params.errorText, blockedReason: params.blockedReason, corsErrorStatus: params.corsErrorStatus });
  if (event.method === 'Network.responseReceived') events.push({ event: 'response', url, timestamp: params.timestamp, status: params.response.status, mimeType: params.response.mimeType, fromDiskCache: params.response.fromDiskCache });
});
await new Promise(resolve => socket.addEventListener('open', resolve, { once: true }));
const { targetInfos } = await send('Target.getTargets', {}, null);
const target = targetInfos.find(target => target.type === 'page');
({ sessionId } = await send('Target.attachToTarget', { targetId: target.targetId, flatten: true }, null));
await send('Network.enable');
console.log('NETWORK_READY');
setTimeout(() => { writeFileSync(process.argv[3], JSON.stringify(events, null, 2)); console.log(JSON.stringify(events)); socket.close(); }, 45000);
