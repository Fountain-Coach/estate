#!/usr/bin/env python3
"""Admit only Kino original-source readiness into the existing Press stage."""
from pathlib import Path
import argparse,hashlib,json,re
from copy import deepcopy
OLD='shared-shell-20261106-v171-kino-verbatim-f50d16c'
NEW='shared-shell-20261106-v172-kino-ready-bc4fdc1'
LOCK_OLD='da0162be45fc9b55a6819df27c9247d62b3c99f87fc03600134c756c1b94a1c2'
INDEX='bd093b088ce6c2aae71958dd1cfae8435409883b5f70e8fa62acf3d4af575022'
BRIDGE='057ccec2f0ea2e9c00bad55f2553f4a07a448976784c109ee0a0346fbcdaf099'
GIT='bc4fdc1b146869d10721720ab46ba9a6f37299f7'
SCRIPT='estate/assets/instruments/kino-verbatim-bridge.js'
RECEIPT='estate/evidence/press-kino-ready-v172.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def encode(m):return json.dumps(m,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
def prepare(parent,candidate):
 if (parent.name,candidate.name)!=(OLD,NEW):raise ValueError('Wrong stage predecessor')
 if sha(parent/'source-lock.json')!=LOCK_OLD or sha(parent/'estate/index.html')!=INDEX:raise ValueError('Wrong pinned v171')
 if sha(candidate/SCRIPT)!=BRIDGE or sha(candidate/'estate/index.html')!=INDEX:raise ValueError('Wrong narrow source delta')
 bridge=(candidate/SCRIPT).read_text()
 if ('#kino-windows .window-step' not in bridge or '#kino-windows .memory-window' not in bridge
     or "frame.style.pointerEvents='none'" not in bridge or "frame.style.pointerEvents='auto'" not in bridge):
  raise ValueError('Unreviewed source-readiness method')
 evidence={
  'schema':'fountain.press.kino-verbatim-source-ready.v172','release':NEW,'predecessor':OLD,
  'owner':'Fountain-Coach/estate','sourceCommit':GIT,
  'readerIndexSHA256':INDEX,'readinessBridgeSHA256':BRIDGE,
  'originalSourceEditorsUnchanged':True,'sourceEditionDigestsPreserved':True,
  'originalAudioUnchanged':True,'fourRecordedAuditionsPreserved':True,
  'originalArchitecturalPlatesPreserved':True,'originalReaderUnchanged':True,
  'historicalSourceScriptsUnmodified':True,'sameFolioPositionOnClose':True,
  'safeReadiness':'enable original iframe pointer interaction after sixteen original-source window controls initialize',
  'privateWLANOnly':True,'publicReleaseAuthorized':False
 }
 (candidate/RECEIPT).parent.mkdir(parents=True,exist_ok=True)
 (candidate/RECEIPT).write_text(encode(evidence))
 receipt_sha=sha(candidate/RECEIPT)
 before={p.relative_to(parent).as_posix():p for p in parent.rglob('*') if p.is_file()}
 after={p.relative_to(candidate).as_posix():p for p in candidate.rglob('*') if p.is_file()}
 if set(after)-set(before)!={RECEIPT} or set(before)-set(after):raise ValueError('Unexpected new/deleted paths')
 for name,p in after.items():
  if p.is_symlink():raise ValueError('Symlink in immutable release')
  if name=='source-lock.json':continue
  expected=BRIDGE if name==SCRIPT else receipt_sha if name==RECEIPT else sha(before[name])
  if sha(p)!=expected:raise ValueError('Unexpected drift '+name)
 lock=deepcopy(json.loads((parent/'source-lock.json').read_text()))
 if 'pressKinoReadyV172Admission' in lock:raise ValueError('Duplicate stage admission')
 lock['pressKinoReadyV172Admission']={
  'schema':'fountain.press.kino-original-source-readiness.v172','release':NEW,'predecessor':OLD,
  'sourceOwner':'Fountain-Coach/estate','sourceCommit':GIT,'readerIndexSHA256':INDEX,
  'bridgeSHA256':BRIDGE,'receiptSHA256':receipt_sha,'originalSourceUnchanged':True,
  'originalReaderUnchanged':True,'privateWLANOnly':True,'publicReleaseAuthorized':False
 }
 (candidate/'source-lock.json').write_text(encode(lock))
 print(json.dumps({'release':NEW,'receiptSHA256':receipt_sha,'sourceLockSHA256':sha(candidate/'source-lock.json'),
  'bridgeSHA256':BRIDGE,'indexSHA256':INDEX,'changed':[SCRIPT],'added':[RECEIPT]},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--previous',type=Path,required=True);p.add_argument('--candidate',type=Path,required=True)
 a=p.parse_args();prepare(a.previous,a.candidate)
