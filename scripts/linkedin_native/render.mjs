import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE);
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,headless:true,args:['--no-sandbox','--disable-background-networking','--disable-component-update']});
try {
 const page=await browser.newPage({viewport:{width:1080,height:1350}});
 await page.route(/^https?:/,r=>r.abort());
 await page.goto(pathToFileURL(process.argv[2]).href,{waitUntil:'load',timeout:30000});
 await page.evaluate(async()=>{await Promise.all([400,500].map(w=>document.fonts.load(w+' 44px Fira')));await document.fonts.ready;});
 const report=await page.evaluate(()=>{
  const errors=[];
  const fonts=[...document.fonts].map(f=>({family:f.family,status:f.status}));
  if(fonts.length<2||fonts.some(f=>f.status!=='loaded'))errors.push('FONT_NOT_LOADED');
  const sections=[...document.querySelectorAll('section')];
  if(!sections.length)errors.push('NO_SLIDES');
  for(const [i,s] of sections.entries()){
   const b=s.getBoundingClientRect();
   if(s.scrollHeight>s.clientHeight+1||s.scrollWidth>s.clientWidth+1)errors.push(`SLIDE_OVERFLOW ${i+1}`);
   for(const el of s.querySelectorAll('h1,h2,p,.card,.step,.label,.value,.interval,.caption,.cta')){
    const r=el.getBoundingClientRect();
    if(r.left<b.left-1||r.right>b.right+1||r.top<b.top-1||r.bottom>b.bottom+1)errors.push(`ELEMENT_OUTSIDE ${i+1}`);
   }
  }
  for(const im of document.images)if(!im.complete||!im.naturalWidth)errors.push('IMAGE_NOT_LOADED');
  return {passed:!errors.length,errors,fonts,pages:sections.length};
 });
 fs.writeFileSync(process.argv[4],JSON.stringify(report,null,2));
 if(!report.passed){console.error(JSON.stringify(report));process.exitCode=1;}
 else await page.pdf({path:process.argv[3],preferCSSPageSize:true,printBackground:true,tagged:true,outline:false});
}finally{await browser.close()}
