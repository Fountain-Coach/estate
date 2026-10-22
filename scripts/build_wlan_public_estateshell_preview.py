#!/usr/bin/env python3
"""FCIS 158 author-WLAN artifact for EXISTING 8200 service. No host effects.

Use eight exact public HTTPS homepage captures, Git-owned Governance chapter
tree, and archived v7/v10 public-asset witnesses. Each source is independently
hashed, and changes are confined to shell and explicit stage-local URL bindings.
All effects belong to the separate EstatePublisher release operation.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, re, shutil
from pathlib import Path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from project_public_estate_shell import project_public
from estate_shell import manifest, VERSION

ROOTS={
 'estate':'https://fountain.coach/',
 'book':'https://book.fountain.coach/',
 'governance':'https://governance.fountain.coach/',
 'midi2':'https://midi2.fountain.coach/',
 'instruments':'https://instruments.fountain.coach/',
 'teatro':'https://teatro.fountain.coach/',
 'pointer':'https://benedikt-eickhoff.de/',
 'solstice':'https://works.benedikt-eickhoff.de/solstice/',
}
FULL_ORDER=('estate','book','governance','midi2','instruments','teatro','satzfunk','pointer','solstice')
DEEP={'solstice/editions/first-reading/index.html':
      'https://works.benedikt-eickhoff.de/solstice/editions/first-reading/'}
CANONICAL_ROOT='/Volumes/NINJA2/fcis-20261022-stage'

def digest(value):return hashlib.sha256(value).hexdigest()
def get_live(url):
    request=Request(url,headers={'Cache-Control':'no-cache, no-store',
                                'User-Agent':'EstatePublisherStageSourceWitness/1.0'})
    with urlopen(request,timeout=20) as r:
        if r.status!=200 or r.url!=url:raise ValueError('source HTTPS changed/redirected: '+url)
        return r.read().decode('utf8')
def files(root):
    for p in sorted(root.rglob('*')):
        if p.is_symlink():raise ValueError('forbidden symlink '+str(p))
        if p.is_file() and not p.name.startswith('._') and p.name!='.DS_Store':
            if p.suffix.lower() in {'.mp4','.wav','.mov','.key','.pem','.p12','.m4a'}:
                raise ValueError('private or raw media prohibited: '+str(p))
            yield p
def copy_subtree(src,dst):
    for p in files(src):
        rel=p.relative_to(src)
        q=dst/rel;q.parent.mkdir(parents=True,exist_ok=True)
        if q.exists():raise ValueError('candidate collision: '+str(q))
        shutil.copy2(p,q)

def rebind(html,identity):
    page=BeautifulSoup(html,'html.parser')
    nav=page.select_one('nav.fc-shell-reel')
    if nav is None:raise ValueError('shared reel absent at '+identity)
    targets={x:f'/{x}/' for x in ROOTS}
    # Keep First Reading's own book route under the Solstice site, not a
    # fabricated book edition.
    for anchor in nav.select('a[data-estate-id]'):
        which=anchor.get('data-estate-id')
        if which not in targets:raise ValueError('unknown editorial stage target')
        old=anchor['href']
        if old!=ROOTS[which]:raise ValueError('unexpected canonical link '+str(which))
        anchor['data-canonical-href']=old
        anchor['data-stage-binding']='wlan-only'
        anchor['href']=targets[which]
    satz=nav.select_one('[data-estate-id="satzfunk"]')
    if satz is None or satz.name!='span' or satz.get('aria-disabled')!='true':
        raise ValueError('public Satzfunk must remain inert')
    publisher=page.select_one('a.fc-publisher')
    if publisher:publisher['href']='/estate/'
    # Only same-origin local URLs are rebound; public HTTPS/legal endpoints
    # and external authorial references remain untouched.
    changes=0
    for tag in page.find_all(True):
        if tag.get('data-stage-binding')=='wlan-only' or 'fc-publisher' in tag.get('class',[]):
            continue
        for attr in ('href','src','poster'):
            value=tag.get(attr)
            if not isinstance(value,str) or not value.startswith('/') or value.startswith('//'):
                continue
            if value.startswith('/assets/estate-shell-'):
                continue
            if value.startswith('/'+identity+'/'):
                continue
            tag[attr]='/'+identity+value
            changes+=1
    ids=tuple(x['data-estate-id'] for x in nav.select('[data-estate-id]'))
    if ids!=FULL_ORDER:raise ValueError('nine-identity reel mismatch')
    if len(page.select('header.fc-estate-shell'))!=1 or len(page.select('footer.fc-estate-shell'))!=1:
        raise ValueError('incorrect common chrome cardinality')
    if len(nav.select('a.estate-info[href="#footer"]'))!=1:
        raise ValueError('one Info control required')
    if page.select_one('meta[name="robots"][content*="noindex"]'):
        raise ValueError('public input unexpectedly noindex')
    return str(page),changes

def main():
    parser=argparse.ArgumentParser()
    for arg in ('v7','v10','governance','out','reel','source-revision'):
        parser.add_argument('--'+arg,required=True)
    o=parser.parse_args()
    v7,v10,gov,out=map(Path,(o.v7,o.v10,o.governance,o.out))
    if out.exists():raise ValueError('immutable output already exists')
    reel=manifest(o.reel)
    capture=json.loads((v7/'capture-lock.json').read_text())
    if capture.get('publicationChanged') is not False:
        raise ValueError('legacy source projection is not a read-only capture')
    v10_lock=json.loads((v10/'source-lock.json').read_text())
    if (v10_lock['templateVersion']!=VERSION or v10_lock['authorPublished'] is not False
        or v10_lock['archiveMediaCopied'] is not False):
        raise ValueError('v10 immutable predecessor failed source lock')
    if not (gov/'index.html').is_file() or len(list((gov/'chapters').rglob('index.html')))!=160:
        raise ValueError('Git Governance publication must contain exactly 160 chapters')
    assets_dir=Path(o.reel).resolve().parents[1]/'shell'
    shared={'/assets/estate-shell.css':assets_dir/'estate-shell.css',
            '/assets/estate-shell-state.js':assets_dir/'estate-shell-state.js',
            '/assets/estate-shell-logo.png':assets_dir/'assets/estate-shell-logo.png'}
    urls={path:'/assets/'+Path(path).stem+'-'+digest(src.read_bytes())[:16]+Path(path).suffix
          for path,src in shared.items()}
    original_sources={};page_receipts={};route_count={}
    out.mkdir(parents=True)
    try:
        # Historical source-asset mirrors, not staging-generated page bytes.
        # Only copy domain-owned original assets; header/page source is fresh
        # independently witnessed HTTPS or Git-owned Governance edition.
        for owner in ROOTS:
            target=out/owner
            target.mkdir()
            if owner!='governance':
                assets=v7/owner/'assets'
                if not assets.is_dir():raise ValueError('missing captured owner assets '+owner)
                copy_subtree(assets,target/'assets')
        # Complete Governance source owner, including 160 authored chapters.
        copy_subtree(gov,out/'governance')
        # Existing accepted First Reading's full assets, keeping Teatro media
        # and any private archives out of the accepted public preview.
        old_v10_deep=v10/'solstice/editions/first-reading'
        if not old_v10_deep.is_dir():raise ValueError('missing existing Linotype deep-route assets')
        for p in files(old_v10_deep):
            rel=p.relative_to(old_v10_deep)
            if rel.as_posix()=='index.html':continue
            dest=out/'solstice/editions/first-reading'/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():
                if digest(dest.read_bytes())!=digest(p.read_bytes()):
                    raise ValueError('First Reading authored asset hash disagreement')
                continue
            shutil.copy2(p,dest)
        # Keep the existing stage startup contract's stable asset names, plus
        # content-addressed public projection assets to defeat stale browser
        # caches without a new staging service.
        for path,src in shared.items():
            stable=out/path.lstrip('/')
            stable.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(src,stable)
            fingerprinted=out/urls[path].lstrip('/')
            shutil.copy2(src,fingerprinted)
        # Shared body compiles use the one Git-owned shell.
        for owner,url in ROOTS.items():
            if owner=='governance':
                source_receipt=json.loads(Path(o.governance).parent.joinpath('governance-candidate-receipt.json').read_text()) if False else None
                roots=[p for p in sorted((out/owner).rglob('*.html')) if not p.name.startswith('._')]
                for file in roots:
                    rendered,changes=rebind(file.read_text(encoding='utf8'),owner)
                    file.write_text(rendered,encoding='utf8')
                    page_receipts[file.relative_to(out).as_posix()]={'source':'git-owner-public-candidate',
                         'digest':digest(rendered.encode()),'rebindings':changes}
                route_count[owner]=len(roots)
                continue
            source=get_live(url)
            source_bytes=source.encode()
            original_sources[owner]={'url':url,'sha256':digest(source_bytes),'bytes':len(source_bytes)}
            output,proof=project_public(source,owner,reel,asset_urls=urls)
            rendered,changes=rebind(output,owner)
            path=out/owner/'index.html'
            path.write_text(rendered,encoding='utf8')
            page_receipts[path.relative_to(out).as_posix()]={'source':url,
                'sourceSHA256':proof['sourceSHA256'],
                'workSHA256':proof['sourceWorkSHA256'],
                'digest':digest(rendered.encode()),'rebindings':changes}
            route_count[owner]=1
        # Real published Linotype edition uses its own source and CSP.
        for relative,url in DEEP.items():
            source=get_live(url)
            output,proof=project_public(source,'solstice',reel,asset_urls=urls)
            rendered,changes=rebind(output,'solstice')
            path=out/relative
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(rendered,encoding='utf8')
            page_receipts[relative]={'source':url,'sourceSHA256':proof['sourceSHA256'],
                'workSHA256':proof['sourceWorkSHA256'],
                'digest':digest(rendered.encode()),'rebindings':changes}
            route_count['solstice']+=1
        # Preserve site-specific CSS but project their local absolute asset
        # references to the owning stage prefix.
        for owner in ROOTS:
            for css in (out/owner).rglob('*.css'):
                if css.name.startswith('._'):continue
                text=css.read_text(encoding='utf8')
                replaced=(text.replace('url(/assets/','url(/'+owner+'/assets/')
                              .replace('url("/assets/','url("/'+owner+'/assets/')
                              .replace("url('/assets/","url('/"+owner+'/assets/')
                              .replace('@import "/assets/','@import "/'+owner+'/assets/'))
                if replaced!=text:css.write_text(replaced,encoding='utf8')
        # Existing server explicitly validates three primary front doors.
        # Report the complete eight-owner coverage independently; do not
        # pretend that the old startup predicate checks all eight.
        lock=copy.deepcopy(v10_lock)
        lock['templateVersion']=VERSION
        lock['releaseReceipt']=None
        lock['archiveMediaCopied']=False
        lock['authorPublished']=False
        lock['status']='WLAN-PREVIEW-NOT-PUBLIC'
        lock['completeEditorialEntrances']=list(ROOTS)
        lock['editorialRouteCounts']=route_count
        lock['governanceFullChapterCount']=160
        lock['stageSourceRevision']=o.source_revision
        lock['stageOriginalHTTPSRootDigests']=original_sources
        lock['stagedPageReceipts']=page_receipts
        lock['siteSourceOwnership']='Governance exact Git revision; other seven roots fetched read-only over public HTTPS and source-hashed'
        lock['stageBindings']={name:'http://benedikt-Macmini.local:8200/'+name+'/' for name in ROOTS}
        lock['stageBindings']['satzfunk']='unpublished-public-identity; private-authenticated-WLAN-archive-not-copied'
        lock['originalPublishedSourceUnchanged']=True
        lock['sourceReelDigest']=digest(Path(o.reel).read_bytes())
        for owner in ('estate','teatro'):
            lock['sites'][owner]['projectionSHA256']=page_receipts[owner+'/index.html']['digest']
        lock['sites']['solstice']['projectionSHA256']=page_receipts['solstice/editions/first-reading/index.html']['digest']
        (out/'source-lock.json').write_text(json.dumps(lock,indent=2,sort_keys=True)+'\n')
        results={f.relative_to(out).as_posix():digest(f.read_bytes()) for f in files(out)}
        record={'sourceRevision':o.source_revision,'stageProfile':'UbuntuEstateShellWLANStage',
            'publicPublished':False,'stageOnly':True,'rootSourceDigests':original_sources,
            'fullGovernanceChapters':160,'pageCount':len(page_receipts),
            'editorialOwners':list(ROOTS),'fileCount':len(results),
            'fileSHA256':results,'candidateByteInventoryDigest':digest(
                ''.join(k+' '+v+'\\n' for k,v in sorted(results.items())).encode()),
            'shellVersion':VERSION,'privateArchiveCopied':False,
            'stageServerStartupGate':'existing 3 primary owner predicates; additional eight-owner acceptance is independent'}
        (out.parent/(out.name+'-candidate-receipt.json')).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k not in ('fileSHA256','rootSourceDigests')},indent=2))
    except BaseException:
        shutil.rmtree(out)
        raise
if __name__=='__main__':main()
