#!/usr/bin/env python3
"""Prepare the one bounded, immutable v149 native nested-type source-lock.

This does not install/activate a release or override ReaderProvenanceGate.
The new essay is a revised source, not an unmodified edition of the 13-page PDF.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

PREDECESSOR = "shared-shell-20261105-v148-specimen-boundary-a9575ba"
RELEASE = "shared-shell-20261105-v149-nested-specimen-ce0c1cd"
SOURCE_OWNER = "Fountain-Coach/fountain.coach"
SOURCE_COMMIT = "ce0c1cd704664027d94d6dd4c196b9c06e037e38"
SOURCE_PATH = "site/essays/what-makes-a-page-modern/combined-essay.md"
SOURCE_SHA256 = "8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6"
OLDER_PDF_SHA256 = "2baaab0012e825b49f04e7a760b64efa52c95dc09deab7117de790f6c6e14bad"
PREDECESSOR_LOCK_SHA256 = "90d23ed381ece45f54d9621ca7341e204d5967738f1f48b3af2d8eab42483e1c"
ROOT_SHA256 = "8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f"
ADMISSION_KEY = "modernPageNestedMeasureAdmission"

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def build(before: Path, result: Path) -> str:
    original = before.read_bytes()
    if sha(original) != PREDECESSOR_LOCK_SHA256:
        raise ValueError("Unexpected v148 source-lock; refuse revision")
    data = json.loads(original)
    if ADMISSION_KEY in data or "modernPageTypographicSpecimenAdmission" not in data:
        raise ValueError("Unrecognized inherited Reader lock")
    data[ADMISSION_KEY] = {
        "schema": "fountain.press.native-nested-type-measure.v1",
        "sourceOwner": SOURCE_OWNER,
        "sourceCommit": SOURCE_COMMIT,
        "sourcePath": SOURCE_PATH,
        "sourceSHA256": SOURCE_SHA256,
        "earlierDruckfahnePDFSHA256": OLDER_PDF_SHA256,
        "predecessor": PREDECESSOR,
        "release": RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchanged": False,
        "existingReaderPreserved": True,
        "pressCompositorSourceChanged": True,
        "specimenSourcePath": "site/essays/what-makes-a-page-modern/specimen-source.txt",
        "specimenSourceSHA256": "693ca56d01757d03d2210234def136256cd04145efce95fc1fc205cf15c6658a",
        "nestedSettings": 2,
        "fixedSVGSpecimensRemovedFromView": 2,
        "historicalSVGAssetsPreserved": True,
        "originalIllustrationsUnchanged": True,
        "typographicSpecimensFramed": 2,
        "duplicateNarrativeSpecimensRemoved": 2,
        "authoredInlineFigureAnchors": 11,
        "fileSHA256": {
            "estate/index.html": ROOT_SHA256,
            "estate/assets/linotype/reading-first-press-engine.js": "67a3c842c92e86839a35cbee44c533d143f893eda954d750c0eddfffcad64058",
            "estate/assets/linotype/reading-first-press-frame.css": "f7a85b7e573655bee124dc4218c0cb9ecdc4300b433b5ab0237e734507a03c03"
        }
    }
    encoded=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    result.parent.mkdir(parents=True,exist_ok=True)
    if result.exists():
        raise ValueError("Refuse to overwrite an existing receipt")
    result.write_bytes(encoded)
    print(json.dumps({"release":RELEASE,"predecessor":PREDECESSOR,
                      "sourceCommit":SOURCE_COMMIT,"sourceSHA256":SOURCE_SHA256,
                      "rootSHA256":ROOT_SHA256,"sourceLockSHA256":sha(encoded)},
                      indent=2))
    return sha(encoded)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--predecessor-lock",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    build(a.predecessor_lock,a.out)
