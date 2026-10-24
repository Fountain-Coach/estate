# Instruments v20 — shared semantic social identity, WLAN only

**Date:** 24 October 2026. **Entry:** http://192.168.8.50:8200/instruments/ (owner WLAN only).

This follows v19, whose independently verified instruments semantic source/three SVG logos are documented in 2026-10-24-semantic-instruments-v19-wlan-stage.md. It closes one retained page-metadata inconsistency: the original technical catalogue's social card remained referenced even after the new logos and three-feature editorial body were staged.

Source owner revision: Fountain-Coach/instruments.fountain.coach commit 224517cb4e3c6d93a7fb3d9b190ab6f829017dbf.
Current immutable staging release: shared-shell-20261024-v20-semantic-social-224517c.
Verified predecessor: shared-shell-20261024-v19-semantic-instruments-d45fa28 (retained).
Observed production remains: estate-20261024-v14-satzfunk-reel-instruments (not changed).
New authored triad image assets: instruments-triad-social.svg and derived 1200x630 PNG, using the same three Sing, Ear and SatzfunkPlayer marks. Metadata points at the eventual canonical HTTPS image location, which is NOT yet publicly deployed.

The bounded v20 candidate preserved every predecessor file except instruments/index.html and source-lock.json and added the two social image assets. Promotion used existing SSH, rsync, SHA-256, atomic symlink and restart of the existing pinned-root HTTP preview service. There was no typed EstatePublisher WLAN receipt, no newly installed service and no public deployment.

Independent HTTP readback confirmed:
- /instruments/ SHA-256 beb96754e4eddc5fdb558209e4856b80ae8f29d54c89cdc161bf1e465025b4ec
- /instruments/assets/instruments-triad-social.png SHA-256 df474597b5f4dc400756f7f5316359bab9c45ba810f617467c61ccfe0505d410
- Three earlier logo SVG paths remain live, with the previously witnessed hash values.
- HTTP status 200, noindex and no-store; the original production release symlink was independently checked and unchanged.

The visitor-visible final staging revision is v20. Neither staging itself nor this receipt constitutes accepted public release or demonstrated native iPad/Safari visual parity.
