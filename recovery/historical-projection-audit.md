# Historical estate projection: public artifact comparison

**Archive evidence only — no ownership reassignment or release admission.**

Git source: [Fountain-Coach/midi2-gpu-fabric](https://github.com/Fountain-Coach/midi2-gpu-fabric/tree/aba0a0ea941a886642bb4d87df5bfd99f674c6d3/estate/sites) at immutable commit `aba0a0ea941a886642bb4d87df5bfd99f674c6d3`.

This audit reads the committed Git blobs, not the old worktree. Public files are fetched via bounded GET requests and compared byte-for-byte. Git-tracked archived pages are **not necessarily public obligations**; HTTP 404 can indicate never-published staging material.

| Public target | Tracked blobs | Exactly matching | Different bytes | HTTP missing | Transport/error |
|---|---:|---:|---:|---:|---:|
| book.fountain.coach/ | 54 | 31 | 23 | 0 | 0 |
| midi2.fountain.coach/ | 36 | 32 | 4 | 0 | 0 |
| works.benedikt-eickhoff.de/solstice/ | 109 | 66 | 38 | 5 | 0 |

## Recoverability decision

**Still BLOCKED.** An exact archival blob match proves one historical projection contains the observed bytes. It does not prove that the canonical owning repository can regenerate them or that the complete release inventory, offsite backups and dynamic dependencies exist.
Do not migrate content ownership to midi2-gpu-fabric merely because the root was found there.
The live `works.benedikt-eickhoff.de/solstice/` prefix is delegated content; `solstice.fountain.coach` is not assumed publicly reachable.
Diffs are evidence of divergent publication revisions, not a signal to overwrite either side.

## Unmatched public observations

### book.fountain.coach/

- `accessibility/index.html`: DIFFERENT (HTTP 200)
- `assets/estate-core.js`: DIFFERENT (HTTP 200)
- `capabilities/csound-auv3-instrument-boundary/index.html`: DIFFERENT (HTTP 200)
- `capabilities/reframe-to-reframe-peer-projection/index.html`: DIFFERENT (HTTP 200)
- `capabilities/scenario-runtime-midi2/index.html`: DIFFERENT (HTTP 200)
- `commands/commands/index.html`: DIFFERENT (HTTP 200)
- `commands/ground/index.html`: DIFFERENT (HTTP 200)
- `commands/pipeline-status/index.html`: DIFFERENT (HTTP 200)
- `commands/readings/index.html`: DIFFERENT (HTTP 200)
- `commands/threads/index.html`: DIFFERENT (HTTP 200)
- `compliance/index.html`: DIFFERENT (HTTP 200)
- `copyright/index.html`: DIFFERENT (HTTP 200)
- `csound-teatro/index.html`: DIFFERENT (HTTP 200)
- `governance/default-semantic-manuscript-projection/index.html`: DIFFERENT (HTTP 200)
- `governance/dynamic-midi2-instrument-factory/index.html`: DIFFERENT (HTTP 200)
- `governance/evidence-cohorts-as-publication-units/index.html`: DIFFERENT (HTTP 200)
- `governance/scenario-pipeline-factory/index.html`: DIFFERENT (HTTP 200)
- `index.html`: DIFFERENT (HTTP 200)
- `legal/index.html`: DIFFERENT (HTTP 200)
- `privacy/index.html`: DIFFERENT (HTTP 200)
- `scenario-driven-development/index.html`: DIFFERENT (HTTP 200)
- `scenarios/index.html`: DIFFERENT (HTTP 200)
- `sticker/index.html`: DIFFERENT (HTTP 200)

### midi2.fountain.coach/

- `assets/estate-core.js`: DIFFERENT (HTTP 200)
- `docs/README.html`: DIFFERENT (HTTP 200)
- `docs/generated/normative-coverage.html`: DIFFERENT (HTTP 200)
- `docs/spec-compliance-dashboard.html`: DIFFERENT (HTTP 200)

### works.benedikt-eickhoff.de/solstice/

- `assets/book-boot.js`: NOT_HTTP_200 (HTTP 404)
- `assets/book.css`: DIFFERENT (HTTP 200)
- `assets/book.js`: DIFFERENT (HTTP 200)
- `assets/linotype-engine.js`: DIFFERENT (HTTP 200)
- `assets/mobile-page-navigation.css`: NOT_HTTP_200 (HTTP 404)
- `assets/mobile-page-navigation.js`: NOT_HTTP_200 (HTTP 404)
- `assets/solstice-mark.svg`: NOT_HTTP_200 (HTTP 404)
- `editions/first-reading/candidates/chapter-wide/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2025-12-22-anweisung-an-den-schmerz/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2025-12-23-integration/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2025-12-28-renaturalization/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-01-08-vier-aussagen-zum-atherleib/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-01-22-three-floors/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-01-23-i-keep-moving/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-02-04-two-rooms/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-02-14-on-a-future-not-yet-drafted/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-02-28-no-optimize/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-03-16-the-teatre-of-the-mind/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-03-20-my-place-in-space/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-03-21-muttersprache/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-04-22-the-writing-hand/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-04-23-who-is-bee/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-04-30-about-writing-letters/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-05-01-a-score-before-production/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-05-25-seitenlicht/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-05-30-the-sheet/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-06-06-the-sentimental-machine/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-06-15-fck-frg-we-all-had-parents/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-06-24-prufe-dein-gewicht/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-07-21-everything-else-is-illustration/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-07-28-bees-journal/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-07-31-n-journal/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-08-17-the-scissors/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-08-19-six-panels/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-08-28-the-old-woman/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-09-04-the-strawberry/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-09-06-leselust/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/entries/2026-09-18-object-crossing-voice/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/index.html`: DIFFERENT (HTTP 200)
- `editions/first-reading/proof/archive/initial-coretext/index.html`: DIFFERENT (HTTP 200)
- … and 3 additional unmatched tracked blobs (see JSON)

## Safety and scope

Only the three named archival projection trees are checked. Public URLs are allowed only beneath their fixed configured host/prefix. Every request is capped at 30000000 bytes, 24 seconds, and moderate concurrency. No live files or credentials are uploaded. Results store only paths, checksums, HTTP evidence and Git identifiers. No SSH, DNS, Caddy, tunnel or production mutation.

Refresh observed bytes: `npm run recovery:archive-probe`; verify frozen report against the current Git blob identities: `npm run recovery:archive-verify`. Re-running the probe may produce different results if publication changes.
