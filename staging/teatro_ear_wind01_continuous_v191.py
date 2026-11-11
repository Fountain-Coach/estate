#!/usr/bin/env python3
"""Source-locked continuous WIND-01 on the existing canonical WLAN staging service.

Exactly one lesson route changes; v190 Koken/NOISE/Bookshelf preserved. Private only.
"""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,ssl,subprocess,sys,time,urllib.request
from pathlib import Path

STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
RELEASES=STAGE/"releases"
CANDIDATES=STAGE/"candidates"
BUNDLE=STAGE/"incoming/wind01-continuous-v191"
META=BUNDLE/"admission.json"
OLD="shared-shell-20261111-v190-koken-head-boxers-e65d62d"
NEW="shared-shell-20261111-v191-wind-continuous-af6f096"
OLD_LOCK="289a242255057dca8e26f85147cd0cce2fe636889eb0dbacef342463272b98f6"
META_SHA="71d44e11fc641b28c276cbce13097ad14d44294f8b432d09b115e8ea853ae07b"
SOURCE_SHA="af6f0968d55fac872c38e0c29227a82e37846100"
LESSON_SHA="4bd180f0cb0f2cfc2cc36bde3facef9162f56eb7"
PREFIX="teatro/learn/two-winds/"
A_NAME="wind01-continuous-admission-v191.json"
GUARD_NAME="serve_wind01_continuous_v191.py"
SECURE_NAME="serve_secure_wind01_continuous_v191.py"
OVERRIDE_NAME="zzzzzzz-wind01-continuous-v191.conf"
BASELINE=RELEASES/"shared-shell-20261103-v140-same-folio-return"
UNITS=("fountain-shell-acceptance-preview.service","fountain-shell-acceptance-preview-https.service")

def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()

def emit(obj):
    return (json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode()

def reject(reason):
    raise RuntimeError("WIND01_CONTINUOUS_V191_REJECTED "+reason)

def active():
    return (STAGE/"current").resolve(strict=True).name

def record(m):
    return {
        "schema":"fountain.teatro-ear.wind01.continuous.wlan.source-bound.v1",
        "sourceOwner":m["sourceOwner"],
        "sourceRevision":SOURCE_SHA,
        "lessonOwner":m["lessonOwner"],
        "lessonRevision":LESSON_SHA,
        "route":m["route"],
        "fileSHA256":m["files"],
        "changedPaths":m["changedPaths"],
        "newFiles":m["newFiles"],
        "admissionSHA256":META_SHA,
        "csoundPatch":"continuous until Stop, irregular Csound-owned gust, live learner control",
        "sourceVoiceStandard":"Fountain-Coach/SatzfunkPlayer@9b7a455; optional source-approved narration; not yet supplied",
        "bbcr128Certification":False,
        "physicalIPadSafariAccepted":False,
        "privateStagingOnly":True,
        "productionAuthorized":False
    }

def input():
    if digest(META)!=META_SHA:reject("incoming admission hash mismatch")
    m=json.loads(META.read_text())
    if any((
        m.get("schema")!="fountain.teatro-ear.wind01.continuous-wlan.v191",
        m.get("oldRelease")!=OLD,m.get("newRelease")!=NEW,
        m.get("oldLockSHA256")!=OLD_LOCK,
        m.get("sourceOwner")!="Fountain-Coach/midi2-gpu-fabric",
        m.get("sourceRevision")!=SOURCE_SHA,
        m.get("lessonOwner")!="Fountain-Coach/teatro-ear",
        m.get("lessonRevision")!=LESSON_SHA,
        m.get("route")!="/teatro/learn/two-winds/",
        m.get("privateStagingOnly") is not True,
        m.get("productionAuthorized") is not False
    )):reject("source revision or lane mismatch")
    files=m.get("files")
    old=m.get("changedPaths")
    added=m.get("newFiles")
    if not isinstance(files,dict) or len(files)!=3 or not isinstance(old,list) or not isinstance(added,list):
        reject("expected exact three-file delta")
    if old!=[PREFIX+"index.html"] or len(added)!=2 or set(files)!=(set(old)|set(added)):
        reject("unexpected replacements/additions")
    for name,expected in files.items():
        p=BUNDLE/"payload"/name
        if not name.startswith(PREFIX) or "." in Path(name).parts or ".." in Path(name).parts:
            reject("unsafe input path")
        if p.is_symlink() or not p.is_file() or digest(p)!=expected:
            reject("asset SHA mismatch "+name)
    actual={p.relative_to(BUNDLE/"payload").as_posix() for p in (BUNDLE/"payload").rglob("*") if p.is_file()}
    if actual!=set(files):reject("unexpected extra input files")
    return m

def guard_text(expected_sha):
    return f'''#!/usr/bin/env python3
"""Inherit exact v190 source guard; permit only WIND-01 v191 changed bytes."""
import hashlib,json,sys
from pathlib import Path
STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
CANDIDATES=STAGE/"candidates"
sys.path.insert(0,str(CANDIDATES))
import serve_koken_head_boxers_v190 as previous
original=previous.original
server=previous.server
A_PATH=CANDIDATES/"{A_NAME}"
A_SHA="{expected_sha}"
def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()
if digest(A_PATH)!=A_SHA:raise SystemExit("WIND v191 admission altered")
A=json.loads(A_PATH.read_text())
if digest(Path(previous.__file__))!=A["inheritedGuardSHA256"]:
    raise SystemExit("WIND v191 inherited v190 reader guard altered")
class WindContinuousV191Gate:
    def __init__(self,baseline,current):
        self.current=Path(current).resolve(strict=True)
        if self.current.name!=A["newRelease"]:
            raise original.UnadmittedReaderRoute("Unexpected continuous WIND-01 release")
        self.previous=self.current.parent/A["oldRelease"]
        if digest(self.previous/"source-lock.json")!=A["oldLockSHA256"] or digest(self.current/"source-lock.json")!=A["newLockSHA256"]:
            raise original.UnadmittedReaderRoute("WIND-01 immutable source-lock mismatch")
        self.inherited=previous.KokenV190Gate(baseline,self.previous)
        before=json.loads((self.previous/"source-lock.json").read_text())
        after=json.loads((self.current/"source-lock.json").read_text())
        change=after.pop("wind01V191Continuous",None)
        if before!=after or change!=A["record"]:
            raise original.UnadmittedReaderRoute("Unapproved WIND-01 source-lock changes")
        old={{p.relative_to(self.previous).as_posix():p for p in self.previous.rglob("*") if p.is_file()}}
        new={{p.relative_to(self.current).as_posix():p for p in self.current.rglob("*") if p.is_file()}}
        files=A["files"]; changed=set(A["changedPaths"]); added=set(A["newFiles"])
        if set(new)!=set(old)|added or changed-set(old) or added&set(old):
            raise original.UnadmittedReaderRoute("Unexpected WIND-01 file inventory")
        for rel,p in old.items():
            if rel in changed or rel=="source-lock.json":continue
            if new[rel].is_symlink() or digest(p)!=digest(new[rel]):
                raise original.UnadmittedReaderRoute("Unrelated stage asset changed "+rel)
        for rel,sha in files.items():
            if new[rel].is_symlink() or digest(new[rel])!=sha:
                raise original.UnadmittedReaderRoute("WIND-01 file hash mismatch "+rel)
        print("WIND01_CONTINUOUS_V191_ADMITTED source="+A["sourceRevision"][:12]+" oldRelease=v190",flush=True)
    def check(self,raw_url):
        rel=original.normalized_request_path(raw_url)
        if rel in A["files"]:
            file=self.current/rel
            if file.is_symlink() or not file.is_file() or digest(file)!=A["files"][rel]:
                raise original.UnadmittedReaderRoute("Altered continuous WIND-01 lesson asset")
            return
        if rel.startswith("{PREFIX}") and rel in A["newFiles"]:
            raise original.UnadmittedReaderRoute("Missing newly admitted WIND-01 asset")
        self.inherited.check(raw_url)
if __name__=="__main__":
    server.ReaderProvenanceGate=WindContinuousV191Gate
    server.main()
'''

def secure_text():
    return '''#!/usr/bin/env python3
"""Reuse the existing owner WLAN HTTPS host with the new source guard."""
import sys
from pathlib import Path
STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
sys.path.insert(0,str(STAGE/"candidates"))
import serve_wind01_continuous_v191 as wind
import serve_shared_shell_preview_https as secure
if __name__=="__main__":
    secure.ReaderProvenanceGate=wind.WindContinuousV191Gate
    secure.main()
'''

def unit_override(secure):
    cmd=f"/usr/bin/python3 {CANDIDATES/(SECURE_NAME if secure else GUARD_NAME)} --root {STAGE/'current'} --bind 192.168.8.50 --port {8243 if secure else 8200}"
    if secure:cmd+=" --cert /etc/teatro-first-readings-staging/fullchain.pem --key /etc/teatro-first-readings-staging/leaf.key"
    return ("[Service]\nExecStart=\nExecStart="+cmd+"\n").encode()

def xwrite(path,data):
    with path.open("xb") as f:f.write(data)

def prepare():
    if active()!=OLD:reject("active stage no longer v190; refuse stale update")
    if digest(RELEASES/OLD/"source-lock.json")!=OLD_LOCK:reject("v190 lock changed")
    m=input()
    candidate=RELEASES/NEW
    if candidate.exists():reject("candidate exists, no overwrite")
    shutil.copytree(RELEASES/OLD,candidate,copy_function=shutil.copy2)
    for name,expected in m["files"].items():
        file=candidate/name
        if name in m["newFiles"] and file.exists():reject("expected new file exists "+name)
        file.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(BUNDLE/"payload"/name,file)
        if digest(file)!=expected:reject("copied asset digest mismatch")
    lock=json.loads((RELEASES/OLD/"source-lock.json").read_text())
    if "wind01V191Continuous" in lock:reject("duplicate admission")
    lock["wind01V191Continuous"]=record(m)
    (candidate/"source-lock.json").write_bytes(emit(lock))
    data={
        "schema":"fountain.teatro-ear.wind01.continuous.guard.v191",
        "oldRelease":OLD,"newRelease":NEW,
        "oldLockSHA256":OLD_LOCK,"newLockSHA256":digest(candidate/"source-lock.json"),
        "inheritedGuardSHA256":digest(CANDIDATES/"serve_koken_head_boxers_v190.py"),
        "sourceRevision":SOURCE_SHA,"lessonRevision":LESSON_SHA,
        "record":record(m),"changedPaths":m["changedPaths"],
        "newFiles":m["newFiles"],"files":m["files"]
    }
    admission_path=CANDIDATES/A_NAME
    xwrite(admission_path,emit(data))
    xwrite(CANDIDATES/GUARD_NAME,guard_text(digest(admission_path)).encode())
    xwrite(CANDIDATES/SECURE_NAME,secure_text().encode())
    xwrite(CANDIDATES/"wind01-v191-http.conf",unit_override(False))
    xwrite(CANDIDATES/"wind01-v191-https.conf",unit_override(True))
    print("WIND01_V191_PREPARED v190 preserved; 1 changed HTML, 2 new JS",flush=True)
    print("SOURCE_LOCK_SHA="+data["newLockSHA256"],flush=True)

def inspect_candidate():
    sys.path.insert(0,str(CANDIDATES))
    import serve_wind01_continuous_v191 as guard
    gate=guard.WindContinuousV191Gate(BASELINE,RELEASES/NEW)
    for rel in (
        "/estate/","/teatro/","/satzfunk/head-boxers/",
        "/teatro/learn/noise-colours/",
        "/teatro/learn/two-winds/",
        "/teatro/learn/two-winds/assets/index-C9imvMgg.js"
    ): gate.check(rel)
    return gate

def activate():
    if active()!=OLD:reject("active predecessor changed")
    m=input()
    if not (RELEASES/NEW).is_dir():reject("candidate absent")
    inspect_candidate()
    dests=[]
    temp=STAGE/"current.wind01-v191-swap"
    current=STAGE/"current"
    try:
        for unit in UNITS:
            folder=Path.home()/".config/systemd/user"/(unit+".d")
            folder.mkdir(parents=True,exist_ok=True)
            dst=folder/OVERRIDE_NAME
            if dst.exists():reject("override exists")
            src=CANDIDATES/("wind01-v191-https.conf" if unit==UNITS[1] else "wind01-v191-http.conf")
            shutil.copy2(src,dst)
            dests.append(dst)
        temp.symlink_to(RELEASES/NEW)
        os.replace(temp,current)
        subprocess.run(["systemctl","--user","daemon-reload"],check=True)
        subprocess.run(["systemctl","--user","restart",*UNITS],check=True,timeout=250)
        deadline=time.monotonic()+210
        for url in (
            "http://192.168.8.50:8200/teatro/learn/two-winds/",
            "https://192.168.8.50:8243/teatro/learn/two-winds/"
        ):
            request=urllib.request.Request(url,headers={"Cache-Control":"no-cache"})
            context=ssl._create_unverified_context() if url.startswith("https://") else None
            last=None
            while time.monotonic()<deadline:
                try:
                    with urllib.request.urlopen(request,context=context,timeout=7) as response:
                        data=response.read()
                        if response.status!=200 or hashlib.sha256(data).hexdigest()!=m["files"][PREFIX+"index.html"]:
                            reject("stage returned wrong HTML bytes")
                        print("WIND01_V191_HTTP_VERIFIED "+url+" SHA256="+hashlib.sha256(data).hexdigest(),flush=True)
                        break
                except (OSError,urllib.error.URLError) as error:
                    last=error
                    time.sleep(3)
            else:reject("staging readback timeout "+url+" "+str(last))
        if active()!=NEW:reject("stage not activated")
        receipt={
            "schema":"fountain.teatro-ear.wind01.continuous.wlan.terminal.v191",
            "predecessor":OLD,"newRelease":NEW,"sourceRevision":SOURCE_SHA,
            "lessonRevision":LESSON_SHA,"files":m["files"],
            "httpAndHttpsSHA256Verified":True,"preservedUnrelatedRoutes":True,
            "productionAffected":False,"physicalIPhoneOrIPadAccepted":False,
            "bbcLoudnessCertified":False,"voiceRecordingAdded":False
        }
        xwrite(STAGE/"wind01-v191-terminal-receipt.json",emit(receipt))
        print("WIND01_V191_STAGE_TERMINAL_SUCCESS",flush=True)
    except Exception:
        if temp.is_symlink():temp.unlink()
        back=STAGE/"current.wind01-v191-rollback"
        back.symlink_to(RELEASES/OLD)
        os.replace(back,current)
        for f in dests:f.unlink(missing_ok=True)
        subprocess.run(["systemctl","--user","daemon-reload"],check=False)
        subprocess.run(["systemctl","--user","restart",*UNITS],check=False,timeout=250)
        raise

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("phase",choices=("prepare","activate"))
    opt=a.parse_args()
    try:
        (prepare if opt.phase=="prepare" else activate)()
    except Exception as e:
        print("WIND01_V191_FAILURE "+str(e),file=sys.stderr,flush=True)
        raise
