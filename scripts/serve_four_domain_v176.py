#!/usr/bin/env python3
"""Pin one additive four-domain editorial candidate to the existing EstateShell gate.

Uses the already accepted unmodified v175 Reader guard and HTTP preview server,
rather than replacing them. All 1736 inherited files must match byte-for-byte.
All 93 new paths must match the Fountain Press source manifest.
Production and current symlink are never changed by this source program.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
ORIGINAL_SERVER=STAGE/"serve_shared_shell_preview.py"
ORIGINAL_GUARD=STAGE/"reader_provenance_gate.py"
SERVER_SHA="ab0082a239661e3809cef9dbb4074e6dab4cb1c53e0ea71aacd305a1feaa8433"
GUARD_SHA="ebb3cfa3f124975eae7921e3719978f3597b4680fb85106b8a6a724f6ec78283"
RELEASE="shared-shell-20261109-v176-four-domain-c265c57"
PREDECESSOR="shared-shell-20261108-v175-governance161-shell-1486f09"
SOURCE="c265c5783e28bd2b91685f96f18ac03b6718aeda"
LOCK_SHA="8029b4c0c2ebe21ae608f42ad51bacdd779124e72a74dcc22b1ca7ba57cd5a2b"
PREVIOUS_LOCK_SHA="d546d92aab66ebdd2615d6e24660461ab759866d6f0f19de290c40f0559edf1a"
OVERLAY_SHA="69e68e01d732585c4576a81f952126c00aaa1a6366b6d83f8d8f81ae45134aa2"
MAP_SHA="dd302ff4c5314078183d4e9c3e0a7f3949b9ce026591c0de4b0a7fb001d0d6ff"
REVIEW="review-20261109"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if sha(ORIGINAL_GUARD)!=GUARD_SHA or sha(ORIGINAL_SERVER)!=SERVER_SHA:
    raise SystemExit("Refuse changed incumbent staging Reader/server source")
sys.path.insert(0,str(STAGE))
import reader_provenance_gate as original
import serve_shared_shell_preview as server

class FourDomainV176ReaderGate:
    def __init__(self,baseline:Path,current:Path):
        self.current=current.resolve(strict=True)
        if self.current.name!=RELEASE:
            raise original.UnadmittedReaderRoute("Unknown source-bound v176 stage")
        self.previous=self.current.parent/PREDECESSOR
        if sha(self.previous/"source-lock.json")!=PREVIOUS_LOCK_SHA:
            raise original.UnadmittedReaderRoute("Unexpected v175 predecessor")
        if sha(self.current/"source-lock.json")!=LOCK_SHA:
            raise original.UnadmittedReaderRoute("Unexpected v176 exact source lock")
        self.previous_gate=original.ReaderProvenanceGate(baseline,self.previous)
        overlay_path=self.current/REVIEW/"overlay-manifest.json"
        if sha(overlay_path)!=OVERLAY_SHA:
            raise original.UnadmittedReaderRoute("Unreviewed stage overlay manifest")
        data=json.loads(overlay_path.read_text())
        if (data.get("sourceRevision")!=SOURCE or
            data.get("domainMapSHA256")!=MAP_SHA or
            len(data.get("files",{}))!=93 or
            not all(p.startswith(REVIEW+"/") for p in data["files"])):
            raise original.UnadmittedReaderRoute("Stage source-to-domain mapping changed")
        if sha(self.current/REVIEW/"domain-map.json")!=MAP_SHA:
            raise original.UnadmittedReaderRoute("Altered semantic domain map")
        old=json.loads((self.previous/"source-lock.json").read_text())
        current=json.loads((self.current/"source-lock.json").read_text())
        admission=current.pop("fourDomainV176Admission",None)
        expected={
            "schema":"fountain.press.four-domain.owner-wlan-review.v176",
            "sourceOwner":"Fountain-Coach/fountain-press",
            "sourceRevision":SOURCE,
            "release":RELEASE,
            "predecessor":PREDECESSOR,
            "predecessorLockSHA256":PREVIOUS_LOCK_SHA,
            "overlayManifestSHA256":OVERLAY_SHA,
            "domainMapSHA256":MAP_SHA,
            "reviewPrefix":REVIEW+"/",
            "overlayCount":93,
            "privateWLANOnly":True,
            "publicReleaseAuthorized":False,
            "productionEffect":False,
            "incumbentFilesUnchanged":True,
            "ownerOperationControlsDisabled":True,
        }
        if current!=old or admission!=expected:
            raise original.UnadmittedReaderRoute("Stage admission does not match exact prior authority")
        self.overlay=dict(data["files"])
        self.overlay[REVIEW+"/overlay-manifest.json"]=OVERLAY_SHA
        prevfiles={p.relative_to(self.previous).as_posix():p for p in self.previous.rglob("*") if p.is_file()}
        nextfiles={p.relative_to(self.current).as_posix():p for p in self.current.rglob("*") if p.is_file()}
        if set(nextfiles)!=set(prevfiles)|set(self.overlay):
            raise original.UnadmittedReaderRoute("New route outside exact editorial overlay")
        for rel,path in prevfiles.items():
            if rel=="source-lock.json":continue
            expected_sha=sha(path)
            here=nextfiles[rel]
            if here.is_symlink() or sha(here)!=expected_sha:
                raise original.UnadmittedReaderRoute("Incumbent route altered: "+rel)
        for rel,digest in self.overlay.items():
            here=nextfiles[rel]
            if here.is_symlink() or sha(here)!=digest:
                raise original.UnadmittedReaderRoute("Altered editorial artifact: "+rel)
        print("FOUR_DOMAIN_V176_ADMITTED",
              f"release={RELEASE} source={SOURCE} files={len(nextfiles)}",
              "production-effect=false",flush=True)

    def check(self,raw_url:str)->None:
        path=original.normalized_request_path(raw_url)
        if path.startswith(REVIEW+"/"):
            expected=self.overlay.get(path)
            if expected is None:
                if (self.current/path).exists():
                    raise original.UnadmittedReaderRoute("Unlisted editorial route")
                return  # Normal 404 for absent editorial path.
            file=self.current/path
            if file.is_symlink() or not file.is_file() or sha(file)!=expected:
                raise original.UnadmittedReaderRoute("Editorial stage byte changed: "+path)
            return
        self.previous_gate.check(raw_url)

if __name__=="__main__":
    # Preserve exactly the existing inspect/Handler and HTTP server controls.
    server.ReaderProvenanceGate=FourDomainV176ReaderGate
    server.main()
