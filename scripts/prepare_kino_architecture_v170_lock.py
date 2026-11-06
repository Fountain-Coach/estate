#!/usr/bin/env python3
"""Admit only the preserved Kino architectural score in the existing Press folio."""
from pathlib import Path
from copy import deepcopy
import json, hashlib, re, argparse
PREV='shared-shell-20261106-v169-kino-live-06f63f7'
NEXT='shared-shell-20261106-v170-kino-visual-263ac6c'
PARENT_LOCK='00e05c0bfa1aab1cc45d79fa5b77ccbece6c00116e9b6dd1beecc1121edb5089'
SITE_COMMIT='263ac6ca34013a6969be80e6f0d91d71899c2eea'
TEATRO_COMMIT='255b98d4c277e48bbc75f538af52a64953c0a3f7'
SRC='0f74f0c0eaccf65e6bbc4a7fed2879c3d92ff70c27c3bb66ae58c3097196319f'
SVG='789ef2af5131529e1f1ed43ff70ae7dce3ea715e91107304fe00632cf4a3677d'
CHANGED={
 'estate/index.html':'75fb9c8c160d6526447b3818225d44ab33acd0caa0fd8e676352ca539ce939d4',
 'teatro/interludes/kino/live-csound/index.html':'6db7c0e4ef4758fdf5fa53af144c27329cbfbcbc6d7a5f35c5b24a7ee59aa816',
 'teatro/interludes/kino/live-csound/live.mjs':'c2135dcec0078c5069aa00b248ecb2ca363c2d1667f021b994b9b26ef6797762'
}
RECEIPT='estate/evidence/press-kino-architecture-v170.json'
RECEIPT_SHA='0ee1eec0a5ada3bff1433cfb505d108dc0c8678e32977e6b92ddea0cbae09ba9'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(previous,candidate):
 if (previous.name,candidate.name)!=(PREV,NEXT):raise ValueError('Unrecognized predecessor/candidate')
 if sha(previous/'source-lock.json')!=PARENT_LOCK:raise ValueError('Wrong predecessor source lock')
 prior={p.relative_to(previous).as_posix():p for p in previous.rglob('*') if p.is_file()}
 current={p.relative_to(candidate).as_posix():p for p in candidate.rglob('*') if p.is_file()}
 if set(current)-set(prior)!={RECEIPT} or set(prior)-set(current):raise ValueError('Unknown added or deleted file')
 for name,path in current.items():
  if path.is_symlink():raise ValueError('Unexpected symlink')
  if name=='source-lock.json':continue
  expected=CHANGED.get(name,RECEIPT_SHA if name==RECEIPT else sha(prior[name]))
  if sha(path)!=expected:raise ValueError('Unreviewed content '+name)
 proof=json.loads((candidate/RECEIPT).read_text())
 if (proof['schema']!='fountain.press.kino-architectural-live-score.v170'
     or proof['manuscriptSHA256']!=SRC
     or proof['sourceKinoSVGsha256']!=SVG
     or proof['changed']!=CHANGED
     or proof['preservedRecordedAuditions']!=4
     or proof['preservedLiveCsoundInstruments']!=4
     or proof['existingReaderUnchanged'] is not True
     or proof['existingArtworkPreserved'] is not True
     or proof['privateWLANOnly'] is not True
     or proof['publicReleaseAuthorized'] is not False):
  raise ValueError('Wrong editorial source, geometry or rights')
 pat=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
 old=(previous/'estate/index.html').read_text()
 new=(candidate/'estate/index.html').read_text()
 a=re.findall(pat,old,re.S);b=re.findall(pat,new,re.S)
 if len(a)!=1 or len(b)!=1 or new.replace(b[0],a[0],1)!=old:raise ValueError('Other book content mutated')
 if (b[0].count('<satzfunk-player compact')!=4 or
     b[0].count('<iframe ')!=2 or
     b[0].count('data-source-illustration-id=')!=2 or
     b[0].count('data-original-kino-svg-sha256="'+SVG+'"')!=2 or
     'data-source-sha256="'+SRC+'"' not in b[0]):
  raise ValueError('Four recordings, two source figures or Kino scores missing')
 score=(candidate/'teatro/interludes/kino/live-csound/index.html').read_text()
 if ('Original Teatro Kino After Dark architectural SVG SHA-256 '+SVG not in score
     or score.count('class="memory-window"')!=16
     or score.count('data-play=')!=4):
  raise ValueError('Not the original Kino architecture')
 lock=deepcopy(json.loads((previous/'source-lock.json').read_text()))
 lock['pressKinoArchitectureV170Admission']={
  'schema':'fountain.press.kino-architecture-score.v170',
  'release':NEXT,'predecessor':PREV,
  'sourceOwner':'Fountain-Coach/fountain.coach','sourceCommit':SITE_COMMIT,
  'teatroOwner':'Fountain-Coach/teatro.fountain.coach','teatroCommit':TEATRO_COMMIT,
  'manuscriptSHA256':SRC,'sourceKinoSVGsha256':SVG,
  'readerIndexSHA256':CHANGED['estate/index.html'],
  'receiptSHA256':RECEIPT_SHA,'existingReaderUnchanged':True,
  'privateWLANOnly':True,'publicReleaseAuthorized':False
 }
 (candidate/'source-lock.json').write_text(json.dumps(lock,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'release':NEXT,'sourceLockSHA256':sha(candidate/'source-lock.json'),'changed':CHANGED,'receiptSHA256':RECEIPT_SHA},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--previous',type=Path,required=True)
 p.add_argument('--candidate',type=Path,required=True)
 a=p.parse_args();prepare(a.previous,a.candidate)
