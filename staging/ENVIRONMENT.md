# Fountain Coach Estate — one named WLAN staging environment

Binding estate-specific identity: [environment.json](environment.json).
Owner: Fountain-Coach/estate. Inspect the registry and actual current symlink
before answering a request to view, update or publish staging.

## Current observed state — 23 October 2026

The existing Ubuntu Intel Mac mini is MacMiniDocker / benedikt-Macmini.local,
currently reachable at 192.168.8.50. The canonical author entrance is:
http://benedikt-Macmini.local:8200/estate/
Direct-IP alternative: http://192.168.8.50:8200/estate/

The existing user service is fountain-shell-acceptance-preview.service.
Its current symlink is /home/benedikt/estate-shell-acceptance-staging/current.
Observed active release: shared-shell-20261023-v12-first-reading-ad04d80-r2.
Retained rollback: shared-shell-20261022-v11-eight-owner-47e7ac71.

First Reading: http://192.168.8.50:8200/solstice/editions/first-reading/
This is the source-owned full-viewport book with its original reader toolbar.
The common estate masthead remains on /solstice/; it is not injected into the
measured book. Its 92 public dependency files, including all 41 images,
30 standalone readings and proof workbenches, are independently HTTP/hash
verified. See the [repair report](../docs/acceptance/2026-10-23-first-reading-staging-repair.md)
and [typed terminal receipt](../docs/acceptance/2026-10-23-first-reading-stage-terminal-receipt.json).

## Identity and release are separate

The actual service/current symlink determines the running release. Registry
observedRelease fields and historical notes are snapshots. Read the service
using existing SSH; verify the entrance, relevant deep route and assets.
Provide a copyable author entrance. Do not redeploy for a viewing request.

Ports 8202 (isolated shell proof), 8201 (release-continuity test), 8198 (earlier
public-byte mirror) and 8180–8182 (separate Bookshelf/reader stage) do not
replace the canonical 8200 entrance. The private 8194 archive remains protected
and is not a public source substitute. Historical .11:8443 and .249 addresses
are not the canonical entrance. Earlier v9/v10/v11 active-release descriptions
are historical snapshots.

WLAN staging is not public DNS/Caddy production. Do not change DNS, Caddy,
private media or unrelated services to inspect it. Inherit organization-wide
[FCIS Goal Fidelity and Non-Invention](https://github.com/Fountain-Coach/.github/blob/main/docs/FCIS-Non-Invention-and-Goal-Fidelity.md).
