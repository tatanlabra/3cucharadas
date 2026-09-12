(() => {
  const d=window.__PAINT_DIAG__={registeredAt:performance.now(),builtinInstalled:window.__AB_VITALS_INSTALLED__===true,events:[],rawPaint:[],rawLcp:[],errors:[],frames:[],fontsReadyAt:null};
  const mark=name=>d.events.push({name,t:performance.now(),visibility:document.visibilityState,focused:document.hasFocus(),readyState:document.readyState});
  mark('init');for(const name of ['DOMContentLoaded','visibilitychange','freeze','resume'])document.addEventListener(name,()=>mark(name));for(const name of ['load','pageshow','pagehide','focus','blur'])window.addEventListener(name,()=>mark(name));
  document.fonts.ready.then(()=>{d.fontsReadyAt=performance.now();mark('fonts-ready-initial');});
  document.addEventListener('DOMContentLoaded',()=>document.fonts.ready.then(()=>{d.fontsReadyAfterDclAt=performance.now();mark('fonts-ready-after-dcl');}));
  for(const [type,key] of [['paint','rawPaint'],['largest-contentful-paint','rawLcp']]){
    try{new PerformanceObserver(list=>{for(const e of list.getEntries())d[key].push({...e.toJSON(),element:e.element?{tag:e.element.tagName,id:e.element.id,className:e.element.className}:null,callbackAt:performance.now()});}).observe({type,buffered:true});}catch(e){d.errors.push(String(e));}
  }
  function frame(t){if(d.frames.length<30)d.frames.push(t);if(performance.now()<6000)requestAnimationFrame(frame);}requestAnimationFrame(frame);
})();
