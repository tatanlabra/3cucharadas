import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
const base=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(import.meta.url);
const {chromium}=require(path.resolve(base,'../../../../../penta-agent/tools/playwright-local-mcp/node_modules/playwright-core'));
const browser=await chromium.launch({executablePath:process.env.HOME+'/.agent-browser/browsers/chrome-151.0.7922.77/chrome',headless:true,args:['--no-sandbox','--disable-background-networking','--disable-component-update']});
try {
 const page=await browser.newPage({viewport:{width:1080,height:1350}});
 await page.route(/^https?:/,r=>r.abort());
 await page.goto(pathToFileURL(process.argv[2]).href,{waitUntil:'load',timeout:30000});
 await page.evaluate(async()=>{await Promise.all([400,500,600].map(w=>document.fonts.load(w+' 44px Fira')));await document.fonts.ready;});
 const fonts=await page.evaluate(()=>[...document.fonts].map(f=>({family:f.family,status:f.status,weight:f.weight})));
 if(fonts.some(f=>f.status!=='loaded'))throw new Error('Unloaded font: '+JSON.stringify(fonts));
 await page.pdf({path:process.argv[3],preferCSSPageSize:true,printBackground:true,tagged:true,outline:false,timeout:60000});
 console.log(JSON.stringify({fonts,pages:await page.locator('section').count()}));
}finally{await browser.close()}
