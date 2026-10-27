# The Door Is a Score — v53 opening and social-image staging acceptance

27 October 2026 · Fountain Coach estate · WLAN staging only. **Not a public publication or Facebook post.**

## Observable request and source

The essay at `/essays/the-door-is-a-score/` lacked its *top* illustration in the active private estate, and the existing social-image metadata still referenced the measurement waveform lower in the essay. The author asked for the opening image to follow the estate's social-publication semantics and supplied an authorized Safari Facebook session as a visual reference, not an instruction to post.

- Canonical source owner: `Fountain-Coach/fountain.coach`, branch `essay/the-door-is-a-score-20261027`, commit `b0a6cc7a2013e5e4a87c74ed95075435f35821ff`. The branch was pushed to the owner's GitHub remote; no main merge or public deployment was performed.
- Opening artwork: `site/essays/the-door-is-a-score/assets/teatro-door-score.png` (1774 × 887, PNG), SHA-256 `47791d9ac527641ae7b2cfe7ffe7111a99b9e39afaf89b28e53d4fa3d44cd4bb`.
- The source's opening `figure.door-opening-score`, essay gallery image, Open Graph image, and Twitter image all select that same asset. The measured `listening-score.png` remains in the Csound listening-study section with its own caption and measurement identity.
- The top artwork is an original contemporary *interpretive* Teatro graphic score, documented in the source repository under `docs/illustrations/the-door-is-a-score.md`. It is not an executable Teatro Scenario or a measured audio plot. Mac Safari screenshots of the author's Facebook stream were inspected; no third-party Facebook post image was copied into the artwork.

## Staging and readback

- Existing canonical WLAN host/service: `MacMiniDocker` / `fountain-shell-acceptance-preview.service` on `192.168.8.50:8200`; secure audio-compatible route at `192.168.8.11:8443`, both on the same owner-controlled estate staging machine.
- Predecessor: `shared-shell-20261027-v52-door-score-424e54d`. New immutable release: `shared-shell-20261027-v53-door-score-art-b0a6cc7`. Both the canonical current symlink and the existing private TLS mirror point to v53; v52 and the earlier rollback releases remain retained.
- Canonical staged route: `http://192.168.8.50:8200/estate/essays/the-door-is-a-score/`.
- Secure listening route: `https://192.168.8.11:8443/fountain.coach/essays/the-door-is-a-score/`.
- Actual route GETs returned HTTP 200. Both stage images returned 200 `image/png`, exactly 1,985,551 bytes, each matching the source SHA-256 above. The canonical essay gallery card returns the same source artwork and navigates to the secure essay.
- The canonical source and ordinary HTTP staging page retain `https://fountain.coach/essays/the-door-is-a-score/assets/teatro-door-score.png` as the Open Graph/Twitter image. The secure WLAN gateway deliberately rewrites both metadata URLs to its private `https://192.168.8.11:8443` image origin; that staging-only rewrite is not a source edit and does not make the image accessible to public Facebook crawlers.
- Mac Safari on the authorized machine rendered the essay opening and estate masthead with the artwork visible. Visual witness: `/Volumes/DockerDisk/codex-estate-runs/door-score-20261027/safari-stage-v53-window.png`. Native iPad Safari was **not tested**. Source-preservation verifiers for the original essay edition, reading continuity and Ear/Sing passed.
- Release diff was bounded to the essay HTML, its local CSS and new PNG, the gallery card, and the stage source lock. 1,103 other existing staged files were preserved; all existing source sounds, rendered studies, engine binaries and listening-score image are unchanged. No new service, credential, port, domain or publishing machinery was introduced.
- Stage terminal record: `/home/benedikt/estate-shell-acceptance-staging/receipts/shared-shell-20261027-v53-door-score-art-b0a6cc7.json`, state `active-verified`.

## Publication boundary and remaining work

The **public** `https://fountain.coach/essays/the-door-is-a-score/` and its image path returned HTTP 404 during readback. The source is ready with the correct social-preview metadata, but a public Meta/Facebook crawler cannot see a private WLAN release. Public promotion requires its own owner-authorized EstatePublisher operation, independent HTTPS readback and then an actual social-platform preview check. No Facebook post was created or changed.

This is a visual/metadata staging acceptance only. It does not establish OpenAI voice synthesis, automatic semantic interpretation, native Teatro Scenario admission, MIDI 2.0 dispatch, physical iPad acceptance, or finished SatzfunkPlayer integration.
