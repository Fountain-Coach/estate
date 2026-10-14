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
