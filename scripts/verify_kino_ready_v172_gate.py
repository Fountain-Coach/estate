#!/usr/bin/env python3
"""Independent gate witness: unchanged original citations, ready bridge and negative routes."""
from pathlib import Path
import importlib.util,sys
B=Path("/home/benedikt/estate-shell-acceptance-staging")
S=B/"reader_provenance_gate_v172_candidate.py"
spec=importlib.util.spec_from_file_location("reader_provenance_gate",S)
m=importlib.util.module_from_spec(spec)
sys.modules["reader_provenance_gate"]=m
spec.loader.exec_module(m)
release=B/"releases/shared-shell-20261106-v172-kino-ready-bc4fdc1"
gate=m.ReaderProvenanceGate(B/"releases"/m.ACCEPTED_STAGE,release)
paths=[
 "estate/index.html","estate/assets/linotype/reading-first-app.js",
 "estate/assets/instruments/kino-verbatim-bridge.js",
 "estate/evidence/press-kino-verbatim-v171.json",
 "estate/evidence/press-kino-ready-v172.json",
 "teatro/interludes/kino/press-citation/manifest.json",
 "teatro/interludes/kino/press-citation/v156/index.html",
 "teatro/interludes/kino/press-citation/v158/index.html",
 "teatro/interludes/kino/press-citation/v156/assets/sampler-v2.mjs",
 "teatro/interludes/kino/press-citation/v158/assets/ambience-v158.mjs",
 "teatro/interludes/kino/press-citation/v156/assets/groove/bass-d2.m4a",
 "teatro/interludes/kino/press-citation/v158/assets/midnight/midnight-cylinder.m4a",
 "estate/media/kino/history/kino-history-groove.m4a",
 "estate/media/kino/history/kino-history-memory.m4a",
 "estate/media/kino/sound-craft/a-literal.m4a",
 "estate/media/kino/sound-craft/b-directed.m4a",
 "estate/essays/a-sound-must-earn-its-place/media/kino-international-night-20261106.jpg",
 "estate/essays/a-sound-must-earn-its-place/media/kino-international-architectural-plate-20261106.jpg"
]
for p in paths:
 gate.check("/"+p)
 print("ACCEPTED",p,flush=True)
for p in [
 "teatro/interludes/kino/press-citation/v156/assets/injected.js",
 "teatro/assets/unapproved.js",
 "estate/assets/instruments/unreviewed.js",
 "teatro/interludes/kino/live-csound/unknown.js"
]:
 try:gate.check("/"+p)
 except m.UnadmittedReaderRoute:print("REFUSED",p,flush=True)
 else:raise AssertionError("Unapproved artifact admitted: "+p)
print("KINO_V172_READY_STAGE_GUARD_PASS",len(gate.approved_essay),flush=True)
