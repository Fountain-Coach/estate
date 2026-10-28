#!/usr/bin/env python3
"""One bounded, reversible Works landing projection for the registered WLAN stage.

This authoring-time tool does not publish, change the active symlink, or alter
a production host. It retains the predecessor stage and all archive media.
"""
from __future__ import annotations
import argparse,hashlib,json,re,shutil
from pathlib import Path

MARKER='data-estate-id="'
ANCHOR=re.compile(r'<a\b[^>]*\bdata-estate-id="[^"]+"[^>]*>.*?</a>',re.S)
IDENT=re.compile(r'\bdata-estate-id="([^"]+)"')
TITLE=re.compile(r'<span>\s*Pointer\s*</span>',re.I)
ATTRS={}
ROUTES={"estate":"/estate/","book":"/book/","governance":"/governance/",
        "midi2":"/midi2/","instruments":"/instruments/","teatro":"/teatro/",
        "works":"/works/","solstice":"/solstice/editions/first-reading/"}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def set_attr(markup,key,value):
    pat=re.compile(r'(?<![\w-])'+re.escape(key)+r'="[^"]*"')
    attr=key+'="'+value+'"'
    if pat.search(markup):
        return pat.sub(lambda _:attr,markup,count=1)
    return markup.replace('<a ', '<a '+attr+' ',1)

def apply_links(text,manifest):
    lookup={e['id']:e for e in manifest['entries']}
    seen=[]
    def replace(match):
        a=match.group()
        m=IDENT.search(a)
        if not m:return a
        ident=m.group(1)
        if ident=='pointer':
            ident='works'
            a=set_attr(a,'data-estate-id','works')
            a=set_attr(a,'data-icon-id','works')
            a=set_attr(a,'aria-label','Works')
            a=TITLE.sub('<span>Works</span>',a,count=1)
            a=re.sub(r'(<path\b[^>]*\bd=")[^"]*(")',lambda x:x.group(1)+lookup['works']['path']+x.group(2),a,count=1)
            a=a.replace(' aria-current="page"','')
        if ident not in lookup:
            return a
        canonical=lookup[ident]['url']
        if ident in ROUTES:
            a=set_attr(a,'data-canonical-href',canonical)
            a=set_attr(a,'data-stage-binding','wlan-only')
            a=set_attr(a,'href',ROUTES[ident])
        elif ident=='satzfunk':
            # Public station was witnessed as released in the 24 October reel
            # source. Do not send visitors into the protected 8194 archive.
            a=set_attr(a,'href',canonical)
        seen.append(ident)
        return a
    out=ANCHOR.sub(replace,text)
    return out,seen

def main():
    parser=argparse.ArgumentParser()
    for name in ('previous','output','works-source','reel','decision-commit','works-commit','estate-commit'):
        parser.add_argument('--'+name,required=True)
    a=parser.parse_args()
    previous=Path(a.previous).resolve(strict=True)
    output=Path(a.output)
    works=Path(a.works_source).resolve(strict=True)
    reel_path=Path(a.reel).resolve(strict=True)
    m=json.loads(reel_path.read_text())
    ids=[x['id'] for x in m['entries']]
    expected=['estate','book','governance','midi2','instruments','teatro','satzfunk','works','solstice']
    assert m['schema']=='fountain.estate.canonical-reel.v1' and ids==expected,ids
    previous_lock=json.loads((previous/'source-lock.json').read_text())
    assert previous_lock['authorPublished'] is False
    assert previous_lock['status']=='WLAN-PREVIEW-NOT-PUBLIC'
    assert previous_lock['sites'].keys()=={'estate','teatro','solstice'}
    assert not output.exists()
    original_index=sha((previous/'works/index.html').read_bytes())
    assert original_index=='ec502cc2f074e01ad918e4a20ccdfe3688199e5ea092b9072ea1b89760fb4cd3', 'Works baseline unexpected'
    # Media and current estate routes are cloned, not re-fetched from Git main.
    shutil.copytree(previous,output,symlinks=True)
    original_archive=(output/'pointer/index.html').read_bytes()
    archive=output/'pointer/archive/index.html'
    archive.parent.mkdir(parents=True,exist_ok=True)
    assert not archive.exists()
    archive.write_bytes(original_archive)

    # Only source-authored HTML and its already versioned EstateShell CSS.
    sources=[p for p in works.rglob('index.html') if '.git' not in p.parts]
    assert len(sources)==38,len(sources)
    assert (works/'assets/estate-shell.css').is_file()
    authored=set()
    for src in sources:
        rel=src.relative_to(works)
        dst=output/'works'/rel
        assert dst.is_file(),str(dst)
        dst.write_bytes(src.read_bytes())
        authored.add(dst.relative_to(output).as_posix())
    shutil.copy2(works/'assets/estate-shell.css',output/'works/assets/estate-shell.css')
    authored.add('works/assets/estate-shell.css')

    changed=[]
    nav_count=0
    for page in output.rglob('*.html'):
        data=page.read_text()
        if MARKER not in data:continue
        result,links=apply_links(data,m)
        if result!=data:
            page.write_text(result)
            changed.append(page.relative_to(output).as_posix())
        if 'fc-shell-reel' in result:
            nav_count+=1
            section=re.search(r'<nav\b[^>]*\bfc-shell-reel\b[^>]*>.*?</nav>',result,re.S)
            if section:
                reel_links=re.findall(r'\bdata-estate-id="([^"]+)"',section.group())
                if reel_links!=expected:
                    raise RuntimeError('Reel mismatch: '+str(page.relative_to(output))+' '+str(reel_links))
    assert nav_count>=3,nav_count
    for page in (output/'works/index.html',output/'works/en/index.html'):
        t=page.read_text()
        assert 'Benedikt Eickhoff' in t and 'data-estate-identity="works"' in t
        assert 'aria-current="page"' in t and 'data-estate-id="works"' in t
        assert 'data-reel-contract="fountain.estate.canonical-reel.v1"' in t
        assert 'href="/works/"' in t
    assert (output/'pointer/albums/index.html').is_file()
    assert sha((output/'estate/essays/the-door-is-a-score/index.html').read_bytes())==sha((previous/'estate/essays/the-door-is-a-score/index.html').read_bytes()),'door score modified'
    assert sha((output/'teatro/index.html').read_bytes())!=sha((previous/'teatro/index.html').read_bytes()),'reel not inherited'

    lock=previous_lock
    lock['personalWorksLanding']={
        'stageFrom':'/pointer/','stageTo':'/works/','httpStatus':308,
        'sourceOwner':'Fountain-Coach/benedikt-eickhoff.de',
        'decisionCommit':a.decision_commit,
        'worksOwner':'Fountain-Coach/works-benedikt-eickhoff',
        'worksSourceCommit':a.works_commit,
        'estateSourceCommit':a.estate_commit,
        'reelManifestSHA256':sha(reel_path.read_bytes()),
        'stageOnly':True,
        'historicalArchiveRoute':'/pointer/archive/',
        'previousStageRelease':previous.name,
        'changedHtmlPages':len(changed),
        'sourceHtmlPages':len(sources),
        'navPagesWithCommonReel':nav_count,
        'liveProductionAffected':False,
        'publicationState':'WLAN-CANDIDATE-NOT-PUBLIC'
    }
    lock['completeEditorialEntrances']=sorted(set(lock.get('completeEditorialEntrances',[]))|{'works'})
    (output/'source-lock.json').write_text(json.dumps(lock,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({
        'candidate':output.name,'predecessor':previous.name,
        'worksOriginalIndexSHA256':original_index,
        'worksCandidateIndexSHA256':sha((output/'works/index.html').read_bytes()),
        'changedHTML':len(changed),'sourceHTML':len(sources),'reelPages':nav_count,
        'archivePreserved':archive.is_file(),'publicAffected':False
    },indent=2))

if __name__=='__main__':
    main()
