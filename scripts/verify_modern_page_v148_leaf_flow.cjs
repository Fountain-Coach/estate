#!/usr/bin/env node
// Check every real paginated leaf of the deployed v148 essay with existing controls.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {webkit}=require('/Users/benedikteickhoff/Developer/fcis.fountain.coach/node_modules/playwright');
(async()=>{
 const browser=await webkit.launch({headless:true});
 const context=await browser.newContext({viewport:{width:820,height:1120},ignoreHTTPSErrors:true});
 const page=await context.newPage();
 try{
   await page.goto('https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern');
   await page.waitForFunction(()=>document.querySelector('#page-viewport')?.dataset.layout==='ready' &&
     document.querySelector('#page-viewport')?.dataset.volume==='essay--what-makes-a-page-modern',{timeout:20000});
   const total=Number(await page.locator('#page-viewport').getAttribute('data-pages'));
   assert.equal(total,19);
   const states=[],errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   for(let i=0;i<total;i++){
      const state=await page.evaluate(()=>{
        const v=document.querySelector('#page-viewport');
        const figures=[...v.querySelectorAll('figure[data-source-block^="what-makes-a-page-modern.plate."]')].map(f=>{
          const r=f.getBoundingClientRect(), image=f.querySelector('img'), caption=f.querySelector('figcaption');
          return {
            id:f.dataset.sourceBlock,
            visible:r.width>0 && r.height>0,
            imgLoaded:!!image?.complete && image.naturalWidth>0,
            figX:r.x,imgX:image?.getBoundingClientRect().x,
            captionX:caption?.getBoundingClientRect().x,
          };
        });
        return {text:v.innerText,figures,scrollOverflow:document.documentElement.scrollWidth-innerWidth};
      });
      assert.ok(state.scrollOverflow<=3,'Horizontal overflow on leaf '+i);
      for(const f of state.figures){
        if(f.visible){
          assert.ok(f.imgLoaded,'Image not loaded '+f.id+' leaf '+i);
          assert.ok(Math.abs(f.imgX-f.captionX)<=2,'Figure/caption alignment '+f.id);
        }
      }
      states.push(state);
      if(i+1<total){
        const before=state.text;
        await page.locator('#next-page').click();
        await page.waitForFunction(before=>document.querySelector('#page-viewport')?.innerText!==before,before,{timeout:6000});
      }
   }
   const allText=states.map(s=>s.text).join('\n');
   for(const p of ['The writer is the first actor','Self Out Loud',
         'If a word becomes difficult','What makes the page modern?',
         'The page is complete only provisionally. The work may continue.']){
     assert.ok(allText.includes(p),'Section not reachable by physical page turning: '+p);
   }
   assert.deepEqual(errors,[]);
   await page.screenshot({path:'/tmp/self-out-loud-v148-LIVE-last-leaf-webkit.png'});
   const figureSet=new Set(states.flatMap(s=>s.figures.map(f=>f.id)));
   console.log('LEAF_FLOW_PASS',total,'leaves','figures encountered',figureSet.size,
     'headings reached','5','last leaf screenshot saved');
   fs.writeFileSync('/tmp/self-out-loud-v148-leaf-flow.json',JSON.stringify({
      schema:'fountain.press.self-out-loud-leaf-flow.v1',
      leaves:total,figureIds:[...figureSet],errors,accepted:true},null,2)+'\n');
 }finally{await context.close();await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
