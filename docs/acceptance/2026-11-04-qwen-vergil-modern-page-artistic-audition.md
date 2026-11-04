# Private Qwen3 Vergil audition for What Makes a Page Modern? (4 November 2026)

This is a bounded owner-controlled WLAN artistic audition. No new Reader, player, public production, source text or Vergil master was created or replaced.

## Author's artistic selection — 4 November 2026

**DECISION: Take A, "Lucid Editorial Vergil", is selected as the vocal character for the spoken edition of *What Makes a Page Modern?*.** The author listened and explicitly chose "the editorial voice" over the warmer Take B in the existing private Qwen3 A/B audition. No alternative voice should be substituted during continuation without a fresh author decision.

- **Selected private audition WAV:** `vergil-a.wav`, SHA-256 `39f19760f619f2dd8e9fad8af33dc51acfc8dab48235e3268881949f82d32a7f`, PCM16 mono 24 kHz, 8.720 seconds. **Private listening MP3:** `vergil-a.mp3`, SHA-256 `6f229cce508aa70236ee5c3b3eeb0bec7fe14bdc2296e0703d18016750ae91f8`.
- **Chosen TTS provider:** offline `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` pinned at `5ecdb67327fd37bb2e042aab12ff7391903235d3`, weight SHA-256 `391e8db219f292c515297cdceeb43e4eae67cdde35fa57e79a6a8a532fca0522`. **Candidate generation seed:** `20261104`. The exact original prompt and generated master belong to the source-owned private audition receipt on the Ubuntu host; do not substitute a fresh unverified rerender as the "same" performance.
- **Original passage source:** `what-makes-a-page-modern.question.p1`, source text digest `ce476fec333cbfa6161b393452275b5b7fc56ed23d96eb9031c10eb5d8a4aa67`.
- **Author verdict scope:** **artistic vocal-character direction accepted**; both Take B and any replacement narrator remain **not selected**. This decision is not a claim that a complete exact-text recording exists, that accent has been independently certified, that the short audio itself is a canonical full edition, or that any MIDI 2.0 word-timing/cursor has passed live acceptance.
- **Follow-on:** preserve Take A's timbre using its hash-locked private audio reference and selected author direction through the existing owner-native spoken-edition workflow; render the *whole* exact text; independently recognize and correct any actual omissions/substitutions; only then derive qualified word timing and connect to the **existing** Fountain Press Linotype/SatzfunkPlayer MIDI2 cursor. Do not create a Reader, alternate transcript, public publication, or new generic voice preset.

**Audit distinction:** the earlier "unaccepted" observations in this document describe the *pre-decision audition* state. This dated author decision supersedes that status for **Take A's artistic character only**. Take B remains an archived comparison, not the selection.

## Source and exact model
The source is the first 126-character passage from what-makes-a-page-modern.question.p1 in the original admitted v144 Fountain Press essay. The essay's authoritative 13-page PDF SHA-256 is 2baaab0012e825b49f04e7a760b64efa52c95dc09deab7117de790f6c6e14bad. The passage begins "Two pages lie on a table" and its SHA-256 is ce476fec333cbfa6161b393452275b5b7fc56ed23d96eb9031c10eb5d8a4aa67.

The self-hosted Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign model at revision 5ecdb67327fd37bb2e042aab12ff7391903235d3 was acquired on the Ubuntu Mac mini. Actual model weights SHA-256 391e8db219f292c515297cdceeb43e4eae67cdde35fa57e79a6a8a532fca0522 and tokenizer weights SHA-256 836b7b357f5ea43e889936a3709af68dfe3751881acefe4ecf0dbd30ba571258 were verified before offline CPU inference; no paid API was invoked.

## Output evidence and limitations
Two private WAV masters remain in the host's ignored local candidate cache. Neither is committed to Git, automatically installed as a narrator voice or approved by the writer.

| Take | Direction | WAV duration | WAV SHA-256 | WLAN MP3 SHA-256 |
| --- | --- | ---: | --- | --- |
| A | Lucid, restrained contemporary British editorial narrator | 8.720 s | 39f19760f619f2dd8e9fad8af33dc51acfc8dab48235e3268881949f82d32a7f | 6f229cce508aa70236ee5c3b3eeb0bec7fe14bdc2296e0703d18016750ae91f8 |
| B | Warmer, conversational contemporary British literary narrator | 9.360 s | 4260e5cdaec0273ea5df4a52a55646eeb791796dfbdd05fa77a4bf728ca4ae1a | 845d07d3404a0527012752057a5c689c78b29cec863bbe9ddd15becc0da207b5 |

The WAV output is mono 24 kHz PCM16. The MP3 derivatives are private review media, not narration masters. Source-blind Qwen3-ASR 0.6B independently transcribed each WAV and recognized the entire spoken opening sentence; its recognition used US orthography "centered" in place of source "centred". Accordingly, strict text-equality acceptance was FALSE for both despite all other recognized words agreeing. This is NOT proof of a native British accent. Only actual listening by the writer and a qualified native-English assessor can admit pronunciation and Vergil's artistic character.

## Existing Reader stage only
Active candidate: shared-shell-20261104-v145-vergil-qwen-private-audition. Predecessor: shared-shell-20261104-v144-webreader-inset-66ec9c5, retained unmodified for rollback. The candidate was made as an independent rsync copy of v144 plus exactly two MP3 files under private-auditions/what-makes-a-page-modern-20261104-qwen3/. Existing Reader root HTML, source-lock and all other files are byte-identical; the original Linotype and MIDI2 assets are unchanged.

The existing ReaderProvenanceGate has a narrowly source-pinned extension that checks the approved v144 predecessor and entire candidate file inventory before serving. It requires exact hashes for both media, refuses any additional or edited file, and returns HTTP 403 for unknown private audition assets. The change is not an alternate reader or a public asset release.

Focused gate regression: 18 / 18 tests passed on the isolated source branch (existing 15 plus 3 candidate/negative tests). Offline gate against the actual immutable v145 candidate accepted the Reader and the two MP3 URLs. The first activation probe reached the newly restarted services before their sockets were listening; its transactional rollback restored both v144 and the previous gate, with independent HTTP and HTTPS 200 readback. The second activation used bounded readiness probing and succeeded. Both existing HTTP 8200 and HTTPS 8243 services were restarted without changing their host or TLS identity. Subsequent independent HTTPS GET readback from the authorized Mac reproduced both MP3 digests above, while the unapproved audition URL returned HTTP 403. The live Reader returned HTTP 200 with no-store and noindex headers.

## User-facing private listening URLs
- A: https://192.168.8.50:8243/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-a.mp3
- B: https://192.168.8.50:8243/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-b.mp3

Only the owner's WLAN staging host is targeted; no public DNS route or published edition changed. Both takes remain human-unaccepted. The existing essay remains readable whether or not the owner reviews the samples.

## Next gates
1. Writer listens and judges A, B or neither against the existing literary Vergil voice specification: natural British pronunciation, understated syntax-led cadence, quiet warmth without sentimentality or declamation, and whether the voice serves the original text.
2. Any accepted candidate must be source-locked through the existing FCIS spoken-edition Kit for longer passages, checked with independent waveform ASR and human accent/fidelity review before full-work rendering.
3. A complete approved chapter needs separately verified word timing and actual MIDI2 cursor synchronization in the existing Fountain Press Reader. The present two samples do NOT establish those claims.
