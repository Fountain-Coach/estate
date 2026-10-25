# The Ear That Learns — source-bound listening edition, canonical WLAN stage v33

**Observed 25 October 2026.** Stage operator: `MacMiniDocker`, canonical registry `Fountain-Coach/estate/staging/environment.json`. This document records the existing WLAN source-locked staging service, not a public release or certificate of native iPad Safari behavior.

## Author's acceptance target

The initial Ear/Sing essay and typographic placeholder illustration failed the author's editorial review: the prose sounded like a loosely ordered list, its image did not share the existing essay print manufacture, and the argument about hearing had no audio. The accepted revision requires a new plate matching the architectural engraving series; continuous prose centered on an actual hearing problem; original Sing sound examples; and **direct source-time commentary using the existing SatzfunkPlayer media model**, not an unrelated generic audio widget.

## Frozen Git sources and media identity

- Fountain Coach owner `Fountain-Coach/fountain.coach@d6736cdb04d8e8a4d5acf6cb6c031e5aaf8d522c`.
- Semantic media owner `Fountain-Coach/SatzfunkPlayer@0d2ee25da224b71a24e997a4050805f157970d0c`.
- Canonical Estate stage-server owner `Fountain-Coach/estate@f2ac868da5d75deb6796958eaacd680229da88aa`.
- Adapted browser player module SHA-256: `c1e305f0886df66ee602d829b8ec61e27ff6a614d9d0cbbfb5f8c82bef7cfa6f`, checked into the essay as an exact copy of its SatzfunkPlayer owner.
- Authored technical engraving: `assets/listening-room.svg` and `assets/listening-room.png`. PNG SHA-256 `d07e55ebed5b0e9100a86191099b686c8c1802770b292c358d86208911dd269e`. The study label is **04 HEARING / REHEARSAL**; no human subject is depicted.
- The article narrates an original five-second synthetic `la mi na` recording and its one pitch-changing melisma as a coherent story. Opera (Italian/German/Spanish), tabla padhant and Hindustani vocal study inform the interpretation; no samples of those traditions are falsely claimed in the player.

Original 48 kHz PCM from Sing and separate private AAC-LC M4A derivatives (browser delivery SHA-256):

| Take | Original WAV SHA-256 | Private AAC SHA-256 |
| --- | --- | --- |
| Plain | `f4826365089889eafef579f5e0b3cf6f77d7bf570fcc0fa6e1d5f85ef191cf24` | `83b45c232a05abea5c3fe5fd25bee71630ce86e66eae78b9817cd60fd9ee8c21` |
| Articulated | `1d285c6b0a9dd2f7b7be58aac1509b5f55bcac5e3636c530cbec25f20db8f505` | `c27fe2ee9bd757b4b1d82aeb3f1ea82f7ff24b1b03741cc77408ebc1638cc807` |
| Expressive | `b7390503bdcb4669235fc417e0d21f8008c578f59228ab7ee0817e3df3ff8d27` | `acf902889e00a37bb832864ff826a612b468fb49900db8de02682cbefd6ab68f` |

The player uses native media controls, one immutable `sourceId`, select-take buttons, commentary at 0.00 / 1.15 / 2.15 / 3.35 s, and reader comments copied together with source WAV SHA, current playback position and a deep link. No comments are transmitted or persisted. Because private WLAN HTTP may not expose clipboard.writeText, the player provides selectable fallback text. Original PCM was used for Ear's published acoustic comparison; AAC is a derivative for human listening, not a source for claimed numerical measurements. The real Japanese singer/PJS references are not part of this private audio exhibition.

## Source and stage lineage

Predecessor `v31` was the private textual essay with source-preserving full published collection. The author-approved revision became immutable `shared-shell-20261025-v32-ear-sing-listening-74bc464` with **10 changed overlay files** (article, collection, CSS, player, SVG/PNG, three M4A files, source-lock). Source SHA-256 inventories and native preview `inspect()` accepted the candidate; unrelated domains were byte-preserved.

Actual Chrome playback revealed that query-addressed seek did not work because the existing WLAN HTTP service only provided `Range` responses for `.mp4`; a `Range: bytes=100-199` request to `.m4a` returned 200 with the full file. Instead of adding another server or altering the media identity, the established `serve_shared_shell_preview.py` was reconciled from the *actually deployed* server state into `Fountain-Coach/estate` and extended to allow `.m4a` ranges with `audio/mp4` MIME, `Accept-Ranges` and exact HTTP 206 responses. Existing historical-media restrictions, private source-lock protection and original `.mp4` handling are preserved.

- Running server original script SHA-256 `d4cb67b029861cd2df143b069f2632e957f2bcded5bf29ec8d2f5e95d3047947`; host backup `serve_shared_shell_preview.py.pre-ear-sing-m4a-20261025`.
- Updated server SHA-256 `68b9738c19ce7c504abb5013c4738628841bc566893f2d8e14df930f2eb76b7b` is the Git source and installed runtime.
- On the existing live service, ranged GET `bytes=100-199` returned **HTTP 206**, `Content-Range: bytes 100-199/166038`, `Content-Type: audio/mp4`, exactly 100 bytes, byte-identical to the underlying original AAC file at that offset.
- The source-owned browser module seek timing adjustment is in active immutable release **`shared-shell-20261025-v33-ear-sing-seek-d6736cd`**, activated from v32. The v32 immutable release remains rollback-ready; the active symlink points to v33. The service is active on the existing port 8200. No new service, public DNS, Caddy write, author media cloning, or GitHub CI was performed.

## Independent live proof

The v32 candidate's nine publicly served changed paths (excluding private source-lock) were each fetched through live WLAN HTTP, with exact SHA-256 matches. All three M4A files returned 200 with `audio/mp4`, the ES module 200 with `text/javascript`, SVG and PNG 200 with correct MIME, and the source-lock/contract remained private (404). The source-matched six-entry Essays collection includes *The Composable Book* and the new illustrated entry. The root, Instruments, Solstice First Reading and Teatro routes remained functional; the other domain files were compared byte-for-byte with the prior active release.

**Browser witness (local Chrome, real live WLAN origin):** 3 selectable takes, 4 comment positions for the current take, articulated 5.248 s AAC metadata and expected MIME, plain take manual cue seek to 2.15 s, expressive selected with source-time reader note and accessible copy fallback, direct address `?take=plain&t=2.15#listening-exhibit` loaded the correct original source **at 2.15 s** without autoplay; phone viewport 390 px, body/document width 390 px, native audio width 324 px, zero horizontal overflow, no unexpected browser network/JavaScript errors. The new shared source-bound player suite has 102 passing tests. This demonstrates browser real playback and sound-addressed comments without claiming actual source-blind phoneme recognition or real singing.

**Not claimed:** native Safari/iPad author acceptance, full public release, new Japanese phone-recognition success, singer qualification, legal right to publish third-party sources, typed EstatePublisher terminal receipt, or a persistent reader-comment backend. Published `https://fountain.coach/essays/the-ear-that-learns/` remains **404** and production `/essays/` and Instruments publicly served SHA digests remained unchanged in preactivation comparison.

## Copyable author review entrances

- Article: `http://192.168.8.50:8200/estate/essays/the-ear-that-learns/`
- First annotated /m/: `http://192.168.8.50:8200/estate/essays/the-ear-that-learns/?take=articulated&t=2.15#listening-exhibit`
- Essays: `http://192.168.8.50:8200/estate/essays/`
- Instruments: `http://192.168.8.50:8200/instruments/`

Outcome: **private staged article, original-sound audition, timed commentary and direct stage interlinking proven; production unchanged; immutable rollback retained.**
