#!/usr/bin/env python3
"""Compare pinned historical root-matching estate trees to current published bytes.

Supplemental Git projection evidence; never changes source ownership or releases.
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recovery'
PATH=OUT/'root-matched-historical-artifacts.json'
MD=OUT/'root-matched-historical-artifacts.md'
WITNESS=ROOT/'inventory/public-readback.json'
SCHEMA='fountain.estate.historical-root-matched-artifacts.v1'
REVISIONS={
 'book.fountain.coach':'e23618e1f5e0f7102faaf7b980a854c2a295f2e2',
 'midi2.fountain.coach':'e23618e1f5e0f7102faaf7b980a854c2a295f2e2',
 'solstice.fountain.coach':'5e9d6b0ba5746abceed41ffefbf69dc5a7d26066',
}
SOURCES={
 'book.fountain.coach':('book.fountain.coach','/','/'),
 'midi2.fountain.coach':('midi2.fountain.coach','/','/'),
 'solstice.fountain.coach':('works.benedikt-eickhoff.de','/solstice/','/solstice/editions/first-reading/'),
}
SPEC=importlib.util.spec_from_file_location('archive_audit',ROOT/'scripts/audit-historical-projection.py')
archive=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive)
def hash_bytes(data):return hashlib.sha256(data).hexdigest()
def witness_hash(host,route):
  rows=json.loads(WITNESS.read_text())['domains']
  entry=next(x for x in rows if x['host']==host)
  row=next(x for x in entry['checks'] if x['route']==route)
  if row['httpStatus']!=200 or not row.get('sha256'):raise ValueError('Missing successful public witness '+host+route)
  return row['sha256']
def make_table(data):
  lines=['# Public-root-matched historical estate artifacts','',
    '**Archival Git evidence; canonical ownership and publication authorization unchanged.**','',
    'Each selected archival revision contains one byte-identical *published root document*, compared against the independent public-readback witness. All Git-tracked files at the selected revision were then compared individually against current public HTTPS. This still does not prove that Git contains *every* public route or asset.',
    '', '| Published surface | Matching archive revision | Committed files | Exact | Different | HTTP missing | Other errors |',
    '|---|---|---:|---:|---:|---:|---:|']
  for row in data['subjects']:
    c=row['counts']
    lines.append('| '+row['publicHost']+row['publicPrefix']+' | `'+row['revision'][:12]+'` | '+str(c['total'])+' | '+str(c['EXACT'])+' | '+str(c['DIFFERENT'])+' | '+str(c['NOT_HTTP_200'])+' | '+str(sum(c[x] for x in ('TRANSPORT_ERROR','TRANSPORT_TIMEOUT','INCOMPLETE_RESPONSE','UNEXPECTED_REDIRECT_HOST')))+' |')
  lines+=['','## Independent authority boundary','',
       '- The archival repository is Fountain-Coach/midi2-gpu-fabric, not the listed publication owner for the Book of Reframe, MIDI2, or the delegated Solstice. This audit **does not** transfer ownership.',
       '- A root-matching archival tree is not a complete public release receipt; individual mismatches and absent files are retained.',
       '- The published Solstice URL is on works.benedikt-eickhoff.de/solstice/, while its canonical source owner is Fountain-Coach/solstice.fountain.coach.',
       '- Never replace present public sites with these Git trees until complete route/asset admission and domain-owner authorization.',
       '', '## Remaining divergences','']
  for row in data['subjects']:
    lines+=['### '+row['publicHost']+row['publicPrefix'],'']
    bad=[f for f in row['files'] if f['comparison']!='EXACT']
    for x in bad[:30]:lines.append('- '+x['comparison']+': `'+x['relativePath']+'` (HTTP '+str(x['httpStatus'])+')')
    if len(bad)>30:lines.append('- '+str(len(bad)-30)+' more divergent files documented in JSON')
    if not bad:lines.append('- No differences among the tracked files in this historical tree; public completeness remains unproved')
    lines.append('')
  lines+=['## Controls','',
       'Probe: `npm run recovery:matched-probe` (read-only GETs and Git committed objects). Verify recorded evidence: `npm run recovery:matched-verify`.',
       'No DNS, SSH, Caddy configuration, public routing, credentials or deployment are changed.']
  return '\n'.join(lines)+'\n'
def audit():
  witness=json.loads(WITNESS.read_text())
  archived={}
  for source,(host,prefix,root_route) in SOURCES.items():
    ref=REVISIONS[source]
    relative_doc=root_route[len(prefix):]
    relative_doc=(relative_doc.rstrip('/')+'/index.html').lstrip('/') if relative_doc else 'index.html'
    root_doc='estate/sites/'+source+'/'+relative_doc
    source_body=archive.git('show',ref+':'+root_doc,as_bytes=True)
    expected=witness_hash(host,root_route)
    if hash_bytes(source_body)!=expected:raise RuntimeError('Pinned historical document no longer matches public witness '+source)
    files=archive.source_files(source,ref)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
      future=[pool.submit(archive.request,row,host,prefix) for row in files]
      checked=[f.result() for f in future]
    checked.sort(key=lambda x:x['relativePath'])
    codes=('EXACT','DIFFERENT','NOT_HTTP_200','TRANSPORT_ERROR','TRANSPORT_TIMEOUT','INCOMPLETE_RESPONSE','UNEXPECTED_REDIRECT_HOST')
    counts=dict(total=len(checked),**{code:sum(f['comparison']==code for f in checked) for code in codes})
    record=dict(archivalSourceHost=source,publicHost=host,publicPrefix=prefix,
                revision=ref,rootWitnessRoute=root_route,
                rootDocumentGitPath=root_doc,rootPublicSHA256=expected,
                sourceBlobCount=len(files),counts=counts,files=checked)
    archived[source]=record
    print('ROOT_MATCHED_ARCHIVE',host+prefix,counts,flush=True)
  return dict(schema=SCHEMA,publicReadbackSHA256=hash_bytes(WITNESS.read_bytes()),
              archivalRepository=archive.PROJECTION,releaseAdmitted=False,
              ownershipTransferred=False,completePublicAssetCoverage=False,
              subjects=[archived[s] for s in sorted(archived)])
def verify():
  data=json.loads(PATH.read_text())
  if data['schema']!=SCHEMA or data['releaseAdmitted'] or data['ownershipTransferred'] or data['completePublicAssetCoverage']:
    raise ValueError('Unsafe/invalid historical archive')
  if data['publicReadbackSHA256']!=hash_bytes(WITNESS.read_bytes()):raise ValueError('Changed public witness')
  if len(data['subjects'])!=len(SOURCES):raise ValueError('Missing source in archive')
  for row in data['subjects']:
    source=row['archivalSourceHost']
    if source not in REVISIONS or row['revision']!=REVISIONS[source]:raise ValueError('Unpinned revision')
    if row['rootPublicSHA256']!=witness_hash(row['publicHost'],row['rootWitnessRoute']):
      raise ValueError('Root witness stale')
    if hash_bytes(archive.git('show',row['revision']+':'+row['rootDocumentGitPath'],as_bytes=True))!=row['rootPublicSHA256']:
      raise ValueError('Root Git blob mismatch')
    files=archive.source_files(source,row['revision'])
    recorded={f['relativePath']:f for f in row['files']}
    if len(files)!=len(recorded) or len(files)!=row['counts']['total']:raise ValueError('Missing files')
    for file in files:
      found=recorded[file['relativePath']]
      if any(file[k]!=found[k] for k in ('sourceGitBlob','sourceSHA256','sourceBytes')):
        raise ValueError('Archived Git source mismatch '+file['relativePath'])
    for code in ('EXACT','DIFFERENT','NOT_HTTP_200','TRANSPORT_ERROR','TRANSPORT_TIMEOUT','INCOMPLETE_RESPONSE','UNEXPECTED_REDIRECT_HOST'):
      if row['counts'][code]!=sum(x['comparison']==code for x in row['files']):
        raise ValueError('Invalid archive count')
  if make_table(data)!=MD.read_text():raise ValueError('Archived report changed')
  print('ROOT_MATCHED_ARCHIVE_VERIFIED',sum(row['counts']['total'] for row in data['subjects']),'committed files')
def main():
  parser=argparse.ArgumentParser();parser.add_argument('action',choices=['probe','verify'])
  args=parser.parse_args()
  if args.action=='verify':verify();return
  data=audit()
  OUT.mkdir(parents=True,exist_ok=True)
  PATH.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
  MD.write_text(make_table(data))
  print('ROOT_MATCHED_ARCHIVE_PROBED',len(data['subjects']))
if __name__=='__main__':main()
