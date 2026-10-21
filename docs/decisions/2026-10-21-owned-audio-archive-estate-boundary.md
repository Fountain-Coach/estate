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

**Observed 2026-10-21:**
**Visible-credit gate inherited (2026-10-21).** [Source and attribution rule](https://github.com/Fountain-Coach/Satzfunk/blob/main/docs/decisions/2026-10-21-visible-credit-provenance-and-release-gate.md): no public text, audio, video or derivative route is admitted unless exact authorship and source-backed notices are visible on the release, source provenance is machine-readable, verified rights cover the intended publication/derivative use and the owner's actual legal footer survives the release. Source-published labels and literal copyright notices must not be misrepresented as proven rightsholders. For *7vst*, keep the distinction among Aeschylus' play, unverified English translator/rights, printed University of Chicago notice and separately evidenced collaborators.

**Updated recovery witness:** 43 distinct Bandcamp public video renditions across two artist pages (33 + 19 with 9 shared), 1,882,811,242 bytes, both Ubuntu and independent Mac external copies hash-verified; [source index](https://github.com/Fountain-Coach/Satzfunk/blob/main/archive/observations/bandcamp-43-video-recovery-index-2026-10-21.json). No upload-original claim or public release.
 Satzfunk has a candidate player and source-bound First Hearing, but not a released public station. The author's own `unpopular-electronics.bandcamp.com/video` page has an independently reverified Ubuntu archive of **33 playback MP4 derivatives / 1,025,972,206 bytes**, each matching SHA-256 from the existing 2026-10-19 [private Bandcamp capture manifest](https://github.com/Fountain-Coach/Satzfunk/blob/main/archive/observations/unpopular-electronics-bandcamp-videos-2026-10-19.json). This is **not** original-upload access, original master approval or public distribution authorization. Ubuntu has ~339 GB free. Hetzner has two 50-GB backup volumes reserved for backup; do not reuse as media. **No new HCloud storage provisioned** because measured capacity is sufficient and master migration remains unresolved. No audio production URL or published Bandcamp original is yet accepted by this decision.

This file records architectural inheritance without updating `manifest.json` ahead of a released source and independently checked public host.