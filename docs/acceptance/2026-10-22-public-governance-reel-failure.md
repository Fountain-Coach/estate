# Public Governance EstateShell — production gate FAILED

**Observed:** 22 October 2026 · public `https://governance.fountain.coach/` · read-only audit

## Actual live state

- The public homepage responded **HTTP 200**, with successful TLS verification. Repeated GETs from the authorized Mac succeeded; this audit did **not** reproduce a whole-site outage.
- Governance Chapter 158, Chapter 159, Chapter 7, and the legal, privacy and accessibility routes responded **HTTP 200**.
- Public Caddy remains active, serving `/srv/fountain-static-publications/governance.fountain.coach/current` → `releases/static-20261020-923d5f9` on the existing Hetzner host. This is the October 20 production release, **not** the October 22 `shared-shell-20261022-v10-editorial` WLAN stage.
- Homepage public HTML has **eight** `data-estate-id` editorial anchors: `estate, book, governance, midi2, instruments, teatro, pointer, solstice`, plus Info. **Satzfunk is absent.** No `data-estate-shell-version` is present.
- Source-owned Governance static tree (Git `03f15306a018eddd85fab491e592d2fdffd61528`) has 166 HTML files: **156** navigation-bearing HTML documents share this eight-item sequence; **10** historical chapter fragments lack the normal navigation entirely. Do not claim whole-book parity from a homepage test.
- Independent public roots also fail canonical reel membership. Fountain Coach, Book, MIDI2, Instruments, Teatro and Pointer have `status` in the top editorial reel rather than the canonical `satzfunk` entry. The Solstice public entrance also has Status in its navigation. None is yet the complete versioned common chrome.
- Public `satzfunk.fountain.coach` currently has **no DNS resolution**. This is a rights/host admission gap, **not** permission to invent a public link to private WLAN material. Status belongs in the legal footer.

## Full publication inventory check

Ran `python3 scripts/verify_publication.py --against-live` in the clean, owning `Fountain-Coach/governance.fountain.coach` checkout.

- Local source integrity: **PASS**, all 294 declared source files, 160 chapter routes, historical six route-manifest exceptions unchanged.
- Independent public bytes: **FAIL: 292/294 match**, with exact drift at `index.html` and `chapters/07-agent-operating-guide/index.html`.
- Retrieved exact live origin files and verified they are identical to public HTTPS. Both drifts are newer Git-owned additions to the FCIS Goal Fidelity and Non-Invention founding rule that have **not yet been deployed** to the October 20 host release. Do not misdiagnose them as tampering or replace all live bytes with Git HEAD automatically.

## What staging actually proves

The existing `scripts/verify-unified-estate-reel.py --root /home/benedikt/estate-unified-reel-staging/current --live`, run against the Ubuntu Mac mini, **PASSES** with 9 locally projected sites, the canonical nine editorial identities, one Info affordance and anonymous Satzfunk archive 403. Its active immutable release is `20261021-canonical-nine-entry-v7` at port `8198`.

The separate author-facing EstateShell `v10` at port `8200` tested Estate, Teatro and First Reading, **not** Governance or all public domains. Neither WLAN proof is a public production receipt. Passing either one cannot establish public estate parity.

## Native browser witness

The Mac's Apple iPad simulator refused to launch **both** `https://governance.fountain.coach/` and `https://www.apple.com/` with LaunchServices error 115. This is an environment failure independent of Governance. A local headless Chrome attempt failed to create its profile due to the Mac root volume being full (`No space left on device`). **No native iPad visual PASS is claimed.** The public semantic failure is already conclusive without visual tests.

## Decision / correction

**FAIL: public estate shared-shell admission.** The production Governance site is presently online, but it lacks the canonical reel and current common shell. The test scope was wrong when the October 22 staged three-owner release was called an estate-wide fix.

Use the already-defined `Fountain-Coach/estate/navigation/canonical-reel.v1.json` and source-owned `EstateShell`, not a new CMS, ad-hoc per-domain patch, broad DNS change or a second test harness. A correct public release requires: (1) truthful Satzfunk public destination/admission or explicitly inert unavailable identity; (2) domain-owner source-preserving projection of the same pinned shell into all eligible public and deep HTML routes; (3) real iPad/WebKit and public multi-host readbacks; (4) owner-authorized EstatePublisher release with immutable predecessor and independently verified HTTPS result.

**No production site, Git owner, DNS record, Caddy service, or staging release was modified by this diagnostic audit.**
