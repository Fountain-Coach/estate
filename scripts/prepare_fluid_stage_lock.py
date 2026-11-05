#!/usr/bin/env python3
"""Add one pinned, additive v150 Reader provenance admission to v149 source-lock."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
PREVIOUS="shared-shell-20261105-v149-nested-specimen-ce0c1cd"
RELEASE="shared-shell-20261105-v150-fluid-nested-3ba1b0e"
SOURCE_COMMIT="3ba1b0e826efcec947e243100c2925ad78d2953e"
BEFORE_LOCK="935275ea1f3971a4307d6df445c7c925e005e8ce3be50ea0d25fa9dd309932e2"
KEY="modernPageFluidMeasureAdmission"
FILES={
    "estate/assets/linotype/reading-first-press-engine.js":"52f30f9fd36f3f1ccb24bd833b14f91289d270df394f8418a77cc672ee7c5342",
    "estate/assets/linotype/reading-first-press-frame.css":"8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6"
}
def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def admission()->dict:
    return {
       "schema":"fountain.press.fluid-parent-and-nested-flow.v1",
       "sourceOwner":"Fountain-Coach/fountain.coach",
       "sourceCommit":SOURCE_COMMIT,
       "sourcePaths":[
          "scenarios/reading-first-20261101/reading-first-press-engine.js",
          "scenarios/reading-first-20261101/reading-first-press-frame.css"
       ],
       "predecessor":PREVIOUS,
       "release":RELEASE,
       "stageOnly":True,
       "publicReleased":False,
       "fountainStoreAdmitted":False,
       "sameReaderShell":True,
       "unchangedBookSources":True,
       "proportionalMeasuredFolio":True,
       "continuationUsesRemainingFolio":True,
       "testedAt":[[390,690],[390,844],[820,1120],[1024,1366],[1200,860],[1200,1500]],
       "fileSHA256":FILES
    }
def main(before:Path,out:Path)->None:
    old=before.read_bytes()
    if sha(old)!=BEFORE_LOCK:raise ValueError("Unaccepted v149 stage source-lock")
    data=json.loads(old)
    if KEY in data or "modernPageNestedMeasureAdmission" not in data:
        raise ValueError("Unrecognized inherited source identity")
    data[KEY]=admission()
    buf=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode()
    if out.exists():raise ValueError("Refuse to overwrite locked receipt")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(buf)
    print(json.dumps({"release":RELEASE,"predecessor":PREVIOUS,"sourceCommit":SOURCE_COMMIT,
        "lockSHA256":sha(buf),"files":FILES},indent=2))
if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--predecessor-lock",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    opts=a.parse_args();main(opts.predecessor_lock,opts.out)
