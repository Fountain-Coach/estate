#!/usr/bin/env python3
"""Fountain Coach source-bound *private WLAN* WIND-01 release v187.

Extends the actual immutable v186 stage in place; no new server, public release,
Reader replacement, Store write, MIDI2 operation, or provider authorization.
The admission record identifies exactly four new browser-Csound files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import ssl

STAGE = Path("/home/benedikt/estate-shell-acceptance-staging")
RELEASES = STAGE / "releases"
CANDIDATES = STAGE / "candidates"
BUNDLE = STAGE / "incoming" / "wind01-v187"
META = BUNDLE / "admission.json"
OLD = "shared-shell-20261111-v186-works-books-b8434c5"
NEW = "shared-shell-20261111-v187-teatro-ear-wind01-af0d6f2"
EXPECTED_META_SHA = "6520fa9b6167f7dc9884f8102022b476d2c500832255a498f7b4988c05552d7c"
EXPECTED_OLD_LOCK_SHA = "4410cd5c364d39d255bdb4447c1b8f6186fa7571c1e0b85bd1d7eff09683a135"
SOURCE_SHA = "af0d6f2bc4ab336306f047fa159203c2265147bf"
LESSON_SHA = "886f12bfc3dc9e651e175eb6cc4966554f300816"
PREFIX = "teatro/learn/two-winds/"
GUARD_NAME = "serve_wind01_v187.py"
SECURE_NAME = "serve_secure_wind01_v187.py"
ADMISSION_NAME = "wind01-admission-v187.json"
BASELINE = RELEASES / "shared-shell-20261103-v140-same-folio-return"
HTTP_UNIT = "fountain-shell-acceptance-preview.service"
HTTPS_UNIT = "fountain-shell-acceptance-preview-https.service"
OVERRIDE_NAME = "zzzz-wind01-v187.conf"

def sha(data_or_path):
    h = hashlib.sha256()
    if isinstance(data_or_path, bytes):
        return hashlib.sha256(data_or_path).hexdigest()
    with Path(data_or_path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def abort(msg):
    raise RuntimeError("WIND01_V187_REJECTED: " + msg)

def active():
    return (STAGE / "current").resolve(strict=True).name

def read_meta():
    if not META.is_file() or sha(META) != EXPECTED_META_SHA:
        abort("input source-bound payload admission SHA mismatch")
    m = json.loads(META.read_text())
    if (m.get("schema") != "fountain.teatro-ear.wind01.wlan-stage.v187"
        or m.get("oldRelease") != OLD or m.get("newRelease") != NEW
        or m.get("sourceOwner") != "Fountain-Coach/midi2-gpu-fabric"
        or m.get("sourceRevision") != SOURCE_SHA
        or m.get("lessonOwner") != "Fountain-Coach/teatro-ear"
        or m.get("lessonRevision") != LESSON_SHA
        or m.get("route") != "/teatro/learn/two-winds/"
        or m.get("privateStagingOnly") is not True
        or m.get("productionAuthorized") is not False):
        abort("unexpected source/lesson/stage identity")
    files = m.get("files")
    if not isinstance(files, dict) or len(files) != 4:
        abort("expected exactly four Csound browser assets")
    for key,digest in files.items():
        parts = Path(key).parts
        if not key.startswith(PREFIX) or ".." in parts or "." in parts or key.endswith("/"):
            abort("unsafe lesson route: " + key)
        if not key.endswith((".js",".css",".html")) or len(digest) != 64:
            abort("unadmitted asset: " + key)
        artifact = BUNDLE / "payload" / key
        if artifact.is_symlink() or not artifact.is_file() or sha(artifact) != digest:
            abort("payload file SHA mismatch: " + key)
    actual = {p.relative_to(BUNDLE/"payload").as_posix()
              for p in (BUNDLE/"payload").rglob("*") if p.is_file()}
    if actual != set(files):
        abort("unexpected extra package file(s)")
    return m

def make_record(meta):
    return {
        "schema":"fountain.teatro-ear.wind01.wlan.source-bound.v1",
        "sourceOwner":meta["sourceOwner"],
        "sourceRevision":SOURCE_SHA,
        "lessonOwner":meta["lessonOwner"],
        "lessonRevision":LESSON_SHA,
        "route":meta["route"],
        "fileSHA256":meta["files"],
        "inputAdmissionSHA256":EXPECTED_META_SHA,
        "musicIntent":"two timed wind gestures, learner turbulence and verbal score",
        "soundEngine":"existing @csound/browser AudioWorklet",
        "authorPublished":False,
        "privateStagingOnly":True,
        "productionAuthorized":False,
        "humanAuditionAccepted":False,
        "physicalIPadSafariAccepted":False,
        "FCISInstrumentReleased":False
    }

def text_json(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)+"\n").encode()

def write_exclusive(path, data):
    with Path(path).open("xb") as f:
        f.write(data)

def render_guard(admission_sha):
    return f'''#!/usr/bin/env python3
"""Exact four-file WIND-01 private WLAN guard over v186's source-owning reader."""
import hashlib,json,sys
from pathlib import Path
STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
CANDIDATES=STAGE/"candidates"
sys.path.insert(0,str(CANDIDATES))
import serve_works_books_v186 as previous
original=previous.original
server=previous.server
A_PATH=CANDIDATES/"{ADMISSION_NAME}"
A_SHA="{admission_sha}"
def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):
            h.update(b)
    return h.hexdigest()
if digest(A_PATH)!=A_SHA:
    raise SystemExit("WIND-01 admission altered")
A=json.loads(A_PATH.read_text())
if digest(Path(previous.__file__))!=A["inheritedGuardSHA256"]:
    raise SystemExit("WIND-01 inherited guard source altered")
class Wind01V187Gate:
    def __init__(self,baseline,current):
        self.current=Path(current).resolve(strict=True)
        if self.current.name!=A["newRelease"]:
            raise original.UnadmittedReaderRoute("Wrong WIND-01 release")
        self.previous=self.current.parent/A["oldRelease"]
        if digest(self.previous/"source-lock.json")!=A["oldLockSHA256"] or digest(self.current/"source-lock.json")!=A["newLockSHA256"]:
            raise original.UnadmittedReaderRoute("WIND-01 source-lock chain mismatch")
        self.inherited=previous.WorksBooksV186Gate(baseline,self.previous)
        before=json.loads((self.previous/"source-lock.json").read_text())
        after=json.loads((self.current/"source-lock.json").read_text())
        change=after.pop("wind01V187Admission",None)
        if before!=after or change!=A["record"]:
            raise original.UnadmittedReaderRoute("Unapproved source-lock delta")
        oldfiles={{p.relative_to(self.previous).as_posix():p for p in self.previous.rglob("*") if p.is_file()}}
        newfiles={{p.relative_to(self.current).as_posix():p for p in self.current.rglob("*") if p.is_file()}}
        expected=A["files"]
        if set(newfiles)!=set(oldfiles)|set(expected) or (set(oldfiles)&set(expected)):
            raise original.UnadmittedReaderRoute("Added/removal file inventory does not match WIND-01")
        for rel,p in oldfiles.items():
            if rel=="source-lock.json": continue  # separately checked against pinned old/new SHAs
            if newfiles[rel].is_symlink() or digest(p)!=digest(newfiles[rel]):
                raise original.UnadmittedReaderRoute("Inherited v186 file changed: "+rel)
        for rel,expected_sha in expected.items():
            if newfiles[rel].is_symlink() or digest(newfiles[rel])!=expected_sha:
                raise original.UnadmittedReaderRoute("WIND-01 payload hash mismatch: "+rel)
        print("WIND01_V187_ADMITTED "+A["sourceRevision"][:12]+" newFiles=4 privateWLAN=true",flush=True)
    def check(self,raw_url):
        rel=original.normalized_request_path(raw_url)
        if rel in A["files"]:
            f=self.current/rel
            if f.is_symlink() or not f.is_file() or digest(f)!=A["files"][rel]:
                raise original.UnadmittedReaderRoute("Altered WIND-01 stage asset")
            return
        if rel.startswith("{PREFIX}"):
            raise original.UnadmittedReaderRoute("Unadmitted WIND-01 asset")
        self.inherited.check(raw_url)
if __name__=="__main__":
    server.ReaderProvenanceGate=Wind01V187Gate
    server.main()
'''

def render_secure():
    return f'''#!/usr/bin/env python3
"""Existing HTTPS stage host with v187 source-bound WIND-01 Reader guard."""
import sys
from pathlib import Path
STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
sys.path.insert(0,str(STAGE/"candidates"))
import {GUARD_NAME.removesuffix(".py")} as wind
import serve_shared_shell_preview_https as secure
if __name__=="__main__":
    secure.ReaderProvenanceGate=wind.Wind01V187Gate
    secure.main()
'''

def override(unit):
    if unit == HTTP_UNIT:
        script = CANDIDATES / GUARD_NAME
        cmd = f"/usr/bin/python3 {script} --root {STAGE/'current'} --bind 192.168.8.50 --port 8200"
    else:
        script = CANDIDATES / SECURE_NAME
        cmd = (f"/usr/bin/python3 {script} --root {STAGE/'current'} --bind 192.168.8.50 --port 8243 "
               "--cert /etc/teatro-first-readings-staging/fullchain.pem "
               "--key /etc/teatro-first-readings-staging/leaf.key")
    return ("[Service]\nExecStart=\nExecStart="+cmd+"\n").encode()

def check_gate(release):
    sys.path.insert(0, str(CANDIDATES))
    import serve_wind01_v187 as gate
    instance=gate.Wind01V187Gate(BASELINE,release)
    for url in ("/teatro/learn/two-winds/","/teatro/learn/two-winds/assets/index-B1e3G1yc.js",
                "/teatro/","/estate/"):
        instance.check(url)
    try:
        instance.check("/teatro/learn/two-winds/assets/unadmitted.js")
    except gate.original.UnadmittedReaderRoute:
        print("WIND01_UNKNOWN_ASSET_REFUSED",flush=True)
    else:
        abort("unknown WIND-01 route was not denied")
    return instance

def prepare():
    if active()!=OLD:
        abort("active staging predecessor changed; refusing stale candidate")
    if sha(RELEASES/OLD/"source-lock.json") != EXPECTED_OLD_LOCK_SHA:
        abort("v186 predecessor lock changed")
    m=read_meta()
    cand=RELEASES/NEW
    if cand.exists():
        abort("candidate release already exists; no overwrite allowed")
    print("PREPARING_WIND01_V187_CANDIDATE",flush=True)
    shutil.copytree(RELEASES/OLD,cand,copy_function=shutil.copy2,symlinks=False)
    for name,expected in m["files"].items():
        to=cand/name
        if to.exists(): abort("WIND-01 path already present: "+name)
        to.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BUNDLE/"payload"/name,to)
        if sha(to)!=expected: abort("copied payload SHA mismatch")
    old=json.loads((RELEASES/OLD/"source-lock.json").read_text())
    rec=make_record(m)
    if "wind01V187Admission" in old:abort("duplicate WIND01 source identity")
    changed=dict(old)
    changed["wind01V187Admission"]=rec
    replacement=cand/"source-lock.json.wind01.tmp"
    replacement.write_bytes(text_json(changed))
    os.replace(replacement,cand/"source-lock.json")
    manifest={
        "schema":"fountain.teatro-ear.wind01.stage-guard.v187",
        "oldRelease":OLD,"newRelease":NEW,
        "oldLockSHA256":EXPECTED_OLD_LOCK_SHA,
        "newLockSHA256":sha(cand/"source-lock.json"),
        "sourceOwner":m["sourceOwner"],
        "sourceRevision":SOURCE_SHA,
        "lessonRevision":LESSON_SHA,
        "record":rec,"files":m["files"],
        "inheritedGuardSHA256":sha(CANDIDATES/"serve_works_books_v186.py")
    }
    out=CANDIDATES/ADMISSION_NAME
    if out.exists():abort("v187 admission file already exists")
    write_exclusive(out,text_json(manifest))
    gsha=sha(out)
    for fname,body in ((GUARD_NAME,render_guard(gsha)),(SECURE_NAME,render_secure())):
        file=CANDIDATES/fname
        if file.exists():abort("v187 guard already exists")
        write_exclusive(file,body.encode())
    for unit in (HTTP_UNIT,HTTPS_UNIT):
        label="http" if unit==HTTP_UNIT else "https"
        write_exclusive(CANDIDATES/f"wind01-v187-{label}.conf",override(unit))
    print("WIND01_V187_PREPARED files=4 oldRelease="+OLD+" newRelease="+NEW,flush=True)
    print("SOURCE_LOCK_SHA256="+manifest["newLockSHA256"],flush=True)
    print("ADMISSION_SHA256="+gsha,flush=True)

def activate():
    if active()!=OLD:
        abort("active staging release no longer v186")
    m=read_meta()
    release=RELEASES/NEW
    if not release.is_dir():
        abort("candidate missing")
    check_gate(release)  # expensive but performed before switching
    home=Path.home()
    installed=[]
    temp=STAGE/"current.wind01-v187.swap"
    target=STAGE/"current"
    try:
        for unit in (HTTP_UNIT,HTTPS_UNIT):
            folder=home/".config/systemd/user"/(unit+".d")
            folder.mkdir(parents=True,exist_ok=True)
            dest=folder/OVERRIDE_NAME
            if dest.exists():abort("overriding an existing v187 service profile")
            src=CANDIDATES/("wind01-v187-http.conf" if unit==HTTP_UNIT else "wind01-v187-https.conf")
            shutil.copy2(src,dest)
            installed.append(dest)
        temp.symlink_to(release)
        os.replace(temp,target)
        subprocess.run(["systemctl","--user","daemon-reload"],check=True)
        subprocess.run(["systemctl","--user","restart",HTTP_UNIT,HTTPS_UNIT],check=True,timeout=230)
        # The inherited 1900-file source guard can take a minute to initialize.
        # Wait for both existing services' real served bytes, not systemd 'active'.
        for url in ("http://192.168.8.50:8200/teatro/learn/two-winds/",
                    "https://192.168.8.50:8243/teatro/learn/two-winds/"):
            request=urllib.request.Request(url,headers={"Cache-Control":"no-cache"})
            context=ssl._create_unverified_context() if url.startswith("https://") else None
            deadline=time.monotonic()+180
            last=None
            while time.monotonic()<deadline:
                try:
                    with urllib.request.urlopen(request,context=context,timeout=6) as response:
                        data=response.read()
                        if response.status!=200 or sha(data)!=m["files"]["teatro/learn/two-winds/index.html"]:
                            abort("staging HTTP(S) readback does not match released bytes")
                        print("WIND01_V187_LIVE "+url+" status=200 sha256="+sha(data),flush=True)
                        break
                except (OSError,urllib.error.URLError) as error:
                    last=error
                    time.sleep(3)
            else:
                abort("stage did not become ready at "+url+": "+str(last))
        if active()!=NEW:
            abort("active symlink mismatch after stage activation")
        result={
            "schema":"fountain.teatro-ear.wind01.owner-wlan-stage-terminal.v187",
            "sourceOwner":m["sourceOwner"],
            "sourceRevision":SOURCE_SHA,
            "lessonOwner":m["lessonOwner"],
            "lessonRevision":LESSON_SHA,
            "newRelease":NEW,
            "predecessor":OLD,
            "activeReleaseVerified":True,
            "browserAssetsSHA256":m["files"],
            "httpAndHTTPSReadback":True,
            "privateStagingOnly":True,
            "publicProductionAffected":False,
            "physicalIPadSafariAccepted":False,
            "humanMusicalAuditionAccepted":False,
            "typedEstatePublisherProductionReceipt":False
        }
        path=STAGE/"wind01-v187-terminal-receipt.json"
        if path.exists():abort("existing stage terminal receipt")
        write_exclusive(path,text_json(result))
        print("WIND01_V187_TERMINAL_COMPLETE "+str(path),flush=True)
    except Exception:
        if temp.is_symlink():temp.unlink()
        rollback=STAGE/"current.wind01-v187.rollback"
        rollback.symlink_to(RELEASES/OLD)
        os.replace(rollback,target)
        for installed_file in installed:
            installed_file.unlink(missing_ok=True)
        subprocess.run(["systemctl","--user","daemon-reload"],check=False)
        subprocess.run(["systemctl","--user","restart",HTTP_UNIT,HTTPS_UNIT],check=False,timeout=230)
        raise

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("action",choices=["prepare","activate"])
    args=parser.parse_args()
    if args.action=="prepare":prepare()
    else:activate()

if __name__=="__main__":
    try:main()
    except Exception as error:
        print(str(error),file=sys.stderr,flush=True)
        raise
