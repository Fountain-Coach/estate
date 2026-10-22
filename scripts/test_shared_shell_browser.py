#!/usr/bin/env python3
"""Read-only Chrome browser witness for three staged owners at four viewports."""
import argparse,json,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
SITES={'estate':'estate/','teatro':'teatro/',
       'solstice':'solstice/editions/first-reading/'}
VIEWS={'desktop':(1180,800),'ipad-landscape':(1024,768),
       'ipad-portrait':(768,1024),'phone-portrait':(390,844)}
IDS=['estate','book','governance','midi2','instruments','teatro','satzfunk','pointer','solstice']
def run(base,chrome,out):
 result={'stage':base,'browser':'Mac headless Chromium, not native iPad Safari',
         'state':'local acceptance candidate, not production release',
         'observations':[],'errors':[],'knownUpstreamDefects':[]}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=chrome,headless=True,args=['--no-sandbox'])
  for width_name,(width,height) in VIEWS.items():
   samples={}
   for identity,path in SITES.items():
    page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
    page.goto(base+path,wait_until='domcontentloaded',timeout=20000)
    page.wait_for_timeout(500)
    m=page.evaluate("""() => {
      const qs=s=>document.querySelector(s);
      const get=(x)=>{const r=x.getBoundingClientRect(),s=getComputedStyle(x);return {
        width:Math.round(r.width),height:Math.round(r.height),color:s.color,
        background:s.backgroundColor,padding:s.padding,font:s.fontFamily,fontSize:s.fontSize}};
      let h=qs('header.fc-estate-shell'),n=qs('nav.fc-shell-reel'),
       f=qs('footer.estate-footer'), logo=qs('img.estate-logo'),
       link=n.querySelector('a[data-estate-id="satzfunk"]');
      return {
        header:get(h),nav:get(n),footer:get(f),logo:get(logo),link:get(link),
        workMain:!!qs('main'),logoReady:logo.complete&&logo.naturalWidth>0,
        visibleReelLabels:[...n.querySelectorAll('a.fc-reel-link span')].filter(x=>{
          const style=getComputedStyle(x),r=x.getBoundingClientRect();
          return style.display!=='none' && style.visibility!=='hidden'
            && style.clipPath==='none' && r.width>3 && r.height>3;
        }).length,
        footerCopyFontPx:parseFloat(getComputedStyle(
          f.querySelector('[data-footer-slot="provenance"] p')).fontSize),
        legalTouchHeights:[...f.querySelectorAll('.fc-legal-links a')].map(x=>
          Math.round(x.getBoundingClientRect().height)),
        identity:h.dataset.estateIdentity,
        reel:[...n.querySelectorAll('a[data-estate-id]')].map(x=>x.dataset.estateId),
        active:[...n.querySelectorAll('a[aria-current="page"]')].map(x=>x.dataset.estateId),
        localLinks:[...n.querySelectorAll('a[data-stage-binding]')]
          .map(x=>({id:x.dataset.estateId,href:x.href,canonical:x.dataset.canonicalHref})),
        footerSlots:[...f.querySelectorAll('[data-footer-slot]')].map(x=>x.dataset.footerSlot),
        statusInFooter:!!f.querySelector('a[href="https://status.fountain.coach/"]'),
        canvases:document.querySelectorAll('canvas').length,
        bookControls:[...document.querySelectorAll('#book-prev,#book-next,#book-toc-button,#book-type-button')].map(x=>x.id),
        documentOverflow:document.documentElement.scrollWidth-innerWidth
      };}""")
    issues=[]
    if m['identity']!=identity or m['active']!=[identity]:issues.append('Wrong active identity')
    if m['reel']!=IDS:issues.append('Nine editorial reel identities drift')
    if len(m['localLinks'])!=4:issues.append('Local binding count drift')
    if not m['statusInFooter']:issues.append('Status absent from footer')
    if m['footerSlots']!=['imprint','provenance','legal','release-state']:issues.append('Footer slots/order drift')
    if not m['logoReady']:issues.append('Publisher mark missing')
    if m['visibleReelLabels']!=10:issues.append('Editorial navigation labels are visually missing')
    if m['footerCopyFontPx']<14:issues.append('Publisher footer print is undersized')
    if width_name=='phone-portrait' and min(m['legalTouchHeights'],default=0)<40:
     issues.append('Phone legal links have undersized touch height')
    if identity=='teatro' and m['canvases']<1:issues.append('Teatro source visual runtime missing')
    if identity=='solstice' and len(m['bookControls'])!=4:issues.append('Linotype source reader controls absent')
    if m['documentOverflow']>3:
     if identity=='solstice' and width_name=='phone-portrait' and m['documentOverflow']==8:
      result['knownUpstreamDefects'].append({'site':identity,'viewport':width_name,
          'overflowPx':8,'cause':'source-owned book-toolbar, also present on live Solstice'})
     else:issues.append('Unexpected document overflow '+str(m['documentOverflow']))
    page.locator('a.estate-info').click()
    page.wait_for_timeout(1300)
    info=page.evaluate("""() => {const f=document.querySelector('footer.estate-footer');
      let r=f.getBoundingClientRect();return {hash:location.hash,
        visible:r.top<innerHeight&&r.bottom>0}}""")
    if info['hash']!='#footer' or not info['visible']:issues.append('Info does not reach visible footer')
    if width_name=='ipad-portrait':
     screenshot=out/f'{identity}-ipad-portrait.png'
     page.screenshot(path=str(screenshot),full_page=False)
     m['viewportScreenshotSHA256']=hashlib.sha256(screenshot.read_bytes()).hexdigest()
    samples[identity]=m
    result['observations'].append({'site':identity,'viewport':width_name,'data':m,
                                    'info':info,'issues':issues})
    for problem in issues: result['errors'].append({'site':identity,'viewport':width_name,'error':problem})
    page.close()
   # The shared chrome is visually equivalent if immutable CSS-derived
   # structure and dimensions match. Natural footer height is content-slot
   # dependent and is not a fixed-size invariant.
   for part in ('header','nav','footer','logo','link'):
    for field in ('width','background','color','font','fontSize','padding'):
     seen={str(samples[id][part][field]) for id in SITES}
     if len(seen)>1:result['errors'].append({'viewport':width_name,'component':part,
        'style':field,'values':{id:samples[id][part][field] for id in SITES}})
   for part in ('header','nav','logo','link'):
    heights={samples[id][part]['height'] for id in SITES}
    if len(heights)>1:result['errors'].append({'viewport':width_name,'component':part,
        'style':'height','values':list(heights)})
  browser.close()
 result['passed']=not result['errors']
 (out/'browser-witness.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'tested':len(result['observations']),'passed':result['passed'],
   'errors':result['errors'][:16],'knownUpstreamDefects':result['knownUpstreamDefects']},indent=2))
 return 0 if result['passed'] else 1
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('--origin',default='http://192.168.8.50:8200/')
 ap.add_argument('--chrome',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 ap.add_argument('--output',type=Path,required=True)
 a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 raise SystemExit(run(a.origin,a.chrome,a.output))
