# Decision: owned audio archive is a supporting estate publication

**Date:** 2026-10-21  
**Status:** Pinned cross-estate integration contract; NOT publicly released or DNS-admitted.

Canonical decision: [Satzfunk audio archive and Bandcamp migration](https://github.com/Fountain-Coach/Satzfunk/blob/main/docs/decisions/2026-10-21-owned-audio-archive-bandcamp-migration.md).

**Preserve exactly three existing public editorial front doors**. The author's catalogue at `works.benedikt-eickhoff.de` remains independently owned. Satzfunk at `satzfunk.fountain.coach` is a proposed **supporting** audio/Hörspiel archive, not a fourth primary Bookshelf cover, and must not silently rewrite any existing root, link, legal/footer or publication state.

Before an audio release:
1. Work/original source and SHA-256, rights/collaborator credits, accepted release media and transcript/metadata are linked in a private authoritative Store manifest. A public Bandcamp link is not release authority or proof of rights.
2. Source-owner publications use an immutable, source-addressed public media projection. Originals/rights evidence and unpublished takes do not enter public Git or HTML.
3. The current canonical Store/EstatePublisher publishing route admits a release and exact host/route. Do not create DNS records, edit Caddy or copy files via SSH merely to make an unadmitted candidate seem public.
4. Independent HTTPS and full audio/download playback/read-back across Mac and iPad match the manifest and hashes.
5. Only once approved does the estate registry add a supporting destination link, with its actual owner revision and observed release state.

**Observed 2026-10-21:** Satzfunk has a candidate player and source-bound First Hearing, but not a released public station. Hetzner has two 50-GB backup volumes reserved for backups; do not treat either as audio capacity. No audio production URL or published Bandcamp original is yet accepted by this decision.

This file records architectural inheritance without updating `manifest.json` ahead of a released source and independently checked public host.