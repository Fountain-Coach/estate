# WIND-01 — Continuous Csound patches: private WLAN v191

**Date:** 2026-11-11. **Scope:** existing canonical Ubuntu Mac mini WLAN staging, `https://192.168.8.50:8243/teatro/learn/two-winds/`. **No production publication.**

## Original reported defects and intended outcome

- Wind I and II must **sustain until the learner presses Stop**, not automatically end after nine seconds. Continuous Csound owns nonperiodic gust motion; live learner gesture changes spectral turbulence without stopping playback. The two wind patches share the same audio engine, not two synthesized event recordings.
- Writer hears different experiences on iPhone and iPad. Preserve a conservative independent listening level and do **not** claim same loudness/timbre across speakers. Physical device audition and headphones comparison remain user acceptance, not a compiled claim.
- Voice is important experiential framing. The existing real `Fountain-Coach/SatzfunkPlayer@9b7a45564dc4d127be5f90b151648b6148bf4690` has `Studio (Csound)` default for admitted **recorded voice**; preserve BBC/EBU R128 *targets* (-23 LUFS integrated, -1 dBTP max true peak) with separate complete-programme measurement. No source-authorized spoken WIND-01 introduction exists in this slice. A browser Csound compressor is not certification and TTS is not a substitution. The voice requirements are pinned in `Fountain-Coach/teatro-ear/docs/ADR-004-voice-framing-and-broadcast-mastering.md`.

## Source and staging lane

- Native sound source: `Fountain-Coach/midi2-gpu-fabric@af6f0968d55fac872c38e0c29227a82e37846100`, branch `feat/teatro-ear-continuous-winds-voice`. `apps/teatro-stage-web/src/ui/Wind01Lesson.tsx` and `src/lesson/wind01Gesture.ts` / `wind01Orchestra.ts` implement no timer, ongoing Csound gust, live gesture and separate listening level.
- Existing **active** WLAN predecessor observed by independent SSH: `shared-shell-20261111-v190-koken-head-boxers-e65d62d` source lock SHA256 `289a242255057dca8e26f85147cd0cce2fe636889eb0dbacef342463272b98f6`. v190 preserves NOISE-01, other works, Koken historical audiovisual media and Fountain Press. Neither a new server nor a public Caddy route is needed.
- Planned v191: `shared-shell-20261111-v191-wind-continuous-af6f096`. Replace only `teatro/learn/two-winds/index.html`, add two content-hashed JS files. Preserve all predecessor bytes and previous Wind/Noise chunks. Add a finite `wind01V191Continuous` source-lock record and inherited SHA-pinned guard `serve_wind01_continuous_v191.py` chained to existing `serve_koken_head_boxers_v190.py`.
- Procedure: `staging/teatro_ear_wind01_continuous_v191.py` from this estate branch. It uses the **existing** authenticated SSH/rsync owner-WLAN release, same two systemd services, immutable release, hash check and rollback. It does not claim a native public EstatePublisher/Caddy receipt.

## Governance reading record

**Chapters read:** 07 bounded per-lesson scope and source owner, 08 independent code/browser/audio/physical-device witnesses, 151 Csound Teatro semantic authority, 158 immutable static release without FountainStore.
**Forbidden:** replacing readers, modifying Koken/NOISE/Bookshelf media, inventing a new synth or unauthorized voice, treating a Chrome AudioWorklet witness as iPhone/iPad acceptance, or treating staging as public publishing.
**Conflict:** earlier WIND-01 nine-second events were governed test candidates; writer now explicitly chooses continuous sound. Overwrite only this specific lesson route. The existing BBC-targeted voice processing is for incoming recorded voice, *not* a generic wind master.
**Excluded:** voice recording/public media rights, Fountain Host, engraving, production release, physical iPhone/iPad acceptance and broadcast loudness certification.

## Acceptance

Source tests `30 passed / 1 skipped`; Vite build PASS; no WIND-01 TypeScript errors (34 older repository errors remain). Local Chrome real WebAssembly/AudioWorklet remains active past 12 seconds; Wind I→Wind II switch, learner slider movement, independent listening level, stop silence and tablet-sized view verified. Exact staging terminal receipt and independent HTTPS readback/browser proof are recorded only **after** activation. No full musical acceptance until the author listens on actual devices.
