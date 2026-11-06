#!/usr/bin/env python3
"""Independent guard readback for source-locked full Kino live release."""
from pathlib import Path
import sys,importlib.util
ROOT=Path("/home/benedikt/estate-shell-acceptance-staging")
FILE=ROOT/"reader_provenance_gate_v169_candidate.py"
spec=importlib.util.spec_from_file_location("reader_provenance_gate",FILE)
mod=importlib.util.module_from_spec(spec)
sys.modules["reader_provenance_gate"]=mod
spec.loader.exec_module(mod)
baseline=ROOT/"releases"/mod.ACCEPTED_STAGE
current=ROOT/"releases"/"shared-shell-20261106-v169-kino-live-06f63f7"
guard=mod.ReaderProvenanceGate(baseline,current)
paths=[
 "estate/index.html",
 "estate/assets/linotype/reading-first-app.js",
 "estate/media/kino/history/kino-history-groove.m4a",
 "estate/media/kino/history/kino-history-memory.m4a",
 "estate/media/kino/sound-craft/a-literal.m4a",
 "estate/media/kino/sound-craft/b-directed.m4a",
 "estate/essays/a-sound-must-earn-its-place/media/kino-international-night-20261106.jpg",
 "estate/essays/a-sound-must-earn-its-place/media/kino-international-architectural-plate-20261106.jpg",
 "teatro/assets/book-csound-host.js",
 "teatro/interludes/kino/live-csound/index.html",
 "teatro/interludes/kino/live-csound/live.mjs",
 "teatro/interludes/kino/live-csound/history-groove.json",
 "teatro/interludes/kino/live-csound/history-memory.json",
 "teatro/interludes/kino/live-csound/literal.json",
 "teatro/interludes/kino/live-csound/directed.json"
]
for path in paths:
 guard.check("/"+path)
 print("ADMITTED",path,flush=True)
for path in ("teatro/interludes/kino/live-csound/foreign.js","teatro/interludes/kino/live-csound/admin.html","teatro/assets/unapproved.js"):
 try:
  guard.check("/"+path)
 except mod.UnadmittedReaderRoute:
  print("REFUSED",path,flush=True)
 else:
  raise AssertionError("Unadmitted runtime source allowed: "+path)
print("V169_GUARD_PASS",len(guard.approved_essay),flush=True)
