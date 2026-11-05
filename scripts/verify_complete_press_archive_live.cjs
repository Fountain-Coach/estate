#!/usr/bin/env node
// Every current publication under the actual active Reader; no HTML/JS/CSS
// interception. Editorial/factual judgments stay in the per-work QA ledger.
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium,webkit}=require('/Users/benedikteickhoff/Developer/fcis.fountain.coach/node_modules/playwright');
if(process.argv.length<3)throw Error('Pass source-owned per-publication ledger path');
const ledger=JSON.parse(fs.readFileSync(process.argv[2]));
const works=ledger.works.filter(x=>x.status==='current-essay'||x.status==='current-first-reading');
assert.equal(works.length,35);
const BASE='https://192.168.8.50:8243/estate/';
const expectedRoot='77f90b8db05a42700f727b4558f7e91a6406e2ae6bf25d59d953fa5ddae7b3d9';
const expectedApp='9fa017c008cebad8586a49a03741aae398a36a0fc61e935364f45b6e913b6345';
const reports=[];
async function run(name,driver,w,h){
 const browser=await driver.launch(name==='chromium'?{headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:{headless:true});
 const context=await browser.newContext({viewport:{width:w,height:h},ignoreHTTPSErrors:true});
 const hash=async url=>{
  const r=await context.request.get(BASE+url,{timeout:13000});
  assert.equal(r.status(),200,url);
  return crypto.createHash('sha256').update(await r.body()).digest('hex');
 };
 try{
   assert.equal(await hash(''),expectedRoot,'Wrong live v152 root');
   assert.equal(await hash('assets/linotype/reading-first-app.js'),expectedApp,'Wrong live v152 app');
   const page=await context.newPage(),problems=[];
   page.on('pageerror',e=>problems.push(e.message));
   page.on('console',m=>{if(m.type()==='error'&&m.text().includes('Fountain Press reader failure'))problems.push(m.text())});
   for(const item of works){
     problems.length=0;
     await page.goto(BASE+'#/read/'+item.id,{waitUntil:'domcontentloaded',timeout:18000});
     await page.waitForFunction(id=>{
       const v=document.querySelector('#page-viewport');
       return v?.dataset.volume===id&&v?.dataset.layout==='ready';
     },item.id,{timeout:25000});
     const state=await page.evaluate(()=>({
       count:Number(document.querySelector('#page-viewport')?.dataset.pages),
       sourceBlocks:document.querySelectorAll('#source-flow [data-source-block]').length,
       title:document.querySelector('#source-flow .book-chapter h2')?.textContent.trim(),
       hasProem:!!document.querySelector('#source-flow [data-editorial-role=proem]'),
       overflow:document.documentElement.scrollWidth-innerWidth,
       mode:document.querySelector('#page-viewport')?.dataset.mode
     }));
     assert.ok(state.count>=1&&state.count<=180,JSON.stringify({id:item.id,state}));
     assert.ok(state.sourceBlocks>0,JSON.stringify({id:item.id,state}));
     assert.equal(state.hasProem,true,'Missing editor preface: '+item.id);
     assert.ok(state.overflow<=3,'Horizontal overflow '+JSON.stringify({id:item.id,state}));
     assert.deepEqual(problems,[],'Reader error '+JSON.stringify({id:item.id,problems}));
     // Normal page turn must stay on this publication, even if the text source flows.
     if(state.count>1){
       await page.locator('#next-page').click();
       await page.waitForFunction(id=>document.querySelector('#page-viewport')?.dataset.volume===id,id,{timeout:10000});
     }
     reports.push({browser:name,width:w,height:h,work:item.id,folios:state.count,sourceAddresses:state.sourceBlocks,
       originalTitle:state.title,sourceProem:true,noOverflow:true,readerErrors:0});
     console.log('CURRENT_WORK_LIVE_PASS',name,w,h,item.id,state.count);
   }
   await page.close();
 }finally{await context.close();await browser.close()}
}
(async()=>{
 await run('webkit',webkit,390,844);
 await run('webkit',webkit,1440,900);
 await run('chromium',chromium,820,1120);
 const report={schema:'fountain.press.current-edition-live-smoke.v1',
    sourceAdmittedWorks:35,tested:reports.length,allPassed:true,
    limitation:'Selected live first folio and page turn on every work; not a full literary/AX/audio witness',
    cases:reports};
 const out=process.argv[3]||'/tmp/fountain-press-all-publications-live-proof.json';
 fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');
 console.log('ALL_PUBLICATIONS_LIVE_VERIFIED',reports.length,'work/layout cases',out);
})().catch(e=>{console.error('ALL_PUBLICATIONS_LIVE_FAILURE',e);process.exitCode=1});
