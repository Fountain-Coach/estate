/* Browser witness for the complete, source-owned, original Fountain Press Reader.
   The app's accepted five-essay collection is unchanged by the review template. */
const assert=require("node:assert/strict");
const {chromium}=require("/home/benedikt/fountain-blackmagic-re/tools/rea/node_modules/playwright-core");
const ORIGIN=process.env.STAGE_ORIGIN||"http://192.168.8.50:8200";
const ROUTE="/estate/read/essay--client-centered/";
const SNAP=process.env.SNAP_DIR||"/home/benedikt/estate-shell-acceptance-staging/candidates/client-centered-v177-bd8f6d9";
(async()=>{
const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
try{
 for(const [device,width,height] of [
  ["phone",390,844],["ipad-portrait",820,1180],
  ["ipad-landscape",1180,820],["desktop",1440,900]
 ]){
  const context=await browser.newContext({viewport:{width,height},hasTouch:device!=="desktop",isMobile:device==="phone",reducedMotion:"reduce"});
  const page=await context.newPage();
  const errors=[];
  page.on("pageerror",e=>errors.push("JS:"+e.message));
  page.on("requestfailed",r=>errors.push("REQUEST:"+r.url()+" "+r.failure()?.errorText));
  page.on("response",r=>{if(r.status()>=400&&
    (r.url().includes("/read/essay--client-centered/")||r.url().includes("reading-first")||
     r.url().includes("satzfunk-media-element")))errors.push("HTTP:"+r.status()+" "+r.url())});
  const res=await page.goto(ORIGIN+ROUTE,{waitUntil:"load",timeout:27000});
  assert.equal(res.status(),200,device);
  await page.waitForFunction(()=>document.querySelector("#page-viewport")?.dataset.layout==="ready",{timeout:27000});
  const metadata=await page.evaluate(()=>({
    title:document.title,initial:document.body.dataset.initialVolume,
    stage:document.querySelector('meta[name="fountain:publication-state"]')?.content,
    source:document.querySelector('meta[name="fountain:source-revision"]')?.content,
    pageCount:document.querySelector("#page-count")?.textContent?.trim(),
    manuscript:document.querySelector("#source-flow")?.innerText||"",
    sourceIDs:[...document.querySelectorAll("#source-flow [data-source-block]")].map(e=>e.dataset.sourceBlock),
    active:document.querySelector("#reader-section")?.value,
    scrollWidth:document.documentElement.scrollWidth,
    clientWidth:document.documentElement.clientWidth
  }));
  assert.match(metadata.title,/Client-Centered/);
  assert.equal(metadata.initial,"essay--client-centered");
  assert.equal(metadata.stage,"owner-WLAN-editorial-review");
  assert.equal(metadata.source,"bd8f6d93e01354cc0c09a9de0bf9417bd9cfde9c");
  assert.ok(metadata.sourceIDs.includes("client-centered.s4.p6"));
  assert.ok(metadata.manuscript.includes("What develops between those two circumstances cannot be entirely designed in advance."));
  assert.ok(metadata.manuscript.includes("What Becomes Possible"));
  assert.ok(metadata.scrollWidth<=metadata.clientWidth+3,device+" horizontal overflow");
  const man=await (await page.request.get(ORIGIN+ROUTE+"edition-manifest.json")).json();
  assert.equal(man.paragraphCount,22);
  assert.equal(man.sections.length,4);
  assert.equal(man.figures.length,2);
  assert.equal(man.productionAuthorized,false);
  for(const f of man.figures){
    const img=await page.request.get(ORIGIN+f.stagingURL);
    assert.equal(img.status(),200,"image "+f.id);
    assert.equal(img.headers()["content-type"].includes("svg"),true);
  }
  await page.screenshot({path:SNAP+"/client-centered-"+device+"-first.png",fullPage:false});
  const found=new Set();
  const seen=new Set();
  let turns=0;
  for(;turns<95;turns++){
    const state=await page.evaluate(()=>{
      const rect=document.querySelector("#page-viewport").getBoundingClientRect();
      const images=[...document.querySelectorAll("#page-viewport img")].filter(img=>{
        const r=img.getBoundingClientRect();
        return r.width>2&&r.height>2&&r.bottom>rect.top&&r.top<rect.bottom&&img.naturalWidth>0;
      }).map(img=>img.getAttribute("src"));
      return {images,loc:document.querySelector("#page-count")?.textContent?.trim()||"",
              nextDisabled:document.querySelector("#next-page")?.disabled||false,
              body:document.querySelector("#page-viewport")?.innerText?.slice(0,180)||""};
    });
    seen.add(state.loc);
    for(const src of state.images){
      if(src.includes("client-centered-positions.svg"))found.add("positions");
      if(src.includes("client-centered-open-method.svg"))found.add("method");
    }
    if(found.size===2||state.nextDisabled)break;
    await page.locator("#next-page").click({timeout:6000});
    await page.waitForTimeout(55);
  }
  assert.ok(found.has("positions"),device+" source-anchored opening score not visible");
  assert.ok(found.has("method"),device+" second source-anchored score not visible");
  assert.deepEqual(errors,[],device+" script/resource errors");
  console.log("CLIENT_CENTERED_ORIGINAL_PRESS_PASS",device,
    "source-paragraphs=22","sections=4","figures=2",
    "turns="+turns,"positions="+[...found].join(","),"folios="+seen.size);
  await context.close();
 }
}finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
