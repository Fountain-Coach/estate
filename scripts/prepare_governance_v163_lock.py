#!/usr/bin/env python3
"""Source-pin the v163 original Governance illustration source-position correction."""
from pathlib import Path
import argparse,hashlib,json

RELEASE="shared-shell-20261106-v163-governance-inline-hero-cfc2745"
PREDECESSOR="shared-shell-20261106-v162-governance-link-fidelity-4d6046b"
PRIOR_SHA="4fbc867a0cc7e50211e2568402341682fd9110fce41c91f8ce30e9f688e4f99e"
CHANGED={"estate/index.html":"4c9298785fa505f8971429be9cf42b10682acc950b534194415193c87472e757"}
ADDED={"estate/evidence/press-governance-v163.json":"8f0125958684dac0a9c2bf1c006f5e39b92e66b95ac43012da62c213745d871e"}
ADMISSION={
  "schema":"fountain.press.governance-inline-hero-wlan-admission.v1",
  "release":RELEASE,"predecessor":PREDECESSOR,
  "sourceOwner":"Fountain-Coach/governance.fountain.coach",
  "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
  "pressOwner":"Fountain-Coach/fountain-press",
  "pressCommit":"cfc2745772c8d3ea306f86e1cae8ac53f8805a9c",
  "readerOwner":"Fountain-Coach/fountain.coach",
  "readerCommit":"748ba55c38e167e9de90d6ec0572191dbcafa41e",
  "chapterCount":160,"statusCurrent":72,"statusReference":88,
  "sourceFigureCount":70,"sourceHeroCount":67,"sourceInlineCount":3,
  "allOriginalLinksUnchanged":True,"existingLinotypeEngineUnchanged":True,
  "privateWLANOnly":True,"publicReleaseAuthorized":False,
  "changedFileSHA256":CHANGED,"addedFileSHA256":ADDED,
}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
if __name__=="__main__":
 p=argparse.ArgumentParser()
 for name in ("prior","candidate","output"):p.add_argument("--"+name,required=True)
 a=p.parse_args()
 if sha(a.prior)!=PRIOR_SHA:raise ValueError("Wrong accepted v162 source-lock")
 for rel,exp in {**CHANGED,**ADDED}.items():
  f=Path(a.candidate)/rel
  if not f.is_file() or sha(f)!=exp:raise ValueError("Unrecognized v163 file "+rel)
 lock=json.loads(Path(a.prior).read_text())
 if "pressGovernanceV163Admission" in lock:raise ValueError("Duplicate admission")
 lock["pressGovernanceV163Admission"]=ADMISSION
 Path(a.output).write_text(json.dumps(lock,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
 print("GOVERNANCE_V163_SOURCE_LOCK",sha(a.output))
