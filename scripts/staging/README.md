# Owner-WLAN editorial stage projections

These scripts document and reproduce the **28 October 2026 v57 staging candidate** from the independently observed, immutable v56 predecessor. They are **not** an additional publisher, a source-owner replacement, or an authorization to mutate production.

`compose_author_entrance_v57.py` projects the approved one-person homepage and authentic Fountain Press catalogue into an isolated copy of the existing staging tree, preserving the complete later essay bodies and media. Its exact author-source revision is `aa38389ba2ef9070d91a36c169e74902ed3b096b`.

`project_private_wlan_chrome.py` adds the shared headmast, nine-entry canonical estate reel, Info and legal footer to compiled stage HTML while preserving article text, images and native reader controls. Labels, canonical destinations and icon identities are read from the **Estate source-owned** `navigation/canonical-reel.v1.json`. This script must never be used to overwrite a publisher's Git source files.

`repair_wlan_assets_v57.py` resolves bounded source-proven stage-path defects in Book links, the original /ground artwork, and essay link aliases for this v57 candidate. It is intentionally release-specific; it is not a broad repair or source-authority override.

`check_private_wlan_chrome.py` runs structural tests on every compiled HTML page. `witness_wlan_v57.py` performs independent HTTP/SHA-256 readback after the private release is activated. Its one intentional compatibility exception is `/pointer/`, a route that the existing stage router serves as the identical `/works/` projection.

The release inventory, **all 509 route results**, Chrome viewport checks and typed receipt are preserved privately on the owner-controlled Mac mini at:

`/home/benedikt/estate-shell-acceptance-staging/receipts/20261028-v57-author-led/`

Use [the v57 release record](../../docs/acceptance/2026-10-28-v57-wlan-release.md) for exact source pins, release identity, verified counts, SHA-256 digests, activation, rollback identity and non-production boundaries.

To build any further release, first confirm the **actual** current predecessor and its source locks. Work on an independently copied, unmodified stage predecessor; run the source and full-route checks; deliver through the existing owner SSH/rsync stage transport to a new immutable release name; inspect the release under the server's native preview validator; activate the named release atomically; restart the preview service if the service resolved `current` on startup; then independently verify the running stage and preserve the previous release for rollback. Do not infer completion from a Git push or a local preview.
