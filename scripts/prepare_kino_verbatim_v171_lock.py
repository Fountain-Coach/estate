#!/usr/bin/env python3
"""Admit two byte-faithful, stage-only Teatro source editions into the existing Press book."""
import argparse,hashlib,json,re
from pathlib import Path
from copy import deepcopy
PREV='shared-shell-20261106-v170-kino-visual-263ac6c'
NAME='shared-shell-20261106-v171-kino-verbatim-f50d16c'
PREV_LOCK='0dab307456a41b082a1057b0270b0e3eb613b647a466e0e891cf4770e285abf1'
INDEX='bd093b088ce6c2aae71958dd1cfae8435409883b5f70e8fa62acf3d4af575022'
SOURCE='fa6d70b4fbf9febbacfe0b02c53947988e501ff180bd5dc4a389f2b62fbf00b4'
RECEIPT='estate/evidence/press-kino-verbatim-v171.json'
RECEIPT_SHA='4af9416989642f0742a23a30d9d4e95ec756ab74f9ebbce51c3932feda659a42'
SITE='f50d16c7438479a3166fd6eee6c2e095d13e8d2f'
TEATRO='74217b710d1955aede0c677cfdd23a0c8c6299cf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(previous,candidate):
 if (previous.name,candidate.name)!=(PREV,NAME):raise ValueError('Unknown source release')
 if sha(previous/'source-lock.json')!=PREV_LOCK:raise ValueError('Stage predecessor lock mismatch')
 if sha(candidate/RECEIPT)!=RECEIPT_SHA:raise ValueError('Candidate receipt changed after build')
 evidence=json.loads((candidate/RECEIPT).read_text())
 if (evidence.get('schema')!='fountain.press.kino-original-source-citations.v171'
     or evidence.get('indexSHA256')!=INDEX or evidence.get('manuscriptSHA256')!=SOURCE
     or evidence.get('parentIndexSHA256')!=sha(previous/'estate/index.html')
     or evidence.get('publicReleaseAuthorized') is not False
     or evidence.get('privateWLANOnly') is not True
     or evidence.get('originalRuntimeUnmodified') is not True
     or evidence.get('existingLinotypeJSUnchanged') is not True
     or evidence.get('iframesInLinotype')!=0
     or evidence.get('liveOriginalSourceIDs')!=['v156','v158']
     or evidence.get('recordedComparisonTracksPreserved')!=['kino-history-groove','kino-history-memory','a-literal','b-directed']):
  raise ValueError('Wrong Press citation provenance or release rights')
 oldfiles={p.relative_to(previous).as_posix():p for p in previous.rglob('*') if p.is_file()}
 newfiles={p.relative_to(candidate).as_posix():p for p in candidate.rglob('*') if p.is_file()}
 allowed={**evidence['added'],RECEIPT:RECEIPT_SHA}
 if set(newfiles)-set(oldfiles)!=set(allowed) or set(oldfiles)-set(newfiles):
  raise ValueError('Unexpected stage asset addition/deletion')
 for name,p in newfiles.items():
  if p.is_symlink():raise ValueError('Unapproved stage symlink')
  if name=='source-lock.json':continue
  h=(INDEX if name=='estate/index.html' else allowed.get(name))
  if h is None:h=sha(oldfiles[name])
  if sha(p)!=h:raise ValueError('Unreviewed staged file '+name)
 previous_html=(previous/'estate/index.html').read_text()
 index=(candidate/'estate/index.html').read_text()
 pat=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
 a=re.findall(pat,previous_html,re.S);b=re.findall(pat,index,re.S)
 bridge='<script type="module" src="/estate/assets/instruments/kino-verbatim-bridge.js"></script>'
 if (len(a)!=1 or len(b)!=1 or index.replace(b[0],a[0],1).replace(bridge,'',1)!=previous_html
     or index.count(bridge)!=1 or b[0].count('<iframe')!=0
     or b[0].count('data-press-verbatim=')!=2
     or b[0].count('<satzfunk-player compact')!=4
     or b[0].count('data-source-illustration-id=')!=2
     or 'data-source-sha256="'+SOURCE+'"' not in b[0]):
  raise ValueError('Reader content or original instruments not source-faithful')
 manifest=json.loads((candidate/'teatro/interludes/kino/press-citation/manifest.json').read_text())
 if manifest.get('publicReleaseAuthorized') is not False or manifest.get('sourceUnmodified') is not True:
  raise ValueError('Original source rights or verbatim claim changed')
 originals={
  'v156':('35fd6a4','12b4613db0472293887c7a9a6f1c7e066151ef406c1632a03c3a5b37dcd360f6'),
  'v158':('e2f5dd2','293cbec0524809e432d1494c91f2c88b1457c4f44680068417408e557041a3bf')
 }
 for m in manifest['editions']:
  commit,digest=originals[m['id']]
  if m['exactSnapshotCommit']!=commit or m['sourceHtmlSHA256']!=digest or sha(candidate/'teatro/interludes/kino/press-citation'/m['id']/'index.html')!=digest:
   raise ValueError('Original Kino source has been replaced')
 lock=deepcopy(json.loads((previous/'source-lock.json').read_text()))
 if 'pressKinoVerbatimV171Admission' in lock:raise ValueError('Repeated admission')
 lock['pressKinoVerbatimV171Admission']={
  'schema':'fountain.press.kino-verbatim-v171','release':NAME,'predecessor':PREV,
  'sourceOwner':'Fountain-Coach/fountain.coach','sourceCommit':SITE,
  'teatroOwner':'Fountain-Coach/teatro.fountain.coach','teatroCommit':TEATRO,
  'sourceSHA256':SOURCE,'readerIndexSHA256':INDEX,'receiptSHA256':RECEIPT_SHA,
  'originalSourceCommits':['35fd6a4','e2f5dd2'],
  'originalReaderUnchanged':True,'originalAudioPreserved':True,
  'noIframeInLinotype':True,'privateWLANOnly':True,'publicReleaseAuthorized':False
 }
 (candidate/'source-lock.json').write_text(json.dumps(lock,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'release':NAME,'sourceLockSHA256':sha(candidate/'source-lock.json'),
  'addedFiles':len(allowed),'changedFiles':1,'originals':list(originals),'sourceCommit':SITE,'teatroCommit':TEATRO},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--previous',type=Path,required=True);p.add_argument('--candidate',type=Path,required=True)
 a=p.parse_args();prepare(a.previous,a.candidate)
