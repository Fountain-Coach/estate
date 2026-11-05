#!/usr/bin/env python3
"""Prepare the one bounded, immutable v147 private Reader source-lock.

This does not install/activate a release or override ReaderProvenanceGate.
The new essay is a revised source, not an unmodified edition of the 13-page PDF.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

PREDECESSOR = "shared-shell-20261104-v146-vergil-qwen-listening-page"
RELEASE = "shared-shell-20261105-v147-self-out-loud-c884a3e"
SOURCE_OWNER = "Fountain-Coach/fountain.coach"
SOURCE_COMMIT = "c884a3e3bd04a2269212b7c5a7dadd6ef92e900f"
SOURCE_PATH = "site/essays/what-makes-a-page-modern/combined-essay.md"
SOURCE_SHA256 = "4b3c0c2b2f02d707d0c88d3c4f045c8119d05707709512a832e995c648edf272"
OLDER_PDF_SHA256 = "2baaab0012e825b49f04e7a760b64efa52c95dc09deab7117de790f6c6e14bad"
PREDECESSOR_LOCK_SHA256 = "9ffddfa9fdd5bf853c973de266bcdc71404f954342c8931ca6e53e82f0da9396"
ROOT_SHA256 = "11cd731753769f5feacd2f91dc2ba1fc8c0e914d5d107b00f9c98ad58eff3c2c"
ADMISSION_KEY = "modernPageSelfOutLoudAdmission"

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def build(before: Path, result: Path) -> str:
    original = before.read_bytes()
    if sha(original) != PREDECESSOR_LOCK_SHA256:
        raise ValueError("Unexpected v146 source-lock; refuse revision")
    data = json.loads(original)
    if ADMISSION_KEY in data or "modernPageWebReaderInsetAdmission" not in data:
        raise ValueError("Unrecognized inherited Reader lock")
    data[ADMISSION_KEY] = {
        "schema": "fountain.press.modern-page-self-out-loud-edition.v1",
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
