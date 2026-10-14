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
