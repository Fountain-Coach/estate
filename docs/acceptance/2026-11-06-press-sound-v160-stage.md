# Fountain Press sound essay: v160 WLAN staging acceptance

**6 November 2026.** Private author-WLAN editorial proof only. **Public production was not changed.** This is the existing Fountain Press Linotype Reader and its existing publication-notes/folio-return interaction, not another reader.

## Source and editor boundary

- Essay: *A Sound Must Earn Its Place*, transferred verbatim from the implementation brief. Source SHA-256: `53b5f7369f68548f211571bdaf5fa4d92bbc85b3fed30aedf8839eaf8e293b7c`.
- Content source owner: `Fountain-Coach/fountain.coach`, `9d833024e202fa37653af3b46f9862d5fc2e82d8`, branch `codex/essay-sound-proof-20261106`.
- Existing relationship-data adapter source owner: `Fountain-Coach/fountain-press`, `71bc32b7ed78798b886c865bb1168cd4f9027a92`, branch `codex/press-relations-20261106`. This pure adapter remains source-level; stage uses the existing `fountain.coach` Reader, not a second system.
- Original Reader composition, accepted five-essay gallery, first-readings inventory, and private Kino audio assets are unchanged. The new volume is explicitly a private **unpublished editorial proof**, not a sixth admitted Essays publication and not an approved book cover.
- The *Audio Production and Artistic Acceptance* standard remains a proposal, not current Governance. The private Kino audio study has no external navigation link. The related public readings are `https://fountain.coach/essays/the-ear-that-learns/` and `https://fountain.coach/essays/the-door-is-a-score/`, observed HTTP 200.

## Native stage lineage and source admission

- Canonical stage: owner Mac mini `192.168.8.50`, existing `fountain-shell-acceptance-preview-https.service` (port 8243), companion HTTP port 8200; one active `current` symlink.
- Predecessor: `shared-shell-20261105-v159-kino-midnight-cylinder-e2f5dd2` (retained, approximately 281 MB).
- Active: `shared-shell-20261106-v160-press-sound-essay-proof-9d83302`.
- Entry: `https://192.168.8.50:8243/estate/#/read/essay--a-sound-must-earn-its-place`.
- The existing operational `reader_provenance_gate.py` was extended, not replaced by a bypass. It first proves the exact v159 predecessor through the full previous admission chain; demands a SHA-pinned v160 source-lock; verifies the new editorial admission, rights-status receipt, exact changed assets, added receipt, and every previously staged file preserved byte-for-byte. The current guard SHA-256 is `88bb63962a3ee85f84a6e8a17820f44ecd6c7f56b66a29b6febb65095e9e5bd0`. Its previous active version remains as `reader_provenance_gate.py.pre-v160`.
- New candidate source-lock SHA-256: `c0b914586f4cfbd3312fe71b8579f2682de20479646252fdc65606d371553324`.
- Exact changed source bytes: `estate/index.html` SHA-256 `7cd67ccb9a8899230b887226a5bc628d23b88613c08385631a9112827518265e`; `estate/assets/linotype/reading-first-app.js` SHA-256 `83c83d45c1b11db03d0227b18f3daa6f6a481e757faeccc60b1fb1dd06d32cc9`. Added `estate/evidence/press-sound-essay-proof-v160.json` SHA-256 `e8f26a9672ec5cbedfe2799d43bd619e3abb9faca91d4fd8aa8b633073892d38`. Only other changed file is `source-lock.json`; all prior release files remain unchanged.

## Acceptance and limitations

- Native guard tested against the complete immutable release: `GUARD_V160_ADMISSION_PASS 20`. The running guard served predecessor v159 over HTTPS 200 before v160 was activated.
- Atomic `current` symlink now resolves to v160; both existing staging services restarted, active. The predecessor directory and old guard are retained for rollback.
- Independent HTTPS readback of actual served index and app returned HTTP 200 and matched both candidate SHA-256 digests above. Existing `/estate/`, First Readings and The Ear That Learns stage routes plus the proof receipt returned HTTPS 200.
- Real browser, no network intercept: `PRESS_LIVE_STAGE=1 node scenarios/reading-first-20261101/editorial-proof/test_stage_proof.cjs` passed 3/3 (768×1024 portrait, 1194×834 landscape, 390×844 phone). All 61 source-addressed blocks, notes, two public related-reading URLs, return to original volume, no JS exceptions, and no horizontal page overflow were checked.
- Real browser related link test: `node .../editorial-proof/test_related_round_trip.cjs` passed. It opened the public *The Ear That Learns* URL and browser Back restored the original `a-sound-must-earn-its-place.title@0` source address and existing Reader volume.
- This is **WLAN staging acceptance**, not a native physical-iPad Safari/VoiceOver witness, Store manuscript admission, adopted Governance standard, public-domain release, or authorization to distribute private recordings.

**Rollback**: atomically restore `current` to the immutable v159 predecessor and restart the existing HTTP/HTTPS staging services. Restore `reader_provenance_gate.py.pre-v160` only if necessary to revert the guard. No new service or DNS route was created.
