# A Sound Must Earn Its Place — v165 staged Csound/Satzfunk A/B

**Verified on 6 November 2026.** **Private owner-WLAN stage accepted; public production untouched.** The work is a revised **editorial proof**, not a sixth publicly admitted essay, an approved audio master or a native admitted Csound Teatro Scenario.

## Outcome and source custody

The writer rejected the over-edited essay and the unrelated Sing examples. This release retains the same Fountain Press Linotype Reader, removes the Sing samples from this proof, and places **two original Csound recordings of one sixteen-second Kino After Dark score** at the point where the essay discusses sound. The audition is A (dry, literal) versus B (more articulated material, stereo movement and room response). Neither version is declared artistically superior without listening.

- Essay source owner: `Fountain-Coach/fountain.coach@eb45a85d7485e7e8e4b093bc259e4f6c8075ec6d`; revised editorial source SHA-256 `b1da1f4c3651e84eb55e104d02d311ebd047278a046f427563600e091348ea44`, fifteen continuous prose blocks, same title and closing point.
- Sound source owner: `Fountain-Coach/teatro.fountain.coach@1d8f6345ee0cb9fc7b8802cf2f3e0cdd6fc14b03`; score SHA-256 `21ae0eda6621d1b2ff90a1baaa792def576d7399da62cc90609022d854abda49`.
- Csound source A: `1f21a92ded2ceeaa699111254987c1d411bb740ebebfc140ef1b919ca9738ab7`; staged AAC SHA-256 `f8db7d1cee00b6e346fb400567c2868e99a97cf4c51007b3fe47fe542dbde427`.
- Csound source B: `928656e3a6e8a6a2edf7ea9fad55b844afca1b27bd4af94140a63b3b5850a202`; staged AAC SHA-256 `5413a93ba9a1c471e2178f93f099e412b464f2e25447b8a7f4ebb960b298d94b`.
- Actual native Csound rendering: stereo PCM at 48 kHz, 16 seconds; AAC playback duration 16.064 s due to encoding; RMS A 0.08193, B 0.08212. The levels are approximately matched; objective acoustics do not establish artistic quality.
- Reuses the existing `SatzfunkMediaElement` and its private rehearsal-grant source hash. No second Player, Reader, public sample, new origin, original copyrighted recording or private sample extract.

## Native staging acceptance

Exact predecessor: `shared-shell-20261106-v164-governance-social-b7b1dee`, retained unchanged. New active immutable release: `shared-shell-20261106-v165-satzfunk-csound-ab-eb45a85`.

- Candidate source changes: exactly `estate/index.html` and existing `estate/assets/linotype/reading-first-app.js`; additions: two Csound CSDs, two original AAC derivatives, one source manifest, one private Satzfunk rehearsal edition, and a stage receipt.
- Existing production-derived Reader engine, authored library, Governance, First Readings, other essays and private recordings preserved byte-identically.
- Source-lock SHA-256: `1f369206aef342b8423f959df437e1c069e0312c5ee75ac1f8a947ec4d0c3a36`.
- Receipt `estate/evidence/press-sound-csound-v165.json`: SHA-256 `9e120b320e7f03206756d4a12d3d81b5bc94b6c1683259603616ef1f22cd0836`.
- Existing `reader_provenance_gate.py` extended with one exact-source v165 acceptance, **not bypassed**; `V165_COMPLETE_NATIVE_GUARD_PREFLIGHT_PASS 352`, including negative tests rejecting unreviewed media/card paths. Guard SHA-256 `3a350aeeffb0a7248283df5405d62f7760dfefb1c7491bc6987554ddf9a5daf7`. The previous operational guard remains as `reader_provenance_gate.py.pre-v165`.
- Atomic `current` activation verified and both existing user services active: HTTP 8200 and HTTPS 8243. The initial live browser attempt hit the normal slow post-restart guard initialization before the servers announced READY; subsequent live tests passed.

## Independent live readback and listening

A Mac performed five independent **actual** HTTPS readbacks with matching SHA-256 (no request interception): `/estate/` SHA `5a2a8c084d806c515890e276be445fe34c21ca0243948d8cc088bcc70e65ab97`, Reader app SHA `46876ca7b54c5f26df2372f1ec037871e61f6773a406ff41ec32a634337b7831`, both AAC hashes above, and receipt SHA above.

Source-over-real-WLAN browser preflight passed **3/3** viewports. Independent **live HTTPS** Chromium acceptance without interception passed **3/3**: 768x1024 portrait, 1194x834 landscape, 390x844 phone. Real audio duration 16.064 seconds for both; playback position advanced for both (roughly one second), switching to B paused A, final stop paused both, correct independent source identities, visible on an actual composed Linotype folio, no JavaScript error or viewport overflow. Source identity and site release were independently checked. Four focused source tests passed.

**Private staging URL:** https://192.168.8.50:8243/estate/#/read/essay--a-sound-must-earn-its-place

**Excluded / not claimed:** public production or DNS release; author approval of prose or sound; listening through physical iPad speakers, Safari / VoiceOver acceptance; live browser Csound synthesis; a native Csound Teatro Scenario admission or instrument-to-Ear/UMP live-run proof. These recordings are *real offline Csound patch renders* played through source-bound SatzfunkPlayer, not a fabricated or fully-live Scenario.

**Rollback:** point `current` atomically at immutable `shared-shell-20261106-v164-governance-social-b7b1dee` and restart existing HTTP/HTTPS services; restore `reader_provenance_gate.py.pre-v165` only if necessary. Do not copy private WLAN audio to public production.
