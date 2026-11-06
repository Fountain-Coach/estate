#!/usr/bin/env python3
"""Independent source/asset and forbidden-route acceptance for Kino v170 stage."""
from pathlib import Path
import importlib.util,sys
B=Path('/home/benedikt/estate-shell-acceptance-staging')
P=B/'reader_provenance_gate_v170_candidate.py'
spec=importlib.util.spec_from_file_location('reader_provenance_gate',P)
mod=importlib.util.module_from_spec(spec)
sys.modules['reader_provenance_gate']=mod
spec.loader.exec_module(mod)
candidate=B/'releases/shared-shell-20261106-v170-kino-visual-263ac6c'
gate=mod.ReaderProvenanceGate(B/'releases'/mod.ACCEPTED_STAGE,candidate)
for path in (
 'estate/index.html',
 'estate/assets/linotype/reading-first-app.js',
 'estate/media/kino/history/kino-history-groove.m4a',
 'estate/media/kino/history/kino-history-memory.m4a',
 'estate/media/kino/sound-craft/a-literal.m4a',
 'estate/media/kino/sound-craft/b-directed.m4a',
 'estate/essays/a-sound-must-earn-its-place/media/kino-international-night-20261106.jpg',
 'estate/essays/a-sound-must-earn-its-place/media/kino-international-architectural-plate-20261106.jpg',
 'teatro/assets/book-csound-host.js',
 'teatro/interludes/kino/live-csound/index.html',
 'teatro/interludes/kino/live-csound/live.mjs',
 'teatro/interludes/kino/live-csound/history-groove.json',
 'teatro/interludes/kino/live-csound/history-memory.json',
 'teatro/interludes/kino/live-csound/literal.json',
 'teatro/interludes/kino/live-csound/directed.json',
 'estate/evidence/press-kino-architecture-v170.json'
):
 gate.check('/'+path)
 print('ACCEPTED',path,flush=True)
for path in (
 'teatro/interludes/kino/live-csound/foreign.js',
 'teatro/assets/unapproved.js',
 'teatro/interludes/kino/live-csound/other.html',
):
 try:gate.check('/'+path)
 except mod.UnadmittedReaderRoute:print('REFUSED',path,flush=True)
 else:raise AssertionError('Unapproved Teatro route accepted: '+path)
print('KINO_ARCHITECTURE_V170_GUARD_PASS',len(gate.approved_essay),flush=True)
