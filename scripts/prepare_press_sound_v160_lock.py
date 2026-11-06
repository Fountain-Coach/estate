#!/usr/bin/env python3
"""Prepare the one exact-source v160 stage admission, preserving every v159 key.

The new admission is proof of a *private editorial preview only*. It cannot
turn the essay into an admitted Bookshelf publication or an audio release.
"""
import argparse
import hashlib
import json
from pathlib import Path

PREDECESSOR = "shared-shell-20261105-v159-kino-midnight-cylinder-e2f5dd2"
RELEASE = "shared-shell-20261106-v160-press-sound-essay-proof-9d83302"
PRIOR_SHA = "44f7285bb1d2d413d437e815f5decab6149eaf39e283ab7ec1e5984019abd99b"
SOURCE_SHA = "53b5f7369f68548f211571bdaf5fa4d92bbc85b3fed30aedf8839eaf8e293b7c"
CHANGED = {
    "estate/index.html": "7cd67ccb9a8899230b887226a5bc628d23b88613c08385631a9112827518265e",
    "estate/assets/linotype/reading-first-app.js": "83c83d45c1b11db03d0227b18f3daa6f6a481e757faeccc60b1fb1dd06d32cc9",
}
ADDED = {
    "estate/evidence/press-sound-essay-proof-v160.json": "e8f26a9672ec5cbedfe2799d43bd619e3abb9faca91d4fd8aa8b633073892d38",
}
ADMISSION = {
    "schema": "fountain.press.sound-essay-editorial-proof-stage.v1",
    "sourceOwner": "Fountain-Coach/fountain.coach",
    "sourceCommit": "9d833024e202fa37653af3b46f9862d5fc2e82d8",
    "pressOwner": "Fountain-Coach/fountain-press",
    "pressCommit": "71bc32b7ed78798b886c865bb1168cd4f9027a92",
    "predecessor": PREDECESSOR,
    "release": RELEASE,
    "sourceSHA256": SOURCE_SHA,
    "sourceStatus": "unadmitted-editorial-proof",
    "publicReleaseAuthorized": False,
    "governanceChapterAdmitted": False,
    "sourceCompositorReused": True,
    "existingEssaysMembershipUnchanged": True,
    "existingPrivateKinoUnchanged": True,
    "existingVoiceAssetsUnchanged": True,
    "changedFileSHA256": CHANGED,
    "addedFileSHA256": ADDED,
}

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def prepare(prior, essay, candidate, output):
    if digest(prior) != PRIOR_SHA: raise ValueError("Unrecognized v159 source-lock predecessor")
    if digest(essay) != SOURCE_SHA: raise ValueError("Editorial essay source drift")
    for rel, expected in {**CHANGED, **ADDED}.items():
        if digest(Path(candidate)/rel) != expected: raise ValueError("Stage candidate source drift: " + rel)
    lock=json.loads(Path(prior).read_text())
    if "pressSoundEssayV160Admission" in lock: raise ValueError("Duplicate admission")
    lock["pressSoundEssayV160Admission"]=ADMISSION
    Path(output).write_text(json.dumps(lock,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("PRESS_SOUND_STAGE_LOCK",digest(output),RELEASE)
    return digest(output)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for arg in ("prior","essay","candidate","output"):
        p.add_argument("--"+arg,required=True)
    x=p.parse_args()
    prepare(x.prior,x.essay,x.candidate,x.output)
