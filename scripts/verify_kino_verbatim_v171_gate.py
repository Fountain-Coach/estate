#!/usr/bin/env python3
"""Independent fail-closed v171 source citation admission and negative route checks."""
import importlib.util,sys
from pathlib import Path
B=Path('/home/benedikt/estate-shell-acceptance-staging')
module=B/'reader_provenance_gate_v171_candidate.py'
spec=importlib.util.spec_from_file_location('reader_provenance_gate',module)
guard_lib=importlib.util.module_from_spec(spec)
sys.modules['reader_provenance_gate']=guard_lib
spec.loader.exec_module(guard_lib)
candidate=B/'releases/shared-shell-20261106-v171-kino-verbatim-f50d16c'
gate=guard_lib.ReaderProvenanceGate(B/'releases'/guard_lib.ACCEPTED_STAGE,candidate)
approved=[
 'estate/index.html','estate/assets/linotype/reading-first-app.js',
 'estate/assets/instruments/kino-verbatim-bridge.js',
 'estate/media/kino/history/kino-history-groove.m4a',
 'estate/media/kino/history/kino-history-memory.m4a',
 'estate/media/kino/sound-craft/a-literal.m4a',
 'estate/media/kino/sound-craft/b-directed.m4a',
 'estate/essays/a-sound-must-earn-its-place/media/kino-international-night-20261106.jpg',
 'estate/essays/a-sound-must-earn-its-place/media/kino-international-architectural-plate-20261106.jpg',
 'teatro/interludes/kino/press-citation/manifest.json',
 'teatro/interludes/kino/press-citation/plates/v156.png',
 'teatro/interludes/kino/press-citation/plates/v158.png',
 'teatro/interludes/kino/press-citation/v156/index.html',
 'teatro/interludes/kino/press-citation/v156/assets/sampler-v2.mjs',
 'teatro/interludes/kino/press-citation/v156/assets/ear-original.js',
 'teatro/interludes/kino/press-citation/v156/assets/groove/bass-d2.m4a',
 'teatro/interludes/kino/press-citation/v158/index.html',
 'teatro/interludes/kino/press-citation/v158/assets/ambience-v158.mjs',
 'teatro/interludes/kino/press-citation/v158/assets/ear-original.js',
 'teatro/interludes/kino/press-citation/v158/assets/midnight/midnight-cylinder.m4a',
 'estate/evidence/press-kino-verbatim-v171.json'
]
for rel in approved:
 gate.check('/'+rel)
 print('ACCEPTED',rel,flush=True)
for rel in (
 'teatro/interludes/kino/press-citation/unreviewed.js',
 'teatro/interludes/kino/press-citation/v156/assets/fake.wav',
 'estate/assets/instruments/other-reader.js',
 'teatro/interludes/kino/live-csound/unapproved.js'):
 try:gate.check('/'+rel)
 except guard_lib.UnadmittedReaderRoute:
  print('REFUSED',rel,flush=True)
 else:raise AssertionError('Unapproved source accepted '+rel)
print('KINO_VERBATIM_V171_ADMITTED',len(gate.approved_essay),flush=True)
