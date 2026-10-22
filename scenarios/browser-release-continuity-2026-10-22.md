# R01 · Browser Release Continuity — Trust Without Cache Rituals

**Date:** 22 October 2026. **Stage:** verified on private Ubuntu LAN. **Public deployment:** blocked.

## Reader contract

A reader never has to clear Safari history, delete cookies, refresh repeatedly, restart devices or become an involuntary browser-test operator to receive a freshly delivered publication. An already-open page keeps its draft, reading position, audio and history intact. It identifies its own release and, when the originating server reports a newer one, calmly offers **Open current edition** without forcing a reload. When the server cannot establish authority, it reports **unverified**, never “fresh.”

This is a **publication-delivery scenario**, not a Reframe Bookshelf membership change, Linotype recomposition or new browser matrix.

## Machine-verifiable protocol

- Exact SHA-256 release IDs derived from source-tree digest, release purpose and shell asset digests.
- Immutable releases and stable versioned assets under `/__estate/<release-id>/` with long-lived immutable caching. Retain old assets for existing tabs.
- HTML and `/__estate/current.json`: `Cache-Control: no-store`. Return `X-Estate-Release`; the pointer endpoint additionally returns `X-Estate-Authority: source-locked`.
- Exact, validated and atomically switched `current` release symlink. Tampered file, inadmissible source, private WAV/MP4 inclusion, arbitrary pointer or missing digest **blocks** serving as current.
- Same-origin, Content Security Policy compatible browser script checks on initial document, Safari `pageshow`, focus, visibility return and quiet foreground interval, with cache-busting requests. Never erase browser state or force reload.
- A detected mismatch yields a non-modal `role=status` notice with deliberate ordinary navigation. An unexpected controlling service worker yields **unverified**.

## One causal test, fully agent-operated

Open A in a clean isolated browser; atomically switch to B without modifying A; check retained A reports stale and preserves an in-page unsaved-data marker; check a new isolated browser receives B; open B explicitly and preserve history; check Back does not misreport old A as current; deny the authority endpoint and prove freshness becomes unverified; restore A.

**Executed result:** 7/7 deterministic HTTP, integrity and security tests passed; 6/6 live Chrome browser transition checks passed. One screenshot and a JSON witness are held with the test run. Ubuntu stage at `http://192.168.8.50:8201/estate/`, under the separate service `fountain-release-continuity-stage.service`. Stage returned to release A following the test. No public estate host, Reframe work or original Satzfunk media was modified.

Baseline release A: `2e3c3b38e0c5ef5bce5c0b996451985372c8b068d34533828fd03eff0929c9c8`.

Simulated promotion B: `1e87dbe2bc7a127daf7ea52c479cc313f9fefeb2b7c85ef3b40ed3a2524bd602`.

Both contain the same source works. B is a controlled **release-transition test**, not a newly authored literary edition.

## Production trust boundary

The implementation is a **staged proof**, not an unconditional freshness guarantee. Older pages that never carried the client script cannot learn the protocol retrospectively. A browser-origin service worker with control over navigation can intercept traffic; the staged client refuses a freshness claim when controlled, but current production worker migration requires explicit planning. Cross-domain HTTPS release must have a trusted current EstatePublisher owner, source and rights admission, pinned shell and deep-route inventory, origin/browser readback evidence and a real rollback receipt. The retired `midi2-gpu-fabric/apps/estate-publisher` checkout must not silently become the GitHub-main publisher.

The pipeline must provide a single release certificate and **block promotion** on an unresolved condition. A green isolated test cannot, by itself, certify nine public domains or native Safari/iPad behavior.

**Done means the reader trusts the system, not that the reader becomes the system's test harness.**
