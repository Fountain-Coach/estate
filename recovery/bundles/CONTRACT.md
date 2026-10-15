# Frozen public estate recovery candidate — 2026-10-15

This is a **recovery candidate for a bounded set of publicly observed static
files**, not the release that is currently authorized to serve the canonical
Fountain Coach domains.

## Artifact

GitHub release tag: `recovery-candidate-20261015-01`

The asset `estate-public-observed-20261015.tar.gz` contains:

- All 600 HTTP 200 responses in the independently recorded 621-URL nine-domain public crawl, normalized to 599 unique host-rooted files.
- A file-by-file SHA-256 and Git provenance manifest, `manifest.json`.
- An isolated Caddy configuration for the **recovery-only** origin port 18480.

No source code that lacks a byte-identical publicly observed response, FountainStore
state, private repository checkout, credentials, or secrets are included.

The candidate references pinned owner revisions, Git archived projections and
ten SHA-256-verified public-readback snapshots already in their respective
owning GitHub repositories. The public archive is intentionally self-contained:
a recovery origin can retrieve the bundle without a private repository token,
the old Hetzner machine, or access to the development Mac.

## Files and verification

- `estate-public-observed-20261015.manifest.json` tracks every requested URL,
  original Git object, resulting file path and bytes SHA-256.
- The report in `README.md` states the exact bundle archive digest.
- `npm run recovery:bundle:build` regenerates the archive deterministically
  from frozen Git objects on an authorized development checkout.
- `npm run recovery:bundle:verify` compares the archive and manifest to
  exact current deterministic outputs, without network or deployment mutation.

**Production admission remains false.** The bounded crawl cannot prove that
unlinked assets, dynamic services, the full private Store, or any other
unsupported server route are recoverable. The 21 public non-200 URLs are
independent findings and are not fabricated as new 200 files.

## Ubuntu local cold rehearsal

Download the GitHub asset into a new isolated directory on Ubuntu. Verify its
public SHA-256 before unpacking. Extract only expected relative regular files,
review the included manifest, and run Caddy in a container bound to
`127.0.0.1:18480` **on the Ubuntu host**. Do not expose the host listener to
other LAN interfaces; a tunnel or official hostname requires separate
authorization.

For local route testing, send the original domain in the HTTP Host header to
`http://127.0.0.1:18480`. Compare the body bytes and HTTP status to the
manifest. None of these actions touches canonical DNS, a production Caddy host,
or the existing Ubuntu WLAN staging services.

Note: embedded absolute links naturally point to the existing public estate.
A temporary tunnel hostname by itself does not provide multi-host browser
redirection equivalence; full interactive reader testing requires separate
hostname mapping or approved preview-host rewriting with clear provenance.

## Acceptance witness

A direct GitHub-release download was independently verified on Ubuntu and served by Caddy on a loopback-only port; all 600 recorded public bytes matched the original independent public witness. See [the local and external test report](../ubuntu-cold-restore-witness-20261015.md), including the disposable one-host Quick Tunnel and limits of this proof.

## GitHub release immutability distinction

The current GitHub release API reports `isImmutable=false`: the release asset/tag are **not protected by GitHub immutable-release enforcement**. Integrity is nevertheless pinned to the exact SHA-256 in this repository and independently checked before every extraction. A mutation of the release asset would make recovery validation **fail closed**, but it is not prevented at the GitHub policy layer. Enabling GitHub immutable releases is a separate repository policy decision applying to future releases, not a property this candidate currently possesses.
