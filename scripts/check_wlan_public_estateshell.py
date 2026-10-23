#!/usr/bin/env python3
"""Strict read-only inspection of one complete static v11 EstateShell stage."""
import argparse,hashlib,json
from pathlib import Path
from bs4 import BeautifulSoup
from complete_first_reading_stage import verify

IDS=('estate','book','governance','midi2','instruments','teatro','satzfunk','pointer','solstice')
OWNERS=tuple(i for i in IDS if i!='satzfunk')
SLOTS=('imprint','provenance','legal','release-state')
def digest(bytes):return hashlib.sha256(bytes).hexdigest()
def validate(root,receipt,reel):
    root=Path(root); receipt=json.loads(Path(receipt).read_text())
    manifest=json.loads(Path(reel).read_text())
    assert tuple(x['id'] for x in manifest['entries'])==IDS
    assert receipt['stageProfile']=='UbuntuEstateShellWLANStage' and receipt['stageOnly'] is True
    assert receipt['publicPublished'] is False and receipt['privateArchiveCopied'] is False
    lock=json.loads((root/'source-lock.json').read_text())
    assert lock['status']=='WLAN-PREVIEW-NOT-PUBLIC'
    assert lock['authorPublished'] is False and lock['archiveMediaCopied'] is False
    assert lock['releaseReceipt'] is None
    assert tuple(lock['completeEditorialEntrances'])==OWNERS
    assert lock['governanceFullChapterCount']==160
    assert not any(p.is_symlink() for p in root.rglob('*'))
    assert not any(p.suffix.lower() in ('.wav','.mp4','.m4a','.mov','.p12','.pem','.key') for p in root.rglob('*') if p.is_file())
    expected=receipt['fileSHA256']
    actual={p.relative_to(root).as_posix():digest(p.read_bytes())
        for p in root.rglob('*') if p.is_file() and not p.name.startswith('._') and p.name!='.DS_Store'}
    assert actual==expected, 'candidate file inventory differs from checked source'
    reader='solstice/editions/first-reading/index.html'
    verified_reading_files=verify(root)
    html=[root/rel for rel in lock['stagedPageReceipts'] if rel!=reader]
    assert len(html)==173,(len(html),'missing expected 173 shell projections')
    deep=[p for p in (root/'governance'/'chapters').rglob('index.html') if not p.name.startswith('._')]
    assert len(deep)==160,(len(deep),'governance chapter count')
    versions=set();failures=[]; owner_counts={}
    for p in sorted(html):
        rel=p.relative_to(root)
        owner=rel.parts[0]
        if owner not in OWNERS:raise ValueError('unadmitted editorial HTML '+str(rel))
        owner_counts[owner]=owner_counts.get(owner,0)+1
        page=BeautifulSoup(p.read_bytes(),'html.parser')
        navs=page.select('nav.fc-shell-reel')
        headers=page.select('header.fc-estate-shell')
        footers=page.select('footer.fc-estate-shell#footer')
        errs=[]
        if len(navs)!=1 or len(headers)!=1 or len(footers)!=1:
            errs.append('shared-shell-count')
        else:
            n=navs[0];f=footers[0];h=headers[0]
            if h.get('data-estate-identity')!=owner:errs.append('owner-active-identity')
            versions.add(h.get('data-estate-shell-version'))
            if h.get('data-estate-shell-version')!=f.get('data-estate-shell-version'):errs.append('header-footer-version')
            if h.get('data-estate-shell-version')!=lock['templateVersion']:errs.append('template-drift')
            if f.get('data-footer-contract')!='fountain.estate.canonical-footer.v1':errs.append('footer-contract')
            if tuple(x.get('data-footer-slot') for x in f.select('[data-footer-slot]'))!=SLOTS:errs.append('footer-structure')
            labels=n.select('[data-estate-id]')
            if tuple(x.get('data-estate-id') for x in labels)!=IDS:errs.append('reel-membership')
            if len(n.select('a.estate-info[href="#footer"]'))!=1:errs.append('info-anchor')
            if n.select('[data-estate-id="status"]'):errs.append('status-in-reel')
            if not f.select_one('a[href="https://status.fountain.coach/"]'):errs.append('missing-status')
            if len(page.select('img.estate-logo'))!=1:errs.append('logo')
            selected=[x.get('data-estate-id') for x in labels if x.get('aria-current')=='page']
            if selected!=[owner]:errs.append('selected-owner')
            for x in labels:
                id=x.get('data-estate-id')
                if id=='satzfunk':
                    if x.name!='span' or x.get('aria-disabled')!='true' or x.get('href'):
                        errs.append('private-satzfunk-leak')
                    continue
                if x.name!='a' or x.get('href')!='/'+id+'/':errs.append('stage-target-'+id)
                if x.get('data-canonical-href')!=next(e['url'] for e in manifest['entries'] if e['id']==id):
                    errs.append('canonical-target-'+id)
                if x.get('data-stage-binding')!='wlan-only':errs.append('binding-marker-'+id)
        if errs:failures.append({'route':rel.as_posix(),'errors':errs})
    assert not failures, 'incomplete shell acceptance: '+json.dumps(failures[:5])
    assert versions=={lock['templateVersion']}
    assert set(owner_counts)==set(OWNERS)
    assert owner_counts['governance']==166
    assert owner_counts['solstice']==1
    assert all(owner_counts[i]==1 for i in OWNERS if i not in ('governance','solstice'))
    return {'passed':True,'scope':'WLAN-staging-structure-not-Safari-or-publication',
            'sourceRevision':receipt['sourceRevision'],
            'htmlRoutes':len(html),'verifiedReadingFiles':verified_reading_files,'governanceChapters':len(deep),
            'ownerCounts':owner_counts,'verifiedStaticFiles':len(expected),
            'shellVersion':next(iter(versions)),'privateArchiveCopied':False,
            'publishedPublicly':False}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--receipt',type=Path,required=True)
    p.add_argument('--reel',type=Path,required=True)
    o=p.parse_args()
    try:r=validate(o.root,o.receipt,o.reel)
    except Exception as ex:
        print(json.dumps({'passed':False,'reason':str(ex)},indent=2));return 1
    print(json.dumps(r,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
