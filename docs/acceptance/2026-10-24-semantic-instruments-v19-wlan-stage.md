# Semantic Instruments v19 — WLAN staging receipt

Date: 24 October 2026. This is private WLAN staging, not a public production release.

Author direction: replace the foreground of the former MIDI 2.0 technical catalogue with a semantic top-down presentation of Sing, Ear and SatzfunkPlayer, starting with three coordinated source-owned vector logos. The previous technical entries remain secondary historical links, not deleted source material.

Source owner: Fountain-Coach/instruments.fountain.coach, commit d45fa282361d7d74d6be998b57e3a495531383ea.
Staging identity: Fountain-Coach/estate/staging/environment.json; existing Ubuntu host MacMiniDocker, service fountain-shell-acceptance-preview.service, canonical path /instruments/ on port 8200.
Verified predecessor: shared-shell-20261023-v18-visual-1b75080, inspected by live symlink.
Active release: shared-shell-20261024-v19-semantic-instruments-d45fa28.
Live production release remains: estate-20261024-v14-satzfunk-reel-instruments.

The old main-body text was independently confirmed identical (normalized) across previous Git, public production and actual v18 staging. The new candidate was composed on that exact predecessor. Among 714 previous files, only instruments/index.html and instruments/assets/site.css changed, plus three new SVG logo files and the explicit source-lock delta. The entire rest of the shared estate, including shell, footer, other routes, assets and v18 rollback release, was retained.

Logo semantics:
- Sing: vocal source and radiating resonance.
- Ear: approaching sound-wave curves and a listening point.
- SatzfunkPlayer: composed still frame and playback timeline.

The page describes the evidence levels separately: Sing has native voice PCM/MIDI2 UMP tests; Ear has browser-local AudioWorklet and MIDI2 observation but not complete physical device acceptance; SatzfunkPlayer has its own software repository and eight tests but not yet automatic semantic poster extraction or MIDI2 instrument admission. Existing Codex Login, Semantic Browser and Csound AUv3 public technical pages are retained as secondary references.

Deployment transport: existing authenticated SSH, rsync, exact SHA-256 comparison and atomic symlink activation, followed by restarting the existing preview service because the serving process pinned the previous symlink target at startup. This deployment has independent HTTP readback but NO typed EstatePublisher WLAN receipt. Do not overstate this.

Independent WLAN HTTP readback, all HTTP 200 and exact SHA-256:
- /instruments/ — c2069fa01fd8e57fffb2c2710225b4a72dc40ccd392754603d1b7d7d261828e9
- /instruments/assets/site.css — 88c2891601afec5a7e57a0edfc253280d3bc87c6c9e2a63bc6f51756ec88ad66
- /instruments/assets/instrument-sing.svg — 4d3869a84d7340af2a2f8b68812847d0e23624aeca8dfadd98db2e07ace6334d
- /instruments/assets/instrument-ear.svg — 0fcc06bf68cda788e2a1ac47621d3142db2665d771633347112d2a87590bd3ee
- /instruments/assets/instrument-satzfunk-player.svg — dfb30a254ac51e3bd4185e7c8a1040dd13f30ac0d59da28e2966b511db06cad9

Other live staging routes /estate/ and /governance/ independently returned HTTP 200 and retained previous hashes. HTTP headers contain no-store and noindex,nofollow. The production Instruments symlink was independently verified unchanged.

Open: visual proofreading in native Safari/iPad, author acceptance of the three marks, and a separate future approval for public production promotion.
