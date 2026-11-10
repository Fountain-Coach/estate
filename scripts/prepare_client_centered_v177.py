#!/usr/bin/env python3
"""Add one exact Client-Centered Fountain Press edition to the immutable v176 stage.

Read-only source/manifest checks, copy-on-write release preparation, source-lock
extension, v176 byte-parity and rollback preservation. No active symlink,
public domain, user service, publisher authority or other source is changed.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess

STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
PREV="shared-shell-20261109-v176-four-domain-c265c57"
RELEASE="shared-shell-20261110-v177-client-centered-bd8f6d9"
LOCK_PREV="8029b4c0c2ebe21ae608f42ad51bacdd779124e72a74dcc22b1ca7ba57cd5a2b"
SOURCE="bd8f6d93e01354cc0c09a9de0bf9417bd9cfde9c"
MANUSCRIPT="03e4497f6deabe173958bd632b721ac7f23ae95e3bbe0043a1204ad5039de78a"
INVENTORY="01b6e426983fc17d69454df37a694bc77aa859f05e543c711068ed3bd28b32f7"
PREFIX="estate/read/essay--client-centered/"
CANDIDATE="client-centered-v177-bd8f6d9"
def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def filemap(root:Path)->dict[str,Path]:
    return {p.relative_to(root).as_posix():p for p in root.rglob("*") if p.is_file()}
def prepare():
    parent=STAGE/"releases"
    original=parent/PREV
    if (STAGE/"current").resolve()!=original.resolve() or sha(original/"source-lock.json")!=LOCK_PREV:
        raise RuntimeError("Refuse stage predecessor drift")
    root=STAGE/"candidates"/CANDIDATE
    manifestfile=STAGE/"candidates"/(CANDIDATE+"-source-inventory.json")
    if sha(manifestfile)!=INVENTORY:
        raise RuntimeError("Unpinned source-to-stage file list")
    manifest=json.loads(manifestfile.read_text())
    if manifest["sourceRevision"]!=SOURCE or manifest["manuscriptSHA256"]!=MANUSCRIPT:
        raise RuntimeError("Manuscript or source revision differs from Git")
    if len(manifest["files"])!=16:raise RuntimeError("Unexpected published Reader overlay")
    source=root/PREFIX
    if not source.is_dir() or any(".." in Path(rel).parts for rel in manifest["files"]):
        raise RuntimeError("Unbounded source inputs")
    actual=filemap(source)
    if set(actual)!=set(manifest["files"]):raise RuntimeError("Unlisted source asset")
    for name,path in actual.items():
        if path.is_symlink() or sha(path)!=manifest["files"][name]:
            raise RuntimeError("Stage source asset changed: "+name)
    edition=json.loads((source/"edition-manifest.json").read_text())
    if edition["sourceRevision"]!=SOURCE or edition["sourceSHA256"]!=MANUSCRIPT or edition["productionAuthorized"] is not False:
        raise RuntimeError("Not the authorized review-only manuscript")
    if edition["paragraphCount"]!=22 or len(edition["sections"])!=4 or len(edition["figures"])!=2:
        raise RuntimeError("Incomplete essay/Teatro Score")
    if not (source/"index.html").read_text().count('data-initial-volume="essay--client-centered"')==1:
        raise RuntimeError("Not using the exact published reading-first volume")
    existing=filemap(original)
    if any((original/PREFIX/name).exists() for name in actual):
        raise RuntimeError("Overwriting a previous work")
    dest=parent/RELEASE
    temp=parent/("."+RELEASE+".unadmitted")
    if dest.exists() or temp.exists():
        raise RuntimeError("Refuse existing immutable release overwrite")
    temp.mkdir()
    try:
        subprocess.run(["cp","-a","--reflink=auto",str(original)+"/.",str(temp)+"/"],check=True)
        for name,path in actual.items():
            target=temp/PREFIX/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,target)
        old=json.loads((original/"source-lock.json").read_text())
        admission={
            "schema":"fountain.press.client-centered.owner-WLAN-review.v177",
            "release":RELEASE,"predecessor":PREV,
            "predecessorLockSHA256":LOCK_PREV,
            "sourceOwner":"Fountain-Coach/fountain.coach",
            "sourceRevision":SOURCE,"manuscriptSHA256":MANUSCRIPT,
            "sourceInventorySHA256":INVENTORY,
            "route":"/"+PREFIX,"addedFiles":16,
            "publishedEngineUnmodified":True,
            "fiveCurrentEssayMembershipUnchanged":True,
            "privateWLANOnly":True,"publicReleaseAuthorized":False,
            "productionEffect":False
        }
        if "clientCenteredV177Admission" in old:raise RuntimeError("Prior identity collision")
        old["clientCenteredV177Admission"]=admission
        nextlock=temp/".source-lock.v177.tmp"
        nextlock.write_text(json.dumps(old,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
        nextlock.replace(temp/"source-lock.json")
        newfiles=filemap(temp)
        expected=set(existing)|{PREFIX+name for name in actual}
        if set(newfiles)!=expected:raise RuntimeError("Release inventory drift")
        for path,oldfile in existing.items():
            if path!="source-lock.json" and sha(oldfile)!=sha(newfiles[path]):
                raise RuntimeError("Inherited predecessor was modified: "+path)
        for name,digest in manifest["files"].items():
            if sha(newfiles[PREFIX+name])!=digest:
                raise RuntimeError("Added source changed: "+name)
        locksha=sha(temp/"source-lock.json")
        temp.rename(dest)
    except BaseException:
        shutil.rmtree(temp)
        raise
    evidence={
       "schema":"fountain.press.client-centered.prepared-release.v177",
       "release":RELEASE,"sourceRevision":SOURCE,"manuscriptSHA256":MANUSCRIPT,
       "sourceInventorySHA256":INVENTORY,"sourceLockSHA256":locksha,
       "predecessor":PREV,"predecessorLockSHA256":LOCK_PREV,
       "oldFiles":len(existing),"newFiles":len(newfiles),"addedFiles":16,
       "activated":False,"productionModified":False,
    }
    rec=STAGE/"candidates"/(CANDIDATE+"-preparation.json")
    rec.write_text(json.dumps(evidence,indent=2)+"\n")
    print(json.dumps(evidence,indent=2))
if __name__=="__main__":prepare()
