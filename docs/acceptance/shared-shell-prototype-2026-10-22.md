# EstateShell shared masthead/reel/footer — acceptance candidate (22 October 2026)

**Status: tested local candidate, not a published release.**

## Scope
This work follows the observed inconsistent top reel and footer across Fountain Coach, Solstice and Teatro. Linotype remains Fountain Press's book compositor; Reframe owns Bookshelf membership and writer admission; EstatePublisher remains the *separate* domain publication authority.

A dedicated feature branch contains a prototype source-preserving shell projector at `scripts/estate_shell.py`. It wraps an admitted body with one masthead, one semantic nine-identity reel, and one four-region footer. The public-site source and native iPad acceptance must not be inferred from a successful Python projection.

## Verified standalone candidate
The separately generated proof package `estate_shell_acceptance_candidate_2026-10-22.zip` includes exact source snapshots of two **public pages** (Fountain Coach and First Reading), a reusable shell/CSS fixture, deterministic source-preservation receipts, structural and negative-control checks and browser images. The package's original source copies are read-only proof inputs, not a new publication authority.

- 15/15 Python regression tests pass: reel order and membership, footer slots, false Status icon, wrong active domain, missing Status footer, duplicated shell, forged identity, source content integrity, Reframe/publication split.
- 2/2 structural checks pass; both pages share exact shell CSS/logo digests.
- Chromium in-memory rendering: eight cases across desktop, iPad landscape, iPad portrait and phone, **zero measured shell-parity failures** after correctly comparing **the same inactive reel icon** rather than an active icon against an inactive one.
- **Caveat**: Admin policy blocks browser navigation to `127.0.0.1`; in-memory snapshots removed original CSP metadata solely for offline CSS injection. These cannot prove real deployed CSP compatibility, nor native iPad Safari or a production release.
- The explicit publication gate remains **FAILED / not admitted**: missing native Safari/iPad transition evidence and an independently witnessed EstatePublisher terminal publication receipt.

## Governing design decision
The estate may have **three primary editorial entrances** yet **nine addressable destinations** in the top rail. These are not interchangeable concepts; legal Status is footer-only. No work becomes a Bookshelf book merely by appearing in Git, no book creates a domain automatically, and original Satzfunk audio and translations stay private until separately cleared.

## Still required
1. Resolve source/live ownership drift, use one approved versioned visual shell under each domain owner rather than public-byte copying.
2. Verify actual page controls and footer/reel geometry on all nine public roots plus deep routes, strict CSP, across native iPad Safari states.
3. Implement a real EstatePublisher scenario accepting measured browser/AX/VRT evidence and negative controls; do not confuse existing scenario declaration tests with runtime browser acceptance.
4. Admit releases through the typed Store/publisher route with exact rights, HTTPS/DNS/TLS readback, rollback and versioned evidence.

**No DNS, Caddy, media, public site or Reframe manuscript was changed.**
