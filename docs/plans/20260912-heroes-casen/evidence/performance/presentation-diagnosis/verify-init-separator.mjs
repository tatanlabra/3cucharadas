import vm from 'node:vm';import fs from 'node:fs';
const dir=new URL('../formal-tools/',import.meta.url),a=fs.readFileSync(new URL('embedded-vitals-init.js',dir),'utf8'),b=fs.readFileSync(new URL('measurement-init.js',dir),'utf8');
const results=[];
for(const [name,separator] of [['observed-red','\n'],['recovery-green',';\n']]){
const c={window:{addEventListener(){}},document:{visibilityState:'visible',hasFocus:()=>true,addEventListener(){}},performance:{now:()=>1},console:{timeStamp(){}},setTimeout(){},PerformanceObserver:class {static supportedEntryTypes=['paint','largest-contentful-paint','layout-shift'];observe(){}}};
try{vm.runInNewContext(a+separator+b,c);results.push({name,registered:Boolean(c.window.__PERF_MEASUREMENT__),error:null});}catch(e){results.push({name,registered:Boolean(c.window.__PERF_MEASUREMENT__),error:String(e)});}
}
fs.writeFileSync(new URL('init-separator-red-green.json',import.meta.url),JSON.stringify(results,null,2));
console.log(JSON.stringify(results));if(results[0].registered||!results[0].error||!results[1].registered||results[1].error)process.exitCode=1;
