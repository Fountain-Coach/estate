# Local Fountain Coach estate — Satzfunk integrated

**Date:** 2026-10-21  
**Scope:** Ubuntu Mac mini **WLAN staging only**. Production DNS/Caddy, FountainStore publication and external rights admission are unchanged.

## Working entrance and routes

| Publication / service | Local address | Authoritative source |
| --- | --- | --- |
| Fountain Coach / Estate bookshelf | http://192.168.8.50:8180/ | Fountain-Coach/fountain.coach |
| First Reading | http://192.168.8.50:8181/editions/first-reading/ | Fountain-Coach/solstice.fountain.coach |
| Teatro | http://192.168.8.50:8182/editions/first-hearing/ | Fountain-Coach/teatro.fountain.coach |
| **Satzfunk — authentic audiovisual radio** | http://192.168.8.50:8194/ | Fountain-Coach/Satzfunk **private access required** |

**Satzfunk is the original six-edition, forty-three-video author archive, not the rejected `public-reel/` link-only mockup.** Its album navigation, source text, preserved recordings, rights panels, archive identity and rendering process remain separate and protected. Its cover is a local bookshelf projection, not a fourth public production publication or replacement for original work credits.

Source-owned original Satzfunk cover: [archive/browser/satzfunk-archive.svg](https://github.com/Fountain-Coach/Satzfunk/blob/main/archive/browser/satzfunk-archive.svg). Exact staged cover SHA-256: `e16c288bd7968dda391872dd93ad5ddb7ecead03674bd68d5d54b4ffed0e4d40`.

## Running release and operational notes

- Current local stage: `/home/benedikt/estate-three-front-staging/current` -> `releases/20261021-satzfunk-four-front-v2`.
- Earlier snapshot preserved: `releases/20261021-satzfunk-four-front-v1`. Additional experimental source-pinned `releases/20261021-integrated-satzfunk-radio-v1` was not promoted.
- Existing `fountain-three-front-stage.service` still serves only three static book roots; the **separate** `satzfunk-bandcamp-preview.service` serves the private archive on port 8194. Neither archive media nor its cookie/token were copied into the local estate.
- The former `192.168.8.249` static listener IP had disappeared from Linux interfaces and returned an unreachable route on the Mac. The stage server's binding and staged navigation were changed to reachable `192.168.8.50`, and the user service restarted. Source authority for the server default is [scripts/serve-wlan-staging.py](../scripts/serve-wlan-staging.py).
- Satzfunk's local-only archive rail in `archive/browser/index.html` and `archive/browser/7vst-originals.html` was also corrected to the same reachable address; both originals were copied to `/home/benedikt/services/satzfunk-private-video-browser/branding-backups/20261021-pre-estate-ip-repair/`.
- The Ubuntu stage HTTP listener remains `noindex, nofollow` with no-store caching. DNS under `satzfunk.fountain.coach` remains a separate production publication task.
- Rebuild/new links must be **address-verified** against the live Ubuntu interface; an old three-front source snapshot might still contain original stage-only `192.168.8.249` navigation, so no naïve release promotion from it is permitted.
- Any return to an older release requires adjusting its local navigation origin to the current reachable staging IP; just pointing to an old 249-address version is not a working rollback. Never substitute a public host or turn off the private archive gate to compensate.

## Verified acceptance

On the authorized Mac (21 Oct 2026), HTTP HEAD requests returned:
- 8180, 8181, 8182 book roots: `200 OK`
- Essays / First Reading / Teatro nested editions: `200 OK`
- Both staged `satzfunk-archive.svg` cover assets: `200 OK`
- Anonymous request for the protected Satzfunk archive on 8194: `403 Forbidden`, **expected**.

Authenticated Ubuntu source browser tests:
- Six original editions, exact forty-three-video order and HTTP byte-range playback: **PASS**.
- All eighteen 7VST published-text references, sha256, lineation and anonymous 403: **PASS**.
- Fountain and Teatro staged root bookshelves each include exactly one `data-book-id="satzfunk"`; cross-site edition-navigation contains the station destination.
- Recursive scan of the active three static site roots found **no stale `192.168.8.249` references**.

**Still pending:** native iPad Safari author-led visual and playable-audio acceptance from the local WLAN. Server acceptance cannot establish mobile visual and audio experience, and a bare archive link remains forbidden until the author has the existing authenticated cookie.

This is a functioning **local estate**, not a claim of public Satzfunk publication.
