#!/usr/bin/env python3
"""Apply bounded Works editorial delta to an existing immutable WLAN release."""
import argparse,hashlib,importlib.util,json,shutil
from pathlib import Path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    for x in ("previous","output","source","reel","estate-helper","works-commit"):
        p.add_argument("--"+x,required=True)
    a=p.parse_args()
    old=Path(a.previous).resolve(strict=True)
    out=Path(a.output)
    source=Path(a.source).resolve(strict=True)
    reel=json.loads(Path(a.reel).read_text())
    spec=importlib.util.spec_from_file_location("staged_route",a.estate_helper)
    impl=importlib.util.module_from_spec(spec);spec.loader.exec_module(impl)
    expected=['estate','book','governance','midi2','instruments','teatro','satzfunk','works','solstice']
    assert [v['id'] for v in reel['entries']]==expected
    lock=json.loads((old/'source-lock.json').read_text())
    state=lock['personalWorksLanding']
    assert state['stageOnly'] is True and state['stageFrom']=='/pointer/'
    assert state['worksSourceCommit']=='66c7c0fd640569aee7e7544ae2434c05918f6d28'
    assert old.name=='shared-shell-20261028-v54-works-landing-66c7c0f'
    assert not out.exists()
    # Copy v54 exactly, including the source-approved rest of the estate.
    shutil.copytree(old,out,symlinks=True)
    works=sorted(p for p in source.rglob('index.html') if '.git' not in p.parts)
    assert len(works)==40,len(works)
    paths=[]
    for page in works:
        rel=page.relative_to(source)
        new=(out/'works'/rel)
        new.parent.mkdir(parents=True,exist_ok=True)
        html,seen=impl.apply_links(page.read_text(),reel)
        new.write_text(html)
        paths.append(new.relative_to(out).as_posix())
        assert 'data-estate-identity="works"' in html
        if '<nav class="fc-shell-reel"' not in html:
            raise RuntimeError('missing canonical reel '+str(rel))
    a_url='https://192.168.8.11:8443/fountain.coach/essays/outside-has-no-viewbox-audition/tutorial/'
    # The private tutorial link is a declared stage-only enhancement; no
    # private origin enters the public Works Git source.
    for rel,caption in [
        ('outside-has-no-viewbox/index.html','Private writing workshop: listen to N. and compare two directing choices'),
        ('en/outside-has-no-viewbox/index.html',"Private writing workshop: listen to N. and compare two directing choices")
    ]:
        path=out/'works'/rel
        page=path.read_text()
        insert='<p class="outside-stage-workshop" data-stage-only="true"><a href="'+a_url+'">'+caption+'</a> · Author WLAN preview, not a released edition.</p>'
        marker='<section class="note-block">'
        assert page.count(marker)>=1
        page=page.replace(marker,insert+marker,1)
        path.write_text(page)
    for name in ['index.html','en/index.html']:
        raw=(out/'works'/name).read_text()
        assert 'outside-feature' in raw and 'href="outside-has-no-viewbox/"' in raw
    for old_essay in ['estate/essays/the-door-is-a-score/index.html','teatro/index.html','pointer/archive/index.html','solstice/editions/first-reading/index.html']:
        assert sha(old/old_essay)==sha(out/old_essay),old_essay
    assert sha(out/'works/assets/estate-shell.css')==sha(old/'works/assets/estate-shell.css')
    lock['personalWorksLanding']['worksSourceCommit']=a.works_commit
    lock['personalWorksLanding']['sourceHtmlPages']=40
    lock['personalWorksLanding']['previousStageRelease']=old.name
    lock['outsideViewBoxWorkCandidate']={
        'sourceOwner':'Fountain-Coach/works-benedikt-eickhoff',
        'sourceCommit':a.works_commit,
        'publicRightsStatus':'not-cleared-for-release',
        'status':'WLAN-PREVIEW-WORK-IN-DEVELOPMENT',
        'sourceRoutes':['works/outside-has-no-viewbox/index.html','works/en/outside-has-no-viewbox/index.html'],
        'indexRoutes':['works/index.html','works/en/index.html'],
        'stageWorkshopURL':a_url,
        'sourceHtmlPages':len(works),
        'stageOnlyPrivateWorkshopLink':True,
        'sourceArtworkPublished':False,
        'privateAudioCopied':False,
        'finalHorspielPublished':False
    }
    (out/'source-lock.json').write_text(json.dumps(lock,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({
        'release':out.name,
        'predecessor':old.name,
        'newWorkRoutes':lock['outsideViewBoxWorkCandidate']['sourceRoutes'],
        'workIndexSHA':sha(out/'works/index.html'),
        'enWorkIndexSHA':sha(out/'works/en/index.html'),
        'privateMediaCopied':False,
        'unchangedEssayAndStage':True,
        'publicProductionAffected':False,
        'sourceHtmlPages':len(works)
    },indent=2))

if __name__=='__main__':main()
