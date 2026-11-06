#!/usr/bin/env python3
"""Narrowly admit source-module readiness without changing original synth editions or Reader."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'staging/reader_provenance_gate.py'
s=p.read_text()
assert 'APPROVED_KINO_READY_V172_RELEASE' not in s
fragment='''# v172: original Teatro sources only enable interaction after original listeners exist.
APPROVED_KINO_READY_V172_RELEASE="shared-shell-20261106-v172-kino-ready-bc4fdc1"
APPROVED_KINO_READY_V172_LOCK_SHA="06ea4f23ccdf7a0e125fb379899e78c0ca79709cfd304d9f0ace736ca849d606"
APPROVED_KINO_READY_V172_RECEIPT="estate/evidence/press-kino-ready-v172.json"
APPROVED_KINO_READY_V172_RECEIPT_SHA="a151f17299e489b5ae5f91749aafbc538a3a503750ad9fa3182fc7123a8c4588"
APPROVED_KINO_READY_V172_BRIDGE_SHA="057ccec2f0ea2e9c00bad55f2553f4a07a448976784c109ee0a0346fbcdaf099"

def approved_kino_ready_v172_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_READY_V172_RELEASE:return {}
    prev=candidate.parent/APPROVED_KINO_VERBATIM_V171_RELEASE
    inherited=approved_kino_verbatim_v171_files(baseline,prev)
    if not inherited:raise UnadmittedReaderRoute("v172 missing accepted source citation predecessor")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_READY_V172_LOCK_SHA:
        raise UnadmittedReaderRoute("v172 source lock mismatch")
    older=json.loads((prev/"source-lock.json").read_text())
    newer=json.loads((candidate/"source-lock.json").read_text())
    admission=newer.pop("pressKinoReadyV172Admission",None)
    expected={
      "schema":"fountain.press.kino-original-source-readiness.v172",
      "release":APPROVED_KINO_READY_V172_RELEASE,
      "predecessor":APPROVED_KINO_VERBATIM_V171_RELEASE,
      "sourceOwner":"Fountain-Coach/estate",
      "sourceCommit":"bc4fdc1b146869d10721720ab46ba9a6f37299f7",
      "readerIndexSHA256":APPROVED_KINO_VERBATIM_V171_INDEX_SHA,
      "bridgeSHA256":APPROVED_KINO_READY_V172_BRIDGE_SHA,
      "receiptSHA256":APPROVED_KINO_READY_V172_RECEIPT_SHA,
      "originalSourceUnchanged":True,
      "originalReaderUnchanged":True,
      "privateWLANOnly":True,
      "publicReleaseAuthorized":False
    }
    if older!=newer or admission!=expected:
        raise UnadmittedReaderRoute("v172 unrecognized source, commit or rights")
    receipt=json.loads((candidate/APPROVED_KINO_READY_V172_RECEIPT).read_text())
    if (sha256(candidate/APPROVED_KINO_READY_V172_RECEIPT)!=APPROVED_KINO_READY_V172_RECEIPT_SHA
        or receipt.get("schema")!="fountain.press.kino-verbatim-source-ready.v172"
        or receipt.get("predecessor")!=APPROVED_KINO_VERBATIM_V171_RELEASE
        or receipt.get("sourceCommit")!=expected["sourceCommit"]
        or receipt.get("readerIndexSHA256")!=APPROVED_KINO_VERBATIM_V171_INDEX_SHA
        or receipt.get("readinessBridgeSHA256")!=APPROVED_KINO_READY_V172_BRIDGE_SHA
        or any(receipt.get(flag) is not True for flag in (
           "originalSourceEditorsUnchanged","sourceEditionDigestsPreserved",
           "originalAudioUnchanged","fourRecordedAuditionsPreserved",
           "originalArchitecturalPlatesPreserved","originalReaderUnchanged",
           "historicalSourceScriptsUnmodified","sameFolioPositionOnClose","privateWLANOnly"))
        or receipt.get("publicReleaseAuthorized") is not False):
        raise UnadmittedReaderRoute("v172 incorrect receipt, source or rights")
    bridge=(candidate/"estate/assets/instruments/kino-verbatim-bridge.js").read_text()
    if ("#kino-windows .window-step" not in bridge
        or "#kino-windows .memory-window" not in bridge
        or "frame.style.pointerEvents='none'" not in bridge
        or "frame.style.pointerEvents='auto'" not in bridge):
        raise UnadmittedReaderRoute("v172 incorrect original source readiness detector")
    oldfiles={x.relative_to(prev).as_posix():x for x in prev.rglob("*") if x.is_file()}
    newfiles={x.relative_to(candidate).as_posix():x for x in candidate.rglob("*") if x.is_file()}
    if set(newfiles)-set(oldfiles)!={APPROVED_KINO_READY_V172_RECEIPT} or set(oldfiles)-set(newfiles):
        raise UnadmittedReaderRoute("v172 unreviewed new files or deletion")
    for rel,path in newfiles.items():
        if path.is_symlink():raise UnadmittedReaderRoute("v172 stage symlink")
        if rel=="source-lock.json":continue
        expected_hash=(APPROVED_KINO_READY_V172_BRIDGE_SHA
           if rel=="estate/assets/instruments/kino-verbatim-bridge.js"
           else APPROVED_KINO_READY_V172_RECEIPT_SHA
           if rel==APPROVED_KINO_READY_V172_RECEIPT else sha256(oldfiles[rel]))
        if sha256(path)!=expected_hash:
            raise UnadmittedReaderRoute("v172 byte changes outside accepted bridge: "+rel)
    return {**inherited,"estate/assets/instruments/kino-verbatim-bridge.js":APPROVED_KINO_READY_V172_BRIDGE_SHA,
            APPROVED_KINO_READY_V172_RECEIPT:APPROVED_KINO_READY_V172_RECEIPT_SHA}


'''
needle='\nclass ReaderProvenanceGate:'
assert s.count(needle)==1
s=s.replace(needle,'\n'+fragment+needle,1)
needle='''        if self.current.name == APPROVED_KINO_VERBATIM_V171_RELEASE:
            self.approved_essay = approved_kino_verbatim_v171_files(
                self.baseline, self.current)
'''
assert s.count(needle)==1
s=s.replace(needle,needle+'''        if self.current.name == APPROVED_KINO_READY_V172_RELEASE:
            self.approved_essay = approved_kino_ready_v172_files(
                self.baseline, self.current)
''',1)
needle='APPROVED_KINO_VERBATIM_V171_RELEASE)'
assert s.count(needle)>=5,s.count(needle)
s=s.replace(needle,'APPROVED_KINO_VERBATIM_V171_RELEASE, APPROVED_KINO_READY_V172_RELEASE)')
needle='''        if self.current.name == APPROVED_KINO_VERBATIM_V171_RELEASE and (
            rel.startswith("teatro/interludes/kino/press-citation/")'''
assert s.count(needle)==1
s=s.replace(needle,'''        if self.current.name in (APPROVED_KINO_VERBATIM_V171_RELEASE, APPROVED_KINO_READY_V172_RELEASE) and (
            rel.startswith("teatro/interludes/kino/press-citation/")''',1)
p.write_text(s)
print("KINO_V172_READY_GUARD_PINNED")
