# Three-front Fountain Coach WLAN staging

This staging is intentionally **not** a public HTTPS deployment. It serves
the three GitHub-owned editorial front doors from a verified, explicitly
pinned, copied release on the Ubuntu Mac mini connected to the home WLAN.

## Staging addresses

- Fountain Coach: http://192.168.8.249:8180/
- First Reading: http://192.168.8.249:8181/editions/first-reading/
- Teatro: http://192.168.8.249:8182/
- Read-only health/status: http://192.168.8.249:8180/__stage/health

Ubuntu host: `MacMiniDocker` (SSH), `benedikt-Macmini.local`,
WLAN address `192.168.8.249`.
Do not confuse with the development Mac `192.168.8.12`.
The iPad must be on the same WLAN; no public DNS or port forwarding is needed.

## Source admission and reproducibility

The release holds exact source file trees from the following GitHub repos:

- `Fountain-Coach/fountain.coach`, site/
- `Fountain-Coach/solstice.fountain.coach`, site/
- `Fountain-Coach/teatro.fountain.coach`, site/

Their 40-character Git revisions are captured in
`releases/<release>/source-lock.json` on Ubuntu, and each pre-transformation
SHA-256 source inventory is under `releases/<release>/manifests/`.
All three inventories passed `sha256sum -c` before staging projection.
The only staging transformation is replacing exactly the three editorial
navigation destinations with the adjacent staging ports on complete HTML
pages. The authored book itself has no site-wide estate rail and retains
its separate Linotype reading controls. Content and typesetting must not
be rewritten to implement a staging shell.

Ubuntu release root:
`/home/benedikt/estate-three-front-staging/releases/20261014-three-front-github-v1`.

Current release symlink:
`/home/benedikt/estate-three-front-staging/current`.

Service:
`systemctl --user status fountain-three-front-stage.service`.
Source:
`scripts/serve-wlan-staging.py` and `scripts/prepare-wlan-staging.py`,
deployed to `/home/benedikt/estate-three-front-staging/`.
The persistent per-user service unit is
`staging/fountain-three-front-stage.service`.

After a new source revision, create a **new release directory** and
repeat exact-source copying, SHA-256 verification, the preparation
step and the smoke checks. Only then move the `current` symlink.
Do not edit GitHub content in the derived staging files and do not change
the real domain/Caddy/Hetzner estate.

## Verification record (14 October 2026)

All three main staging pages independently returned HTTP 200 from the
Mac at `192.168.8.12`. Their CSS/JS images and bundle assets
returned HTTP 200. The book contained real original edition images and
Linotype scripts. The health endpoint returned `ready` with the three
canonical Git source revisions and `productionPublished: false`.

The existing browser automation against the staging book URL passed:
phone portrait, iPad portrait, compact iPad landscape, iPad landscape,
laptop and desktop. **Phone landscape failed** a sheet-fit geometry
assertion: sheet top at 49px vs viewport top at 54px; the sheet bottom
was also approximately 5px past viewport. This is a **source layout
issue**, not a missing HTTP file, and must be fixed in the owning
Linotype source rather than patched in staging. iPad device-specific
Safari proof remains a separate human visual acceptance task.

Do not claim production publication or that a live iPad was tested from
Mac-host browser emulation.
