# Cold restore rehearsal — Ubuntu WLAN origin, 15 October 2026

**Outcome:** PASS for an *isolated observed-public-static-byte reconstruction*. This is
not a complete production-disaster-recovery acceptance or permission to move DNS.

## Evidence

- Public GitHub release: [recovery-candidate-20261015-01](https://github.com/Fountain-Coach/estate/releases/tag/recovery-candidate-20261015-01)
- Build commit: [43a2031](https://github.com/Fountain-Coach/estate/commit/43a20311dd3b066aa0e7f47a10782b2e800983c3)
- Release asset: `estate-public-observed-20261015.tar.gz`
- Immutable gzip SHA-256: `20232def0be2be915d608c9ea491ffbd131edb5350e3721c3d081a7086d7b444`
- Original evidence: [bounded 621-URL public crawl](public-route-census.md), [600/600 exact Git byte coverage](public-git-coverage.md)
- Recovery location: `/home/benedikt/fountain-recovery-cold-20261015/` on the existing Ubuntu 24.04 machine
- Caddy Docker image: `caddy:2.10.2`, registry digest `sha256:c3d7ee5d2b11f9dc54f947f68a734c84e9c9666c92c88a7f30b9cba5da182adb`
- Cloudflared Docker image: `sha256:9b49eed8f62806d5d45ddf59ecefb5710429598ea6d3fcccd2af938f621b2b07`

## Cold-recovery execution

The Ubuntu machine downloaded the archive **directly from public GitHub HTTPS**, with
no Git credential, Mac data transfer, legacy Hetzner Git path or original Hetzner
application server. `sha256sum -c` passed against the pinned release hash.
Unpacked content was checked against the 600 URL records and their original public
SHA-256 digests. A second clean extraction using
`scripts/validate-cold-restore-archive.py` verified archive safety, allowed
file types, path confinement, all 599 unique bytes and the explicit
`releaseAdmitted=false` manifest.

Caddy was started in a **new, non-restarting, read-only-mounted container**,
`fountain-estate-restore-20261015`, with the container's port 18480 published
**only to `127.0.0.1:18480`** on Ubuntu. Caddy admin and automatic TLS are
disabled for this isolated HTTP origin. Existing LAN staging listeners were not
modified. Caddy's configuration validation passed.

`scripts/verify-ubuntu-recovery-proof.py` then issued HTTP requests to
`127.0.0.1:18480`, sending each of the nine original published HTTP Host
headers and preserving its URL path. It compared HTTP 200 response bytes
against the exact original public SHA-256 and length:

| Restored original host | Exact URL matches |
|---|---:|
| benedikt-eickhoff.de | 23 |
| book.fountain.coach | 54 |
| fountain.coach | 26 |
| governance.fountain.coach | 277 |
| instruments.fountain.coach | 14 |
| midi2.fountain.coach | 37 |
| status.fountain.coach | 22 |
| teatro.fountain.coach | 5 |
| works.benedikt-eickhoff.de (including delegated Solstice) | 142 |
| **TOTAL** | **600 / 600** |

**Zero byte mismatches; zero HTTP failures; zero redirect hops.**

## External Cloudflare quick-tunnel witness

A temporary Cloudflare Quick Tunnel connects the isolated Caddy origin
outbound, without changing home router forwarding, canonical DNS, Hetzner
or any published domain. Its container, `fountain-estate-quick-tunnel-20261015`,
uses `--network container:fountain-estate-restore-20261015` rather than the
Ubuntu host network namespace, runs without privileged capabilities, and has
no independently published Docker ports. It overrides its origin Host header
to `fountain.coach` for this one-host external test.

Temporary HTTPS preview:
**https://generators-handling-combining-linux.trycloudflare.com/**

An HTTPS GET from the Mac to the public Cloudflare edge reported HTTP 200,
successful certificate validation and the exact original Fountain Coach root
SHA-256:

`e5d4c2a2ef3471a05c4d53c22374fd2bf67be6be336e99519a148329152dd3fb`

The public Cloudflare edge was reached via normal internet routing, but an
independent device *physically outside* the home WLAN has not yet performed a
separate human witness. This is an ephemeral, unauthenticated Quick Tunnel,
not a persistent failover endpoint or a canonical-domain test. It only
projections `fountain.coach`; all nine original hostnames were tested
on local Ubuntu Caddy through explicit Host headers. Embedded site links
can lead to the current public estate rather than the recovered preview.

## Commands / shutdown

The scripts under `scripts/` are reusable for another cold rehearsal:

- `build-static-recovery-bundle.py`: rebuild immutable source artifact
- `validate-cold-restore-archive.py`: check SHA, safe extract and verify manifest
- `start-ubuntu-recovery-proof.sh`: validate an isolated Ubuntu source directory
  and start loopback-only Caddy (does not start the public tunnel)
- `verify-ubuntu-recovery-proof.py`: verify 600 complete served byte responses

To stop the temporary public proof without affecting any other Ubuntu services:

```sh
docker stop fountain-estate-quick-tunnel-20261015
docker rm fountain-estate-quick-tunnel-20261015
docker stop fountain-estate-restore-20261015
docker rm fountain-estate-restore-20261015
```

Only these *two specifically named* rehearsal containers may be removed by
that command. The downloaded read-only proof directory remains for audit.

## What this does NOT prove

- A complete atomic last-published release or the existence of every public
  *unlinked* asset (the input was a bounded 621-URL read-only crawl).
- Replacement of dynamic services, private FountainStore, media outside the
  static census, Secrets/owner trust, OAuth or device-bound authority.
- Registrar-level control and alternative authoritative DNS for a complete
  Hetzner-provider-loss canonical-domain switch.
- All-nine-domain real public hostname/tunnel/TLS routing; the disposable
  Cloudflare tunnel presently demonstrates one hostname only.
- A highly available origin: the Ubuntu machine depends on home power,
  hardware and ISP connectivity.

The top-level candidate release lock remains `releaseAdmitted=false` and
`allowRecoveryDeployment=false`. This outcome is precisely
**LOCAL_OBSERVED_STATIC_COLD_RESTORE_VERIFIED**, **NOT**
`EMERGENCY_DOMAIN_FAILOVER_READY`.
