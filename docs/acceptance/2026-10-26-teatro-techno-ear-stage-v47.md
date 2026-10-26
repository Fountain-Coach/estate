# Teatro Classic Techno Deck — Ear feedback, WLAN stage v47

**Date:** 26 October 2026  
**Scope:** Owner-controlled WLAN staging only. No public production publication.

## Release

- Canonical staging owner: `Fountain-Coach/estate/staging/environment.json`.
- Running staging service: `fountain-shell-acceptance-preview.service` on the registered Ubuntu Mac mini.
- Predecessor (observed before activation): `shared-shell-20261026-v46-governance160-editorial-fbc957d`.
- Activated immutable release: `shared-shell-20261026-v47-teatro-techno-ear-dd34fd8`.
- Native source: `Fountain-Coach/midi2-gpu-fabric`, commit `dd34fd84556ceb5fb51b5d3af2db10dd0c014d2c`, path `apps/teatro-stage-web`, branch `codex/teatro-classic-techno-ear-20261026`.
- Authored scenario: `Fountain-Coach/teatro.fountain.coach`, commit `724fa6783164b1a6ca2c741b80814fe5cee7fd54`, `scenarios/csound-teatro/classic-techno-deck.live.json`, branch `codex/teatro-techno-ear-scenario-20261026`.
- Delta: six new files under `teatro/experiments/classic-techno-deck/` plus additive `source-lock.json` release metadata. All 1,077 original predecessor files preserved.
- HTML artifact SHA-256 (source, stage, and readback): `e4df008a057d8836520c7d0182ac2e7b832975bf3f398789e8c260fdb564e433`.
- Private canonical route: `http://192.168.8.50:8200/teatro/experiments/classic-techno-deck/`. HTTP serves the deck but **cannot run WebAudio AudioWorklet**.
- Private secure audio route: `https://192.168.8.11:8443/teatro.fountain.coach/experiments/classic-techno-deck/`. This uses the **pre-existing legacy TLS gateway** for secure playback of the identical staging files; it is **not** the canonical estate entrance nor a new public environment. The local CA must be trusted on iPad/Safari.
- The v46 release is retained unchanged for rollback.

## Acceptance

- Production Vite build succeeded. Three focused Ear-feedback Vitest tests passed. Native Csound syntax check: zero errors.
- First full real Chrome localhost cycle exposed and led to correction of an uncompiled Ear AudioWorklet URL, an unattached worklet sink, and optional Csound cleanup handling. Rebuilt after fixes.
- On actual staged HTTPS route **after activation**, Chrome reported `isSecureContext=true`, six channel strips and no puppet canvas; Play started `@csound/browser`; 357 real Ear analysis windows reported live nonzero signal (`RMS 0.0174`, `peak 0.0550`) with nonzero Ear→Csound follow (21%); feedback Off disconnected and On returned nonzero follow (18%); Stop closed AudioContext, returned zero Ear RMS and no signal; zero page errors and zero HTTP failures; at 390 px there was no horizontal overflow.
- After atomic activation and systemd user-service restart, active symlink pointed to v47, server returned the exact artifact digest, and all eight previously checked estate entrances (`/estate/`, `/book/`, `/governance/`, `/midi2/`, `/instruments/`, `/teatro/`, `/pointer/`, `/solstice/`) returned HTTP 200.

## Evidence boundaries

- Scenario status is **candidate-unadmitted**. The existing Teatro 0.1 source checker is hard-coded to the separate Composing-by-Ear fixture; this new authored scenario was not native-admitted. The verified result is an actual **Csound/Ear browser rehearsal**, not evidence of MIDI 2.0 hardware discovery, MIDI-CI negotiation, FountainStore admission, or public publication.
- TypeScript project-wide `tsc --noEmit` still reports existing errors in puppet/physics/WebMidi/test code; it did not pass and must not be presented as passing.
- Chrome desktop/mobile-viewport acceptance is **not native iPad Safari acceptance**. The local CA trust on the user's iPad is not independently verified.
- The deployment used the existing authenticated SSH transfer, immutable release, atomic symlink and independent readback. No typed public EstatePublisher deployment receipt is claimed.

## Rollback

Atomically reset `/home/benedikt/estate-shell-acceptance-staging/current` to v46, restart `systemctl --user restart fountain-shell-acceptance-preview.service` on MacMiniDocker, and verify the canonical entrance. The v46 predecessor is preserved.
