# What Makes a Page Modern? — typographic specimen boundary — private WLAN v148

## Observed defect and accepted correction

The v147 book accidentally displayed the same specimen passage **four times**: each of the two intentional classical/modernist source SVG compositions and two full copies in normal narrative prose. A live WebKit witness showed the classical SVG and one redundant paragraph together on leaf 3. The unanchored inline illustrations were also distributed by the existing Reader's fallback evenly across paragraphs, moving them away from their actual textual contexts. The user requested a visibly clear *stage on a stage*, not uncontrolled repetition.

The source-authorized correction removes the two prose copies and describes the single shared source used in the **two** deliberately repeated but typographically different specimens. The original SVGs remain byte-for-byte unchanged. The nested specimen fields have a thin enclosing rule, distinct inset paper, visible labels `ONE PASSAGE / TWO SETTINGS`, `SPECIMEN I · CLASSICAL MEASURE`, `SPECIMEN II · MODERNIST MEASURE`. The comparison judgment follows both specimens.

The existing Reader already supports the author-specified `data-inline-after-paragraph` attribute; this edition now sets exact source paragraph addresses for all 11 secondary figures rather than accepting fallback spacing. This is a source-owned content setting, not a new Reader, figure compositor or independent CSS system.

## Source and provenance

- **Source owner:** `Fountain-Coach/fountain.coach`; branch `codex/modern-page-specimen-boundary-20261105`.
- **Source commit:** `a9575ba976917433baf0cc67940b5941e4c1de96`.
- **Revised manuscript:** `site/essays/what-makes-a-page-modern/combined-essay.md`, SHA-256 `8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6`.
- **Historical Druckfahne source PDF:** SHA-256 `2baaab0012e825b49f04e7a760b64efa52c95dc09deab7117de790f6c6e14bad` (not falsely represented as the revised manuscript's exact text).
- **Stage predecessor:** `shared-shell-20261105-v147-self-out-loud-c884a3e`, HTML SHA-256 `11cd731753769f5feacd2f91dc2ba1fc8c0e914d5d107b00f9c98ad58eff3c2c`, retained immutable for rollback.
- **New immutable active stage:** `shared-shell-20261105-v148-specimen-boundary-a9575ba`.
- **Only changed files against v147:** `estate/index.html`, SHA-256 `532dbdf6603fb1300a974418130c50cbc17636262d9dcf7c0a802c3aabfdd81c`; `source-lock.json`, SHA-256 `90d23ed381ece45f54d9621ca7341e204d5967738f1f48b3af2d8eab42483e1c`. The 1320-file release inventory has no new/deleted files; 12 original illustrated assets and all original private audition media are preserved.
- **Guard owner:** `Fountain-Coach/estate` `codex/modern-page-specimen-stage-20261105`; first guard source commit `2ef807b1f62af1f999ad4efed3af6698535e9f68`. Existing source-owned Reader provenance guard extended by one narrowly pinned admission. Installed v148 guard SHA-256 `765606ce63c53a3b2cef69ecd20d6f1117a0d2a58247193b65af16edf478d351`; previous v147 guard backed up with original SHA-256 `4fe2faa992b7fefcc5a5b76786b5eb0de713eb9ccd1dff6fc0fbd4333914a413`.

## Independent checks

- **Candidate provenance, before activation:** The prospective guard confirmed the original production-derived Reader source line, accepted unchanged v145 private WAV/MP3 and v146 listening page bytes and accepted only the revised authorized root and lock. Forged source commit, root SHA and source-lock SHA were refused. The guard's file comparison found precisely the expected two changed files, none elsewhere.
- **Guard installation continuity:** Applied the new guard first while active stage remained v147. Both HTTP/HTTPS services restarted under their existing user units; exact v147 HTTPS SHA was independently read back before stage activation.
- **Atomic stage activation:** Existing `current` symlink switched from v147 to v148 in one rename, followed by restart of the same two existing preview units. HTTP `:8200` and HTTPS `:8243` independently returned the exact new `532dbdf...` SHA; both existing services were active.
- **Live stage browser checks, no local HTML interception:** 6/6 Chromium and WebKit profiles passed at 820×1120 (19 leaves), 1200×860 (29 leaves), 390×844 (35 leaves). The Reader showed 12 intact semantic figures, 17 headings and 133 source-addressed blocks, exactly two framed type specimens, **zero unframed specimen prose copies**, and 11 source-addressed inline figures. No page JavaScript exceptions or horizontal overflow. Essays gallery still six works; Teatro route reopened.
- **Complete live reading:** WebKit page-turn navigation traversed **all 19 portrait-sized leaves**, encountered all 12 figures, verified image loading and caption/figure alignment within 2 CSS px, and reached the final closure. Physical iPad Safari and VoiceOver acceptance remain separate, not inferred.
- **Visual witness:** Live WebKit captured leaf 3 as an enclosed classical specimen and leaf 4 as the identically sourced but differently composed modernist specimen. Each now lives in its own measured, labelled inset field on the page and no duplicate specimen paragraph follows either. Mac/phone WebKit viewport evidence also passed.
- **Audio/TLS boundaries:** The automation used an explicit ignore-CA flag for the private WLAN certificate, not a public TLS claim. Existing first-reading MP3 preload cancellations/retries were reported separately; no new audio editing/playback or live `Self Out Loud` control instrument was attempted.

## Rollback / publication scope

The unchanged v147 release and its guard remain available. To revert, atomically restore the `current` symlink to `shared-shell-20261105-v147-self-out-loud-c884a3e` and restart the two existing user-level preview services. The v148 guard also continues to recognize v147; the old guard backup is retained for precise recovery if required.

**Exact author-WLAN reading route:** `https://192.168.8.50:8243/estate/#/read/essay--what-makes-a-page-modern`

**Final state:** ACTIVE AND VERIFIED PRIVATE STAGING v148. No public production release, source-rights elevation, live human-voice recording/MIDI synchronization or new Reader.
