/* Local benchmark only. No DOM/style edits. Light theme is set through browser media before navigation. */
(() => {
  window.__PERF_MEASUREMENT__ = {supported: PerformanceObserver.supportedEntryTypes, errors:[], shifts:[]};
  const m=window.__PERF_MEASUREMENT__;
  try {new PerformanceObserver(list=>{for(const e of list.getEntries()){if(!e.hadRecentInput)m.shifts.push({value:e.value,startTime:e.startTime,sources:(e.sources||[]).map(s=>({node:s.node?.tagName,id:s.node?.id,class:s.node?.className,previousRect:s.previousRect,currentRect:s.currentRect}))});}}).observe({type:'layout-shift',buffered:true});}catch(e){m.errors.push(String(e));}
  setTimeout(()=>{
    window.__PERF_FINAL__={
      capturedAt:performance.now(),timeOrigin:performance.timeOrigin,url:location.href,
      visibility:document.visibilityState,readyState:document.readyState,
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
