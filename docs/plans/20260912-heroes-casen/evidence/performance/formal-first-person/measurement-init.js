/* Local benchmark only. No DOM/style edits. Light theme is set through browser media before navigation. */
(() => {
  window.__PERF_MEASUREMENT__ = {registeredAt:performance.now(), builtinInstalled:window.__AB_VITALS_INSTALLED__===true, supported: PerformanceObserver.supportedEntryTypes, errors:[], shifts:[], lcpEntries:[], paints:[], lifecycle:[], fontsReadyAt:null, longtasks:[]};
  const m=window.__PERF_MEASUREMENT__;
  const event=name=>m.lifecycle.push({name,t:performance.now(),visibility:document.visibilityState,focused:document.hasFocus()});
  event('init');document.addEventListener('visibilitychange',()=>event('visibilitychange'));window.addEventListener('focus',()=>event('focus'));window.addEventListener('blur',()=>event('blur'));
  document.addEventListener('DOMContentLoaded',()=>{event('DOMContentLoaded');document.fonts.ready.then(()=>{m.fontsReadyAt=performance.now();event('fonts-ready-after-dcl');});});
  for(const [type,key] of [['largest-contentful-paint','lcpEntries'],['paint','paints'],['longtask','longtasks']]){try{new PerformanceObserver(list=>{for(const e of list.getEntries())m[key].push({...e.toJSON(),callbackAt:performance.now()});}).observe({type,buffered:true});}catch(e){m.errors.push(String(e));}}

  try {new PerformanceObserver(list=>{for(const e of list.getEntries()){if(!e.hadRecentInput)m.shifts.push({value:e.value,startTime:e.startTime,sources:(e.sources||[]).map(s=>({node:s.node?.tagName,id:s.node?.id,class:s.node?.className,previousRect:s.previousRect,currentRect:s.currentRect}))});}}).observe({type:'layout-shift',buffered:true});}catch(e){m.errors.push(String(e));}
  setTimeout(()=>{
    window.__PERF_FINAL__={
      capturedAt:performance.now(),timeOrigin:performance.timeOrigin,url:location.href,
      visibility:document.visibilityState,focused:document.hasFocus(),readyState:document.readyState,fontsStatus:document.fonts.status,
      cwv:JSON.parse(JSON.stringify(window.__AB_VITALS__||null)),
      observation:JSON.parse(JSON.stringify(m)),
      navigation:performance.getEntriesByType('navigation').map(e=>e.toJSON()),
      resources:performance.getEntriesByType('resource').map(e=>e.toJSON()),
      device:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,userAgent:navigator.userAgent,hardwareConcurrency:navigator.hardwareConcurrency,deviceMemory:navigator.deviceMemory,theme:document.documentElement.dataset.theme,connection:navigator.connection?{effectiveType:navigator.connection.effectiveType,rtt:navigator.connection.rtt,downlink:navigator.connection.downlink,saveData:navigator.connection.saveData}:null},
      images:[...document.images].map(i=>({src:i.currentSrc,complete:i.complete,naturalWidth:i.naturalWidth,loading:i.loading})),
      title:document.title,h1:[...document.querySelectorAll('h1')].map(x=>x.textContent.trim())
    };
  },5000);
})();
