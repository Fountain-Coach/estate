# Kino International — two illustrated source figures in the existing sound essay (v166)

**Verified 6 November 2026.** Owner-WLAN **staging only**, not a public production release, a new Reader, a new audio instrument or an editorial acceptance of the acoustic result.

## Bounded writer request

Stage the same essay `A Sound Must Earn Its Place` with two writer-chosen figures: an architectural interpretation of Kino International after the opening paragraph, and the **original actual night photograph** near the transition to the Csound listening study. Do not produce a split collage, repeat the over-edited essay, alter either existing Csound recording, invent building dimensions, or silently copy private audio to public production. Preserve existing source addresses and captions.

## Source / exact delta

- Essay source owner `Fountain-Coach/fountain.coach`, source commit **`d79f9e0704c143f41dbf5d06a7458997e016f3e1`** on `codex/essay-csound-ab-20261106`.
- Revised source `a-sound-must-earn-its-place-v3.md` SHA-256 **`74d99a870040926c6e2ba86cb20e29b7c55585f385e9d0f56d6cc47b481f4432`**; same fifteen prose source blocks and same two native-Csound rendered audio tracks.
- Architectural plate: authored image interpretation from writer-provided photos, **not a measured elevation**, source-bound full web JPEG SHA-256 `9bfa71540c6b54a4ac83696fbc0506e31ae58e47c681634d9b93dc4386d31a1c`, width 1200.
- Night photograph: writer's genuine `IMG_1410.jpeg`, full web JPEG SHA-256 `cb7b399aeb472a65a7156f9d9990b39564ba492337ef19365ed079c68ac1bc52`, height 1450.
- Source manifest SHA-256 `3e40e8e014a66511cc23270ad8bd3e1ef7c693db1f855fac5e9d7c6bd325df9b`. Captions distinguish real photograph from architectural interpretation; no new copyright/rights claim for public release.
- Inherited v165 release `shared-shell-20261106-v165-satzfunk-csound-ab-eb45a85` remains immutable, all other works, Governances, Reader app `46876ca7b54c5f26df2372f1ec037871e61f6773a406ff41ec32a634337b7831` and existing Csound samples untouched.
- New v166 `estate/index.html` SHA-256 **`2184719abcb24b13ae3ca2c795f2dbabef5419ab46b817343a487efe8407abe1`**; only the one essay source template changed. The newly added files are precisely the two JPEGs, provenance manifest and stage evidence receipt (`53ca8c476c62fa8e95bbff3a566a58c4ce2de7db22aacb1d03c5a941bda3e3bc`). All preserved files independently compared.

## Active stage / acceptance

- Active immutable WLAN release: **`shared-shell-20261106-v166-essay-kino-figures-d79f9e0`**.
- New source-lock SHA-256: **`3ed927bf7388694d85aeb9c3afba878288e8ade4e9654c44285df3a4d59464ee`**.
- Existing native `reader_provenance_gate.py` extended with exact v166 source-and-asset admissions; **356-file guard acceptance passed**, including negative tests rejecting unknown image and sound paths. Guard SHA-256 `f441cd2ffd1a7d290b131055bd02f1ad5834e210d32a057486b51c065d9814ab`. Previous guard saved `reader_provenance_gate.py.pre-v166`.
- Atomic current pointer updated only after preflight. Existing HTTP 8200 and HTTPS 8243 services restarted; no new service/origin.
- Independent live HTTPS SHA-256 readbacks matched the full page, both image assets, provenance JSON and both untouched 16-second AAC files.
- **Three live Chromium layouts passed** (768x1024 iPad portrait, 1194x834 landscape, 390x844 phone): both images appear in source order, decode at nonzero dimensions, retain distinct captions, no horizontal overflow, existing Reader text through the closing sentence, and original Csound players remain part of the folios.
- **Separate actual live audio playback** passed in all three layouts when run without concurrent browser media tests: both existing source-bound takes play; switching to B stops A, final stop pauses both, each decodes at 16.064 seconds. A concurrent initial run encountered an intermittent no-advance media test; the subsequent single-run test passed in all viewports without any file change.

## Boundaries / rollback

- **Staging link:** https://192.168.8.50:8243/estate/#/read/essay--a-sound-must-earn-its-place
- **Not claimed:** public production promotion, physical iPad Safari or VoiceOver verification, measured architectural reproduction, or artistic/authorial judgment of the Csound work.
- **Rollback:** atomically repoint `current` to immutable `shared-shell-20261106-v165-satzfunk-csound-ab-eb45a85`, restart the existing staging services, and restore prior native guard from `reader_provenance_gate.py.pre-v166` if necessary. Do not publish WLAN-private audio or figures to public release by implication.
