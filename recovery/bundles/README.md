# Immutable observed public estate recovery candidate

**Not approved for production deployment.** No dynamic/private state is represented.

This tarball preserves exactly 600 byte-verified public HTTPS resources under host-rooted paths and 599 unique filesystem destinations, with a Caddy origin file and SHA-256 manifest. The public crawl observed 21 additional non-200 URLs and cannot prove absent/unlinked URLs, an atomic published release, or live API state.

Artifact: estate-public-observed-20261015.tar.gz (80135281 compressed bytes)

Archive SHA-256: `20232def0be2be915d608c9ea491ffbd131edb5350e3721c3d081a7086d7b444`

Generated from committed historical Git objects only; the archive may only contain files whose bytes were served publicly and match the frozen census digest. A public user can retrieve this artifact without any access to the private development source tree. The archive is a recovery **candidate** and must not become the canonical estate until an explicit owner-admitted release and cutover authority exist.

The included Caddyfile serves only a loopback-published Docker port 18480 when used with the documented external runtime; host routing uses the original domain Host header. The Caddyfile itself does not configure the host Docker port mapping.

Reproduce from historical owning Git objects: `npm run recovery:bundle:build`. Verify immutable bytes: `npm run recovery:bundle:verify`. For the first LAN-only rehearsal, use the isolated Ubuntu verification scenario without changing production DNS, TLS, or existing Caddy services.
