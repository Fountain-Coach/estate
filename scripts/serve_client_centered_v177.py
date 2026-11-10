#!/usr/bin/env python3
"""Extend the already-active v176 EstateShell guard for one Client-Centered work.

The Fountain Press engine, CSS, published Bookshelf and HTTP handler are
unchanged. This is only the exact-source route admission for immutable v177.
"""
from pathlib import Path
import hashlib,json,sys

STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
V176_WRAPPER=STAGE/"candidates/serve_four_domain_v176.py"
PINNED_V176_WRAPPER="a27ac8d6567d83eb6d3cc86dd844135d3c1726067fefa1596fb0dec3f2217913"
PREV="shared-shell-20261109-v176-four-domain-c265c57"
PREV_LOCK="8029b4c0c2ebe21ae608f42ad51bacdd779124e72a74dcc22b1ca7ba57cd5a2b"
RELEASE="shared-shell-20261110-v177-client-centered-bd8f6d9"
RELEASE_LOCK="f67e3dd27d08d73e96f04e6c67a08983bb6c87145126f45c62f924a3fea4c688"
SOURCE="bd8f6d93e01354cc0c09a9de0bf9417bd9cfde9c"
MANUSCRIPT="03e4497f6deabe173958bd632b721ac7f23ae95e3bbe0043a1204ad5039de78a"
MANIFEST="01b6e426983fc17d69454df37a694bc77aa859f05e543c711068ed3bd28b32f7"
PREFIX="estate/read/essay--client-centered/"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
if sha(V176_WRAPPER)!=PINNED_V176_WRAPPER:
    raise SystemExit("Refuse unexpected predecessor Reader guard")
sys.path.insert(0,str(STAGE/"candidates"))
import serve_four_domain_v176 as v176
original=v176.original
server=v176.server
class ClientCenteredV177ReaderGate:
    def __init__(self,baseline:Path,current:Path):
        self.current=current.resolve(strict=True)
        if self.current.name!=RELEASE:
            raise original.UnadmittedReaderRoute("Refuse unpinned v177 release")
        self.previous=self.current.parent/PREV
        if sha(self.previous/"source-lock.json")!=PREV_LOCK:
            raise original.UnadmittedReaderRoute("Predecessor source-lock changed")
        if sha(self.current/"source-lock.json")!=RELEASE_LOCK:
            raise original.UnadmittedReaderRoute("Candidate source-lock changed")
        self.previous_gate=v176.FourDomainV176ReaderGate(baseline,self.previous)
        f=STAGE/"candidates/client-centered-v177-bd8f6d9-source-inventory.json"
        if sha(f)!=MANIFEST:
            raise original.UnadmittedReaderRoute("Unrecognized source inventory")
        data=json.loads(f.read_text())
        if (data["sourceRevision"]!=SOURCE or data["manuscriptSHA256"]!=MANUSCRIPT
            or len(data["files"])!=16):
            raise original.UnadmittedReaderRoute("Partial or incorrect work")
        self.manifest={PREFIX+k:v for k,v in data["files"].items()}
        before=json.loads((self.previous/"source-lock.json").read_text())
        after=json.loads((self.current/"source-lock.json").read_text())
        admission=after.pop("clientCenteredV177Admission",None)
        expected={
            "schema":"fountain.press.client-centered.owner-WLAN-review.v177",
            "release":RELEASE,"predecessor":PREV,
            "predecessorLockSHA256":PREV_LOCK,
            "sourceOwner":"Fountain-Coach/fountain.coach",
            "sourceRevision":SOURCE,"manuscriptSHA256":MANUSCRIPT,
            "sourceInventorySHA256":MANIFEST,
            "route":"/"+PREFIX,"addedFiles":16,
            "publishedEngineUnmodified":True,
            "fiveCurrentEssayMembershipUnchanged":True,
            "privateWLANOnly":True,"publicReleaseAuthorized":False,
            "productionEffect":False,
        }
        if after!=before or admission!=expected:
            raise original.UnadmittedReaderRoute("Owner review admission differs")
        prevfiles={p.relative_to(self.previous).as_posix():p for p in self.previous.rglob("*") if p.is_file()}
        nowfiles={p.relative_to(self.current).as_posix():p for p in self.current.rglob("*") if p.is_file()}
        if set(nowfiles)!=set(prevfiles)|set(self.manifest):
            raise original.UnadmittedReaderRoute("Unlisted route outside exact work")
        for path,old in prevfiles.items():
            if path!="source-lock.json":
                present=nowfiles[path]
                if present.is_symlink() or sha(old)!=sha(present):
                    raise original.UnadmittedReaderRoute("Inherited release altered: "+path)
        for path,expected_sha in self.manifest.items():
            present=nowfiles[path]
            if present.is_symlink() or sha(present)!=expected_sha:
                raise original.UnadmittedReaderRoute("Work asset unrecognized: "+path)
        print("CLIENT_CENTERED_V177_ADMITTED",SOURCE,len(nowfiles),
              "source-owned-Press=true public-production=false",flush=True)

    def check(self,raw_url:str)->None:
        path=original.normalized_request_path(raw_url)
        if path.startswith(PREFIX):
            expected=self.manifest.get(path)
            if expected is None:
                if (self.current/path).exists():
                    raise original.UnadmittedReaderRoute("Unlisted work source file")
                return
            file=self.current/path
            if file.is_symlink() or not file.is_file() or sha(file)!=expected:
                raise original.UnadmittedReaderRoute("Unverified page/image/asset")
            return
        self.previous_gate.check(raw_url)
if __name__=="__main__":
    server.ReaderProvenanceGate=ClientCenteredV177ReaderGate
    server.main()
