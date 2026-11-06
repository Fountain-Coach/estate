#!/usr/bin/env python3
"""Exact source-pinned v161 Governance full-book WLAN admission.

No public release or Governance source mutation. The admitted v160 stage is
unchanged, all its keys inherited; no new compositor or public authority.
"""
import argparse
import hashlib
import json
from pathlib import Path

RELEASE="shared-shell-20261106-v161-governance-complete-9dfb0fc"
PREDECESSOR="shared-shell-20261106-v160-press-sound-essay-proof-9d83302"
PREDECESSOR_SHA256="c0b914586f4cfbd3312fe71b8579f2682de20479646252fdc65606d371553324"
SOURCE_COMMIT="03f15306a018eddd85fab491e592d2fdffd61528"
PRESS_COMMIT="9dfb0fcb1234879a84671ee514b631d4f286fe12"
READER_COMMIT="80f09f059db61611925cf273ca0c3cd54cabe4eb"
CHANGED={
    "estate/index.html":"c2b45a1743aac8f504a8011b62b3de76b19762af94f9ad998a3c1fa71063ebfd",
    "estate/assets/linotype/reading-first-app.js":"9fc914956045523522a1a4557721bb22a20fe995cb82f2f8c85c053f1f929f09",
}
ADDED={
    "estate/evidence/press-governance-v161.json":"cc88dab7dc8a9973b306401a47746508af4d4f23b841da003dafafd36fc09fbe",
}
ADMISSION={
    "schema":"fountain.press.governance-complete-wlan-admission.v1",
    "predecessor":PREDECESSOR,
    "release":RELEASE,
    "sourceOwner":"Fountain-Coach/governance.fountain.coach",
    "sourceCommit":SOURCE_COMMIT,
    "readerOwner":"Fountain-Coach/fountain.coach",
    "readerCommit":READER_COMMIT,
    "pressOwner":"Fountain-Coach/fountain-press",
    "pressCommit":PRESS_COMMIT,
    "sourceStatusSHA256":"48d563a4f0e7a03fb9ee27c63e00c0745b4b50364a73e91ba0c86cd4433482b3",
    "sourceChapterCount":160,
    "sourceCurrentCount":72,
    "sourceReferenceCount":88,
    "sourceOriginalFigures":70,
    "existingLinotypeCompositorUnchanged":True,
    "existingReaderAndPrivateMediaPreserved":True,
    "governanceSourceUnchanged":True,
    "privateWLANOnly":True,
    "publicReleaseAuthorized":False,
    "changedFileSHA256":CHANGED,
    "addedFileSHA256":ADDED,
}


def sha(path:Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(prior:Path,candidate:Path,output:Path):
    if sha(prior)!=PREDECESSOR_SHA256:raise ValueError("Unrecognized accepted v160 source lock")
    for rel,digest in {**CHANGED,**ADDED}.items():
        path=candidate/rel
        if not path.is_file() or sha(path)!=digest:raise ValueError("Wrong original Governance candidate "+rel)
    prior_json=json.loads(prior.read_text())
    if "pressGovernanceV161Admission" in prior_json:raise ValueError("Duplicate Governance admission")
    prior_json["pressGovernanceV161Admission"]=ADMISSION
    output.write_text(json.dumps(prior_json,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("GOVERNANCE_V161_SOURCE_LOCK_SHA256",sha(output))
    return sha(output)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for arg in ("prior","candidate","output"):ap.add_argument("--"+arg,required=True)
    opts=ap.parse_args()
    prepare(Path(opts.prior),Path(opts.candidate),Path(opts.output))
