#!/usr/bin/env python3
"""Prepare one exact, immutable, owner-WLAN-only editorial release after v175.

No DNS, public publishing, credential mutation, or live symlink changes.
The 93 additive editorial files are SHA-256 pinned to a source-bound Press
build. Existing stage files are copied byte-identically, not rewritten.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
PREVIOUS="shared-shell-20261108-v175-governance161-shell-1486f09"
RELEASE="shared-shell-20261109-v176-four-domain-c265c57"
SOURCE="c265c5783e28bd2b91685f96f18ac03b6718aeda"
OVERLAY_SHA="69e68e01d732585c4576a81f952126c00aaa1a6366b6d83f8d8f81ae45134aa2"
MAP_SHA="dd302ff4c5314078183d4e9c3e0a7f3949b9ce026591c0de4b0a7fb001d0d6ff"
LOCK_V175="d546d92aab66ebdd2615d6e24660461ab759866d6f0f19de290c40f0559edf1a"
REVIEW="review-20261109"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def files(root):
    return {p.relative_to(root).as_posix():p for p in root.rglob("*") if p.is_file()}

def prepare():
    parent=STAGE/"releases"
    prev=parent/PREVIOUS
    if not prev.is_dir() or sha(prev/"source-lock.json")!=LOCK_V175:
        raise RuntimeError("Refuse unfamiliar current v175 source lock")
    if (STAGE/"current").resolve()!=prev.resolve():
        raise RuntimeError("Refuse changed stage predecessor")
    overlay=STAGE/"candidates"/"four-domain-v176-c265c57"
    manifestfile=STAGE/"candidates"/"four-domain-v176-c265c57-overlay-manifest.json"
    if sha(manifestfile)!=OVERLAY_SHA:
        raise RuntimeError("Unpinned source-derived overlay manifest")
    data=json.loads(manifestfile.read_text())
    assert data["sourceRevision"]==SOURCE
    assert data["domainMapSHA256"]==MAP_SHA
    assert len(data["files"])==93
    assert all(path.startswith(REVIEW+"/") for path in data["files"])
    assert all(".." not in Path(path).parts for path in data["files"])
    before=files(prev)
    if set(data["files"]) & set(before):
        raise RuntimeError("Refuse to overwrite pre-existing staging source")
    actual=files(overlay)
    if set(actual)!=set(data["files"]):
        raise RuntimeError("Unexpected overlay inventory")
    for name,digest in data["files"].items():
        path=actual[name]
        if path.is_symlink() or sha(path)!=digest:
            raise RuntimeError("Altered source overlay: "+name)
    destination=parent/RELEASE
    temporary=parent/("."+RELEASE+".unadmitted")
    if destination.exists() or temporary.exists():
        raise RuntimeError("Refuse release overwrite; inspect existing artifact")
    temporary.mkdir(mode=0o755)
    try:
        subprocess.run(["cp","-a","--reflink=auto",str(prev)+"/.",str(temporary)+"/"],check=True)
        for name,path in actual.items():
            target=temporary/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,target)
        document=temporary/REVIEW/"overlay-manifest.json"
        shutil.copy2(manifestfile,document)
        admission={
            "schema":"fountain.press.four-domain.owner-wlan-review.v176",
            "sourceOwner":"Fountain-Coach/fountain-press",
            "sourceRevision":SOURCE,
            "release":RELEASE,
            "predecessor":PREVIOUS,
            "predecessorLockSHA256":LOCK_V175,
            "overlayManifestSHA256":OVERLAY_SHA,
            "domainMapSHA256":MAP_SHA,
            "reviewPrefix":REVIEW+"/",
            "overlayCount":len(data["files"]),
            "privateWLANOnly":True,
            "publicReleaseAuthorized":False,
            "productionEffect":False,
            "incumbentFilesUnchanged":True,
            "ownerOperationControlsDisabled":True,
        }
        old=json.loads((prev/"source-lock.json").read_text())
        if "fourDomainV176Admission" in old:
            raise RuntimeError("Predecessor already includes new admission")
        old["fourDomainV176Admission"]=admission
        lock=temporary/"source-lock.json"
        # Atomic replacement, not an in-place write to a possibly reflinked file.
        next_lock=temporary/".next-source-lock.json"
        next_lock.write_text(json.dumps(old,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
        next_lock.replace(lock)
        candidate=files(temporary)
        expected=set(before)|set(actual)|{REVIEW+"/overlay-manifest.json"}
        if set(candidate)!=expected:
            raise RuntimeError("Candidate file inventory differs from admitted increment")
        for name,path in before.items():
            if name!="source-lock.json" and sha(candidate[name])!=sha(path):
                raise RuntimeError("Inherited stage file changed: "+name)
        if sha(candidate[REVIEW+"/overlay-manifest.json"])!=OVERLAY_SHA:
            raise RuntimeError("Missing manifest in actual candidate")
        for name,digest in data["files"].items():
            if sha(candidate[name])!=digest:raise RuntimeError("Bad prepared byte: "+name)
        newsha=sha(lock)
        temporary.rename(destination)
    except BaseException:
        shutil.rmtree(temporary)
        raise
    evidence={
        "release":RELEASE,"predecessor":PREVIOUS,
        "accessSourceRevision":SOURCE,
        "candidateSourceLockSHA256":newsha,
        "predecessorSourceLockSHA256":LOCK_V175,
        "overlayManifestSHA256":OVERLAY_SHA,
        "domainMapSHA256":MAP_SHA,
        "overlayFiles":93,"incumbentFiles":len(before),
        "candidateFiles":len(expected),
        "activated":False,"productionEffect":False,
    }
    receipt=STAGE/"candidates"/"four-domain-v176-c265c57-preparation.json"
    receipt.write_text(json.dumps(evidence,indent=2)+"\n")
    print(json.dumps(evidence,indent=2))

if __name__=="__main__":prepare()
