#!/usr/bin/env node
// Independently inspect actual v148 HTTPS stage. No route interception, no
// substitution of local HTML, no invented Reader or new server.
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
const {chromium,webkit}=require('/Users/benedikteickhoff/Developer/fcis.fountain.coach/node_modules/playwright');
const root='https://192.168.8.50:8243';
const wanted='essay--what-makes-a-page-modern';
const htmlSHA='532dbdf6603fb1300a974418130c50cbc17636262d9dcf7c0a802c3aabfdd81c';
const textSHA='8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const results=[];
async function run(browserType,label){
 const browser=await browserType.launch(label==='chromium'?
   {headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:
   {headless:true});
 try{
  for(const [w,h] of [[820,1120],[1200,860],[390,844]]){
   // Automation's temporary browser context does not trust the owner WLAN CA.
   // This exception does not substitute a physical trusted iPad Safari check.
   const context=await browser.newContext({viewport:{width:w,height:h},ignoreHTTPSErrors:true});
   const warnings=[],errors=[];
   const page=await context.newPage();
   page.on('pageerror',e=>errors.push(e.message));
   page.on('requestfailed',r=>{
     const reason=r.failure()?.errorText||'';
     if(r.url().includes('/estate/media/first-readings/') &&
       (reason.includes('ERR_ABORTED')||reason.includes('ERR_TOO_MANY_RETRIES'))){
       warnings.push(reason);return;
     }
     errors.push(r.url()+' '+reason);
   });
   page.on('response',r=>{if(r.status()>=400)errors.push('HTTP '+r.status()+' '+r.url());});
   try{
     const resp=await context.request.get(root+'/estate/');
     assert.equal(resp.status(),200);
     assert.equal(sha(await resp.body()),htmlSHA,'actual HTTPS content has wrong digest');
     await page.goto(root+'/estate/#/read/'+wanted,{waitUntil:'domcontentloaded',timeout:20000});
     await page.waitForFunction(id=>{
       const v=document.querySelector('#page-viewport');
       return v?.dataset.volume===id && v?.dataset.layout==='ready';
     },wanted,{timeout:30000});
     const state=await page.evaluate(id=>{
       const v=document.querySelector('#page-viewport');
       const t=document.querySelector('template[data-reader-volume="'+id+'"]');
       const text=t.content.textContent;
       const figs=t.content.querySelectorAll('figure[data-source-block^="what-makes-a-page-modern.plate."]');
       const pages=Number(v.dataset.pages);
       return {
         volume:v.dataset.volume,pages,
         manuscriptSHA:t.content.querySelector('[data-source-work-sha256]')?.getAttribute('data-source-work-sha256'),
         headingCount:t.content.querySelectorAll('p.frame-subheading').length,
         figureCount:figs.length,
         specimenFrames:t.content.querySelectorAll("figure[data-typographic-specimen]").length,
         unframedSpecimenProse:t.content.querySelectorAll('[data-source-unit-id="what-makes-a-page-modern.specimen"]').length,
         sourceAnchoredFigures:t.content.querySelectorAll("figure[data-inline-after-paragraph]").length,
         sourceBlocks:t.content.querySelectorAll('[data-source-block]').length,
         hasSelfOutLoud:text.includes('Self Out Loud'),
         hasPronunciation:text.includes('If a word becomes difficult'),
         hasJoyce:text.includes('Darantière'),
         hasSixthCondition:text.includes('Only the writer authorizes the next composition'),
         hasClosing:text.includes('The page is complete only provisionally. The work may continue.'),
         overflow:document.documentElement.scrollWidth-innerWidth,
         readerRoot:document.querySelector('#reader-parent')?.getAttribute('data-reader-target')
       };
     },wanted);
     assert.equal(state.volume,wanted);
     assert.equal(state.manuscriptSHA,textSHA);
     assert.equal(state.figureCount,12);
     assert.equal(state.specimenFrames,2);
     assert.equal(state.unframedSpecimenProse,0);
     assert.equal(state.sourceAnchoredFigures,11);
     assert.equal(state.readerRoot,'essays');
     assert.ok(state.headingCount>=16);
     assert.ok(state.sourceBlocks>=130);
     assert.ok(state.pages>=16 && state.pages<=60,JSON.stringify(state));
     assert.ok(state.overflow<=3);
     assert.ok(state.hasSelfOutLoud && state.hasPronunciation && state.hasJoyce && state.hasSixthCondition && state.hasClosing);
     assert.deepEqual(errors,[]);
     const shot='/tmp/self-out-loud-LIVE-'+label+'-'+w+'x'+h+'.png';
     await page.screenshot({path:shot});
     await page.goto(root+'/estate/#/read/library',{waitUntil:'domcontentloaded'});
     await page.waitForFunction(()=>document.querySelector('#page-viewport')?.dataset.volume==='library'
       && document.querySelector('#page-viewport')?.dataset.layout==='ready',{timeout:30000});
     assert.equal(await page.locator('.reader-gallery-scroll[data-collection="essays"] .reader-gallery-item').count(),6);
     await page.goto(root+'/estate/#/read/teatro',{waitUntil:'domcontentloaded'});
     await page.waitForFunction(()=>document.querySelector('#page-viewport')?.dataset.volume==='teatro'
       && document.querySelector('#page-viewport')?.dataset.layout==='ready',{timeout:30000});
     console.log('LIVE_PASS',label,w,h,'pages',state.pages,'plates',state.figureCount,'blocks',state.sourceBlocks,'shot',shot);
     results.push({browser:label,width:w,height:h,...state,warnings});
   }finally{await context.close();}
  }
 }finally{await browser.close();}
}
(async()=>{
 await run(chromium,'chromium');
 await run(webkit,'webkit');
 const receipt={schema:'fountain.press.modern-page-self-out-loud-live-proof.v1',
   stage:'shared-shell-20261105-v148-self-out-loud-c884a3e',htmlSHA256:htmlSHA,results};
 const dest='/tmp/self-out-loud-live-v148-acceptance.json';
 fs.writeFileSync(dest,JSON.stringify(receipt,null,2)+'\n');
 console.log('PROVED',results.length,'live profiles',dest);
})().catch(err=>{console.error(err);process.exitCode=1;});
