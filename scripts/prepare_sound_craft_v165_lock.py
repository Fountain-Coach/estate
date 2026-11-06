#!/usr/bin/env python3
"""Prepare the exact v164 -> v165 private Sound-Craft A/B stage addition.

Run on the owner WLAN staging machine *after* copying the immutable v164
release into a new sibling and overlaying only source-owner admitted files.
Never activate, publish or change the current symlink in this preparer.
"""
from pathlib import Path
import argparse,hashlib,json,re
from copy import deepcopy

V164="shared-shell-20261106-v164-governance-social-b7b1dee"
V165="shared-shell-20261106-v165-satzfunk-csound-ab-eb45a85"
V164_LOCK_SHA="61703c3eb1271dd19461b6f79d09df21634efadfc1737d1c01735304e59b3771"
SITE_SHA="eb45a85d7485e7e8e4b093bc259e4f6c8075ec6d"
TEATRO_SHA="1d8f6345ee0cb9fc7b8802cf2f3e0cdd6fc14b03"
SOURCE_SHA="b1da1f4c3651e84eb55e104d02d311ebd047278a046f427563600e091348ea44"
SCORE_SHA="21ae0eda6621d1b2ff90a1baaa792def576d7399da62cc90609022d854abda49"
OUTPUT_INDEX_SHA="5a2a8c084d806c515890e276be445fe34c21ca0243948d8cc088bcc70e65ab97"
OUTPUT_APP_SHA="46876ca7b54c5f26df2372f1ec037871e61f6773a406ff41ec32a634337b7831"
ORIGINAL_INDEX_SHA="4c9298785fa505f8971429be9cf42b10682acc950b534194415193c87472e757"
ORIGINAL_APP_SHA="9fc914956045523522a1a4557721bb22a20fe995cb82f2f8c85c053f1f929f09"
MODIFIED={"estate/index.html":OUTPUT_INDEX_SHA,
          "estate/assets/linotype/reading-first-app.js":OUTPUT_APP_SHA}
ADDITIONS={
 "estate/media/kino/sound-craft/source-manifest.json":"712488ba5ae545692a7336f82a0b126b5165b85d62fcdf1d7ca91929c17786b7",
 "estate/media/kino/sound-craft/edition.json":"20ff8f8acfb30efe189ec6e9981fffd3c8297a80cd4ad08a34523c68956b9e0f",
 "estate/media/kino/sound-craft/a-literal.csd":"1f21a92ded2ceeaa699111254987c1d411bb740ebebfc140ef1b919ca9738ab7",
 "estate/media/kino/sound-craft/b-directed.csd":"928656e3a6e8a6a2edf7ea9fad55b844afca1b27bd4af94140a63b3b5850a202",
 "estate/media/kino/sound-craft/a-literal.m4a":"f8db7d1cee00b6e346fb400567c2868e99a97cf4c51007b3fe47fe542dbde427",
 "estate/media/kino/sound-craft/b-directed.m4a":"5413a93ba9a1c471e2178f93f099e412b464f2e25447b8a7f4ebb960b298d94b"
}
RECEIPT_PATH="estate/evidence/press-sound-csound-v165.json"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def assert_valid(parent,child):
    if parent.name!=V164 or child.name!=V165:
        raise ValueError("Unexpected release source/target name")
    if not parent.is_dir() or not child.is_dir() or parent.samefile(child):
        raise ValueError("Not two distinct immutable release directories")
    if sha(parent/"source-lock.json")!=V164_LOCK_SHA:
        raise ValueError("Wrong pinned v164 source-lock")
    if (sha(parent/"estate/index.html")!=ORIGINAL_INDEX_SHA or
        sha(parent/"estate/assets/linotype/reading-first-app.js")!=ORIGINAL_APP_SHA):
        raise ValueError("Unverified existing Reader v164")
    for rel,h in {**MODIFIED,**ADDITIONS}.items():
        file=child/rel
        if not file.is_file() or file.is_symlink() or sha(file)!=h:
            raise ValueError("Expected source-owned changed asset not exact: "+rel)
    old={p.relative_to(parent).as_posix():p for p in parent.rglob("*") if p.is_file()}
    new={p.relative_to(child).as_posix():p for p in child.rglob("*") if p.is_file()}
    extras=set(new)-set(old)
    if extras!=set(ADDITIONS) or set(old)-set(new):
        raise ValueError("Unexpected stage artifact additions/removals: "+str(sorted(extras-set(ADDITIONS))))
    for rel,file in new.items():
        if file.is_symlink():raise ValueError("Symlink in new release: "+rel)
        if rel in ADDITIONS or rel in MODIFIED or rel=="source-lock.json":continue
        if sha(file)!=sha(old[rel]):raise ValueError("Unrelated released work changed: "+rel)
    m=json.loads((child/"estate/media/kino/sound-craft/source-manifest.json").read_text())
    e=json.loads((child/"estate/media/kino/sound-craft/edition.json").read_text())
    if (m.get("sourceScoreSHA256")!=SCORE_SHA or
        m.get("noOutsideRecordings") is not True or
        len(m.get("files",[]))!=2 or
        m.get("noNativeScenarioAdmissionClaim") is not True or
        e.get("schema")!="satzfunk.recorded-essay-rehearsal.v1" or
        e.get("scoreSHA256")!=SCORE_SHA or
        e.get("mediaBasePrefix")!="/estate/" or
        len(e.get("tracks",[]))!=2 or
        any(t.get("publicReleaseAuthorized") is not False or
            t.get("privateRehearsalAuthorized") is not True or
            t.get("sourceSHA256")!=SCORE_SHA for t in e["tracks"])):
        raise ValueError("False Csound/Satzfunk custody or public grant")
    previous=(parent/"estate/index.html").read_text()
    revised=(child/"estate/index.html").read_text()
    reg=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    a=re.findall(reg,previous,re.S);b=re.findall(reg,revised,re.S)
    if len(a)!=1 or len(b)!=1 or revised.replace(b[0],a[0],1)!=previous:
        raise ValueError("Edited another book, Reader shell, or source volume")
    if ("data-editorial-state=\"proof-revision\"" not in b[0] or
        'data-source-sha256="'+SOURCE_SHA+'"' not in b[0] or
        b[0].count("<satzfunk-player compact")!=2 or
        'It is ready when the work can answer for it.' not in b[0] or
        "sing-plain-compare" in b[0]):
        raise ValueError("Wrong approved essay/audio source")
    original_app=(parent/"estate/assets/linotype/reading-first-app.js").read_text()
    updated_app=(child/"estate/assets/linotype/reading-first-app.js").read_text()
    if (updated_app.count("function syncSatzfunkPlayer(){")!=1 or
        updated_app.count("const soundCraftPromise=")!=1 or
        original_app.count("const soundEditionPromise=")!=1 or
        updated_app.count("const soundEditionPromise=")!=1 or
        'private-wlan-rehearsal' not in updated_app or
        'if(volume===proofVolume)' not in updated_app):
        raise ValueError("Lost existing live SatzfunkPlayer binding")
    if RECEIPT_PATH in old or RECEIPT_PATH in new:
        raise ValueError("Non-fresh receipt path")
    return old,new

def prepare(previous,candidate):
    assert_valid(previous,candidate)
    receipt={
      "schema":"fountain.press.satzfunk-csound-essay-stage.v165",
      "release":V165,"predecessor":V164,
      "sourceOwner":"Fountain-Coach/fountain.coach","sourceCommit":SITE_SHA,
      "teatroOwner":"Fountain-Coach/teatro.fountain.coach","teatroCommit":TEATRO_SHA,
      "readerOwner":"Fountain-Coach/fountain.coach",
      "originalReaderIndexSHA256":ORIGINAL_INDEX_SHA,
      "originalReaderAppSHA256":ORIGINAL_APP_SHA,
      "editorialSourceSHA256":SOURCE_SHA,
      "csoundSourceScoreSHA256":SCORE_SHA,
      "twoSourceBoundRealCsoundPatches":True,
      "player":"existing SatzfunkMediaElement with private-WLAN rehearsal grant",
      "artisticallyAccepted":False,"nativeCsoundScenarioAdmitted":False,
      "privateWLANOnly":True,"publicReleaseAuthorized":False,"iPadNativeAccepted":False,
      "sourceFileCount":len(ADDITIONS)+len(MODIFIED),
      "changedSHA256":{**MODIFIED,**ADDITIONS}
    }
    receipt_bytes=(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    path=candidate/RECEIPT_PATH
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(receipt_bytes)
    prev_lock=json.loads((previous/"source-lock.json").read_text())
    lock=deepcopy(prev_lock)
    admission={
      "schema":"fountain.press.satzfunk-csound-editorial-audition.v1",
      "release":V165,"predecessor":V164,
      "sourceOwner":receipt["sourceOwner"],"sourceCommit":SITE_SHA,
      "teatroOwner":receipt["teatroOwner"],"teatroCommit":TEATRO_SHA,
      "editorialSourceSHA256":SOURCE_SHA,
      "csoundScoreSHA256":SCORE_SHA,
      "readerIndexSHA256":OUTPUT_INDEX_SHA,
      "readerAppSHA256":OUTPUT_APP_SHA,
      "receiptSHA256":sha(path),
      "privateWLANOnly":True,"publicReleaseAuthorized":False,
      "otherWorksPreserved":True,"nativeCsoundScenarioAdmissionClaimed":False
    }
    if "pressSoundCsoundV165Admission" in lock:raise ValueError("Repeated admission")
    lock["pressSoundCsoundV165Admission"]=admission
    lock_path=candidate/"source-lock.json"
    lock_path.write_text(json.dumps(lock,ensure_ascii=False,indent=2)+"\n")
    expected=set(ADDITIONS)|set(MODIFIED)|{RECEIPT_PATH}
    print(json.dumps({
       "state":"V165_SOURCE_LOCK_PREPARED_NOT_ACTIVE",
       "previous":V164,"candidate":V165,"files":len(expected),
       "sourceLockSHA256":sha(lock_path),
       "receiptSHA256":sha(path),"receiptPath":RECEIPT_PATH,
       "sourceScoreSHA256":SCORE_SHA
    },indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--previous",type=Path,required=True)
    p.add_argument("--candidate",type=Path,required=True)
    a=p.parse_args();prepare(a.previous,a.candidate)
