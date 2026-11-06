#!/usr/bin/env python3
"""Author the bounded v162 Governance link-fidelity stage admission.
Only v161's protected Reader HTML changes; all other estate bytes are retained.
"""
from pathlib import Path
import argparse
import hashlib
import json

RELEASE="shared-shell-20261106-v162-governance-link-fidelity-4d6046b"
PREDECESSOR="shared-shell-20261106-v161-governance-complete-9dfb0fc"
PRIOR_LOCK_SHA="c852c8ea2d3e89a8c1edfa48aa7a69c8a3c1ac638dc81e2d3b0dd8a167fe983d"
CHANGED={"estate/index.html":"35ade43f8c38ba56773e1130505d0262e11aec87b716f7d07614eebb13d7156c"}
ADDED={"estate/evidence/press-governance-v162.json":"d69c9208dd03dce8b910271a75c4db664d8481200376f911243d58a0adb00343"}
ADMISSION={
    "schema":"fountain.press.governance-link-fidelity-wlan-admission.v1",
    "predecessor":PREDECESSOR,
    "release":RELEASE,
    "sourceOwner":"Fountain-Coach/governance.fountain.coach",
    "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
    "pressOwner":"Fountain-Coach/fountain-press",
    "pressCommit":"4d6046b6fd2438e8e7f0bfe41f6469916922179d",
    "readerOwner":"Fountain-Coach/fountain.coach",
    "readerCommit":"82efaddeec7a149774e4611fca908354c1ed74a0",
    "chapterCount":160,
    "statusCurrent":72,
    "statusReference":88,
    "originalLinksPreserved":1132,
    "originalFiguresPreserved":70,
    "priorLinotypeEngineUnchanged":True,
    "governanceCanonicalSourceUnmodified":True,
    "privateWLANOnly":True,
    "publicReleaseAuthorized":False,
    "changedFileSHA256":CHANGED,
    "addedFileSHA256":ADDED,
}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for name in ("prior","candidate","output"):ap.add_argument("--"+name,required=True)
    o=ap.parse_args()
    if sha(o.prior)!=PRIOR_LOCK_SHA:raise ValueError("Unrecognized v161 source lock")
    for rel,exp in {**CHANGED,**ADDED}.items():
        file=Path(o.candidate)/rel
        if not file.is_file() or sha(file)!=exp:raise ValueError("Wrong v162 artifact "+rel)
    lock=json.loads(Path(o.prior).read_text())
    if "pressGovernanceV162Admission" in lock:raise ValueError("Duplicate source lock admission")
    lock["pressGovernanceV162Admission"]=ADMISSION
    Path(o.output).write_text(json.dumps(lock,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("GOVERNANCE_V162_LOCK",sha(o.output))
