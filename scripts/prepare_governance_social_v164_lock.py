#!/usr/bin/env python3
"""Pin v164's complete source-owned social-file inventory to the accepted v163."""
import argparse
import hashlib
import json
from pathlib import Path

RELEASE="shared-shell-20261106-v164-governance-social-b7b1dee"
PREDECESSOR="shared-shell-20261106-v163-governance-inline-hero-cfc2745"
PRIOR_LOCK_SHA="75198bfc5ae03f75d53a5fbc9c1a69b73bde0e5d0f563863d5fe8f73b7989091"
MANIFEST_SHA="07097d3f5d485644b4a28e849d6fbca9e6829daed811f9852efcb417943ce2bc"
RECEIPT_SHA="ea820fd6dd8b20dc888eec5e3494885a159598641df9852b17011c052a8c1244"
PRESS_COMMIT="b7b1deec4d42f249c0cacbb009709486bfc1154d"
ADMISSION={
    "schema":"fountain.press.governance.static-social-wlan-admission.v1",
    "release":RELEASE,"predecessor":PREDECESSOR,
    "sourceOwner":"Fountain-Coach/governance.fountain.coach",
    "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
    "pressOwner":"Fountain-Coach/fountain-press","pressCommit":PRESS_COMMIT,
    "readerOwner":"Fountain-Coach/fountain.coach",
    "readerCommit":"748ba55c38e167e9de90d6ec0572191dbcafa41e",
    "shareManifestSHA256":MANIFEST_SHA,
    "shareReceiptSHA256":RECEIPT_SHA,
    "shareDirectory":"estate/share/governance/",
    "shareSourceChapterCount":160,
    "heroDerivativeCount":68,"firstLandscapePageCount":92,
    "rightsRaisedForPublicUse":False,
    "readerAndSourceUnchanged":True,
    "privateWLANOnly":True,"publicReleaseAuthorized":False,
}
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    for k in ("prior","candidate","output"):
        parser.add_argument("--"+k,required=True)
    a=parser.parse_args()
    if sha(a.prior)!=PRIOR_LOCK_SHA:
        raise ValueError("Unknown inherited v163 source-lock")
    m=Path(a.candidate)/"estate/share/governance/manifest.json"
    r=Path(a.candidate)/"estate/evidence/press-governance-social-v164.json"
    if sha(m)!=MANIFEST_SHA or sha(r)!=RECEIPT_SHA:
        raise ValueError("Unpinned generated v164 social artifacts")
    lock=json.loads(Path(a.prior).read_text())
    if "pressGovernanceSocialV164Admission" in lock:
        raise ValueError("Duplicate social admission")
    lock["pressGovernanceSocialV164Admission"]=ADMISSION
    Path(a.output).write_text(json.dumps(lock,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("GOVERNANCE_SOCIAL_V164_LOCK_SHA256",sha(a.output))
if __name__=="__main__":
    main()
