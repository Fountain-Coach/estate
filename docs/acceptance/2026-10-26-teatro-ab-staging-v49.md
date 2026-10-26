# Teatro A/B Soft Mutation and Preset Bank — verified owner-WLAN staging v49

**Date:** 2026-10-26  
**Mode:** owner-controlled, private WLAN staging; no public production publication.

## Observed release identity

- Canonical estate environment: `Fountain-Coach/estate/staging/environment.json`, logical entrance `http://benedikt-Macmini.local:8200/estate/`; running Ubuntu MacMiniDocker, `fountain-shell-acceptance-preview.service`.
- **Active immutable release:** `shared-shell-20261026-v49-teatro-ab-scenario-063c1d8`.
- **Verified predecessor and retained rollback:** `shared-shell-20261026-v48-teatro-ab-morph-1f3d2e2`. Earlier v47 was also preserved, not overwritten.
- **Stage route:** `http://192.168.8.50:8200/teatro/experiments/classic-techno-deck/` (read-only; HTTPS is necessary for browser Csound AudioWorklet execution).
- **Playable HTTPS route:** `https://192.168.8.11:8443/teatro.fountain.coach/experiments/classic-techno-deck/`. This is a *secure projection through the existing legacy TLS gateway* of the same active staging bytes; not another canonical stage, public DNS release, or new server. The owner's WLAN certificate authority must be trusted by each client.
- **Owner source:** `Fountain-Coach/midi2-gpu-fabric`, commit `1f3d2e2541b4bdbf9a96f149a4f54abc80bd860e`, `apps/teatro-stage-web` on branch `codex/teatro-ab-morph-preset-crossfade-20261026`.
- **Authored Scenario:** `Fountain-Coach/teatro.fountain.coach`, commit `063c1d8feab5a906b0612a9e25bd705dac26aae3`, `scenarios/csound-teatro/classic-techno-deck.live.json`.
- **Unchanged HTML source SHA-256:** `933abd5ee0755b3b41f2457ccc953572a599713a1bc88e306b10525a9a2d26df` on Git-derived build, stage HTTP readback and HTTPS mirror.
- **Updated staged Scenario SHA-256:** `fbf75e20b36206bf9057ccdfaa00226b7b93ef989c490caa1730ec0024989642`. Its versioned Scenario now accurately describes the A/B patch graph topology and the four performance operations. Status remains `candidate-unadmitted`.

## Scope and immutable lineage

From already-accepted stage v48, v49 changed only the two authored route metadata files `teatro/experiments/classic-techno-deck/scenario.json` and `release.json`, plus additive candidate `source-lock.json`. The six visible/audio route files and the rest of the estate were byte-preserved. Prepared with hardlink snapshot and **atomic replacement** of modified hardlinked files so the retained v48 source was not overwritten. Existing user systemd stage service restarted after symlink activation; previous release remains rollback-ready.

A first post-restart readback happened before the HTTP socket was listening, and **v48 was rolled back immediately**. The second attempt used a bounded readiness poll on the same established service and passed. No new security ceremony, stage server, account or deployment runtime was introduced. The original staging entry and every other checked estate route were preserved.

## Functional Definition of Done — verified after v49 activation

- **Csound itself:** two independently stateful synthesized six-strip patch graphs inside **one** original @csound/browser AudioWorklet. A real Csound `instr 900` uses `cos(π x / 2)` and `sin(π x / 2)` to blend their stereo PCM outputs. Not two player applications or an extra engine.
- **Soft Mutate All:** bounded perturbation of all continuous parameters, including tempo, six channel faders, filter, drive, delay, swing, master, and Ear depth; mute/solo/routing do not mutate randomly. Smoothstep morph durations available: 2, 4, 8, 16 seconds.
- **Presets:** eight named factory patches, four browser-local stored user slots; recall morphs without stopping playback.
- **Clone:** copy selected A to B (or B to A) as a complete, independent patch; later sound edits change only the selected patch.
- **Ear:** actual Ear AudioWorklet hears Csound's final crossfaded output and supplies bounded RMS control to the two individual bass graphs; no raw PCM feedback wiring.
- **Live Chrome acceptance at active HTTPS route:** secure context; no puppet; six mixer strips; eight factory/four user presets; Csound A/B playback and **234 real Ear windows, RMS 0.0078**, live follow signal; A filter mutated from 0.54 to 0.44; B independently retained 0.54 until cloning; B became 0.44 on clone and mutated to 0.35; a full A/B real-audio crossfade with B master-zero silence and subsequent sound return; factory preset recall, user slot store/re-recall, and persistence across reload. Stop closed the AudioContext and Ear returned to zero. At 390px width there was zero horizontal overflow. **No HTTP or page errors** during the acceptance run.
- **Native Csound** 6.18 syntax check zero errors. **Vite production build** passed. **10 targeted Vitest tests** (patch model + Ear feedback) passed. Project-wide `tsc --noEmit` was not asserted to pass; historical unrelated typing errors in the older stage UI remain outside this route acceptance.
- **Post-activation estate preservation:** canonical stage service active; both private HTTP and TLS route respond 200 with SHA agreement; eight root routes `/estate/`, `/book/`, `/governance/`, `/midi2/`, `/instruments/`, `/teatro/`, `/pointer/`, `/solstice/` each respond 200.

## Proof boundaries

- **Actual live browser rehearsal accepted, not native Scenario admission.** The existing specialized 0.1 Scenario checker is tied to the separate Composing-by-Ear fixture, so neither Git validity nor browser audio authorizes a native Csound Teatro Scenario run. No native FCIS Scenario receipt, MIDI2 hardware discovery, MIDI-CI transaction, or FountainStore admission is claimed.
- **Not an iPad Safari witness:** actual Chrome on the Mac, including a 390px mobile viewport, was exercised. Native iPad Safari WebAudio and certificate trust on that iPad have not been observed.
- **Not a public production release:** no DNS/Caddy production publication, no typed public EstatePublisher receipt, and no public redistributive rights change.
- **Rollback:** atomically point `/home/benedikt/estate-shell-acceptance-staging/current` to v48, restart the preexisting user service and recheck HTTP readback; atomically restore TLS alias `classic-techno-deck` to `classic-techno-deck-v48`. Both exact immutable predecessor trees are retained.
