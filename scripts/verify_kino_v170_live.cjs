#!/usr/bin/env node
const assert=require('node:assert/strict');
const {chromium,webkit}=require('/Users/benedikteickhoff/Developer/fcis.fountain.coach/node_modules/playwright');
const URL='https://192.168.8.50:8243/estate/#/read/essay--a-sound-must-earn-its-place';
const SVG='789ef2af5131529e1f1ed43ff70ae7dce3ea715e91107304fe00632cf4a3677d';
const IDS=['history-groove','history-memory','literal','directed'];
async function visit(engine,label,viewport){
 const browser=await engine.launch(label==='Chromium'?{headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--autoplay-policy=no-user-gesture-required']}:{headless:true});
 try{
 const context=await browser.newContext({viewport,ignoreHTTPSErrors:true});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(URL,{waitUntil:'domcontentloaded',timeout:30000});
 await page.waitForFunction(()=>document.querySelector('#page-viewport')?.dataset.layout==='ready',{timeout:40000});
 const original=await page.evaluate(()=>{
  const t=document.querySelector('template[data-reader-volume="essay--a-sound-must-earn-its-place"]');
  return {players:[...t.content.querySelectorAll('satzfunk-player')].map(x=>x.dataset.soundTrackId),
    images:[...t.content.querySelectorAll('figure[data-source-illustration-id]')].map(x=>x.dataset.sourceIllustrationId),
    frames:[...t.content.querySelectorAll('iframe')].map(x=>x.getAttribute('src'))};
 });
 assert.deepEqual(original.players,['kino-history-groove','kino-history-memory','a-literal','b-directed']);
 assert.deepEqual(original.images,['architectural-plate','night-photograph']);
 assert.deepEqual(original.frames,['/teatro/interludes/kino/live-csound/?pair=history','/teatro/interludes/kino/live-csound/?pair=controlled']);
 let total=Number(await page.locator('#page-viewport').getAttribute('data-pages'));
 const played=new Set(),visible=new Set(),pics=new Set();
 for(let i=0;i<total;i++){
  const current=await page.evaluate(()=>{
   const view=document.querySelector('#page-viewport');
   return {frames:[...view.querySelectorAll('iframe[src*="live-csound"]')].map(x=>({src:x.getAttribute('src'),height:x.getBoundingClientRect().height,width:x.getBoundingClientRect().width})),
     figures:[...view.querySelectorAll('figure[data-source-illustration-id]')].map(x=>x.dataset.sourceIllustrationId),
     overflow:document.documentElement.scrollWidth-innerWidth};
  });
  assert.ok(current.overflow<=3,'Overflow leaf '+i);
  for(const fig of current.figures) pics.add(fig);
  for(const item of current.frames){
   const pair=new URL(item.src,'https://192.168.8.50').searchParams.get('pair');
   visible.add(pair);
   assert.ok(item.height>=280 && item.width>150,'Kino architecture clipped on leaf '+i);
   const f=page.frameLocator('#page-viewport iframe[src="'+item.src+'"]');
   await f.locator('.stage svg').waitFor({state:'visible',timeout:20000});
   await f.locator('.memory-window').first().waitFor({state:'attached',timeout:20000});
   const geometry=await f.locator('.stage').evaluate(node=>({
     svg:node.querySelector('svg')?.outerHTML,
     windows:node.querySelectorAll('.memory-window').length,
     source:node.innerHTML.includes('Original Teatro Kino After Dark architectural SVG SHA-256 '+''+'789ef2af5131529e1f1ed43ff70ae7dce3ea715e91107304fe00632cf4a3677d')
   }));
   assert.ok(geometry.source && geometry.windows===16 && geometry.svg.includes('K I N O   I N T E R N A T I O N A L'));
   await page.waitForTimeout(2400);
   for(const key of pair==='history'?IDS.slice(0,2):IDS.slice(2)){
    if(played.has(key))continue;
    await f.locator('button[data-play="'+key+'"]').click({timeout:20000});
    await f.locator('#status').filter({hasText:'Csound running'}).waitFor({timeout:25000});
    let audible=false,alive=false;
    for(let tick=0;tick<10;tick++){
      await page.waitForTimeout(500);
      const vals=await f.locator('section[data-synth="'+key+'"] .meter span').evaluate(el=>({meter:el.style.width,window:document.querySelector('.memory-window')?.style.getPropertyValue('--window-level')}));
      if(parseFloat(vals.meter)>0.1 && parseFloat(vals.window)>0.04){audible=true;break}
    }
    assert.ok(audible,'No sound-responsive windows from '+key);
    played.add(key);
    console.log('KINO_LIVE_SVG_AUDIO_PASS',label,key);
    await f.locator('#stop').click({timeout:20000});
    await page.waitForTimeout(1400);
   }
  }
  if(await page.locator('#next-page').isDisabled())break;
  await page.locator('#next-page').click();
  await page.waitForTimeout(200);
 }
 assert.deepEqual([...played].sort(),IDS.slice().sort());
 assert.deepEqual([...visible].sort(),['controlled','history']);
 assert.deepEqual([...pics].sort(),original.images.slice().sort());
 assert.deepEqual(errors,[]);
 console.log('KINO_V170_COMPLETE',label,total,'leaves; four live synths, four recordings, sixteen source windows');
 await context.close();
 }finally{await browser.close()}
}
(async()=>{await visit(chromium,'Chromium',{width:820,height:1120});await visit(webkit,'WebKit',{width:1194,height:834});console.log('KINO_V170_VISUAL_LIVE_ACCEPTANCE_PASS')})().catch(e=>{console.error(e.stack||e);process.exit(1)});
