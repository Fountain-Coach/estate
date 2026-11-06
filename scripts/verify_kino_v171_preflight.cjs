#!/usr/bin/env node
// Preview authentic Press edition against the current stage without activating candidate.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium,webkit}=require('/Users/benedikteickhoff/Developer/fcis.fountain.coach/node_modules/playwright');
const ROOT='/private/tmp/fountain-kino-verbatim-v171/candidate';
const ESSAY_URL='https://192.168.8.50:8243/estate/#/read/essay--a-sound-must-earn-its-place';
const ids=['v156','v158'];
const stageActive=process.env.STAGE_ACTIVE==='1';
const previewBridge=process.env.PREVIEW_BRIDGE==='1';
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.m4a':'audio/mp4'};
async function verify(engine,label,viewport,mobile=false){
 const browser=await engine.launch(label.startsWith('Chrome')?{
  headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  args:['--autoplay-policy=no-user-gesture-required']
 }:{headless:true});
 try{
  const context=await browser.newContext({viewport,deviceScaleFactor:2,hasTouch:mobile,isMobile:mobile,ignoreHTTPSErrors:true});
  if(previewBridge)await context.route('**/estate/assets/instruments/kino-verbatim-bridge.js',route=>route.fulfill({status:200,contentType:'text/javascript',body:fs.readFileSync('/Users/benedikteickhoff/Developer/.estate-press-sound-proof-20261106/staging/press-kino-verbatim-bridge.js')}));
  if(!stageActive)await context.route('**/*',route=>{
   let parsed;try{parsed=new URL(route.request().url())}catch{return route.continue()}
   const target=parsed.pathname;
   let local=null;
   if(target==='/estate/'||target==='/estate'||target==='/estate/index.html'){local=path.join(ROOT,'estate/index.html');console.log('INTERCEPT_INDEX',target);}
   else if(target==='/estate/assets/instruments/kino-verbatim-bridge.js')local=path.join(ROOT,target.slice(1));
   else if(target.startsWith('/teatro/interludes/kino/press-citation/'))
    local=path.join(ROOT,target.slice(1),target.endsWith('/')?'index.html':'');
   if(!local)return route.continue();
   if(!fs.existsSync(local)||!fs.statSync(local).isFile())return route.fulfill({status:404,body:'Candidate source missing'});
   const ext=path.extname(local);
   return route.fulfill({status:200,body:fs.readFileSync(local),contentType:mime[ext]||'application/octet-stream'});
  });
  const page=await context.newPage();
  const errors=[],failed=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',msg=>{if(msg.type()==='error')errors.push(msg.text())});
  page.on('response',r=>{if(r.status()>=400)failed.push(r.status()+': '+r.url())});
  await page.goto(ESSAY_URL,{waitUntil:'domcontentloaded',timeout:35000});
  await page.waitForFunction(()=>document.querySelector('#page-viewport')?.dataset.layout==='ready',{timeout:35000});
  const source=await page.evaluate(()=>{
   const t=document.querySelector('template[data-reader-volume="essay--a-sound-must-earn-its-place"]');
   return {buttons:[...t.content.querySelectorAll('[data-press-verbatim]')].map(e=>e.dataset.pressVerbatim),
    iframes:t.content.querySelectorAll('iframe').length,
    players:[...t.content.querySelectorAll('satzfunk-player')].map(e=>e.dataset.soundTrackId),
    illustrations:[...t.content.querySelectorAll('figure[data-source-illustration-id]')].map(e=>e.dataset.sourceIllustrationId)};
  });
  console.log('READ_SOURCE',label,JSON.stringify(source),'url',page.url());
  assert.deepEqual(source.buttons,ids);
  assert.equal(source.iframes,0);
  assert.equal(source.players.length,4);
  assert.deepEqual(source.illustrations,['architectural-plate','night-photograph']);
  const count=Number(await page.locator('#page-viewport').getAttribute('data-pages'));
  assert.ok(count>=8 && count<=45,'Unexpected page count '+count);
  const encountered=new Set();
  for(let i=0;i<count;i++){
   const actual=await page.evaluate(()=>({
    page:document.querySelector('#page-viewport')?.dataset.layout,
    text:document.querySelector('#page-viewport')?.innerText.slice(0,100),
    buttons:[...document.querySelectorAll('#page-viewport [data-press-verbatim]')].map(e=>e.dataset.pressVerbatim),
    status:document.querySelector('#page-counter')?.textContent||''
   }));
   assert.equal(actual.page,'ready','Blank page after layout/turn at leaf '+i);
   for(const id of actual.buttons){
    if(encountered.has(id))continue;
    encountered.add(id);
    await page.locator('#page-viewport [data-press-verbatim="'+id+'"]').click();
    const dialog=page.locator('dialog.press-source-sheet');
    await dialog.waitFor({state:'visible',timeout:12000});
    const frame=page.frameLocator('dialog.press-source-sheet iframe.press-source-original');
    await frame.locator('#toggle').waitFor({state:'visible',timeout:25000});
    if(previewBridge||process.env.STAGE_V172==='1')
      await dialog.locator('.press-source-identity small').filter({hasText:'Source ready'}).waitFor({timeout:30000});
    else await page.waitForTimeout(2100); // Old v171 has no source-readiness handshake.
    const claim=await frame.locator('h1').innerText();
    assert.match(claim,/Kino/);
    if(stageActive){
      await frame.locator('#toggle').click();
      await frame.locator('#status').filter({hasText:/Playing|listening|Could not start audio/i}).waitFor({timeout:30000});
      const state=await frame.locator('#status').innerText();
      assert.ok(/Playing|listening|room/i.test(state),id+': original source did not perform: '+state);
      console.log('VERBATIM_SOURCE_PERFORMS',label,id,state.replace(/\n/g,' ').slice(0,96));
    }else console.log('VERBATIM_SOURCE_UI_PREFLIGHT',label,id,claim);
    await dialog.locator('.press-source-close').click();
    await dialog.waitFor({state:'detached',timeout:10000});
    assert.equal(await page.locator('#page-viewport').getAttribute('data-layout'),'ready');
   }
   if(await page.locator('#next-page').isDisabled())break;
   await page.locator('#next-page').click();
   await page.waitForTimeout(160);
  }
  assert.deepEqual([...encountered].sort(),ids);
  if(errors.length||failed.length)throw Error(JSON.stringify({errors,failed}).slice(0,1600));
  console.log('VERBATIM_PRESS_PAGINATION_PASS',label,viewport.width+'x'+viewport.height,count,'leaves; source controls=2; recordings=4; book iframes=0');
  await context.close();
 }finally{await browser.close()}
}
(async()=>{
 await verify(chromium,'Chrome landscape',{width:1194,height:834});
 await verify(webkit,'WebKit iPad landscape',{width:1194,height:834},true);
 await verify(webkit,'WebKit iPad portrait',{width:768,height:1024},true);
 console.log('V171_CANDIDATE_BOOK_ACCEPTANCE_PASS');
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
