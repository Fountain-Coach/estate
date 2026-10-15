# Fountain Coach: Three-front WLAN staging

The Ubuntu Intel Mac mini, `benedikt-Macmini.local` / `192.168.8.249`, serves the
**current GitHub-owned editorial estate** from a separate staging release.
This is NOT the public DNS or Caddy publisher and requires no Hetzner Git.

Publicly usable only **within the WLAN**:

1. **Fountain Coach**: http://192.168.8.249:8180/
2. **First Reading**: http://192.168.8.249:8181/editions/first-reading/
3. **Teatro**: http://192.168.8.249:8182/

All three header rail links are rewritten in the **disposable staging copy only**
to these three exact URLs. First Reading retains its author-owned original
Linotype reader, not a synthetic new shell. `status.fountain.coach` is still
footer/legal material and is not admitted as a fourth publication.

## Original sources

- `Fountain-Coach/fountain.coach` — `site/`
- `Fountain-Coach/solstice.fountain.coach` — `site/`; active authorial page
  `editions/first-reading/` (future `solstice.fountain.coach` DNS not assumed)
- `Fountain-Coach/teatro.fountain.coach` — `site/`
- `Fountain-Coach/estate` — `manifest.json` and these staging scripts.

The staging release on Ubuntu is:
`/home/benedikt/estate-three-front-staging/releases/20261014-three-front-github-v1/`.
The stable symlink is `/home/benedikt/estate-three-front-staging/current`.
Source commits and file counts are in `current/source-lock.json`; the SHA-256
inventories are in `current/manifests/`. The complete source inventories were
checked before the stage-only link rewrite.

`staging/fountain-three-front-stage.service` is installed under the Ubuntu
user's `~/.config/systemd/user/` and enabled. It serves three independent
site roots from a *single* Python process, bound only to WLAN address
`192.168.8.249`, on ports `8180/8181/8182`. Old estate staging ports
`8089` through `8096` are left untouched. Check using
`systemctl --user status fountain-three-front-stage.service` over SSH.

## Repeatable refresh

1. Update and review each owning GitHub repository independently; ensure
   `site/` and `publication-files.sha256` agree at a pinned 40-character SHA.
2. Create a **new** release directory under Ubuntu `releases/`; `rsync`
   each owner's `site/` to its `fountain/`, `solstice/`, or `teatro/` root.
   Preserve older releases and source repos. Do not synchronize `proof/`/
   `candidates/` into source; these are generated print artifacts.
3. Copy SHA-256 inventories, verify with `sha256sum -c --status` from each
   site root, and create `source-lock.json` with the three GitHub SHAs.
4. Run `python3 prepare-wlan-staging.py --release /absolute/new-release` on
   Ubuntu. It rewrites **only three nav links**, leaving original source
   and book content unchanged. A repeat run should change zero HTML pages.
5. Atomically advance the `current` symlink and restart the user service if
   needed. Roll back by repointing `current` to the previous release.
6. Run `npm run staging:verify` from this repository on the Mac while the
   Ubuntu target is on the same WLAN. Verify the real iPad Safari experience.

The service uses a `systemd --user` unit. The Ubuntu user currently has
`Linger=no`, so automatic startup after a reboot with nobody logged in is **not
guaranteed**. The user session's `default.target` does enable the service.
For round-the-clock boot-time availability, enroll user linger via a separately
authorized system-admin operation; do not bypass the password/polkit boundary.

## Scope and prohibitions

This preview performs no public Caddy/DNS write, no EstatePublisher operation,
no GitHub Actions, no new Git clone on Ubuntu, and no machine-wide service
installation. It is not a production release. All routes send
`X-Robots-Tag: noindex, nofollow` and `Cache-Control: no-store`.

## 14 October: Fountain Coach is an essay-first Linotype volume

The staged http://192.168.8.249:8180/ now shows the full three-essay
book, built from Fountain-Coach/fountain.coach at commit 49a35bf14.
The old promotional homepage recedes into Git history. Complete source
essay routes, figures and metadata remain with the owning repository.

Staging release: 20261014-essays-linotype-three-front-v2. Original source
SHA-256 inventories were checked on Ubuntu before stage-only link rewrites.
Because the Fountain entrance is now a book, it has two related edition
links on its cover instead of an old three-link header rail. Existing
source essay pages under /essays/ retain locally rewritten three-link rails.
First Reading and Teatro remain on ports 8181 and 8182.

Real Ubuntu-hosted browser QA passes for iPad portrait, iPad landscape
spread, desktop, phone portrait, and phone landscape. The whole authorial
essay content is preserved verbatim: 77 paragraphs and five original plates.
No source essays have been rewritten.


## New staging hierarchy: v3

The active release `20261014-editions-hierarchy-three-front-v3` makes
`http://192.168.8.249:8180/` and `/editions/` the **editions catalogue**.
The Fountain Coach estate rail points to
`http://192.168.8.249:8180/editions/essays/`; the Essays edition contains
three separately typeset sub-editions at `/editions/essays/<slug>/`.
The original source essay directory `/essays/` remains an archive of the
unchanged published essays. Stage-only rail rewriting is done on disposable
Ubuntu release copies, not in the Git owner, including on standalone books
and original source pages. First Reading and Teatro now also link directly
into the essay edition from their estate rails.

The source inventory was independently SHA-256 verified before link rewriting
and the complete WLAN release checked for every edition route, legal footer,
original assets and nested reader. Browser checks against the live Ubuntu
stage verify all three nested editions on iPad portrait, iPad landscape, and
phone portrait, and the omnibus on iPad and phone in both orientations.
Earlier v1/v2 releases remain available for rollback. No DNS or Caddy
production mutation is performed.


## Teatro book-first WLAN release v4

Active GitHub-sourced WLAN stage:
20261014-teatro-first-hearing-satzfunk-v4.

Teatro now opens at http://192.168.8.249:8182/ as a complete measured
Linotype book. The exact edition is also addressed at
/editions/first-hearing/. The old, working Csound stage is preserved
as the secondary interactive /editions/stage/ edition, with a return to
the manuscript. The estate rail of Fountain Coach and First Reading
now points directly into this Teatro book.

The source owner Fountain-Coach/teatro.fountain.coach at 564be196,
Fountain Coach original authored essay and original image, and the
Satzfunk cross-edition adapter at fad7009 are independently pinned.
The three-front staging server has verified source-byte inventories
and source-only stage navigation projection. Independent browser checks
on the real Ubuntu service pass the book on iPad portrait/landscape,
phone and desktop; the Stage mount is present. No recorded narration
was released, and actual audio output was not independently witnessed.
Prior stage v3 is retained for rollback.

## Final Teatro source v5

Active WLAN release 20261014-teatro-book-first-hearing-v5 tracks the GitHub owner 205a7c8 and has exact source-byte SHA verification. Only the Teatro Git owner changed; Fountain Coach and First Reading still match their prior pinned revisions. No new sound take was authorized or published.

## Teatro executable plate v6

Active Ubuntu staging: 20261014-teatro-live-webgl-book-plate-v6, pinned to owner 7063ae3; the animated scene is a full book leaf, not a link to a separate app. Automated Chrome used animated SVG fallback because WebGL creation was unavailable. On-device WebGL requires iPad verification.

## Teatro source-addressed mixed-media v7

Active WLAN release: 20261014-teatro-r12-anchored-mixed-media-v7. Git owner Fountain-Coach/teatro.fountain.coach 17c76b1, Press 7f8411e. Full authored 22-paragraph essay unchanged, source-anchored spatial scene on the same page as its prose and edition-specific running imprint. Browser verification passed in Chrome-emulated iPad portrait/landscape, phone and desktop. Actual iPad Safari GPU and author acceptance remain pending.

## Teatro puppetry v8

Active WLAN release: 20261014-teatro-r12-moving-puppet-v8, owner e7b1d70. On WebGL failure the book loads a canonical StageEngine/StageView SVG puppet with bar, strings, torso and limbs. All four actual WLAN browser profiles witnessed motion and book page-exit cleanup. Original WebGL/Csound bundle remains unchanged, no spoken edition released; actual iPad Safari author acceptance pending.

## Teatro MIDI2 player, Ear and Csound candidate v9

Active WLAN release: 20261014-teatro-r12-midi2-player-ear-v9. GitHub-owned Teatro source 3e42a98; Fountain Press UMP player 476ab2b. Old Scene/Hear header links and empty narration rail removed. Compact player exposes four Csound channels, Web Audio preview on HTTP, and measured Ear activity. Native MIDI2 host transport and HTTPS Csound Safari witness are not yet accepted.

## Teatro MIDI2 player and Ear v10 — active

WLAN release `20261014-teatro-r12-csound-ear-midi2-v10`, source
`Fountain-Coach/teatro.fountain.coach@1ea0bc2`, verified source SHA,
prepared/activated on Ubuntu. Estate verification passes. Four layout
profiles pass browser checks, including real puppet motion and MIDI2
UMP controls. On live HTTP WLAN, a clicked Web Audio preview rendered
witnessed RMS 0.0038. On secure localhost, the real Csound AudioWorklet
registered and rendered RMS 0.00235, the actual Ear AudioWorklet reported
55+ analysis observations, a 64-bit MIDI2 UMP parameter event was
verified, and user-stop shut down playback. The official Csound host
remains upstream branch code; hardware MIDI2 and trusted iPad HTTPS are
unverified. No public HTTPS site was changed.

## R13 mobile thumbnail identity and canonical Play — WLAN v11

Active Ubuntu staging: `20261014-teatro-r13-mobile-atlas-play-v11`,
source GitHub owner `Fountain-Coach/teatro.fountain.coach@eb7910e`,
Fountain Press `1c03e6b` (code `bbff388`).
Phone thumbnails are no longer oversized chapter-title overlays on
duplicated page DOM. They use source-derived page mark / authored plate /
interactive-score triangle, stable folio, full accessibility title.
The score's idle visual is now an actionable right-facing Play triangle,
not a random stage-room poster. It loads the original moving puppet
on activation and releases it on page exit.
Actual source inventory SHA-256 and full live WLAN book tests pass on
phone portrait and landscape plus iPad portrait/landscape and desktop.
This is a candidate for writer acceptance; Csound HTTPS and native MIDI2
are separate R12 gates and public HTTPS remains unchanged.


## R14 — centered Linotype controls; no website furniture — v12

Active Ubuntu staging:
`20261014-teatro-r14-centered-book-rail-v12`.
Source Teatro GitHub owner `6b43f79`, Fountain Press `4012388`.
The original authorial paragraphs and score have not changed.
The book does not present website-like estate/edition links at its top
or company/legal links in the bottom pagination. Previous, progress and
next form a compact centered book footer; sound/Ear and an icon-driven
Contents affordance form the centered header. Opening Contents creates
a **true adjacent reflowing rail**, not a modal overlay. No Aa/font-size
percentage selector remains; authored typography stays at one editorial
scale. The idle scene Play affordance is held at a small, paper-proportional
size rather than a full-size poster.

Source SHA-256 and five live WLAN browser profiles passed, including
phone/iPad portrait and landscape. The secure localhost Csound/Ear
worklet regression also passes, but native MIDI2, secure iPad Safari
Csound/HTTPS, durable editing and author acceptance remain pending.
The book is still a staging candidate; the production/public Teatro
route was not changed.

## R15: reciprocal Teatro/book Play, measured Ear — WLAN v14

Active Ubuntu WLAN release `20261014-teatro-r15-calibrated-ear-v14`;
GitHub Teatro owner `775d11d`, Press owner `dd72832`.
The player and its disclosure are at the **top-left**, accompanied by
the proportional Ear logo; the Contents rail icon is **right-aligned**.
The previous visual equalizer bars are removed. Touching the Play
affordance inside an authored Teatro score starts the same book-audio
transport and mounts the original animated puppet. Vice versa, starting
global book audio while the score leaf is visible enters the scene.
The top Pause stops actual audio and releases scene resources. Ear
scales over a bounded 0.84–1.22 range from real, source-calibrated
RMS—not a looped decorative animation—and continues publishing
typed MIDI2 UMP observations.

Source SHA and five **live WLAN** browser layouts passed, including real
pointer activation, reciprocal transport, measured HTTP-preview Ear,
parameter-panel clipping checks, source paragraphs/score and page-turn
cleanup. Secure localhost Csound AudioWorklet/Ear worklet regression
also passed, but HTTP WLAN on iPad still only provides the separately
labeled Web Audio preview. Physical iPad Safari acceptance, public HTTPS
and native MIDI2 host bridge are independent unaccepted R12/R15 gates.

## R16: measured Play color, Ear in the parameter panel — WLAN v16

Active Ubuntu WLAN staging release
`20261014-teatro-r16-play-ring-calibrated-v16` pins Teatro
`69656eb` and Fountain Press `45e28c7`; v15 remains available for
rollback. There is no top-row Ear anymore. Play/Pause and disclosure
stay left, Contents stays right; the transport circle receives a
restrained output-RMS-dependent tint and narrow halo (both reset
on Stop, with zero transition duration for reduced motion).
The actual Ear SVG is inside the progressive sound-parameter
panel, next to the measured status text, replacing the redundant
literal word label.

The official original Teatro score, 22 original essay paragraphs,
shared audio transport, Csound/Ear AudioWorklet on secure localhost,
and MIDI2 UMP parameter/observation plane are preserved. WLAN HTTP
continues to use the disclosed Web Audio preview. Physical iPad Safari
approval, secure-origin Csound in Safari, native hardware MIDI2 and
durable Reframe editorial persistence remain unaccepted.

## Author acknowledged Teatro / Linotype v16 as a beta state

On 14 October 2026 the author, after repeated visual iPad review of
the running WLAN book, said “okay ! this is a great beta state !
please document accordingly”. The approved reference concerns the
**book-first reader/listening UX**, not the complete Reframe editor or
a public Teatro publication. Reframe records the exact decision in
`docs/milestones/2026-10-14-teatro-linotype-beta-v16.md` in its own
GitHub repository.

The active Ubuntu WLAN release remains
`20261014-teatro-r16-play-ring-calibrated-v16`, Teatro source
`69656eb`, Fountain Press `45e28c7`, with v15 available for rollback.
The original literary text/plate and the five-layout browser,
RMS-driven Play-circle, side Contents, synchronized score/audio,
secure-loopback Csound/Ear and browser-local MIDI2 UMP evidence
remain the technical witnesses. The HTTP WLAN uses a clearly
identified Web Audio preview. **No public HTTPS deployment was made**;
Safari Csound on trusted HTTPS, native MIDI2, durable Reframe writer
operations and spoken media release are still open.

Treat this as a positive **beta design milestone and regression anchor**,
not permission to deploy to production or bypass source authority.

## R17 — Teatro Bookshelf landing, v16 reader preserved

The stage preview now serves a source-bound Linotype Bookshelf at both
`http://192.168.8.249:8182/` and `/editions/`, using the Press
`6131c16` template. It contains exactly one authorized book
with the real Teatro source plate as miniature **and** cover; the
whole object enters `/editions/first-hearing/` at the unchanged
author-acknowledged beta reader. Teatro owner `d415c39`,
Ubuntu release `20261014-teatro-r17-bookshelf-landing-v17`.
The original v16 release stays on the host for rollback.

Source SHA inventory passed before estate projection.
The staging preparation modifies precisely the existing managed
`editions/stage/index.html` navigation shell, which means that
prepared file is a declared estate projection rather than a raw
byte-equivalent copy of the Git owner file. The untouched bookshelf,
original 22 paragraphs/score, direct reading URL and browser
audio/MIDI2 experience passed five live layout checks.
Original Stage remains independently accessible and is not a book.

**Only WLAN staged.** No public HTTPS, no native MIDI2, no
newly admitted books and no full Reframe writer acceptance.
The author has approved the earlier v16 book as beta, while the
new Bookshelf entrance still needs their UX verdict.

## R18 — full edition proofreading gallery

Active Teatro staging release
`20261014-teatro-r18-six-book-proofreading-v18`:
six actual edition covers, one upright cover per book, no tilted
thumbnail, no invented books. First Reading has a public HTTPS
reader; the rest are visible, functioning WLAN proofs. The six
cards resolve on the WLAN to First Reading port 8181, Fountain
Coach essays port 8180 and Teatro's preserved First Hearing port
8182. The release projection rewrites the **exact six source-owned
bookshelf hrefs** as disposable staging navigation; it does not
rewrite the GitHub-owned canonical addresses. Source SHA was
verified before projection. The original stage-return rail
also has its existing separate managed staging change.

Five live responsive browser suites passed source cover loading,
no horizontal overflow, page-entry, all v16 Teatro audio/MIDI2
and original source-anchored stage behavior. The estate verifier
independently fetched the five cross-domain book destinations
and source artwork. The new R18 author's approval is pending;
there is no production deployment.

## R19 cover-thumbnail table — live v19

Active release `20261014-teatro-r19-cover-grid-v19`,
with exactly six cover thumbnails, zero extra links/labels
under the covers, no off-axis decorative miniatures and a
responsive 3×2 iPad / two-column phone grid. All six
source-admitted book destinations and original artworks
are preserved, with a true cover-click opening the existing
reader. The bounded cross-domain WLAN link projection
to ports 8180/8181 remains intact; Teatro's v16 First
Hearing remains on 8182. Five live responsive browser
profiles, the source-manifest checks, and estate route
checks pass. Public HTTPS was not modified. Author
acceptance of this corrected landing remains pending.

## R20 — original brand mark and three root editions

The active three-domain WLAN projection presents a logo-only
Fountain Press shelf at 192.168.8.249:8182. Its mark was copied
unchanged from the live fountain.coach original and hash-verified.
Three source-image cover links route to Fountain Coach Essays
(8180), First Reading (8181) and the author-approved Teatro
First Hearing (8182). All individual essays stay nested in
Fountain Coach; no invented top-level books, counters, headings,
titles, labels, additional links or site furniture appear in
the landing. The estate verifier checks the 3:1 edition-to-logo
projection, original asset SHA and actual reader routes.
Previous releases remain available for rollback; the public
HTTPS estate is unchanged.

## R21 — continuous background, no inset paper

The author approved the simplification path and requested removal of
the remaining lighter cream background block on the three-edition
Linotype Bookshelf. The owning Fountain Press stylesheet now renders
the shelf container with `background:transparent` and
`box-shadow:none`, showing the existing outer `#dfd9ce` field
continuously behind the original hand-and-spring logo and three
source-art covers. The book covers retain their own fine paper
surfaces and shadows; this is not a redesign of the accepted reader.

Source: Fountain Press `9479d27f1637cca4f974752f821c26d5be44de97`,
Teatro `7aeb45ed947711d17e521d1d48c7fd29d8fc4bd9`.
Active WLAN release
`20261014-teatro-r21-continuous-background-v21`; v20 and the
accepted v16 book releases remain available for rollback. iPad
portrait browser test witnessed a fully transparent panel,
no shadow and the unchanged book entry/audio controls. The
estate staging verifier passed all three real edition routes.
Public HTTPS remains unchanged.

## R22 — left-aligned publisher signature

The Fountain Coach hand/spring image is paired with the discreet
`FOUNTAIN COACH` wordmark and aligned with the left edge of the
first cover. The three-cover row, source artwork, continuous background,
and accepted v16 reader remain unchanged. The iPad live browser
check measured identical x positions for branding and first cover.

Source: Fountain Press `cd1cb6f882c7f46b37ce65d9935887d8cbf6ba50`,
Teatro `2c328c284cdd15176e41d2ce13a98a0279f19a90`.
Current WLAN release: `20261014-teatro-r22-left-brand-signature-v22`.
No public HTTPS deployment was made; v21 remains available for rollback.

## 15 October 2026 — Fountain Press shared Bookshelf v27

WLAN release: `20261015-fountain-press-shared-bookshelf-v27`.
Active iPad review entrance: `http://192.168.8.249:8180/`.
The exact same root content is served at `/editions/`.

The Fountain Coach owner now renders the accepted shared Fountain Press
`runtime/bookshelf.py` and `runtime/bookshelf.css` instead of a duplicate
estate-specific stylesheet and HTML grid. It projects the canonical three
front-door destinations from the Git-owned `estate/manifest.json`; the Teatro
cover enters `/editions/first-hearing/` directly. The authentic logo and
three admitted original cover artworks remain unchanged. The paper container
is transparent and shadow-free; individual covers retain their restrained
borders, shadows, and keyboard-focus affordance. There is no visible edition
metadata or navigation outside the cover artwork.

Source lock: Fountain Coach `30fc01d4d`, First Reading `bb365cae7`,
Teatro `2c543589e`, Estate `13d7c8b`; exact 40-character SHAs are recorded
in the immutable staging release's `source-lock.json`. All 79/101/59 original
source files passed independent SHA-256 inventory validation before the
WLAN-only link projection. The Fountain Coach responsive Chrome proof passed
on desktop, iPad landscape/portrait and phone landscape/portrait; complete
essay-source, paragraph, image, pagination and sub-edition checks passed.
The live three-port `npm run staging:verify` passed, including the original
Teatro First Hearing/Ear/Stage boundary. The beta v16 reader and its media
assets were not modified. Actual human iPad Safari visual acceptance remains
an editorial review, not an automated claim. Previous v26 release is retained
for rollback. No public HTTPS, DNS or Caddy production release was performed.

## 15 October 2026 — actual grid of empties, WLAN v28

The author rejected the previous four-object horizontal strip and supplied
`instruments.fountain.coach` as the concrete grid reference. **The missing
feature was visible, repeated vacant slots, not different cover artwork.**
Shared Fountain Press now projects four occupied first-row cells (one genuine
logo plus three unchanged source covers), followed by 20 explicit non-clickable,
aria-hidden empty slots with restrained dashed borders. The cell lattice
responds at six desktop, four iPad and two narrow-phone columns. Tall covers
remain within square cells, without stretching the empty-slot rhythm.
The common warm background and transparent, shadowless paper container remain.
No further text, navigation, cards, fictitious books or extra cover copies
appear. Each actual cover links directly to its existing Linotype edition.

New three-port release: `20261015-bookshelf-vacant-grid-v28`, active at
`http://192.168.8.249:8180/`. Previous v27 remains for rollback.
Source owners: Fountain Press `f7e7dee`, Fountain Coach `099da69`,
Teatro `4cabb35` and the previously deployed First Reading source
`bb365cae`. Exact source SHAs and original file inventories are locked into
the release; all 79/101/59 source files were checksum verified before the
bounded staging-only navigation remap. The shared Press CSS digest is identical
for Fountain Coach and Teatro. Responsive browser, Linotype pagination,
Teatro First Hearing/audio/Stage, and full WLAN estate checks pass.
Public DNS/HTTPS were not changed. iPad Safari author acceptance remains open.

## 15 October 2026 — circular identity v29

Active WLAN preview: `http://192.168.8.249:8180/`; release
`20261015-fountain-identity-circle-v29`. The Fountain Coach hand-and-spring
logo now occupies a delicate, true circular border in its grid cell, sharing
Fountain Press's `identity-circle.css` radius/stroke rule with Teatro's single
Play/Stop button. The logo is inert and never animates. The Play/Stop circle
retains its genuine measured-volume color/halo and unchanged media behavior.
Grid structure (four occupied positions plus 20 inactive dashed slots), three
original covers, edition routing, and reader typography remain unchanged.

Source commits: Fountain Press `96f865e`, Fountain Coach `8ce1d83`, Teatro
`aa29e86` (includes implementation `da4b124`), First Reading `bb365cae`.
The pinned release source lock includes complete repository commit IDs.
Source inventory SHA-256 checks passed: 80 Fountain Coach, 101 First Reading,
60 Teatro files. The shared identity stylesheet has the same checksum on
both owner origins. Browser tests passed responsive grids and Teatro's Play,
Stop, Ear, Stage and pagination. The three-port live WLAN verification also
passed. Previous v28 release remains on host for rollback. Public DNS,
production HTTPS and Caddy were not modified. Author iPad visual acceptance
is still required.

## 15 October 2026 — v30 square thumbnail correction

Current WLAN release: `20261015-rounded-square-thumbnails-v30`, active at
`http://192.168.8.249:8180/`. Author screenshot of v29 revealed rectangular
portrait cover cards inside a lattice of rounded-square empty thumbnails.
The originating Fountain Press `runtime/bookshelf.css` now renders each
occupied thumbnail at exactly the same square size and 22.37% corner
radius as the empty slots. Genuine source art is contained unaltered inside
those rounded-square objects, rather than used as the outer geometry. The
one publisher-logo circle and its shared Play/Stop identity are unchanged.

Source owner commits: Fountain Press `6e9c4b6`, Fountain Coach `8d79039`
(source styling `206a0ac`), Teatro `dbf2543`, First Reading `bb365cae`.
80/101/60 tracked source files passed SHA-256 inventories before the
bounded three-origin preview projection. Chrome browser verification checked
all three occupied frames, their matching empty-cell radius, source artwork
containment and absence of overflow across desktop, iPad portrait/landscape
and phone portrait/landscape. Teatro's direct book entry, pagination,
Play/Stop, Ear and Stage tests passed. The active WLAN three-port verifier
passed; production remained untouched. Previous v29 remains for rollback.

## 15 October 2026 — v31 Score-first semantic navigation

Current WLAN staging release:
`20261015-score-trace-navigation-v31`, served at
`http://192.168.8.249:8180/` with Teatro book at
`http://192.168.8.249:8182/editions/first-hearing/`. Previous v30
release is retained intact for rollback.

The Teatro Bookshelf cover navigates to the **authentic Teatro Score as the
first measured editorial leaf**, not to the inherited generic Essays cover.
The original Score SVG is moved once from the former chapter opener, with
its artwork checksum unchanged and no duplicate image; the original
22-paragraph manuscript, interactive scene, MIDI2, Play/Stop and Ear remain
intact. Exactly one publisher-admitted relation is available:
`06 ATTENTION / AUTHORITY → teatro:unfinished-composition:empty-chair-attention`.
The other six Score movements have no admitted links. A visible and keyboard
accessible Score link opens the precise source passage. A return link and
browser history lead back to the Score. The exact same trace survives
responsive pagination with different physical folio numbers; an unknown
trace is visibly refused and cannot be silently reassigned.

Source commits pinned into `source-lock.json`:
Fountain Press `003288d`, Teatro `e5ee775`, Fountain Coach `8d79039`,
First Reading `bb365cae`, Estate pre-release verifier `4658be0`.
The 80/101/60 owner-file SHA-256 inventories passed before the staging-only
link projection. Full Fountain Press First Reading regression, 22-paragraph
Teatro source tests, existing five-layout audio/Stage browser checks, and
four-layout reciprocal navigation/deep-link/reflow/invalid-trace tests all
passed. The same navigation test passed **against the live WLAN address**,
not merely the local workstation preview. Live three-port
`npm run staging:verify` also passed with the new Score assertions.
No public DNS, Caddy or HTTPS deployment was attempted. iPad Safari human
visual/editorial acceptance is still a distinct action, not an automated
claim.
