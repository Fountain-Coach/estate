#!/usr/bin/env python3
"""Add narrowly scoped v169 Teatro live-source admission to existing Press staging guard."""
from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/"staging/reader_provenance_gate.py"
s=p.read_text()
assert "APPROVED_KINO_LIVE_V169_RELEASE" not in s
fragment='''# The author requested the executable Kino instruments within the established Reader.
APPROVED_KINO_LIVE_V169_RELEASE="shared-shell-20261106-v169-kino-live-06f63f7"
APPROVED_KINO_LIVE_V169_LOCK_SHA="00e05c0bfa1aab1cc45d79fa5b77ccbece6c00116e9b6dd1beecc1121edb5089"
APPROVED_KINO_LIVE_V169_INDEX_SHA="9f951ffc2d8cb81653058a2b745233c8cd267b115dff06bb5796731a33ee9577"
APPROVED_KINO_LIVE_V169_SOURCE_SHA="22e7d1ee3bcc442767d256c090dc6da5be222f9e1b7cb50eef807ffdf62f71ab"
APPROVED_KINO_LIVE_V169_ADDED={
 "teatro/assets/book-csound-host.js":"2a02492a70b6c6bc5352cf405f5203feca4122a3d3dc87a68d38df5ef228e601",
 "teatro/interludes/kino/live-csound/directed.json":"749f61ebe5b7b7b3dfd8d4f5a9f8389763d9e94e3b9398e0e158a89e49c08632",
 "teatro/interludes/kino/live-csound/index.html":"a150360ec0f83326181d0db6afa6bedcf9bd192fa6e1df369d7ef07defd310cc",
 "teatro/interludes/kino/live-csound/literal.json":"336be538389e156c013e6c06188a4d32e59d668aeef990acd0d6f74ab87f7deb",
 "teatro/interludes/kino/live-csound/live.mjs":"d5212945e12484d055583c8656e400d65b6227655a3552f872bdc73ea652d111",
 "teatro/interludes/kino/live-csound/history-groove.json":"c37ab308dba5431e1911cf823f592c4dec1707cf170c92c819ed3c2052b4046c",
 "teatro/interludes/kino/live-csound/history-memory.json":"b3d780bdbc02c9a9464765cd7217764453b514b7bb1e83f5cc85e7a36b498ef5",
 "estate/evidence/press-kino-live-v169.json":"279d3c89b58996c2e8a5a2fcca4938473d7b86e7c282177951057399aa751ecf",
}
def approved_kino_live_v169_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_LIVE_V169_RELEASE:return {}
    previous=candidate.parent/APPROVED_KINO_COMPLETE_V168_RELEASE
    inherited=approved_kino_complete_v168_files(baseline,previous)
    if not inherited:raise UnadmittedReaderRoute("v169 predecessor not admitted")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_LIVE_V169_LOCK_SHA:
        raise UnadmittedReaderRoute("v169 unexpected source-lock")
    old_lock=json.loads((previous/"source-lock.json").read_text())
    new_lock=json.loads((candidate/"source-lock.json").read_text())
    expected={
      "schema":"fountain.press.kino-live-csound.v169",
      "release":APPROVED_KINO_LIVE_V169_RELEASE,
      "predecessor":APPROVED_KINO_COMPLETE_V168_RELEASE,
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":"06f63f797c0d5050d0ede0fb9c6ce2ce24f41973",
      "teatroOwner":"Fountain-Coach/teatro.fountain.coach",
      "teatroCommit":"29211dd2eda1a887da413db1081fc3cb4d471ca0",
      "manuscriptSHA256":APPROVED_KINO_LIVE_V169_SOURCE_SHA,
      "indexSHA256":APPROVED_KINO_LIVE_V169_INDEX_SHA,
      "readerAppSHA256":APPROVED_KINO_COMPLETE_V168_CHANGED["estate/assets/linotype/reading-first-app.js"],
      "receiptSHA256":APPROVED_KINO_LIVE_V169_ADDED["estate/evidence/press-kino-live-v169.json"],
      "liveCsoundAudioWorkletCount":4,
      "historicalCapturesClaimed":False,
      "privateWLANOnly":True,
      "publicReleaseAuthorized":False
    }
    admission=new_lock.pop("pressKinoLiveV169Admission",None)
    if old_lock!=new_lock or admission!=expected:
        raise UnadmittedReaderRoute("v169 lineage/rights/admission mismatch")
    receipt=json.loads((candidate/"estate/evidence/press-kino-live-v169.json").read_text())
    if (receipt.get("schema")!="fountain.press.kino-live-csound-stage.v169"
        or receipt.get("manuscriptSHA256")!=APPROVED_KINO_LIVE_V169_SOURCE_SHA
        or receipt.get("readerIndexSHA256")!=APPROVED_KINO_LIVE_V169_INDEX_SHA
        or receipt.get("readerAppSHA256")!=expected["readerAppSHA256"]
        or receipt.get("recordedComparisonCount")!=4
        or receipt.get("liveSourceCount")!=4
        or receipt.get("liveSynthIDs")!=["history-groove","history-memory","literal","directed"]
        or receipt.get("existingImagesPreserved") is not True
        or receipt.get("originalBrowserCapturesClaimed") is not False
        or receipt.get("privateWLANOnly") is not True
        or receipt.get("publicReleaseAuthorized") is not False
        or receipt.get("changed")!={"estate/index.html":APPROVED_KINO_LIVE_V169_INDEX_SHA}
        or receipt.get("added")!={k:v for k,v in APPROVED_KINO_LIVE_V169_ADDED.items() if k!="estate/evidence/press-kino-live-v169.json"}):
        raise UnadmittedReaderRoute("v169 receipt/rights/source mismatch")
    original=(previous/"estate/index.html").read_text()
    revised=(candidate/"estate/index.html").read_text()
    pattern=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    old=re.findall(pattern,original,re.S)
    new=re.findall(pattern,revised,re.S)
    if (len(old)!=1 or len(new)!=1 or revised.replace(new[0],old[0],1)!=original
        or new[0].count("<satzfunk-player compact")!=4
        or new[0].count('data-source-illustration-id=')!=2
        or new[0].count("<iframe ")!=2
        or new[0].count('data-press-live-csound="')!=2
        or 'data-source-sha256="'+APPROVED_KINO_LIVE_V169_SOURCE_SHA+'"' not in new[0]):
        raise UnadmittedReaderRoute("v169 changed unrelated book or missing live Csound")
    for pair in ("history","controlled"):
        if new[0].count('src="/teatro/interludes/kino/live-csound/?pair='+pair+'"')!=1:
            raise UnadmittedReaderRoute("v169 changed approved live instrument projection")
    oldfiles={x.relative_to(previous).as_posix():x for x in previous.rglob("*") if x.is_file()}
    newfiles={x.relative_to(candidate).as_posix():x for x in candidate.rglob("*") if x.is_file()}
    if set(newfiles)-set(oldfiles)!=set(APPROVED_KINO_LIVE_V169_ADDED) or set(oldfiles)-set(newfiles):
        raise UnadmittedReaderRoute("v169 unapproved files added/deleted")
    for rel,path in newfiles.items():
        if path.is_symlink():raise UnadmittedReaderRoute("v169 asset symlink")
        if rel=="source-lock.json":continue
        expected_hash=APPROVED_KINO_LIVE_V169_INDEX_SHA if rel=="estate/index.html" else APPROVED_KINO_LIVE_V169_ADDED.get(rel)
        if expected_hash is None:expected_hash=sha256(oldfiles[rel])
        if sha256(path)!=expected_hash:raise UnadmittedReaderRoute("v169 asset mismatch: "+rel)
    return {**inherited,"estate/index.html":APPROVED_KINO_LIVE_V169_INDEX_SHA,**APPROVED_KINO_LIVE_V169_ADDED}


'''
needle="\nclass ReaderProvenanceGate:"
assert s.count(needle)==1
s=s.replace(needle,"\n"+fragment+needle,1)
needle='''        if self.current.name == APPROVED_KINO_COMPLETE_V168_RELEASE:
            self.approved_essay = approved_kino_complete_v168_files(
                self.baseline, self.current)
'''
assert s.count(needle)==1
s=s.replace(needle,needle+'''        if self.current.name == APPROVED_KINO_LIVE_V169_RELEASE:
            self.approved_essay = approved_kino_live_v169_files(
                self.baseline, self.current)
''',1)
needle="APPROVED_KINO_COMPOSITION_V167_RELEASE, APPROVED_KINO_COMPLETE_V168_RELEASE)"
assert s.count(needle)>=5,s.count(needle)
s=s.replace(needle,"APPROVED_KINO_COMPOSITION_V167_RELEASE, APPROVED_KINO_COMPLETE_V168_RELEASE, APPROVED_KINO_LIVE_V169_RELEASE)")
needle='''        # Only the reviewed vector assets may exist under this work folder.'''
assert s.count(needle)==1
s=s.replace(needle,'''        if self.current.name == APPROVED_KINO_LIVE_V169_RELEASE and (
            rel.startswith("teatro/interludes/kino/live-csound/")
            or rel.startswith("teatro/assets/")
        ):
            expected=self.approved_essay.get(rel)
            target=self.current/rel
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target)!=expected:
                raise UnadmittedReaderRoute("Unadmitted live Csound Teatro asset: "+rel)
            return
'''+needle,1)
p.write_text(s)
print("V169_GATE_PATCHED",s.count("APPROVED_KINO_LIVE_V169_RELEASE"))
