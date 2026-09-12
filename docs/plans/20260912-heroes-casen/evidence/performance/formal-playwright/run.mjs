import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
const req=createRequire('/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/package.json');
const {chromium}=req('playwright-core');
const HERE=path.dirname(new URL(import.meta.url).pathname),PERF=path.dirname(HERE),PLAN=path.resolve(PERF,'../..'),REPO=path.resolve(PLAN,'../../..');
const pairs=Number(process.argv[2]||1),OUT=path.resolve(process.argv[3]||path.join(PERF,'presentation-diagnosis/product-canary'));
if(![1,5].includes(pairs))throw Error('Only1canary or5formal pairs allowed');
fs.mkdirSync(OUT,{recursive:true});if(fs.existsSync(path.join(OUT,'runs.json')))throw Error('Output already contains runs; preserve prior observations');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const dump=(n,d)=>fs.writeFileSync(path.join(OUT,n),JSON.stringify(d,null,2)+'\n');
const sourcePath=path.join(PLAN,'evidence/editorial/source-first-person-before-build.json'),buildPath=path.join(PERF,'formal-candidate-first-person-freeze.json');
const source=JSON.parse(fs.readFileSync(sourcePath)),build=JSON.parse(fs.readFileSync(buildPath));
const ROOTS={baseline:'/tmp/3c-heroes-baseline-site',candidate:'/tmp/3c-heroes-first-person-site'},PORTS={baseline:4041,candidate:4042};
const PAGES={'avaluos-ii':'/datos/territorio/avaluos-ii-brecha-residencial/','casen-long':'/datos/politica-publica/julia/casen/casen2024-julia-waffles-politica-publica/'};
const exe='/home/ende/.agent-browser/browsers/chrome-151.0.7922.77/chrome',server=path.join(REPO,'scripts/catastro_sii/serve_range_static.mjs');
const builtin=path.join(PERF,'formal-tools/embedded-vitals-init.js'),measurement=path.join(PERF,'formal-tools/measurement-init.js');
const init=fs.readFileSync(builtin,'utf8')+';\n'+fs.readFileSync(measurement,'utf8');
function verifyInput(){for(const [f,h] of Object.entries(source.manifest))if(sha(path.join(REPO,f))!==h)throw Error('Source drift:'+f);for(const [f,h] of Object.entries(build.files))if(sha(path.join(ROOTS.candidate,f))!==h)throw Error('Candidate drift:'+f);}
verifyInput();
const manifest={};for(const [side,root] of Object.entries(ROOTS)){manifest[side]={};for(const url of Object.values(PAGES))manifest[side][url]=sha(path.join(root,url,'index.html'));}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function cpu(){const ticks=fs.readFileSync('/proc/stat','utf8').split('\n')[0].trim().split(/\s+/).slice(1).map(Number),procs={};for(const pid of fs.readdirSync('/proc')){if(!/^\d+$/.test(pid))continue;try{const s=fs.readFileSync('/proc/'+pid+'/stat','utf8'),end=s.lastIndexOf(')'),r=s.slice(end+2).split(' ');procs[pid]={comm:s.slice(s.indexOf('(')+1,end),ticks:Number(r[11])+Number(r[12])};}catch{}}return {at:performance.now(),ticks,procs,loadavg:os.loadavg()};}
function delta(a,b){const t=b.ticks.map((x,i)=>x-a.ticks[i]),total=t.slice(0,8).reduce((a,b)=>a+b,0),secs=(b.at-a.at)/1000,top=[];for(const [pid,p] of Object.entries(b.procs))if(a.procs[pid]&&p.ticks>a.procs[pid].ticks)top.push({pid:Number(pid),comm:p.comm,cpu_ticks_delta:p.ticks-a.procs[pid].ticks});top.sort((a,b)=>b.cpu_ticks_delta-a.cpu_ticks_delta);return {duration_s:secs,cpu_busy_percent:100*(total-t[3]-t[4])/total,loadavg_start:a.loadavg,loadavg_end:b.loadavg,top_processes:top.slice(0,12),note:'Process deltas in kernel ticks, no assumed CLK_TCK; global percentage from /proc/stat'};}
function cls(es){let start=null,prev=null,total=0,max=0;for(const e of [...es].sort((a,b)=>a.startTime-b.startTime)){if(start===null||e.startTime-prev>=1000||e.startTime-start>=5000){start=e.startTime;total=0;}total+=e.value;max=Math.max(max,total);prev=e.startTime;}return max;}
function median(v){const a=[...v].sort((a,b)=>a-b);return a[Math.floor(a.length/2)];}
const inputs={source_manifest:path.relative(PLAN,sourcePath),source_manifest_sha256:sha(sourcePath),source_digest:source.source_digest,build_root:ROOTS.candidate,build_manifest:path.relative(OUT,buildPath),build_manifest_sha256:sha(buildPath)};
const settings={label:pairs===5?'formal-playwright':'canary-playwright',pairs,pages:PAGES,roots:ROOTS,viewport:[1440,1000],dpr:1,media:'light,no-preference',window_ms:5000,collector:'Unmodified formal embedded+raw init concatenated in deterministic order before navigation; standard LCP.startTime and CLS session windows',driver:'Single Node process using canonical pinned playwright-core',executable:exe,version:null,cold:'Fresh Chrome browser and context per pair/page/side',warm:'Reload same context; no-store server, not HTTP cache hit',network:'loopback only by context routing; no emulated throttle',cpu:'Native host;10second pre-pair window and per-navigation deltas; retain every sample',order:'AB/BA alternating pair/page; cold then warm',interaction:'No screenshot, rAF pumping, clicks, scrolling or CLI polling; page.waitForTimeout5100 after navigation, frozen snapshot5000ms',hashes:{harness:sha(new URL(import.meta.url)),server:sha(server),builtin:sha(builtin),measurement:sha(measurement),chrome:sha(exe),playwright_package:sha('/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/node_modules/playwright-core/package.json'),playwright_lock:sha('/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/package-lock.json')},inputs,served_page_hashes:manifest};
const servers=[],rows=[],windows=[];let activeBrowser=null,closed=0;
try{
 for(const [side,root] of Object.entries(ROOTS)){const log=fs.openSync(path.join(OUT,'server-'+side+'.log'),'w');const child=spawn('node',[server,root,String(PORTS[side]),'127.0.0.1'],{stdio:['ignore',log,log]});servers.push(child);fs.closeSync(log);await sleep(400);if(child.exitCode!==null)throw Error('Server did not start:'+side);}
 settings.server_headers={};for(const side of Object.keys(ROOTS)){const res=await fetch('http://127.0.0.1:'+PORTS[side]+Object.values(PAGES)[0]);settings.server_headers[side]=Object.fromEntries(res.headers);if(res.headers.get('cache-control')!=='no-store')throw Error('Expectedno-store');await res.arrayBuffer();}
 dump('settings.json',settings);
 for(let pair=1;pair<=pairs;pair++)for(const [index,[page,url]] of Object.entries(Object.entries(PAGES))){
  const before=cpu();await sleep(10000);windows.push({pair,page,...delta(before,cpu())});dump('cpu-before-pairs.json',windows);
  const order=(pair+Number(index))%2?['baseline','candidate']:['candidate','baseline'];
  for(const side of order){
   activeBrowser=await chromium.launch({headless:true,executablePath:exe});settings.version=activeBrowser.version();dump('settings.json',settings);
   const context=await activeBrowser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1,colorScheme:'light',reducedMotion:'no-preference',serviceWorkers:'block'});
   await context.route('**/*',route=>{const u=new URL(route.request().url());return ['127.0.0.1','localhost'].includes(u.hostname)?route.continue():route.abort('blockedbyclient');});
   await context.addInitScript({content:init});const tab=await context.newPage();const pageErrors=[];tab.on('pageerror',e=>pageErrors.push(String(e)));
   for(const temperature of ['cold','warm']){
    const before=cpu(),row={pair,page,side,temperature,started_at:new Date().toISOString(),missing:true,collector:'playwright canonical library; sameChrome151; preserved formal PerformanceObserver init'};
    try{
     if(temperature==='cold')await tab.goto('http://127.0.0.1:'+PORTS[side]+url,{waitUntil:'load',timeout:45000});else await tab.reload({waitUntil:'load',timeout:45000});
     await tab.waitForTimeout(5100);row.sample=await tab.evaluate(()=>window.__PERF_FINAL__);
     const raw=row.sample,origin=await tab.evaluate(()=>performance.timeOrigin);
     if(!raw||raw.timeOrigin!==origin||raw.url!=='http://127.0.0.1:'+PORTS[side]+url||raw.readyState!=='complete'||raw.h1.length!==1||raw.visibility!=='visible')throw Error('Invalid navigation state');
     if(raw.device.width!==1440||raw.device.height!==1000||raw.device.dpr!==1||raw.device.theme!=='light')throw Error('Different viewport/theme');
     if(raw.observation.errors.length)throw Error('Observer error');
     row.metrics={lcp_ms:raw.cwv?.lcp?.startTime??null,fcp_ms:raw.cwv?.fcp??null,cls_raw_sum:raw.cwv?.cls??null,cls_session_window:cls(raw.observation.shifts)};
     row.missing=row.metrics.lcp_ms===null||row.metrics.fcp_ms===null;row.eval_snapshot_did_not_navigate=true;
     row.resources_sha256={};for(const res of raw.resources){const u=new URL(res.name);if(u.hostname==='127.0.0.1'){const f=path.join(ROOTS[side],decodeURIComponent(u.pathname));if(fs.existsSync(f)&&fs.statSync(f).isFile())row.resources_sha256[u.pathname]=sha(f);}}
    }catch(e){row.error=String(e);}
    row.page_errors=[...pageErrors];row.cpu_during_navigation=delta(before,cpu());rows.push(row);dump('runs.json',rows);console.log(JSON.stringify({pair,page,side,temperature,metrics:row.metrics,missing:row.missing,error:row.error}));
   }
   await context.close();await activeBrowser.close();activeBrowser=null;closed++;
  }
 }
 verifyInput();for(const [side,files] of Object.entries(manifest))for(const [url,h] of Object.entries(files))if(sha(path.join(ROOTS[side],url,'index.html'))!==h)throw Error('ServedHTMLdrift');
 inputs.build_bytes_unchanged_after_collection=true;
 const summary=[];for(const page of Object.keys(PAGES))for(const temperature of ['cold','warm']){const g={};for(const side of ['baseline','candidate']){const rs=rows.filter(r=>r.page===page&&r.temperature===temperature&&r.side===side);g[side]=rs.length===pairs&&rs.every(r=>!r.missing)?median(rs.map(r=>r.metrics.lcp_ms)):null;}
 const regression=g.baseline&&g.candidate!==null?(g.candidate/g.baseline-1)*100:null;summary.push({page,temperature,median_lcp_ms:g,regression_percent:regression,lcp_threshold_diagnostic:regression===null?'missing':g.candidate<=2500&&regression<=10?'pass':'fail'});}
 dump('summary.json',{groups:summary,n_runs:rows.length,missing_runs:rows.filter(r=>r.missing).length,formal_acceptance:false,qualification:'Requires root acceptance of current input binding and standard metric thresholds; canary is not formal'});
}finally{
 if(activeBrowser)await activeBrowser.close();for(const child of servers)child.kill('SIGTERM');await sleep(300);
 const files={};for(const f of fs.readdirSync(OUT))if(f!=='receipt.json'&&fs.statSync(path.join(OUT,f)).isFile())files[f]=sha(path.join(OUT,f));
 dump('receipt.json',{schema_version:1,task:pairs===5?'Q1-formal-performance-playwright':'Q1-product-canary-playwright',timestamp:new Date().toISOString(),status:'requires-review',formal_acceptance:false,counts:{runs_total:rows.length,expected_total:pairs*8,pairs_per_page:pairs,lcp_observed:rows.filter(r=>r.metrics?.lcp_ms!=null).length,lcp_missing:rows.filter(r=>r.metrics?.lcp_ms==null).length,cls_observed:rows.filter(r=>r.metrics?.cls_session_window!=null).length,cpu_windows:windows.length,sessions_closed:closed},inputs,cleanup:{all_own_sessions_closed:true,servers4041_4042_closed:servers.every(x=>x.exitCode!==null||x.signalCode!==null),server4004_untouched:true},files});
}
