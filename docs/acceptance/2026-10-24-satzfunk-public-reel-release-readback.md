# Canonical Satzfunk reel: public release and readback

**Date:** 24 October 2026. **Intent:** The user reported that the Satzfunk entry in the estate reel was not clickable. The six original production domains, and the independently discovered seventh public personal-pointer domain, carried a source-identical disabled span saying Satzfunk was not yet public.

**Source owner:** Fountain-Coach/estate, commits de46d7bd7aba436b3d6b91831b643d63586d3716 (six-domain fix) and b01ce67832eab294f2234058456921933657b04f (seventh pointer); exact per-file SHA-256 witnesses in docs/acceptance/2026-10-24-public-satzfunk-reel-repair-seven-domain-witness.json.

**Production:** All seven independently activated v14 immutable releases with native EstatePublisher. Seven typed receipts under docs/acceptance/2026-10-24-satzfunk-public-reel-release-receipts/ contain state=active, activated=true, the version-specific Git source revision and independent HTTPS /index.html byte witness. All seven prior v13 releases were preserved.

**Independent readback:** Seven production homepages were fetched over certificate-validated HTTPS from their verified published address (65.109.14.71), and each matched its SHA-256 manifest; each contained exactly one normal anchor data-estate-id=satzfunk pointing to https://satzfunk.fountain.coach/, without aria-disabled. Three representative Governance deep pages (/accessibility/index.html, /chapters/21-training-perspectives/index.html, /privacy/index.html) independently served the same working anchor; all 166 changed Governance HTML pages had exact after-change SHA-256 hashes validated in the immutable full release by EstatePublisher.

**Real browser interaction:** A separate live browser session opened https://fountain.coach/, clicked the visible Satzfunk reel item (not a typed direct URL), and landed successfully at https://satzfunk.fountain.coach/. The published Satzfunk page loaded the six-edition historic catalogue.

**No unrelated deployment:** Caddy, DNS, source recordings, rights, authored prose, Solstice reader and all non-navigation assets were unchanged. The change was the same existing reel icon/label promoted from disabled span to focusable canonical HTTPS anchor. This is not an assertion that every unrelated estate surface has a common reel.
