#!/usr/bin/env python3
"""EstatePublisher-facing shared-shell gate; publication fails closed.

This checker has no deployment side effects. It distinguishes structural
readiness from native Safari and independently witnessed public publication.
"""
import argparse, hashlib, json
from html.parser import HTMLParser
from pathlib import Path

SLOTS=('imprint','provenance','legal','release-state')

class Page(HTMLParser):
    def __init__(self,html):
        super().__init__();self.nav=0;self.footer=0;self.logos=0;self.links=[]
        self.slots=[];self.legal=[];self.info=0;self.reel=None;self.version=[];self.footer_version=None
        self.feed(html)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);cs=set(a.get('class','').split())
        if tag=='header' and 'fc-estate-shell' in cs:self.version.append(a.get('data-estate-shell-version'))
        if tag=='nav' and 'estate-nav' in cs:
            self.nav+=1;self.reel=a.get('data-reel-contract');self.innav=True
        if tag=='footer' and 'estate-footer' in cs:
            self.footer+=1;self.footer_version=a.get('data-footer-contract');self.infooter=True
            self.footer_id=a.get('id');self.version.append(a.get('data-estate-shell-version'))
        if tag=='img' and 'estate-logo' in cs:self.logos+=1
        if getattr(self,'innav',False) and tag=='a':
            if 'data-estate-id' in a:self.links.append(a)
            if 'estate-info' in cs and a.get('href')=='#footer':self.info+=1
        if getattr(self,'infooter',False):
            if a.get('data-footer-slot'):self.slots.append(a['data-footer-slot'])
            if tag=='a':self.legal.append(a.get('href'))
    def handle_endtag(self,tag):
        if tag=='nav':self.innav=False
        if tag=='footer':self.infooter=False

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def acceptance(manifest,sites,css,logo,mode,webkit=None,publisher=None):
    ids=[e['id'] for e in manifest['entries']]
    if len(ids)!=9 or len(set(ids))!=9 or 'status' in ids:raise ValueError('invalid canonical editorial reel')
    if len(sites)<2:raise ValueError('at least two distinct domains required')
    if set(sites)!=set(css) or set(sites)!=set(logo):raise ValueError('asset/route coverage mismatch')
    checks=[];versions=set()
    for ident,path in sites.items():
        page=Page(Path(path).read_text(encoding='utf8'))
        errors=[]
        def require(test,reason):
            if not test:errors.append(reason)
        require(page.nav==1,'one top reel required')
        require(page.footer==1,'one estate footer required')
        require(page.logos==1,'one publisher logo required')
        require(page.reel=='fountain.estate.canonical-reel.v1','reel contract mismatch')
        require(page.footer_version=='fountain.estate.canonical-footer.v1','footer contract mismatch')
        require(len(page.version)==2 and page.version[0] and len(set(page.version))==1,'shared shell revision drift')
        if page.version and page.version[0]:versions.add(page.version[0])
        require([x.get('data-estate-id') for x in page.links]==ids,'reel membership/order drift')
        for got,expected in zip(page.links,manifest['entries']):
            require(all(got.get(key)==val for key,val in [('href',expected['url']),('aria-label',expected['label']),('data-icon-id',expected['id'])]),'reel link/icon drift: '+expected['id'])
        active=[x.get('data-estate-id') for x in page.links if x.get('aria-current')=='page']
        require(active==([ident] if ident!='status' else []),'active identity mismatch')
        require(page.info==1 and page.footer_id=='footer','Info/footer anchor mismatch')
        require(tuple(page.slots)==SLOTS,'footer slot order drift')
        require('https://status.fountain.coach/' in page.legal,'Status must appear in legal footer')
        require('https://governance.fountain.coach/legal/' in page.legal,'missing legal notice')
        checks.append({'site':ident,'passed':not errors,'errors':errors})
    cssset={digest(v) for v in css.values()};logoset={digest(v) for v in logo.values()}
    if len(cssset)!=1:checks.append({'site':'shared-css','passed':False,'errors':['CSS byte drift']})
    if len(logoset)!=1:checks.append({'site':'shared-mark','passed':False,'errors':['logo byte drift']})
    if len(versions)!=1:checks.append({'site':'shared-version','passed':False,'errors':['shell version drift']})
    structural=all(x['passed'] for x in checks)
    gates={'structural':structural,'nativeWebKit':False,'authorizedPublication':False}
    if webkit:
        e=json.loads(Path(webkit).read_text())
        gates['nativeWebKit']=bool(e.get('nativeSafariIPad') is True and e.get('headerFooterTransitionReport') and e.get('screenshotHashes') and e.get('sourceRevisions'))
    if publisher:
        e=json.loads(Path(publisher).read_text())
        gates['authorizedPublication']=bool(e.get('estatePublisherTerminalReceipt') and e.get('publicHTTPSReadbacks') and e.get('rollbackRelease'))
    # An arbitrary JSON evidence file is NOT a cryptographically admitted
    # native WebKit witness or an authorized EstatePublisher terminal receipt.
    # Keep publication closed until native verification consumes both through
    # the proper executor. Never turn a forged filename/string into authority.
    untrustedEvidenceSupplied = bool(webkit or publisher)
    if mode == 'publication':
        passed = False
        gates['nativeWebKit'] = False
        gates['authorizedPublication'] = False
    else:
        passed = structural
    return {'passed':passed,'mode':mode,'checks':checks,'gates':gates,
            'primaryEditorialFrontDoors':['estate','solstice','teatro'],
            'reelDestinations':ids,'cssSHA256':next(iter(cssset)) if len(cssset)==1 else None,
            'logoSHA256':next(iter(logoset)) if len(logoset)==1 else None,
            'publicReleasedByThisOperation':False,
            'reason':('native EstatePublisher must authenticate browser and publication receipts' if mode == 'publication' else None),
            'untrustedEvidenceSupplied':untrustedEvidenceSupplied}

def mapping(args):
    out={}
    for item in args:
        if '=' not in item:raise ValueError('expected identity=path')
        id,path=item.split('=',1)
        if id in out:raise ValueError('duplicate identity')
        out[id]=path
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--manifest',required=True,type=Path)
    p.add_argument('--site',required=True,action='append')
    p.add_argument('--css',required=True,action='append')
    p.add_argument('--logo',required=True,action='append')
    p.add_argument('--mode',choices=['structural','publication'],default='structural')
    p.add_argument('--webkit-evidence',type=Path)
    p.add_argument('--publisher-receipt',type=Path)
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    try:
        r=acceptance(json.loads(a.manifest.read_text()),mapping(a.site),mapping(a.css),mapping(a.logo),a.mode,a.webkit_evidence,a.publisher_receipt)
    except (ValueError,AssertionError,OSError,KeyError) as e:r={'passed':False,'reason':str(e)}
    if a.out:a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2));return 0 if r['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
