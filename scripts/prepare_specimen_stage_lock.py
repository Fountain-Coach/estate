#!/usr/bin/env python3
"""Prepare the one bounded, immutable v148 private Reader source-lock.

This does not install/activate a release or override ReaderProvenanceGate.
The new essay is a revised source, not an unmodified edition of the 13-page PDF.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

PREDECESSOR = "shared-shell-20261105-v147-self-out-loud-c884a3e"
RELEASE = "shared-shell-20261105-v148-specimen-boundary-a9575ba"
SOURCE_OWNER = "Fountain-Coach/fountain.coach"
SOURCE_COMMIT = "a9575ba976917433baf0cc67940b5941e4c1de96"
SOURCE_PATH = "site/essays/what-makes-a-page-modern/combined-essay.md"
SOURCE_SHA256 = "8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6"
OLDER_PDF_SHA256 = "2baaab0012e825b49f04e7a760b64efa52c95dc09deab7117de790f6c6e14bad"
PREDECESSOR_LOCK_SHA256 = "75b8407fbc9762718df82560f5a7b2d4bb433dd6f52881c663fc115530453ea8"
ROOT_SHA256 = "532dbdf6603fb1300a974418130c50cbc17636262d9dcf7c0a802c3aabfdd81c"
ADMISSION_KEY = "modernPageTypographicSpecimenAdmission"

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def build(before: Path, result: Path) -> str:
    original = before.read_bytes()
    if sha(original) != PREDECESSOR_LOCK_SHA256:
        raise ValueError("Unexpected v147 source-lock; refuse revision")
    data = json.loads(original)
    if ADMISSION_KEY in data or "modernPageSelfOutLoudAdmission" not in data:
        raise ValueError("Unrecognized inherited Reader lock")
    data[ADMISSION_KEY] = {
        "schema": "fountain.press.typographic-specimen-source-anchor.v1",
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
        "readerRuntimeUnchanged": True,
        "originalIllustrationsUnchanged": True,
        "typographicSpecimensFramed": 2,
        "duplicateNarrativeSpecimensRemoved": 2,
        "authoredInlineFigureAnchors": 11,
        "fileSHA256": {"estate/index.html": ROOT_SHA256}
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
