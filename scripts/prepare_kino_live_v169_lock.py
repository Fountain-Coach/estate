#!/usr/bin/env python3
"""Pin live Kino Teatro sources and the exact intended Fountain Press stage delta."""
import json, hashlib, argparse, re
from pathlib import Path
PREV="shared-shell-20261106-v168-kino-complete-9a2fd4f"
NAME="shared-shell-20261106-v169-kino-live-06f63f7"
PREVLOCK="9bf083f2bf813385cc3d3e3095305ef7d7abb4e2d7e8c70172f23f7a06a3f075"
SOURCE="06f63f797c0d5050d0ede0fb9c6ce2ce24f41973"
TEATRO="29211dd2eda1a887da413db1081fc3cb4d471ca0"
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def prepare(prev,candidate):
 if (prev.name,candidate.name)!=(PREV,NAME):raise ValueError("Unexpected release")
 if digest(prev/"source-lock.json")!=PREVLOCK:raise ValueError("Unaccepted source predecessor")
 files={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
 before={p.relative_to(prev).as_posix():p for p in prev.rglob("*") if p.is_file()}
 delta={k:digest(p) for k,p in files.items() if k not in before}
 changed={k:digest(p) for k,p in files.items() if k in before and digest(p)!=digest(before[k]) and k!="source-lock.json"}
 receipt="estate/evidence/press-kino-live-v169.json"
 proof=json.loads((candidate/receipt).read_text())
 if proof["schema"]!="fountain.press.kino-live-csound-stage.v169" or proof["liveSourceCount"]!=4 or proof["recordedComparisonCount"]!=4 or proof["publicReleaseAuthorized"] is not False:raise ValueError("Incorrect source proof")
 if delta!={**proof["added"],receipt:digest(candidate/receipt)} or changed!=proof["changed"]:raise ValueError("Unreviewed source delta")
 if set(changed)!={"estate/index.html"}:raise ValueError("Unexpected reader mutation")
 old=(prev/"estate/index.html").read_text();new=(candidate/"estate/index.html").read_text()
 pat=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
 o=re.findall(pat,old,re.S);n=re.findall(pat,new,re.S)
 if len(o)!=1 or len(n)!=1 or new.replace(n[0],o[0],1)!=old:raise ValueError("Unrelated book mutation")
 if n[0].count("<satzfunk-player compact")!=4 or n[0].count("<iframe ")!=2 or n[0].count("data-source-illustration-id=")!=2:raise ValueError("Lost source evidence")
 lock=json.loads((prev/"source-lock.json").read_text())
 lock["pressKinoLiveV169Admission"]={"schema":"fountain.press.kino-live-csound.v169","release":NAME,"predecessor":PREV,"sourceOwner":"Fountain-Coach/fountain.coach","sourceCommit":SOURCE,"teatroOwner":"Fountain-Coach/teatro.fountain.coach","teatroCommit":TEATRO,"manuscriptSHA256":proof["manuscriptSHA256"],"indexSHA256":changed["estate/index.html"],"readerAppSHA256":proof["readerAppSHA256"],"receiptSHA256":delta[receipt],"liveCsoundAudioWorkletCount":4,"historicalCapturesClaimed":False,"privateWLANOnly":True,"publicReleaseAuthorized":False}
 (candidate/"source-lock.json").write_text(json.dumps(lock,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
 print(json.dumps({"lockSHA256":digest(candidate/"source-lock.json"),"changed":changed,"added":delta,"sourceCommit":SOURCE,"teatroCommit":TEATRO},indent=2))
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--previous",type=Path,required=True)
 p.add_argument("--candidate",type=Path,required=True)
 a=p.parse_args()
 prepare(a.previous,a.candidate)
