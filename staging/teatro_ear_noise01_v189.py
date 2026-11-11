#!/usr/bin/env python3
"""Fountain Coach source-bound *private WLAN* NOISE-01 release v189.

Extends the actual immutable v188 stage in place; no new server, public release,
Reader replacement, Store write, MIDI2 operation, or provider authorization.
The admission record identifies exactly six new browser-Csound files.
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
BUNDLE = STAGE / "incoming" / "noise01-v189"
META = BUNDLE / "admission.json"
OLD = "shared-shell-20261111-v188-wind-gestures-13a7980"
NEW = "shared-shell-20261111-v189-noise-colours-a6dcb72"
EXPECTED_META_SHA = "ff6cd09868acc66adb7cc492aeb8340d4f3545e8bc8a26dbe354e1639f643ed2"
EXPECTED_OLD_LOCK_SHA = "afe90f2381e79b1ced2ffa5f27362330ad0ad21e27de65c5d02b58ea7099bf38"
SOURCE_SHA = "a6dcb72e5c43f6254948153e457478e3352e85bc"
LESSON_SHA = "1d8bfd338efdb4a3a89b8cedacd3dacc83a7ff05"
PREFIX = "teatro/learn/noise-colours/"
GUARD_NAME = "serve_noise01_v189.py"
SECURE_NAME = "serve_secure_noise01_v189.py"
ADMISSION_NAME = "noise01-admission-v189.json"
BASELINE = RELEASES / "shared-shell-20261103-v140-same-folio-return"
HTTP_UNIT = "fountain-shell-acceptance-preview.service"
HTTPS_UNIT = "fountain-shell-acceptance-preview-https.service"
OVERRIDE_NAME = "zzzzz-noise01-v189.conf"

def sha(data_or_path):
    h = hashlib.sha256()
    if isinstance(data_or_path, bytes):
        return hashlib.sha256(data_or_path).hexdigest()
    with Path(data_or_path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def abort(msg):
    raise RuntimeError("NOISE01_V189_REJECTED: " + msg)

def active():
    return (STAGE / "current").resolve(strict=True).name

def read_meta():
    if not META.is_file() or sha(META) != EXPECTED_META_SHA:
        abort("input source-bound payload admission SHA mismatch")
    m = json.loads(META.read_text())
    if (m.get("schema") != "fountain.teatro-ear.noise01.wlan-stage.v189"
        or m.get("oldRelease") != OLD or m.get("newRelease") != NEW
        or m.get("sourceOwner") != "Fountain-Coach/midi2-gpu-fabric"
        or m.get("sourceRevision") != SOURCE_SHA
        or m.get("lessonOwner") != "Fountain-Coach/teatro-ear"
        or m.get("lessonRevision") != LESSON_SHA
        or m.get("route") != "/teatro/learn/noise-colours/"
        or m.get("privateStagingOnly") is not True
        or m.get("productionAuthorized") is not False):
        abort("unexpected source/lesson/stage identity")
    files = m.get("files")
    if not isinstance(files, dict) or len(files) != 6:
        abort("expected exactly six Csound browser assets")
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
        "schema":"fountain.teatro-ear.noise01.wlan.source-bound.v1",
        "sourceOwner":meta["sourceOwner"],
        "sourceRevision":SOURCE_SHA,
        "lessonOwner":meta["lessonOwner"],
        "lessonRevision":LESSON_SHA,
        "route":meta["route"],
        "fileSHA256":meta["files"],
        "inputAdmissionSHA256":EXPECTED_META_SHA,
        "musicIntent":"three steady noise spectra before musical gestures",
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
"""Exact six-file NOISE-01 private WLAN guard over v188's source-owning reader."""
import hashlib,json,sys
from pathlib import Path
STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
CANDIDATES=STAGE/"candidates"
sys.path.insert(0,str(CANDIDATES))
import serve_wind01_v188 as previous
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
    raise SystemExit("NOISE-01 admission altered")
A=json.loads(A_PATH.read_text())
if digest(Path(previous.__file__))!=A["inheritedGuardSHA256"]:
    raise SystemExit("NOISE-01 inherited guard source altered")
class Noise01V189Gate:
    def __init__(self,baseline,current):
        self.current=Path(current).resolve(strict=True)
        if self.current.name!=A["newRelease"]:
            raise original.UnadmittedReaderRoute("Wrong NOISE-01 release")
        self.previous=self.current.parent/A["oldRelease"]
        if digest(self.previous/"source-lock.json")!=A["oldLockSHA256"] or digest(self.current/"source-lock.json")!=A["newLockSHA256"]:
            raise original.UnadmittedReaderRoute("NOISE-01 source-lock chain mismatch")
        self.inherited=previous.Wind01V188Gate(baseline,self.previous)
        before=json.loads((self.previous/"source-lock.json").read_text())
        after=json.loads((self.current/"source-lock.json").read_text())
        change=after.pop("noise01V189Admission",None)
        if before!=after or change!=A["record"]:
            raise original.UnadmittedReaderRoute("Unapproved source-lock delta")
        oldfiles={{p.relative_to(self.previous).as_posix():p for p in self.previous.rglob("*") if p.is_file()}}
        newfiles={{p.relative_to(self.current).as_posix():p for p in self.current.rglob("*") if p.is_file()}}
        expected=A["files"]
        if set(newfiles)!=set(oldfiles)|set(expected) or (set(oldfiles)&set(expected)):
            raise original.UnadmittedReaderRoute("Added/removal file inventory does not match NOISE-01")
        for rel,p in oldfiles.items():
            if rel=="source-lock.json": continue  # separately checked against pinned old/new SHAs
            if newfiles[rel].is_symlink() or digest(p)!=digest(newfiles[rel]):
                raise original.UnadmittedReaderRoute("Inherited v188 file changed: "+rel)
        for rel,expected_sha in expected.items():
            if newfiles[rel].is_symlink() or digest(newfiles[rel])!=expected_sha:
                raise original.UnadmittedReaderRoute("NOISE-01 payload hash mismatch: "+rel)
        print("NOISE01_V189_ADMITTED "+A["sourceRevision"][:12]+" newFiles=6 privateWLAN=true",flush=True)
    def check(self,raw_url):
        rel=original.normalized_request_path(raw_url)
        if rel in A["files"]:
            f=self.current/rel
            if f.is_symlink() or not f.is_file() or digest(f)!=A["files"][rel]:
                raise original.UnadmittedReaderRoute("Altered NOISE-01 stage asset")
            return
        if rel.startswith("{PREFIX}"):
            raise original.UnadmittedReaderRoute("Unadmitted NOISE-01 asset")
        self.inherited.check(raw_url)
if __name__=="__main__":
    server.ReaderProvenanceGate=Noise01V189Gate
    server.main()
'''

def render_secure():
    return f'''#!/usr/bin/env python3
"""Existing HTTPS stage host with v189 source-bound NOISE-01 Reader guard."""
import sys
from pathlib import Path
STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
sys.path.insert(0,str(STAGE/"candidates"))
import {GUARD_NAME.removesuffix(".py")} as noise
import serve_shared_shell_preview_https as secure
if __name__=="__main__":
    secure.ReaderProvenanceGate=noise.Noise01V189Gate
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
    import serve_noise01_v189 as gate
    instance=gate.Noise01V189Gate(BASELINE,release)
    m=read_meta()
    for rel in m["files"]:
        instance.check("/"+rel if rel!="teatro/learn/noise-colours/index.html" else "/teatro/learn/noise-colours/")
    for path in ("/teatro/","/estate/","/teatro/learn/two-winds/"):
        instance.check(path)
    try:
        instance.check("/teatro/learn/noise-colours/assets/not-admitted.js")
    except gate.original.UnadmittedReaderRoute:
        print("NOISE01_V189_UNKNOWN_ASSET_REFUSED",flush=True)
    else:
        abort("NOISE-01 unadmitted path incorrectly accepted")
    return instance

def prepare():
    if active()!=OLD:
        abort("active staging predecessor changed; refusing stale candidate")
    if sha(RELEASES/OLD/"source-lock.json") != EXPECTED_OLD_LOCK_SHA:
        abort("v188 predecessor lock changed")
    m=read_meta()
    cand=RELEASES/NEW
    if cand.exists():
        abort("candidate release already exists; no overwrite allowed")
    print("PREPARING_NOISE01_V189_CANDIDATE",flush=True)
    shutil.copytree(RELEASES/OLD,cand,copy_function=shutil.copy2,symlinks=False)
    for name,expected in m["files"].items():
        to=cand/name
        if to.exists(): abort("NOISE-01 path already present: "+name)
        to.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BUNDLE/"payload"/name,to)
        if sha(to)!=expected: abort("copied payload SHA mismatch")
    old=json.loads((RELEASES/OLD/"source-lock.json").read_text())
    rec=make_record(m)
    if "noise01V189Admission" in old:abort("duplicate NOISE01 source identity")
    changed=dict(old)
    changed["noise01V189Admission"]=rec
    replacement=cand/"source-lock.json.noise01.tmp"
    replacement.write_bytes(text_json(changed))
    os.replace(replacement,cand/"source-lock.json")
    manifest={
        "schema":"fountain.teatro-ear.noise01.stage-guard.v189",
        "oldRelease":OLD,"newRelease":NEW,
        "oldLockSHA256":EXPECTED_OLD_LOCK_SHA,
        "newLockSHA256":sha(cand/"source-lock.json"),
        "sourceOwner":m["sourceOwner"],
        "sourceRevision":SOURCE_SHA,
        "lessonRevision":LESSON_SHA,
        "record":rec,"files":m["files"],
        "inheritedGuardSHA256":sha(CANDIDATES/"serve_wind01_v188.py")
    }
    out=CANDIDATES/ADMISSION_NAME
    if out.exists():abort("v189 admission file already exists")
    write_exclusive(out,text_json(manifest))
    gsha=sha(out)
    for fname,body in ((GUARD_NAME,render_guard(gsha)),(SECURE_NAME,render_secure())):
        file=CANDIDATES/fname
        if file.exists():abort("v189 guard already exists")
        write_exclusive(file,body.encode())
    for unit in (HTTP_UNIT,HTTPS_UNIT):
        label="http" if unit==HTTP_UNIT else "https"
        write_exclusive(CANDIDATES/f"noise01-v189-{label}.conf",override(unit))
    print("NOISE01_V189_PREPARED files=6 oldRelease="+OLD+" newRelease="+NEW,flush=True)
    print("SOURCE_LOCK_SHA256="+manifest["newLockSHA256"],flush=True)
    print("ADMISSION_SHA256="+gsha,flush=True)

def activate():
    if active()!=OLD:
        abort("active staging release no longer v188")
    m=read_meta()
    release=RELEASES/NEW
    if not release.is_dir():
        abort("candidate missing")
    check_gate(release)  # expensive but performed before switching
    home=Path.home()
    installed=[]
    temp=STAGE/"current.noise01-v189.swap"
    target=STAGE/"current"
    try:
        for unit in (HTTP_UNIT,HTTPS_UNIT):
            folder=home/".config/systemd/user"/(unit+".d")
            folder.mkdir(parents=True,exist_ok=True)
            dest=folder/OVERRIDE_NAME
            if dest.exists():abort("overriding an existing v187 service profile")
            src=CANDIDATES/("noise01-v189-http.conf" if unit==HTTP_UNIT else "noise01-v189-https.conf")
            shutil.copy2(src,dest)
            installed.append(dest)
        temp.symlink_to(release)
        os.replace(temp,target)
        subprocess.run(["systemctl","--user","daemon-reload"],check=True)
        subprocess.run(["systemctl","--user","restart",HTTP_UNIT,HTTPS_UNIT],check=True,timeout=230)
        # The inherited 1900-file source guard can take a minute to initialize.
        # Wait for both existing services' real served bytes, not systemd 'active'.
        # Wait for both real routed services, then verify every source-owned
        # HTML, CSS and JS response, not just the index page.
        for host in ("http://192.168.8.50:8200","https://192.168.8.50:8243"):
            context=ssl._create_unverified_context() if host.startswith("https://") else None
            for key,expected in m["files"].items():
                route="/teatro/learn/noise-colours/" if key.endswith("/index.html") else "/"+key
                url=host+route
                request=urllib.request.Request(url,headers={"Cache-Control":"no-cache"})
                deadline=time.monotonic()+180
                last=None
                while time.monotonic()<deadline:
                    try:
                        with urllib.request.urlopen(request,context=context,timeout=9) as response:
                            body=response.read()
                            if response.status!=200 or sha(body)!=expected:
                                abort("staging route byte mismatch "+url)
                            print("NOISE01_V189_LIVE "+url+" status=200 sha256="+expected,flush=True)
                            break
                    except (OSError,urllib.error.URLError) as error:
                        last=error
                        time.sleep(3)
                else:
                    abort("staging route unavailable: "+url+" "+str(last))
        # Neighbor checks must remain on the same existing server.
        for path in ("/teatro/","/estate/","/teatro/learn/two-winds/"):
            with urllib.request.urlopen("https://192.168.8.50:8243"+path,context=ssl._create_unverified_context(),timeout=15) as response:
                if response.status!=200:abort("neighbor route failed "+path)
                print("NOISE01_V189_NEIGHBOR_OK "+path,flush=True)
        if active()!=NEW:
            abort("active symlink mismatch after stage activation")
        result={
            "schema":"fountain.teatro-ear.noise01.owner-wlan-stage-terminal.v189",
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
        path=STAGE/"noise01-v189-terminal-receipt.json"
        if path.exists():abort("existing stage terminal receipt")
        write_exclusive(path,text_json(result))
        print("NOISE01_V189_TERMINAL_COMPLETE "+str(path),flush=True)
    except Exception:
        if temp.is_symlink():temp.unlink()
        rollback=STAGE/"current.noise01-v189.rollback"
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
