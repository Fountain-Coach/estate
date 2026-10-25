# The Ear That Learns — canonical WLAN staging v31

25 October 2026 · Fountain-Coach/estate · **OBSERVED / PROVEN within private WLAN scope**

## Authorized goal and boundary

Publish the authored Ear/Sing essay first on the **existing canonical staging domain**, with navigation from the Fountain Coach landing and Essays collection and reciprocal links in Instruments. Public HTTPS production was not approved for promotion and was not modified.

Canonical registry: `staging/environment.json`; named SSH host `MacMiniDocker`, canonical service `fountain-shell-acceptance-preview.service`, URL `http://benedikt-Macmini.local:8200/estate/` (verified direct IP `192.168.8.50`). No additional service or DNS namespace was created.

## Verified source authorities

- Fountain Coach essay source: `Fountain-Coach/fountain.coach@39d75db8efdd1bcb763c4e9148b70a8375c81c0b`. New route: `site/essays/the-ear-that-learns/index.html`. The article is original authored editorial prose and remains separate from Ear recognition qualification.
- Instruments catalogue: `Fountain-Coach/instruments.fountain.coach@69ec0e5e87db33934463e0e29076cbbe4f5b2cd0`. Ear and Sing entries link to the essay.
- Estate staging registry parent before this record: `5fb64d1732d204efce13ac92099419fd64eb1bbf`.

## Production-first affected-scope reconciliation

Independent public HTTPS readbacks were made and checked again directly before activation. The published `/essays/` baseline was SHA-256 `30bf86c2c53e299cf60fe76410fd2fbd2c3257a08e10769c6fa2ef51ba6bfcbb`, with five existing gallery entries, **including** `/essays/the-composable-book/`. The latest Fountain Coach Git essay index did not yet contain that publicly released entry; consequently the candidate preserved the **live published gallery** and added only the new Ear/Sing editorial card. All six existing public essay routes were read as a baseline, including Composable Book, Reading Continuity, Teatro, Semantic Compilation and Reframe/Business Value. Existing public images and the Reading Continuity PDF were imported read-only, hashed, and retained. Public source CSS was the baseline for an essay-scoped stylesheet, with only the newly authored Ear/Sing plate rules appended.

The new article `/essays/the-ear-that-learns/` independently returned **404** on public HTTPS before and after stage activation. That is an observed missing route and a declared **new staging route**, not a public release. Production Instruments returned 200 and did not yet include the new essay links; its main authored text matched the current staged Instruments main text.

Published homepage HTML and the previously staged homepage differ as complete bytes because staging carries an admitted common shell, but their main editorial text was independently compared and matched. The old portal was **not** overwritten by a newer Bookshelf root. The existing stage portal received two bounded editorial links, preserving its adopted shell and all other publication identities.

This comparison is a witnessed/manual route-scoped production baseline and declared delta. It is **not a claim that a new native production-first guard was installed or executed**.

## Immutable staging transition

- Expected and observed predecessor: `shared-shell-20261024-v30-first-reading-safari-39904c5`.
- Active immutable release: `shared-shell-20261025-v31-ear-sing-39d75db`.
- Delivery: copy prior immutable release, then existing authenticated SSH/rsync for **23 source-locked overlay files**; verify all 23 transferred SHA-256 digests and the existing staging-server source-lock acceptance before activation. Preserve other domain files: Solstice First Reading, Teatro, Book, Governance, Pointer and MIDI2 were byte-identical to v30.
- Activation: the existing atomic `current` symlink and restart of the existing `fountain-shell-acceptance-preview.service`.
- The first attempt's immediate readback outran service readiness; its rollback **restored v30** and the service. A bounded retry on the same service succeeded. No new machinery was deployed.
- The active symlink was independently confirmed to point to v31; the service was active; v30 remains available for rollback.

## Independent live readback

After activation, from the Mac over the private WLAN, the running HTTP service returned all 22 publicly accessible changed files with **byte-for-byte SHA-256 equality** to the offline candidate; the 23rd overlay file `source-lock.json` remained unserved (404), as did the private `contract.json`. Resource GETs passed on the landing, collection, new essay, Instruments, Solstice First Reading, and Teatro pages. The following deep links were directly observed:

- `http://benedikt-Macmini.local:8200/estate/` — portal with links to Essays and **The Ear That Learns**
- `http://benedikt-Macmini.local:8200/estate/essays/` — six existing public essays plus the new article, retaining **The Composable Book**
- `http://benedikt-Macmini.local:8200/estate/essays/the-ear-that-learns/` — 200, complete article, staged page SHA-256 `941e8592a16004303ee5081e94a8fb50939aa332ff1020d4267b8e7c6c23c570`
- `http://benedikt-Macmini.local:8200/instruments/` — Ear and Sing reciprocal links to this same private article
- `http://benedikt-Macmini.local:8200/estate/assets/essay-site.css` — 200, source-scoped typographic plate styles

The canonical owner-WLAN service serves `X-Robots-Tag: noindex, nofollow`; no public production Caddy release, DNS mutation, private singer audio, or new MIDI transport occurred. No native Safari/iPad visual acceptance or typed EstatePublisher terminal stage receipt is claimed by this operation. It proves an authenticated existing-path SSH stage transition and independent live HTTP content/asset validation, not a universal FCIS certification.

## Result

**Staging publication succeeded, production unchanged.** Current author-facing WLAN entrance and affected routes are ready for editorial proofreading; release v30 remains the rollback target.
