import {createRequire} from 'node:module';
import fs from 'node:fs';
const req=createRequire('/home/ende/Descargas/programaciones/penta-agent/tools/playwright-local-mcp/package.json');
const {chromium}=req('playwright-core');
const out=new URL('.',import.meta.url).pathname;
const rows=[];
for(const [name,executablePath] of [['canonical',chromium.executablePath()],['same-chrome151','/home/ende/.agent-browser/browsers/chrome-151.0.7922.77/chrome']]){
 const browser=await chromium.launch({headless:true,executablePath});
 try{
 for(const fixture of ['fast','late']){
 const context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 await context.addInitScript(()=>{
 window.__CANARY__={lcp:[],paint:[],input:[],lifecycle:[],registeredAt:performance.now()};
 for(const [type,key] of [['largest-contentful-paint','lcp'],['paint','paint']])new PerformanceObserver(l=>window.__CANARY__[key].push(...l.getEntries().map(e=>({...e.toJSON(),callbackAt:performance.now()})))).observe({type,buffered:true});
 for(const type of ['pointerdown','keydown','wheel'])addEventListener(type,e=>window.__CANARY__.input.push({type,trusted:e.isTrusted,t:performance.now()}));
 setTimeout(()=>{window.__FINAL__={...JSON.parse(JSON.stringify(window.__CANARY__)),at:performance.now(),visibility:document.visibilityState,focused:document.hasFocus(),url:location.href,timeOrigin:performance.timeOrigin,ua:navigator.userAgent,width:innerWidth,height:innerHeight}},5000);
 });
 const page=await context.newPage();
 for(const nav of ['cold','warm']){
 if(nav==='cold')await page.goto('http://127.0.0.1:4044/'+fixture+'.html');else await page.reload();
 await page.waitForTimeout(5100);
 const sample=await page.evaluate(()=>window.__FINAL__);
 rows.push({driver:'playwright',browser:name,version:browser.version(),executablePath,fixture,nav,sample});
 fs.writeFileSync(out+'playwright-runs.json',JSON.stringify(rows,null,2));
 console.log(JSON.stringify({browser:name,fixture,nav,lcp:sample.lcp.at(-1)?.startTime??null,fcp:sample.paint.find(x=>x.name==='first-contentful-paint')?.startTime??null}));
 }
 await context.close();
 }
 }finally{await browser.close();}
}
