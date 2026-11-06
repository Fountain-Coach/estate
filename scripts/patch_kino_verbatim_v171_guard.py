#!/usr/bin/env python3
"""Admit the two authentic archived Teatro instruments without changing Fountain Press Reader."""
from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/'staging/reader_provenance_gate.py'
s=p.read_text()
assert 'APPROVED_KINO_VERBATIM_V171_RELEASE' not in s
fragment='''# V171: two ORIGINAL source-faithful Kino synths in the existing Linotype folio.
APPROVED_KINO_VERBATIM_V171_RELEASE="shared-shell-20261106-v171-kino-verbatim-f50d16c"
APPROVED_KINO_VERBATIM_V171_LOCK_SHA="da0162be45fc9b55a6819df27c9247d62b3c99f87fc03600134c756c1b94a1c2"
APPROVED_KINO_VERBATIM_V171_INDEX_SHA="bd093b088ce6c2aae71958dd1cfae8435409883b5f70e8fa62acf3d4af575022"
APPROVED_KINO_VERBATIM_V171_SOURCE_SHA="fa6d70b4fbf9febbacfe0b02c53947988e501ff180bd5dc4a389f2b62fbf00b4"
APPROVED_KINO_VERBATIM_V171_RECEIPT="estate/evidence/press-kino-verbatim-v171.json"
APPROVED_KINO_VERBATIM_V171_RECEIPT_SHA="4af9416989642f0742a23a30d9d4e95ec756ab74f9ebbce51c3932feda659a42"
APPROVED_KINO_VERBATIM_V171_BRIDGE_SHA="8064a68e8b8f84e737850f4bdce3ac2b1c3e2a0683f879c6049ef62b4174caa6"
APPROVED_KINO_VERBATIM_V171_SOURCE_COMMITS={
 "v156":("35fd6a4","12b4613db0472293887c7a9a6f1c7e066151ef406c1632a03c3a5b37dcd360f6"),
 "v158":("e2f5dd2","293cbec0524809e432d1494c91f2c88b1457c4f44680068417408e557041a3bf")
}

def approved_kino_verbatim_v171_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_VERBATIM_V171_RELEASE:return {}
    prev=candidate.parent/APPROVED_KINO_ARCHITECTURE_V170_RELEASE
    inherited=approved_kino_architecture_v170_files(baseline,prev)
    if not inherited:raise UnadmittedReaderRoute("v171 missing admitted v170 predecessor")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_VERBATIM_V171_LOCK_SHA:
        raise UnadmittedReaderRoute("v171 source lock mismatch")
    older=json.loads((prev/"source-lock.json").read_text())
    current=json.loads((candidate/"source-lock.json").read_text())
    claim=current.pop("pressKinoVerbatimV171Admission",None)
    expected={
      "schema":"fountain.press.kino-verbatim-v171",
      "release":APPROVED_KINO_VERBATIM_V171_RELEASE,
      "predecessor":APPROVED_KINO_ARCHITECTURE_V170_RELEASE,
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":"f50d16c7438479a3166fd6eee6c2e095d13e8d2f",
      "teatroOwner":"Fountain-Coach/teatro.fountain.coach",
      "teatroCommit":"74217b710d1955aede0c677cfdd23a0c8c6299cf",
      "sourceSHA256":APPROVED_KINO_VERBATIM_V171_SOURCE_SHA,
      "readerIndexSHA256":APPROVED_KINO_VERBATIM_V171_INDEX_SHA,
      "receiptSHA256":APPROVED_KINO_VERBATIM_V171_RECEIPT_SHA,
      "originalSourceCommits":["35fd6a4","e2f5dd2"],
      "originalReaderUnchanged":True,
      "originalAudioPreserved":True,
      "noIframeInLinotype":True,
      "privateWLANOnly":True,
      "publicReleaseAuthorized":False
    }
    if older!=current or claim!=expected:
        raise UnadmittedReaderRoute("v171 source/rights/lineage mismatch")
    receipt=json.loads((candidate/APPROVED_KINO_VERBATIM_V171_RECEIPT).read_text())
    if (receipt.get("schema")!="fountain.press.kino-original-source-citations.v171"
        or sha256(candidate/APPROVED_KINO_VERBATIM_V171_RECEIPT)!=APPROVED_KINO_VERBATIM_V171_RECEIPT_SHA
        or receipt.get("sourceOwner")!="Fountain-Coach/fountain.coach"
        or receipt.get("teatroOwner")!="Fountain-Coach/teatro.fountain.coach"
        or receipt.get("manuscriptSHA256")!=APPROVED_KINO_VERBATIM_V171_SOURCE_SHA
        or receipt.get("indexSHA256")!=APPROVED_KINO_VERBATIM_V171_INDEX_SHA
        or receipt.get("parentIndexSHA256")!=sha256(prev/"estate/index.html")
        or receipt.get("publicReleaseAuthorized") is not False
        or receipt.get("privateWLANOnly") is not True
        or receipt.get("originalRuntimeUnmodified") is not True
        or receipt.get("existingLinotypeJSUnchanged") is not True
        or receipt.get("iframesInLinotype")!=0
        or receipt.get("liveOriginalSourceIDs")!=["v156","v158"]
        or receipt.get("recordedComparisonTracksPreserved")!=["kino-history-groove","kino-history-memory","a-literal","b-directed"]
        or receipt.get("existingFiguresPreserved")!=["architectural-plate","night-photograph"]
        or receipt.get("changed")!={"estate/index.html":APPROVED_KINO_VERBATIM_V171_INDEX_SHA}
        or receipt.get("added",{}).get("estate/assets/instruments/kino-verbatim-bridge.js")!=APPROVED_KINO_VERBATIM_V171_BRIDGE_SHA):
        raise UnadmittedReaderRoute("v171 source evidence/rights mismatch")
    manifest=json.loads((candidate/"teatro/interludes/kino/press-citation/manifest.json").read_text())
    if (manifest.get("publicReleaseAuthorized") is not False
        or manifest.get("sourceUnmodified") is not True
        or len(manifest.get("editions",[]))!=2):
        raise UnadmittedReaderRoute("v171 original synthesis source or rights misrepresented")
    for edition in manifest["editions"]:
        key=edition.get("id")
        if key not in APPROVED_KINO_VERBATIM_V171_SOURCE_COMMITS:
            raise UnadmittedReaderRoute("Unknown historical Kino edition")
        commit,digest=APPROVED_KINO_VERBATIM_V171_SOURCE_COMMITS[key]
        if (edition.get("exactSnapshotCommit")!=commit
            or edition.get("sourceHtmlSHA256")!=digest
            or sha256(candidate/("teatro/interludes/kino/press-citation/"+key+"/index.html"))!=digest):
            raise UnadmittedReaderRoute("Synth not original Teatro source: "+key)
    before=(prev/"estate/index.html").read_text()
    after=(candidate/"estate/index.html").read_text()
    pat=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    a=re.findall(pat,before,re.S);b=re.findall(pat,after,re.S)
    addon='<script type="module" src="/estate/assets/instruments/kino-verbatim-bridge.js"></script>'
    if (len(a)!=1 or len(b)!=1 or after.replace(b[0],a[0],1).replace(addon,"",1)!=before
        or after.count(addon)!=1
        or b[0].count("<iframe")!=0
        or b[0].count('data-press-verbatim=')!=2
        or b[0].count("<satzfunk-player compact")!=4
        or b[0].count('data-source-illustration-id=')!=2
        or 'data-source-sha256="'+APPROVED_KINO_VERBATIM_V171_SOURCE_SHA+'"' not in b[0]):
        raise UnadmittedReaderRoute("v171 made unrelated Reader change or inserted pagination iframe")
    oldfiles={x.relative_to(prev).as_posix():x for x in prev.rglob("*") if x.is_file()}
    newfiles={x.relative_to(candidate).as_posix():x for x in candidate.rglob("*") if x.is_file()}
    allowed={**receipt["added"],APPROVED_KINO_VERBATIM_V171_RECEIPT:APPROVED_KINO_VERBATIM_V171_RECEIPT_SHA}
    if set(newfiles)-set(oldfiles)!=set(allowed) or set(oldfiles)-set(newfiles):
        raise UnadmittedReaderRoute("Unapproved v171 route addition or deletion")
    for rel,path in newfiles.items():
        if path.is_symlink():raise UnadmittedReaderRoute("Unapproved stage symlink")
        if rel=="source-lock.json":continue
        expected_hash=APPROVED_KINO_VERBATIM_V171_INDEX_SHA if rel=="estate/index.html" else allowed.get(rel)
        if expected_hash is None:expected_hash=sha256(oldfiles[rel])
        if sha256(path)!=expected_hash:
            raise UnadmittedReaderRoute("Unreviewed v171 stage artifact: "+rel)
    return {**inherited,"estate/index.html":APPROVED_KINO_VERBATIM_V171_INDEX_SHA,**allowed}


'''
needle='\nclass ReaderProvenanceGate:'
assert s.count(needle)==1
s=s.replace(needle,'\n'+fragment+needle,1)
needle='''        if self.current.name == APPROVED_KINO_ARCHITECTURE_V170_RELEASE:
            self.approved_essay = approved_kino_architecture_v170_files(
                self.baseline, self.current)
'''
assert s.count(needle)==1
s=s.replace(needle,needle+'''        if self.current.name == APPROVED_KINO_VERBATIM_V171_RELEASE:
            self.approved_essay = approved_kino_verbatim_v171_files(
                self.baseline, self.current)
''',1)
needle='APPROVED_KINO_ARCHITECTURE_V170_RELEASE)'
assert s.count(needle)>=5,s.count(needle)
s=s.replace(needle,'APPROVED_KINO_ARCHITECTURE_V170_RELEASE, APPROVED_KINO_VERBATIM_V171_RELEASE)')
needle='''        # Only the reviewed vector assets may exist under this work folder.'''
assert s.count(needle)==1
s=s.replace(needle,'''        if self.current.name == APPROVED_KINO_VERBATIM_V171_RELEASE and (
            rel.startswith("teatro/interludes/kino/press-citation/")
            or rel.startswith("estate/assets/instruments/")
            or rel.startswith("teatro/interludes/kino/live-csound/")
            or rel.startswith("teatro/assets/")
        ):
            expected=self.approved_essay.get(rel)
            target=self.current/rel
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target)!=expected:
                raise UnadmittedReaderRoute("Unapproved historic Kino instrument citation: "+rel)
            return
'''+needle,1)
p.write_text(s)
print("V171_VERBATIM_READER_GUARD_EXTENDED")
