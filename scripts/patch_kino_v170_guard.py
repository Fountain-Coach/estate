#!/usr/bin/env python3
"""Admit only the Kino original-architecture visual translation over v169."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'staging/reader_provenance_gate.py'
s=p.read_text()
assert 'APPROVED_KINO_ARCHITECTURE_V170_RELEASE' not in s
block='''# V170 keeps the original Teatro Kino façade as the instrument surface in Press.
APPROVED_KINO_ARCHITECTURE_V170_RELEASE="shared-shell-20261106-v170-kino-visual-263ac6c"
APPROVED_KINO_ARCHITECTURE_V170_LOCK_SHA="0dab307456a41b082a1057b0270b0e3eb613b647a466e0e891cf4770e285abf1"
APPROVED_KINO_ARCHITECTURE_V170_INDEX_SHA="75fb9c8c160d6526447b3818225d44ab33acd0caa0fd8e676352ca539ce939d4"
APPROVED_KINO_ARCHITECTURE_V170_SOURCE_SHA="0f74f0c0eaccf65e6bbc4a7fed2879c3d92ff70c27c3bb66ae58c3097196319f"
APPROVED_KINO_ARCHITECTURE_V170_SVG_SHA="789ef2af5131529e1f1ed43ff70ae7dce3ea715e91107304fe00632cf4a3677d"
APPROVED_KINO_ARCHITECTURE_V170_RECEIPT_SHA="0ee1eec0a5ada3bff1433cfb505d108dc0c8678e32977e6b92ddea0cbae09ba9"
APPROVED_KINO_ARCHITECTURE_V170_CHANGED={
 "estate/index.html":APPROVED_KINO_ARCHITECTURE_V170_INDEX_SHA,
 "teatro/interludes/kino/live-csound/index.html":"6db7c0e4ef4758fdf5fa53af144c27329cbfbcbc6d7a5f35c5b24a7ee59aa816",
 "teatro/interludes/kino/live-csound/live.mjs":"c2135dcec0078c5069aa00b248ecb2ca363c2d1667f021b994b9b26ef6797762"
}
APPROVED_KINO_ARCHITECTURE_V170_RECEIPT="estate/evidence/press-kino-architecture-v170.json"

def approved_kino_architecture_v170_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_ARCHITECTURE_V170_RELEASE:return {}
    previous=candidate.parent/APPROVED_KINO_LIVE_V169_RELEASE
    inherited=approved_kino_live_v169_files(baseline,previous)
    if not inherited:raise UnadmittedReaderRoute("v170 predecessor not admitted")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_ARCHITECTURE_V170_LOCK_SHA:
        raise UnadmittedReaderRoute("v170 unknown source lock")
    before=json.loads((previous/"source-lock.json").read_text())
    after=json.loads((candidate/"source-lock.json").read_text())
    admission=after.pop("pressKinoArchitectureV170Admission",None)
    expected={
      "schema":"fountain.press.kino-architecture-score.v170",
      "release":APPROVED_KINO_ARCHITECTURE_V170_RELEASE,
      "predecessor":APPROVED_KINO_LIVE_V169_RELEASE,
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":"263ac6ca34013a6969be80e6f0d91d71899c2eea",
      "teatroOwner":"Fountain-Coach/teatro.fountain.coach",
      "teatroCommit":"255b98d4c277e48bbc75f538af52a64953c0a3f7",
      "manuscriptSHA256":APPROVED_KINO_ARCHITECTURE_V170_SOURCE_SHA,
      "sourceKinoSVGsha256":APPROVED_KINO_ARCHITECTURE_V170_SVG_SHA,
      "readerIndexSHA256":APPROVED_KINO_ARCHITECTURE_V170_INDEX_SHA,
      "receiptSHA256":APPROVED_KINO_ARCHITECTURE_V170_RECEIPT_SHA,
      "existingReaderUnchanged":True,
      "privateWLANOnly":True,
      "publicReleaseAuthorized":False
    }
    if before!=after or admission!=expected:
        raise UnadmittedReaderRoute("v170 source ownership/rights mismatch")
    receipt=json.loads((candidate/APPROVED_KINO_ARCHITECTURE_V170_RECEIPT).read_text())
    if (receipt.get("schema")!="fountain.press.kino-architectural-live-score.v170"
        or receipt.get("manuscriptSHA256")!=APPROVED_KINO_ARCHITECTURE_V170_SOURCE_SHA
        or receipt.get("sourceKinoSVGsha256")!=APPROVED_KINO_ARCHITECTURE_V170_SVG_SHA
        or receipt.get("readerIndexSHA256")!=APPROVED_KINO_ARCHITECTURE_V170_INDEX_SHA
        or receipt.get("changed")!=APPROVED_KINO_ARCHITECTURE_V170_CHANGED
        or receipt.get("preservedRecordedAuditions")!=4
        or receipt.get("preservedLiveCsoundInstruments")!=4
        or receipt.get("existingReaderUnchanged") is not True
        or receipt.get("existingArtworkPreserved") is not True
        or receipt.get("privateWLANOnly") is not True
        or receipt.get("publicReleaseAuthorized") is not False):
        raise UnadmittedReaderRoute("v170 evidence or authorization mismatch")
    old=(previous/"estate/index.html").read_text()
    new=(candidate/"estate/index.html").read_text()
    pat=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    a=re.findall(pat,old,re.S);b=re.findall(pat,new,re.S)
    if (len(a)!=1 or len(b)!=1 or new.replace(b[0],a[0],1)!=old
        or b[0].count('<satzfunk-player compact')!=4
        or b[0].count('data-source-illustration-id=')!=2
        or b[0].count("<iframe ")!=2
        or b[0].count('data-original-kino-svg-sha256="'+APPROVED_KINO_ARCHITECTURE_V170_SVG_SHA+'"')!=2
        or 'data-source-sha256="'+APPROVED_KINO_ARCHITECTURE_V170_SOURCE_SHA+'"' not in b[0]):
        raise UnadmittedReaderRoute("v170 damaged other books, audio or figures")
    score=(candidate/"teatro/interludes/kino/live-csound/index.html").read_text()
    if ("Original Teatro Kino After Dark architectural SVG SHA-256 "+APPROVED_KINO_ARCHITECTURE_V170_SVG_SHA not in score
        or score.count('class="memory-window"')!=16
        or score.count("data-play=")!=4):
        raise UnadmittedReaderRoute("v170 replaced original Kino architecture or synths")
    oldfiles={x.relative_to(previous).as_posix():x for x in previous.rglob("*") if x.is_file()}
    newfiles={x.relative_to(candidate).as_posix():x for x in candidate.rglob("*") if x.is_file()}
    if set(newfiles)-set(oldfiles)!={APPROVED_KINO_ARCHITECTURE_V170_RECEIPT} or set(oldfiles)-set(newfiles):
        raise UnadmittedReaderRoute("v170 unreviewed file added/deleted")
    for rel,path in newfiles.items():
        if path.is_symlink():raise UnadmittedReaderRoute("v170 unreviewed symlink")
        if rel=="source-lock.json":continue
        expected_sha=(APPROVED_KINO_ARCHITECTURE_V170_RECEIPT_SHA
            if rel==APPROVED_KINO_ARCHITECTURE_V170_RECEIPT else
            APPROVED_KINO_ARCHITECTURE_V170_CHANGED.get(rel))
        if expected_sha is None:expected_sha=sha256(oldfiles[rel])
        if sha256(path)!=expected_sha:raise UnadmittedReaderRoute("v170 file drift: "+rel)
    return {**inherited,**APPROVED_KINO_ARCHITECTURE_V170_CHANGED,
            APPROVED_KINO_ARCHITECTURE_V170_RECEIPT:APPROVED_KINO_ARCHITECTURE_V170_RECEIPT_SHA}


'''
needle='\nclass ReaderProvenanceGate:'
assert s.count(needle)==1
s=s.replace(needle,'\n'+block+needle,1)
needle='''        if self.current.name == APPROVED_KINO_LIVE_V169_RELEASE:
            self.approved_essay = approved_kino_live_v169_files(
                self.baseline, self.current)
'''
assert s.count(needle)==1
s=s.replace(needle,needle+'''        if self.current.name == APPROVED_KINO_ARCHITECTURE_V170_RELEASE:
            self.approved_essay = approved_kino_architecture_v170_files(
                self.baseline, self.current)
''',1)
needle='APPROVED_KINO_LIVE_V169_RELEASE)'
assert s.count(needle)>=5,s.count(needle)
s=s.replace(needle,'APPROVED_KINO_LIVE_V169_RELEASE, APPROVED_KINO_ARCHITECTURE_V170_RELEASE)')
needle='''        # Only the reviewed vector assets may exist under this work folder.'''
assert s.count(needle)==1
s=s.replace(needle,'''        if self.current.name == APPROVED_KINO_ARCHITECTURE_V170_RELEASE and (
            rel.startswith("teatro/interludes/kino/live-csound/")
            or rel.startswith("teatro/assets/")
        ):
            expected=self.approved_essay.get(rel)
            target=self.current/rel
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target)!=expected:
                raise UnadmittedReaderRoute("Unadmitted v170 Teatro live source: "+rel)
            return
'''+needle,1)
p.write_text(s)
print("V170_READER_PROVENANCE_GUARD_EXTENDED")
