#!/usr/bin/env python3
"""Compile an immutable, source-pinned private WLAN v59 inventory over v58."""
from pathlib import Path
from hashlib import sha256
import json,datetime
base=Path('/home/benedikt/estate-shell-acceptance-staging')
new='shared-shell-20261029-v59-living-essays-5ec8c54'
old='shared-shell-20261028-v58-composable-css-05b3915'
candidate=base/'incoming'/new
assert (base/'current').is_symlink()
assert (base/'current').readlink().as_posix()=='releases/'+old
previous=json.loads((base/'receipts/20261028-v58-composable-css/release-inventory.json').read_text())
assert previous['release']==old and previous['fileCount']==1139
lock=candidate/'source-lock.json'
meta=json.loads(lock.read_text())
assert meta['status']=='WLAN-PREVIEW-NOT-PUBLIC' and meta['authorPublished'] is False
assert meta.get('readerFirstStageV59',{}).get('sourceRevision','5ec8c5490c8a1fe2b4a941185ecb3f415a7bdfdd')=='5ec8c5490c8a1fe2b4a941185ecb3f415a7bdfdd'
meta['readerFirstStageV59']={
 'schema':'fountain.estate.reader-first-scenario.v1',
 'status':'WLAN-PREVIEW-NOT-PUBLIC',
 'release':new,'predecessor':old,
 'sourceOwner':'Fountain-Coach/fountain.coach',
 'sourceRevision':'5ec8c5490c8a1fe2b4a941185ecb3f415a7bdfdd',
 'sourcePlan':'editorial/living-essays-reader-source.json',
 'rootRole':'reader-first living Essays book',
 'chapterCount':7,
 'firstWrittenWork':'the-door-is-a-score',
 'firstWrittenDate':'2026-10-27',
 'semanticPathways':['recent','sound','reading','systems'],
 'originalAuthorLedScenario':'/estate/scenarios/author-led/',
 'allOriginalEssayRoutesPreserved':True,
 'measuredPressPagination':True,
 'stageActivatedAtBuild':False,
 'publicProductionAffected':False,
}
lock.write_text(json.dumps(meta,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
entries=[]
for p in sorted(candidate.rglob('*')):
 if p.is_symlink():raise AssertionError('Unexpected symlink '+str(p))
 if not p.is_file():continue
 relative=p.relative_to(candidate).as_posix()
 h=sha256()
 with p.open('rb') as f:
  for part in iter(lambda:f.read(1<<20),b''):h.update(part)
 entries.append(dict(path=relative,sha256=h.hexdigest(),bytes=p.stat().st_size))
before={x['path']:x for x in previous['files']}
after={x['path']:x for x in entries}
added=set(after)-set(before)
expected={'estate/scenarios/reader-first/index.html',
          'estate/scenarios/author-led/index.html',
          'estate/assets/linotype/living-essays.js',
          'estate/assets/linotype/living-essays.css'}
assert added==expected,('Extra/missing new routes',added^expected)
assert set(before)-set(after)==set()
modified=[key for key in before if after[key]!=before[key]]
assert sorted(modified)==['estate/index.html','source-lock.json'],modified
assert len([e for e in entries if e['path'].endswith('/index.html')])==511
assert after['estate/scenarios/author-led/index.html']['sha256']==before['estate/index.html']['sha256']
assert after['estate/scenarios/reader-first/index.html']['sha256']==after['estate/index.html']['sha256']
assert all(after[key]==before[key] for key in before if key.startswith('estate/essays/'))
manifest=''.join(e['path']+'  '+e['sha256']+'\n' for e in entries)
m={'schema':'fountain.estate.wlan-stage-release-inventory.v1',
 'release':new,'priorRelease':old,
 'sourceOwner':'Fountain-Coach/fountain.coach',
 'sourceRevision':'5ec8c5490c8a1fe2b4a941185ecb3f415a7bdfdd',
 'estateOwner':'Fountain-Coach/estate',
 'stageHost':'benedikt-Macmini',
 'stageService':'fountain-shell-acceptance-preview.service',
 'publicAuthorized':False,'scope':'PRIVATE WLAN READER-FIRST LANDING SCENARIO',
 'fileCount':len(entries),'htmlCount':511,
 'totalBytes':sum(x['bytes'] for x in entries),
 'inventorySHA256':sha256(manifest.encode()).hexdigest(),
 'mutation':{'added':sorted(added),'modified':modified,'originalEssayHTMLChanged':0},
 'openingWork':'the-door-is-a-score','pathways':['recent','sound','reading','systems'],
 'files':entries,'receiptState':'CANDIDATE-NOT-ACTIVATED'}
out=base/'incoming/v59-living-essays-release-inventory.json'
out.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
(base/'incoming/v59-living-essays-release-inventory.sha256').write_text(manifest)
print(json.dumps({k:v for k,v in m.items() if k!='files'},indent=2))
