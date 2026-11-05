#!/usr/bin/env python3
"""Pin the exact v151 semantic-spread Press engine delta to an admitted v150 source-lock."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
PREVIOUS="shared-shell-20261105-v150-fluid-nested-3ba1b0e"
RELEASE="shared-shell-20261105-v151-semantic-spread-17e32af"
SOURCE_COMMIT="17e32af5b875ec5356ddfa8a9680711d60aaa4eb"
BEFORE_LOCK="f10275f49d5da6837d6572b6508bb51b9752a4a25ffcb08ed4f9835fa986eee0"
KEY="modernPageSemanticSpreadAdmission"
FILES={"estate/assets/linotype/reading-first-press-engine.js":
       "e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a"}
def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def admission()->dict:
    return {
       "schema":"fountain.press.semantic-spread-balance.v1",
       "sourceOwner":"Fountain-Coach/fountain.coach",
       "sourceCommit":SOURCE_COMMIT,
       "sourcePath":"scenarios/reading-first-20261101/reading-first-press-engine.js",
       "predecessor":PREVIOUS,
       "release":RELEASE,
       "stageOnly":True,
       "publicReleased":False,
       "fountainStoreAdmitted":False,
       "sameReaderShell":True,
       "unchangedBookSources":True,
       "unchangedOriginalImages":True,
       "unchangedPrivateVoiceAuditions":True,
       "rightLeafRetainsProseReserve":True,
       "leftLeafMayCarryPictureAcrossGutter":True,
       "headingAttachedToReadableOpening":True,
       "minimumSecondaryImageScale":0.72,
       "compactReaderProvenIdentical":True,
       "fileSHA256":FILES
    }
def build(before:Path,out:Path)->None:
    original=before.read_bytes()
    if sha(original)!=BEFORE_LOCK:raise ValueError("Not exact source-admitted v150 predecessor")
    obj=json.loads(original)
    if KEY in obj or "modernPageFluidMeasureAdmission" not in obj:raise ValueError("Unrecognized lineage")
    obj[KEY]=admission()
    content=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    if out.exists():raise ValueError("Refuse overwriting candidate source-lock")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(content)
    print(json.dumps({"predecessor":PREVIOUS,"release":RELEASE,"source":SOURCE_COMMIT,
     "newSourceLockSHA256":sha(content),"changedFiles":FILES},indent=2))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--predecessor-lock",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    opts=parser.parse_args()
    build(opts.predecessor_lock,opts.out)
