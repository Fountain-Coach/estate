"""Fail-closed guard for the existing EstateShell WLAN preview Reader routes.

A copied/rewritten HTML page is not an admitted Fountain Press Reader.
The accepted v140 reader and public production asset comparison are pinned
below. No staged source-lock or newly copied page can whitelist itself.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ACCEPTED_STAGE = "shared-shell-20261103-v140-same-folio-return"
ACCEPTED_SOURCE_LOCK_SHA256 = "d263837865d282f495de905e3c43833be3b118faf0332529f61564b137bfaebc"
ACCEPTED_BOOKSHELF_SHA256 = "69e656346b219be35c030e437100e72338f54d3a70abecbe6030971773cb1c01"
ACCEPTED_LINOTYPE_TREE_SHA256 = "307a04e852c382229f45c43ed6ad075674b24e3fcf3cae51e012fbb223458569"

# Deliberately reviewed exception to the accepted Reader's content source only.
# The source Git branch/commit and the immutable candidate receipt have both
# been checked against the *same* v140 Reader, not against a second HTML app.
APPROVED_ESSAY_RELEASE = "shared-shell-20261104-v142-modern-page-original-reader-5be4d5d"
APPROVED_ESSAY_SOURCE_COMMIT = "5be4d5d4219171686b31a377cfa480e707d27d6b"
APPROVED_ESSAY_PDF_SHA256 = "2baaab0012e825b49f04e7a760b64efa52c95dc09deab7117de790f6c6e14bad"
APPROVED_ESSAY_LOCK_SHA256 = "6f25b5a3adc714b5a0f82a15713c2f566955063a348dce03bfb5bf1071408066"
APPROVED_ESSAY_INDEX_SHA256 = "c6a3f3744a8c18ed015096b7990133a037eb4c9ff23ffb38c7529d2af087ffd1"
APPROVED_ESSAY_APP_SHA256 = "46afd64a10b76f7d9cdc11ddf665a25efbb874d78da59fb165d4e00fc707a27c"
APPROVED_ESSAY_ASSETS = {
    "address.svg", "classical.svg", "colophon.svg", "conditions.svg",
    "cursor.svg", "joyce.svg", "machine.svg", "midi.svg", "modern.svg",
    "proof.svg", "question.svg", "reader.svg", "return.svg"
}
APPROVED_ESSAY_ASSET_DIR = "estate/essays/what-makes-a-page-modern/assets/"
APPROVED_FIGURE_RELEASE = "shared-shell-20261104-v143-modern-page-balanced-6a15b6c"
APPROVED_WEB_READER_RELEASE = "shared-shell-20261104-v144-webreader-inset-66ec9c5"

# Author-WLAN-only listening derivatives. No Reader or narration source mutation.
# Original WAVs, model snapshots, transcripts and approval receipts stay private.
APPROVED_VERGIL_AUDITION_RELEASE = "shared-shell-20261104-v145-vergil-qwen-private-audition"
APPROVED_VERGIL_LISTENING_RELEASE = "shared-shell-20261104-v146-vergil-qwen-listening-page"
APPROVED_VERGIL_LISTENING_ROUTE = "private-auditions/what-makes-a-page-modern-20261104-qwen3/index.html"
APPROVED_VERGIL_LISTENING_GIT_BLOB = "76b48a3fe14f1fb7e08de08e362de104b620c109"

# Writer-approved combined essay on the ORIGINAL production-derived Reader.
# Source is a new revision; the earlier 13-page PDF is retained as provenance.
# v146 private Vergil/Qwen auditions and all Reader runtime bytes stay unchanged.
APPROVED_SELF_OUT_LOUD_RELEASE = "shared-shell-20261105-v147-self-out-loud-c884a3e"
APPROVED_SELF_OUT_LOUD_PREDECESSOR = APPROVED_VERGIL_LISTENING_RELEASE
APPROVED_SELF_OUT_LOUD_SOURCE_COMMIT = "c884a3e3bd04a2269212b7c5a7dadd6ef92e900f"
APPROVED_SELF_OUT_LOUD_SOURCE_SHA256 = "4b3c0c2b2f02d707d0c88d3c4f045c8119d05707709512a832e995c648edf272"
APPROVED_SELF_OUT_LOUD_READER_SHA256 = "11cd731753769f5feacd2f91dc2ba1fc8c0e914d5d107b00f9c98ad58eff3c2c"
APPROVED_SELF_OUT_LOUD_LOCK_SHA256 = "75b8407fbc9762718df82560f5a7b2d4bb433dd6f52881c663fc115530453ea8"

# A source-owned typographic demonstration, inside the SAME Reader.
# v148 restores 11 exact author-specified figure anchors and clearly stages
# the original pair of specimen SVGs; all other stage assets are untouched.
APPROVED_SPECIMEN_RELEASE = "shared-shell-20261105-v148-specimen-boundary-a9575ba"
APPROVED_SPECIMEN_PREDECESSOR = APPROVED_SELF_OUT_LOUD_RELEASE
APPROVED_SPECIMEN_SOURCE_COMMIT = "a9575ba976917433baf0cc67940b5941e4c1de96"
APPROVED_SPECIMEN_SOURCE_SHA256 = "8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6"
APPROVED_SPECIMEN_READER_SHA256 = "532dbdf6603fb1300a974418130c50cbc17636262d9dcf7c0a802c3aabfdd81c"
APPROVED_SPECIMEN_LOCK_SHA256 = "90d23ed381ece45f54d9621ca7341e204d5967738f1f48b3af2d8eab42483e1c"

# First true nested measured typography on the existing Press compositor.
# Exact Git content and a fixed four-file delta from the admitted v148 stage.
APPROVED_NESTED_RELEASE = "shared-shell-20261105-v149-nested-specimen-ce0c1cd"
APPROVED_NESTED_PREDECESSOR = APPROVED_SPECIMEN_RELEASE
APPROVED_NESTED_SOURCE_COMMIT = "ce0c1cd704664027d94d6dd4c196b9c06e037e38"
APPROVED_NESTED_SOURCE_SHA256 = "8f7d60f9ae3cfd1dd6e95a92d869c050241a93482ab00688be7ad3422d2786d6"
APPROVED_NESTED_SPECIMEN_SOURCE_SHA256 = "693ca56d01757d03d2210234def136256cd04145efce95fc1fc205cf15c6658a"
APPROVED_NESTED_LOCK_SHA256 = "935275ea1f3971a4307d6df445c7c925e005e8ce3be50ea0d25fa9dd309932e2"
APPROVED_NESTED_FILES = {
    "estate/index.html": "8ca2c693f4ae275f16331f3989790016a7f0ba3d0a2c2dc34d58e3a4f432478f",
    "estate/assets/linotype/reading-first-press-engine.js": "67a3c842c92e86839a35cbee44c533d143f893eda954d750c0eddfffcad64058",
    "estate/assets/linotype/reading-first-press-frame.css": "f7a85b7e573655bee124dc4218c0cb9ecdc4300b433b5ab0237e734507a03c03"
}

# v150: exactly two Press compositor/styles source files differ from v149.
# Do not admit a new reader, author route, media file, or public edition.
APPROVED_FLUID_RELEASE = "shared-shell-20261105-v150-fluid-nested-3ba1b0e"
APPROVED_FLUID_PREDECESSOR = APPROVED_NESTED_RELEASE
APPROVED_FLUID_SOURCE_COMMIT = "3ba1b0e826efcec947e243100c2925ad78d2953e"
APPROVED_FLUID_LOCK_SHA256 = "f10275f49d5da6837d6572b6508bb51b9752a4a25ffcb08ed4f9835fa986eee0"
APPROVED_FLUID_FILES = {
    "estate/assets/linotype/reading-first-press-engine.js":
        "52f30f9fd36f3f1ccb24bd833b14f91289d270df394f8418a77cc672ee7c5342",
    "estate/assets/linotype/reading-first-press-frame.css":
        "8e175ccbdfdd71e506979772059c72fcfb85de8d3daa366a34544ccc7d4502e6"
}


# One admissible source-bound v151 semantic spread compositor revision.
# Its only published-stage code delta is the existing Press engine.
APPROVED_SPREAD_RELEASE = "shared-shell-20261105-v151-semantic-spread-17e32af"
APPROVED_SPREAD_PREDECESSOR = APPROVED_FLUID_RELEASE
APPROVED_SPREAD_SOURCE_COMMIT = "17e32af5b875ec5356ddfa8a9680711d60aaa4eb"
APPROVED_SPREAD_LOCK_SHA256 = "ad15c096e83c4695c1b0feb1ec85a3f5f354498baf3a3ffc42d05cff1cad97b9"
APPROVED_SPREAD_FILES = {
    "estate/assets/linotype/reading-first-press-engine.js":
        "e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a"
}


# v152 archive current membership while preserving the original authored work.
APPROVED_ARCHIVE_RELEASE = "shared-shell-20261105-v152-editorial-archive-1609cb9"
APPROVED_ARCHIVE_PREDECESSOR = APPROVED_SPREAD_RELEASE
APPROVED_ARCHIVE_SOURCE_COMMIT = "1609cb909ae2f89b4b28223fe70c482638d6b854"
APPROVED_ARCHIVE_LOCK_SHA256 = "34953bb41c8bb405183809a138b1d0e32272419dcf303fe3f74ce7c875061317"
APPROVED_ARCHIVE_FILES = {
    "estate/index.html":"77f90b8db05a42700f727b4558f7e91a6406e2ae6bf25d59d953fa5ddae7b3d9",
    "estate/assets/linotype/reading-first-app.js":"9fa017c008cebad8586a49a03741aae398a36a0fc61e935364f45b6e913b6345",
    "estate/essays/index.html":"a72cf4bcd1cffebb94585ee20ccb7c4eb2dab4652a85c7d9555cac2b62014e08",
    "estate/assets/essay-share/manifest.json":"21326154d893de327ca889596b4bd8da074d984c16d476a3f1afc0f8abfeefa3"
}
APPROVED_ARCHIVED_WORK_SOURCE_SHA256 = "553b26f69963d0787c416b64b56591d3ccb46b01541d57debf1f79dc5d6a1714"
APPROVED_ARCHIVED_WORK_STAGE_SHA256 = "2eb20df27e4b1a85c2c531f061a712f2aaf66f792df5cda518bb14b62d0822b3"


APPROVED_VERGIL_AUDITION_ASSETS = {
    "private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-a.mp3":
        "6f229cce508aa70236ee5c3b3eeb0bec7fe14bdc2296e0703d18016750ae91f8",
    "private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-b.mp3":
        "845d07d3404a0527012752057a5c689c78b29cec863bbe9ddd15becc0da207b5",
}

APPROVED_WEB_READER_SOURCE_COMMIT = "66ec9c5144953766bc99e7f9cf704b5ea17cf7a0"
APPROVED_WEB_READER_LOCK_SHA256 = "9ffddfa9fdd5bf853c973de266bcdc71404f954342c8931ca6e53e82f0da9396"
APPROVED_WEB_READER_INDEX_SHA256 = "9d8b6c330146f4b7d1b6e437aa916f89aca99e110de7c8f24060df29050bd8c5"
APPROVED_WEB_READER_SVG_SHA256 = "778a1a33b7f69e34f5603e02950d245abd221fff3ea260c02310a2a4d79df9fb"
APPROVED_WEB_READER_SVG_PATH = "estate/essays/what-makes-a-page-modern/assets/reader.svg"
APPROVED_FIGURE_LOCK_SHA256 = "0471e8d18d3ba80b365b1d744bfebd5548840da50ee2945cedc5274715a64990"
APPROVED_FIGURE_SOURCE_COMMIT = "6a15b6c63d64a5e09da491b93f6e35c6dcc29b21"
APPROVED_FIGURE_HTML_SHA256 = "610f1cde53ca00d3e2e249c2cc965acd53f084a7b447566855f05fa28766c720"
APPROVED_FIGURE_ASSET_SHA256 = {
    "address.svg": "5fb7b53bd74fe4425c9e2bc2e967084170d3b940a57c4b2a0c9dff1d0cca7d2b",
    "classical.svg": "87843cf80d8069cd94c78032709c2fcb9e7546b253fe8e1cbeb63fcb7f843c60",
    "colophon.svg": "be5a4e96c9138562cace84faf2001e90f8e9b829f06ec20876460edae5e7ebe4",
    "conditions.svg": "151aa2a5c715dbc44327ca1762d001de80f2f8abaf2a2d9c3224c49df4f98fc8",
    "cursor.svg": "da859a9f710f0cd983141bff9167608d57801f23856d91e523f78c7016ae5076",
    "joyce.svg": "bd0a30128db88aa2d0e5341d08de1810c13f9d57f3e89ac314e959f89150e965",
    "machine.svg": "b896e4bac655bef13df12618cde4a8ec4dd7cbcdcb29aec30d5f44621213f341",
    "midi.svg": "70c06ea968b1cbcccf96fe178dfa54ce3b8a48562f17941573515614d34aa7d3",
    "modern.svg": "dfd404b517d475121a11fc49f1596816dbbf7bae74268b02c14f4cb97710a98e",
    "proof.svg": "7da53f80040b50820f0bf5248d0e3b4ccc04d3537c00767de21ef6c09eb64bd2",
    "question.svg": "147d2cfd793518420603fc253af102aea44bb875f2ab9c6044ace8dbf4f61888",
    "reader.svg": "4584338a86f27c26f446eb5b9e269a9e43c12ce540bdf026a7f9f211615be7bb",
    "return.svg": "a6928ab50245d72fef67dda6dd6383c4aba226761a7e99c8f8d66f960802ac7f",
}
APPROVED_ESSAY_CHANGE_PATHS = frozenset({
    "estate/index.html", "estate/assets/linotype/reading-first-app.js",
    *(APPROVED_ESSAY_ASSET_DIR + f for f in APPROVED_ESSAY_ASSETS),
})

# Observed from public HTTPS and the accepted v140 WLAN Reader on 2026-11-04.
# The main Reader app has a stage-only source-address/rehearsal delta.
# It must not be silently overwritten by public bytes or a new implementation.
PRODUCTION_READER = {
    "reading-first-press-engine.js": "0fed47d6d2bb4c61565cbc37d9f6df21da3f650b365dc1856ee72fdb95eaba4d",
    "reading-first-app.js": "4243dea9d3d8be1187f0c72cbde994e7748eebaeacc78e91d618b222024cfea4",
    "teatro-vergil-hearing.mjs": "185744bbc4daa72cc55044720d089b854f1cf2d6ca2eab10d868ac74e72ca720",
    "vergil-prologue-hearing.mjs": "5d60ecfa5ecadce573c40ede51f83c88cd359c8f6e822fe18938c5fef336a9d8",
    "reading-first-press-frame.css": "4cd2f853315d51bdd2c31917782d42759fee0a9a20cf18ae4d261af085bd0e51",
    "reading-first-press-host.css": "a0ce4a3ba7c0e549354de8b3aaed608ad178f62bcfbc3451e3443f2989ea84b0",
    "reading-first-shell.css": "769fb12fbe7205e90269ecbf3760c8a6d226e78347bd1d62f05035174d671247",
    "teatro-vergil-hearing.css": "aff97c7676e9f3cf254beba93f5e17d3d0bf57956b72f86e4c9cff750317314a",
    "vergil-prologue-hearing.css": "a77abac2539be9c991e23f064851d12db5a1dfeb2e853de8a1a5c7beb3c553ce",
}
STAGE_READER = dict(PRODUCTION_READER, **{
    "reading-first-app.js": "557ba7736110ccf1ae4819549b3bf80fa1d6c411cf3b77b0e977db8aace23253",
    "teatro-vergil-hearing.mjs": "ef22bbe0109dd39d3fc5772f222b6e38d6b388d2ee327467c522f4ea6515dd18",
    "vergil-prologue-hearing.mjs": "25a248b4a12ec189292fe44e297b2c7f2a7b2edd59d9a58db48ce66fcb938b61"
})


class UnadmittedReaderRoute(ValueError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linotype_inventory(root: Path) -> tuple[str, dict[str, str]]:
    directory = root / "estate/assets/linotype"
    if not directory.is_dir():
        raise UnadmittedReaderRoute("Accepted Reader asset directory missing")
    assets = {}
    for p in sorted(directory.rglob("*")):
        if p.is_file():
            rel = p.relative_to(directory).as_posix()
            if p.is_symlink() or not p.resolve().is_relative_to(directory.resolve()):
                raise UnadmittedReaderRoute("Unexpected Reader asset symlink")
            assets[rel] = sha256(p)
    witness = "\n".join(name + "\t" + digest for name, digest in assets.items())
    return hashlib.sha256(witness.encode()).hexdigest(), assets


def normalized_request_path(raw_url: str) -> str:
    parsed = urlsplit(raw_url)
    path = unquote(parsed.path)
    if not path.startswith("/") or "\x00" in path or "\\" in path:
        raise UnadmittedReaderRoute("Invalid Reader URL")
    parts = path.strip("/").split("/")
    if any(part in (".", "..") for part in parts):
        raise UnadmittedReaderRoute("Unsafe Reader URL")
    if path.endswith("/"):
        path += "index.html"
    return path.lstrip("/")


def protected_reader_html(rel: str) -> bool:
    # No new or modified HTML within a book/publication root may be served
    # without independent source and production-lineage approval. This also
    # covers new deep-link conventions and not just the incident's /essays URL.
    return rel.endswith(".html") and rel.startswith((
        "estate/", "book/", "solstice/editions/"))


def reader_parent(rel: str) -> str | None:
    match = re.match(r"^estate/essays/([^/]+)/assets/", rel)
    return "estate/essays/" + match.group(1) + "/index.html" if match else None


def approved_essay_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Re-admit ONLY the signed-off v140 content delta. The stage cannot
    authorize itself by editing its source-lock: the lock's bytes and owning
    Git identity are independently pinned here in this reviewed source file.
    """
    if candidate.name != APPROVED_ESSAY_RELEASE:
        return {}
    if sha256(candidate / "source-lock.json") != APPROVED_ESSAY_LOCK_SHA256:
        raise UnadmittedReaderRoute("Wrong edition admission/source-lock digest")
    try:
        current_lock = json.loads((candidate / "source-lock.json").read_text())
        original_lock = json.loads((baseline / "source-lock.json").read_text())
        admission = current_lock.pop("modernPageExistingReaderAdmission")
    except (ValueError, KeyError, OSError) as error:
        raise UnadmittedReaderRoute("Missing bounded Reader source admission") from error
    if current_lock != original_lock:
        raise UnadmittedReaderRoute("Existing source-lock lineage was rewritten")
    approved_meta = {
        "schema": "fountain.press.existing-reader.essay-addition.v1",
        "sourceOwner": "Fountain-Coach/fountain.coach",
        "sourceCommit": APPROVED_ESSAY_SOURCE_COMMIT,
        "sourcePDFSHA256": APPROVED_ESSAY_PDF_SHA256,
        "predecessor": ACCEPTED_STAGE,
        "release": APPROVED_ESSAY_RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchangedExceptGalleryMembership": True,
        "notAnAlternateReader": True,
    }
    if set(admission) != set(approved_meta) | {"fileSHA256"} or any(
        admission[k] != value for k, value in approved_meta.items()
    ):
        raise UnadmittedReaderRoute("Unrecognized edited-reader admission")
    files = admission["fileSHA256"]
    if not isinstance(files, dict) or set(files) != APPROVED_ESSAY_CHANGE_PATHS:
        raise UnadmittedReaderRoute("New Reader files do not match reviewed scope")
    if files["estate/index.html"] != APPROVED_ESSAY_INDEX_SHA256 or (
        files["estate/assets/linotype/reading-first-app.js"] != APPROVED_ESSAY_APP_SHA256
    ):
        raise UnadmittedReaderRoute("Reader source does not match approved Git")
    for name, expected in files.items():
        file = candidate / name
        if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
            raise UnadmittedReaderRoute("Invalid admitted asset digest")
        if file.is_symlink() or not file.is_file() or sha256(file) != expected:
            raise UnadmittedReaderRoute("Unverified approved Reader asset: " + name)

    # Exact candidate = unchanged v140 release + the allowed 15 files and
    # the pinned source-lock. Do not trust a new route merely because its
    # HTML references the genuine engine.
    def files_under(root: Path):
        return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}
    before = files_under(baseline)
    after = files_under(candidate)
    changed = set(before) ^ set(after)
    for name in set(before) & set(after):
        left, right = before[name], after[name]
        a, b = left.stat(), right.stat()
        if a.st_dev == b.st_dev and a.st_ino == b.st_ino:
            continue
        if sha256(left) != sha256(right):
            changed.add(name)
    if changed != APPROVED_ESSAY_CHANGE_PATHS | {"source-lock.json"}:
        raise UnadmittedReaderRoute("Unexpected addition or modification in staged Reader")
    return dict(files)


def approved_balanced_essay_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Bounded v143 correction on the SAME v142 reader; no alternate shell.

    Protect the old v142 signed admission as a predecessor, not just an
    editable JSON manifest inside the candidate. Full-tree file comparison
    excludes undeclared changed bytes, including source-owned SVGs.
    """
    if candidate.name != APPROVED_FIGURE_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_ESSAY_RELEASE
    if not predecessor.is_dir():
        raise UnadmittedReaderRoute("Missing admitted v142 predecessor")
    inherited = approved_essay_files(baseline, predecessor)
    if len(inherited) != 15 or (
        sha256(predecessor / "source-lock.json") != APPROVED_ESSAY_LOCK_SHA256
    ):
        raise UnadmittedReaderRoute("No verified v142 Reader predecessor")
    if sha256(candidate / "source-lock.json") != APPROVED_FIGURE_LOCK_SHA256:
        raise UnadmittedReaderRoute("Changed balanced-figure source-lock digest")
    try:
        current_lock = json.loads((candidate / "source-lock.json").read_text())
        original_lock = json.loads((predecessor / "source-lock.json").read_text())
        admission = current_lock.pop("modernPageFigureBalanceAdmission")
    except (ValueError, KeyError, OSError) as error:
        raise UnadmittedReaderRoute("Missing reviewed figure-layout admission") from error
    if current_lock != original_lock:
        raise UnadmittedReaderRoute("v142 Reader source identity was rewritten")
    meta = {
        "schema": "fountain.press.figure-balance.existing-reader.v1",
        "sourceOwner": "Fountain-Coach/fountain.coach",
        "sourceCommit": APPROVED_FIGURE_SOURCE_COMMIT,
        "sourcePDFSHA256": APPROVED_ESSAY_PDF_SHA256,
        "predecessor": APPROVED_ESSAY_RELEASE,
        "release": APPROVED_FIGURE_RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchanged": True,
        "originalManuscriptUnchanged": True,
        "visibleFrameAlignedToText": True,
    }
    if set(admission) != set(meta) | {"fileSHA256"} or any(
        admission.get(name) != value for name, value in meta.items()
    ):
        raise UnadmittedReaderRoute("Unrecognized source-owned figure revision")
    exact = {"estate/index.html": APPROVED_FIGURE_HTML_SHA256}
    exact.update({
        APPROVED_ESSAY_ASSET_DIR + name: digest
        for name, digest in APPROVED_FIGURE_ASSET_SHA256.items()
    })
    if admission["fileSHA256"] != exact:
        raise UnadmittedReaderRoute("Figure source digest registry mismatched")
    for name, digest in exact.items():
        path = candidate / name
        if path.is_symlink() or not path.is_file() or sha256(path) != digest:
            raise UnadmittedReaderRoute("Unreviewed figure source bytes: " + name)

    def inventory(root: Path):
        return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}
    before = inventory(predecessor)
    after = inventory(candidate)
    changed = set(before) ^ set(after)
    for name in set(before) & set(after):
        older, newer = before[name], after[name]
        a, b = older.stat(), newer.stat()
        if a.st_dev == b.st_dev and a.st_ino == b.st_ino:
            continue
        if sha256(older) != sha256(newer):
            changed.add(name)
    if changed != set(exact) | {"source-lock.json"}:
        raise UnadmittedReaderRoute("Unexpected Reader change beyond approved figures")
    return {**inherited, **exact}


def approved_web_reader_inset_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """One SVG internal-ink correction on the accepted, unchanged v143 Reader."""
    if candidate.name != APPROVED_WEB_READER_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_FIGURE_RELEASE
    if not predecessor.is_dir():
        raise UnadmittedReaderRoute("No original v143 Reader predecessor")
    inherited = approved_balanced_essay_files(baseline, predecessor)
    if len(inherited) != 15 or sha256(predecessor / "source-lock.json") != APPROVED_FIGURE_LOCK_SHA256:
        raise UnadmittedReaderRoute("v143 figure source was not admitted")
    if sha256(candidate / "source-lock.json") != APPROVED_WEB_READER_LOCK_SHA256:
        raise UnadmittedReaderRoute("Changed v144 source-lock receipt")
    try:
        current_lock = json.loads((candidate / "source-lock.json").read_text())
        original_lock = json.loads((predecessor / "source-lock.json").read_text())
        admission = current_lock.pop("modernPageWebReaderInsetAdmission")
    except (KeyError, ValueError, OSError) as error:
        raise UnadmittedReaderRoute("Missing verified WEB READER inset admission") from error
    if current_lock != original_lock:
        raise UnadmittedReaderRoute("Existing v143 editorial source was modified")
    exact = {
        "estate/index.html": APPROVED_WEB_READER_INDEX_SHA256,
        APPROVED_WEB_READER_SVG_PATH: APPROVED_WEB_READER_SVG_SHA256,
    }
    required = {
        "schema": "fountain.press.semantic-figure-inset.existing-reader.v1",
        "sourceOwner": "Fountain-Coach/fountain.coach",
        "sourceCommit": APPROVED_WEB_READER_SOURCE_COMMIT,
        "sourcePDFSHA256": APPROVED_ESSAY_PDF_SHA256,
        "predecessor": APPROVED_FIGURE_RELEASE,
        "release": APPROVED_WEB_READER_RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchanged": True,
        "originalManuscriptUnchanged": True,
        "innerTextFitsFrame": True,
        "fileSHA256": exact,
    }
    if admission != required:
        raise UnadmittedReaderRoute("v144 source identity/allowed files do not match source")
    for rel, digest in exact.items():
        item = candidate / rel
        if not item.is_file() or item.is_symlink() or sha256(item) != digest:
            raise UnadmittedReaderRoute("Unverified internal diagram source: " + rel)
    def inventory(root: Path):
        return {x.relative_to(root).as_posix():x for x in root.rglob("*") if x.is_file()}
    before, after = inventory(predecessor), inventory(candidate)
    if set(before) != set(after):
        raise UnadmittedReaderRoute("Changed v143 Reader route inventory")
    changed = set()
    for rel in before:
        a,b = before[rel],after[rel]
        if a.stat().st_dev==b.stat().st_dev and a.stat().st_ino==b.stat().st_ino:
            continue
        if sha256(a) != sha256(b):
            changed.add(rel)
    if changed != set(exact) | {"source-lock.json"}:
        raise UnadmittedReaderRoute("Change beyond approved WEB READER internal padding")
    return {**inherited, **exact}


def approved_private_vergil_audition_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Allow only two hash-pinned audition MP3s beside unchanged v144 Reader.

    This cannot authorize itself from a modified source-lock or arbitrary
    stage content. The predecessor must pass the existing v144 check first.
    """
    if candidate.name != APPROVED_VERGIL_AUDITION_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_WEB_READER_RELEASE
    if not predecessor.is_dir() or not candidate.is_dir():
        raise UnadmittedReaderRoute("Missing v144 Reader predecessor for private audition")
    inherited = approved_web_reader_inset_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Unverified v144 Reader predecessor for private audition")
    before = {p.relative_to(predecessor).as_posix(): p
              for p in predecessor.rglob("*") if p.is_file()}
    after = {p.relative_to(candidate).as_posix(): p
             for p in candidate.rglob("*") if p.is_file()}
    if set(after) != set(before) | set(APPROVED_VERGIL_AUDITION_ASSETS):
        raise UnadmittedReaderRoute("Private audition changed v144 Reader inventory")
    for rel, original in before.items():
        present = after[rel]
        if present.is_symlink() or sha256(original) != sha256(present):
            raise UnadmittedReaderRoute("Private audition changed Reader file: " + rel)
    for rel, expected in APPROVED_VERGIL_AUDITION_ASSETS.items():
        present = after[rel]
        if present.is_symlink() or sha256(present) != expected:
            raise UnadmittedReaderRoute("Wrong private audition recording: " + rel)
    return inherited


def git_blob_sha1(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + bytes([0]) + raw).hexdigest()


def approved_private_vergil_listening_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Only one pinned Git-owned HTML listening route beyond exact v145."""
    if candidate.name != APPROVED_VERGIL_LISTENING_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_VERGIL_AUDITION_RELEASE
    if not predecessor.is_dir() or not candidate.is_dir():
        raise UnadmittedReaderRoute("Missing reviewed v145 audition predecessor")
    inherited = approved_private_vergil_audition_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Unverified v145 audition predecessor")
    before = {p.relative_to(predecessor).as_posix(): p
              for p in predecessor.rglob("*") if p.is_file()}
    after = {p.relative_to(candidate).as_posix(): p
             for p in candidate.rglob("*") if p.is_file()}
    if set(after) != set(before) | {APPROVED_VERGIL_LISTENING_ROUTE}:
        raise UnadmittedReaderRoute("Unapproved private listening release inventory")
    for rel, original in before.items():
        candidate_file = after[rel]
        if candidate_file.is_symlink() or sha256(candidate_file) != sha256(original):
            raise UnadmittedReaderRoute("Existing Reader or audition file changed: " + rel)
    page = after[APPROVED_VERGIL_LISTENING_ROUTE]
    if page.is_symlink() or git_blob_sha1(page) != APPROVED_VERGIL_LISTENING_GIT_BLOB:
        raise UnadmittedReaderRoute("Unverified Git-owned listening page")
    return inherited


def approved_self_out_loud_essay_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """v147: allow only a new source-bound essay composition on exact v146.

    Preserve both v145 private recordings, v146 private listening page, the
    production-derived Reader engine and every other book. Pin the revised
    manuscript's Git commit/digest separately from the immutable candidate.
    """
    if candidate.name != APPROVED_SELF_OUT_LOUD_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_SELF_OUT_LOUD_PREDECESSOR
    if not predecessor.is_dir() or not candidate.is_dir():
        raise UnadmittedReaderRoute("Missing exact approved v146 predecessor")
    inherited = approved_private_vergil_listening_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Unverified accepted v146 Reader before new manuscript")
    if sha256(candidate / "source-lock.json") != APPROVED_SELF_OUT_LOUD_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unrecognized v147 manuscript source-lock digest")
    try:
        current_lock = json.loads((candidate / "source-lock.json").read_text())
        before_lock = json.loads((predecessor / "source-lock.json").read_text())
        admission = current_lock.pop("modernPageSelfOutLoudAdmission")
    except (ValueError, KeyError, OSError) as error:
        raise UnadmittedReaderRoute("Missing v147 source admission") from error
    if current_lock != before_lock:
        raise UnadmittedReaderRoute("v147 changed inherited source-lock identity")
    expected = {
        "schema": "fountain.press.modern-page-self-out-loud-edition.v1",
        "sourceOwner": "Fountain-Coach/fountain.coach",
        "sourceCommit": APPROVED_SELF_OUT_LOUD_SOURCE_COMMIT,
        "sourcePath": "site/essays/what-makes-a-page-modern/combined-essay.md",
        "sourceSHA256": APPROVED_SELF_OUT_LOUD_SOURCE_SHA256,
        "earlierDruckfahnePDFSHA256": APPROVED_ESSAY_PDF_SHA256,
        "predecessor": APPROVED_SELF_OUT_LOUD_PREDECESSOR,
        "release": APPROVED_SELF_OUT_LOUD_RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchanged": True,
        "originalIllustrationsUnchanged": True,
        "fileSHA256": {"estate/index.html": APPROVED_SELF_OUT_LOUD_READER_SHA256}
    }
    if admission != expected:
        raise UnadmittedReaderRoute("v147 source revision is not the approved Git manuscript")
    root = candidate / "estate/index.html"
    if root.is_symlink() or not root.is_file() or sha256(root) != APPROVED_SELF_OUT_LOUD_READER_SHA256:
        raise UnadmittedReaderRoute("Revised essay root does not match approved content digest")
    before = {p.relative_to(predecessor).as_posix(): p
              for p in predecessor.rglob("*") if p.is_file()}
    after = {p.relative_to(candidate).as_posix(): p
             for p in candidate.rglob("*") if p.is_file()}
    if set(before) != set(after):
        raise UnadmittedReaderRoute("v147 added or removed existing stage files")
    changed = set()
    for rel, old_file in before.items():
        file = after[rel]
        if file.is_symlink() or not file.is_file():
            raise UnadmittedReaderRoute("v147 introduced an unreviewed symlink")
        if old_file.stat().st_dev == file.stat().st_dev and old_file.stat().st_ino == file.stat().st_ino:
            continue
        if sha256(old_file) != sha256(file):
            changed.add(rel)
    if changed != {"estate/index.html", "source-lock.json"}:
        raise UnadmittedReaderRoute("v147 modified unrelated Reader, media or source assets")
    return {**inherited, "estate/index.html": APPROVED_SELF_OUT_LOUD_READER_SHA256}


def approved_typographic_specimen_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Admit a single source-owned v148 setting correction to v147 Reader.

    The printer's nested type specimens have their own frames and precise
    source paragraph anchors, but the existing Reader engine, original SVG
    art, books, private recordings and listening routes are unchanged.
    """
    if candidate.name != APPROVED_SPECIMEN_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_SPECIMEN_PREDECESSOR
    if not predecessor.is_dir() or not candidate.is_dir():
        raise UnadmittedReaderRoute("v148 requires the exact admitted v147 Reader")
    inherited = approved_self_out_loud_essay_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Unadmitted v147 Reader ancestor")
    if sha256(candidate / "source-lock.json") != APPROVED_SPECIMEN_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unrecognized v148 source-lock digest")
    try:
        after = json.loads((candidate / "source-lock.json").read_text())
        before = json.loads((predecessor / "source-lock.json").read_text())
        admission = after.pop("modernPageTypographicSpecimenAdmission")
    except (KeyError, ValueError, OSError) as exc:
        raise UnadmittedReaderRoute("Missing signed-off v148 source addition") from exc
    if after != before:
        raise UnadmittedReaderRoute("v148 mutated inherited publication source identity")
    expected = {
        "schema": "fountain.press.typographic-specimen-source-anchor.v1",
        "sourceOwner": "Fountain-Coach/fountain.coach",
        "sourceCommit": APPROVED_SPECIMEN_SOURCE_COMMIT,
        "sourcePath": "site/essays/what-makes-a-page-modern/combined-essay.md",
        "sourceSHA256": APPROVED_SPECIMEN_SOURCE_SHA256,
        "earlierDruckfahnePDFSHA256": APPROVED_ESSAY_PDF_SHA256,
        "predecessor": APPROVED_SPECIMEN_PREDECESSOR,
        "release": APPROVED_SPECIMEN_RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchanged": True,
        "originalIllustrationsUnchanged": True,
        "typographicSpecimensFramed": 2,
        "duplicateNarrativeSpecimensRemoved": 2,
        "authoredInlineFigureAnchors": 11,
        "fileSHA256": {"estate/index.html": APPROVED_SPECIMEN_READER_SHA256}
    }
    if admission != expected:
        raise UnadmittedReaderRoute("Revised typographic source identity is not admitted")
    html = candidate / "estate/index.html"
    if html.is_symlink() or not html.is_file() or sha256(html) != APPROVED_SPECIMEN_READER_SHA256:
        raise UnadmittedReaderRoute("Wrong v148 source-bound Reader root")
    before_files = {p.relative_to(predecessor).as_posix():p for p in predecessor.rglob("*") if p.is_file()}
    after_files = {p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(before_files) != set(after_files):
        raise UnadmittedReaderRoute("v148 changed stage inventory")
    changed=set()
    for rel, older in before_files.items():
        current=after_files[rel]
        if current.is_symlink() or not current.is_file():
            raise UnadmittedReaderRoute("v148 changed file into symlink")
        if older.stat().st_dev == current.stat().st_dev and older.stat().st_ino == current.stat().st_ino:
            continue
        if sha256(older)!=sha256(current):
            changed.add(rel)
    if changed != {"estate/index.html","source-lock.json"}:
        raise UnadmittedReaderRoute("v148 changed unrelated Reader, media or stage assets")
    return {**inherited,"estate/index.html":APPROVED_SPECIMEN_READER_SHA256}


def approved_nested_measure_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """One native measured nested-type exception on the accepted v148 Reader."""
    if candidate.name != APPROVED_NESTED_RELEASE:
        return {}
    before = candidate.parent / APPROVED_NESTED_PREDECESSOR
    if not candidate.is_dir() or not before.is_dir():
        raise UnadmittedReaderRoute("Unknown v149 predecessor")
    inherited = approved_typographic_specimen_files(baseline, before)
    if not inherited:
        raise UnadmittedReaderRoute("Original Reader or previous edition not admitted")
    if sha256(candidate / "source-lock.json") != APPROVED_NESTED_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unrecognized nested measure source-lock")
    try:
        current_lock = json.loads((candidate / "source-lock.json").read_text())
        previous_lock = json.loads((before / "source-lock.json").read_text())
        new_admission = current_lock.pop("modernPageNestedMeasureAdmission")
    except (KeyError, ValueError, OSError) as exc:
        raise UnadmittedReaderRoute("Missing v149 author and source admission") from exc
    if current_lock != previous_lock:
        raise UnadmittedReaderRoute("Unexpected inherited source identity mutation")
    expected_admission = {
        "schema": "fountain.press.native-nested-type-measure.v1",
        "sourceOwner": "Fountain-Coach/fountain.coach",
        "sourceCommit": APPROVED_NESTED_SOURCE_COMMIT,
        "sourcePath": "site/essays/what-makes-a-page-modern/combined-essay.md",
        "sourceSHA256": APPROVED_NESTED_SOURCE_SHA256,
        "earlierDruckfahnePDFSHA256": APPROVED_ESSAY_PDF_SHA256,
        "predecessor": APPROVED_NESTED_PREDECESSOR,
        "release": APPROVED_NESTED_RELEASE,
        "stageOnly": True,
        "publicReleased": False,
        "fountainStoreAdmitted": False,
        "readerRuntimeUnchanged": False,
        "existingReaderPreserved": True,
        "pressCompositorSourceChanged": True,
        "specimenSourcePath": "site/essays/what-makes-a-page-modern/specimen-source.txt",
        "specimenSourceSHA256": APPROVED_NESTED_SPECIMEN_SOURCE_SHA256,
        "nestedSettings": 2,
        "fixedSVGSpecimensRemovedFromView": 2,
        "historicalSVGAssetsPreserved": True,
        "originalIllustrationsUnchanged": True,
        "typographicSpecimensFramed": 2,
        "duplicateNarrativeSpecimensRemoved": 2,
        "authoredInlineFigureAnchors": 11,
        "fileSHA256": APPROVED_NESTED_FILES
    }
    if new_admission != expected_admission:
        raise UnadmittedReaderRoute("Unapproved nested type source or compositor revision")
    older = {p.relative_to(before).as_posix(): p
             for p in before.rglob("*") if p.is_file()}
    newer = {p.relative_to(candidate).as_posix(): p
             for p in candidate.rglob("*") if p.is_file()}
    if set(older) != set(newer):
        raise UnadmittedReaderRoute("v149 added or removed stage files")
    changed = set()
    for rel, previous in older.items():
        current = newer[rel]
        if not current.is_file() or current.is_symlink():
            raise UnadmittedReaderRoute("Unreviewed symlink or file: " + rel)
        if previous.stat().st_dev == current.stat().st_dev and previous.stat().st_ino == current.stat().st_ino:
            continue
        if sha256(previous) != sha256(current):
            changed.add(rel)
    if changed != set(APPROVED_NESTED_FILES) | {"source-lock.json"}:
        raise UnadmittedReaderRoute("v149 changed unrelated Reader or private media assets")
    for rel, approved_sha in APPROVED_NESTED_FILES.items():
        if sha256(newer[rel]) != approved_sha:
            raise UnadmittedReaderRoute("Wrong approved nested Reader asset: " + rel)
    return {**inherited, **APPROVED_NESTED_FILES}


def approved_fluid_nested_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """v150: only the parent folio measure and nested continuation may change.

    Preserves the original production-derived Reader, accepted v149 book and
    unchanged private audition assets; the candidate cannot self-admit.
    """
    if candidate.name != APPROVED_FLUID_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_FLUID_PREDECESSOR
    if not candidate.is_dir() or not predecessor.is_dir():
        raise UnadmittedReaderRoute("Missing exact v149 Reader ancestor")
    inherited = approved_nested_measure_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Unadmitted v149 source/Press baseline")
    if sha256(candidate / "source-lock.json") != APPROVED_FLUID_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unrecognized fluid-layout source-lock")
    try:
        after = json.loads((candidate / "source-lock.json").read_text())
        before = json.loads((predecessor / "source-lock.json").read_text())
        admission = after.pop("modernPageFluidMeasureAdmission")
    except (ValueError,KeyError,OSError) as err:
        raise UnadmittedReaderRoute("Missing pinned v150 source revision") from err
    if after != before:
        raise UnadmittedReaderRoute("v150 mutates inherited publication identity")
    expected = {
       "schema": "fountain.press.fluid-parent-and-nested-flow.v1",
       "sourceOwner": "Fountain-Coach/fountain.coach",
       "sourceCommit": APPROVED_FLUID_SOURCE_COMMIT,
       "sourcePaths": [
          "scenarios/reading-first-20261101/reading-first-press-engine.js",
          "scenarios/reading-first-20261101/reading-first-press-frame.css"
       ],
       "predecessor": APPROVED_FLUID_PREDECESSOR,
       "release": APPROVED_FLUID_RELEASE,
       "stageOnly": True,
       "publicReleased": False,
       "fountainStoreAdmitted": False,
       "sameReaderShell": True,
       "unchangedBookSources": True,
       "proportionalMeasuredFolio": True,
       "continuationUsesRemainingFolio": True,
       "testedAt": [[390,690],[390,844],[820,1120],[1024,1366],[1200,860],[1200,1500]],
       "fileSHA256": APPROVED_FLUID_FILES
    }
    if admission != expected:
        raise UnadmittedReaderRoute("Unapproved fluid folio/Press source revision")
    older = {p.relative_to(predecessor).as_posix():p
             for p in predecessor.rglob("*") if p.is_file()}
    newer = {p.relative_to(candidate).as_posix():p
             for p in candidate.rglob("*") if p.is_file()}
    if set(older) != set(newer):
        raise UnadmittedReaderRoute("v150 changed the immutable Reader inventory")
    changed = set()
    for rel, prior in older.items():
        current = newer[rel]
        if current.is_symlink() or not current.is_file():
            raise UnadmittedReaderRoute("Unreviewed link or file: "+rel)
        if prior.stat().st_dev == current.stat().st_dev and prior.stat().st_ino == current.stat().st_ino:
            continue
        if sha256(prior) != sha256(current):
            changed.add(rel)
    if changed != set(APPROVED_FLUID_FILES)|{"source-lock.json"}:
        raise UnadmittedReaderRoute("v150 changed an unrelated Reader/media file")
    for rel,digest in APPROVED_FLUID_FILES.items():
        if sha256(newer[rel]) != digest:
            raise UnadmittedReaderRoute("Wrong verified fluid Reader asset: "+rel)
    return {**inherited, **APPROVED_FLUID_FILES}


def approved_semantic_spread_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Admit only the measured facing-leaf editorial correction on v150.

    The same production-derived Press Reader, manuscript/illustration source,
    and all private audition media must remain byte-identical.
    """
    if candidate.name != APPROVED_SPREAD_RELEASE:
        return {}
    ancestor=candidate.parent / APPROVED_SPREAD_PREDECESSOR
    if not ancestor.is_dir() or not candidate.is_dir():
        raise UnadmittedReaderRoute("Missing accepted v150 Reader predecessor")
    inherited=approved_fluid_nested_files(baseline,ancestor)
    if not inherited:
        raise UnadmittedReaderRoute("Unadmitted original Reader ancestry")
    if sha256(candidate / "source-lock.json") != APPROVED_SPREAD_LOCK_SHA256:
        raise UnadmittedReaderRoute("Wrong source-locked semantic spread identity")
    try:
        current=json.loads((candidate / "source-lock.json").read_text())
        prior=json.loads((ancestor / "source-lock.json").read_text())
        new_admission=current.pop("modernPageSemanticSpreadAdmission")
    except (ValueError,KeyError,OSError) as error:
        raise UnadmittedReaderRoute("Missing semantic spread source admission") from error
    if current!=prior:
        raise UnadmittedReaderRoute("Modified inherited Reader or source lineage")
    expected={
        "schema":"fountain.press.semantic-spread-balance.v1",
        "sourceOwner":"Fountain-Coach/fountain.coach",
        "sourceCommit":APPROVED_SPREAD_SOURCE_COMMIT,
        "sourcePath":"scenarios/reading-first-20261101/reading-first-press-engine.js",
        "predecessor":APPROVED_SPREAD_PREDECESSOR,
        "release":APPROVED_SPREAD_RELEASE,
        "stageOnly":True,
        "publicReleased":False,
        "fountainStoreAdmitted":False,
        "sameReaderShell":True,
        "unchangedBookSources":True,
        "unchangedOriginalImages":True,
        "unchangedPrivateVoiceAuditions":True,
        "rightLeafRetainsProseReserve":True,
        "leftLeafMayCarryPictureAcrossGutter":True,
        "headingAttachedToReadableOpening":True,
        "minimumSecondaryImageScale":0.72,
        "compactReaderProvenIdentical":True,
        "fileSHA256":APPROVED_SPREAD_FILES
    }
    if new_admission!=expected:
        raise UnadmittedReaderRoute("Unapproved measured-spread compositor decision")
    before={p.relative_to(ancestor).as_posix():p
            for p in ancestor.rglob("*") if p.is_file()}
    after={p.relative_to(candidate).as_posix():p
           for p in candidate.rglob("*") if p.is_file()}
    if set(before)!=set(after):
        raise UnadmittedReaderRoute("Spread update changed stage file inventory")
    changed=set()
    for rel,source in before.items():
        target=after[rel]
        if target.is_symlink() or not target.is_file():
            raise UnadmittedReaderRoute("Spread update contains unexpected link or file: "+rel)
        if (source.stat().st_dev==target.stat().st_dev and
            source.stat().st_ino==target.stat().st_ino):
            continue
        if sha256(source)!=sha256(target):
            changed.add(rel)
    if changed != set(APPROVED_SPREAD_FILES)|{"source-lock.json"}:
        raise UnadmittedReaderRoute("Spread update mutated unrelated Reader/media files")
    for rel,digest in APPROVED_SPREAD_FILES.items():
        if sha256(after[rel])!=digest:
            raise UnadmittedReaderRoute("Unexpected active Press asset: "+rel)
    return {**inherited,**APPROVED_SPREAD_FILES}


def approved_editorial_archive_files(baseline: Path, candidate: Path) -> dict[str,str]:
    """Current edition excludes one writer-archived essay, never its source."""
    if candidate.name != APPROVED_ARCHIVE_RELEASE:return {}
    predecessor=candidate.parent / APPROVED_ARCHIVE_PREDECESSOR
    if not predecessor.is_dir() or not candidate.is_dir():
        raise UnadmittedReaderRoute("Missing immutable accepted v151 ancestor")
    inherited=approved_semantic_spread_files(baseline,predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Unadmitted Fountain Press source ancestry")
    if sha256(candidate / "source-lock.json") != APPROVED_ARCHIVE_LOCK_SHA256:
        raise UnadmittedReaderRoute("Incorrect v152 editorial archive source lock")
    try:
        after=json.loads((candidate / "source-lock.json").read_text())
        before=json.loads((predecessor / "source-lock.json").read_text())
        receipt=after.pop("machineReadingEditorialArchiveAdmission")
    except (ValueError,KeyError,OSError) as e:
        raise UnadmittedReaderRoute("Missing explicit writer archive admission") from e
    if after!=before:
        raise UnadmittedReaderRoute("v152 rewrites inherited Reader publication identity")
    expected={
      "schema":"fountain.press.publication-editorial-archive.v1",
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":APPROVED_ARCHIVE_SOURCE_COMMIT,
      "sourcePaths":[
         "scenarios/reading-first-20261101/index.html",
         "scenarios/reading-first-20261101/reading-first-app.js",
         "scenarios/reading-first-20261101/essay-share-manifest.json",
         "site/essays/index.html",
         "scenarios/reading-first-20261101/editorial-archive-decision.json"
      ],
      "predecessor":APPROVED_ARCHIVE_PREDECESSOR,
      "release":APPROVED_ARCHIVE_RELEASE,
      "writerDecisionDate":"2026-11-05",
      "archivedWork":"essay--to-read-is-not-to-remember",
      "archivedWorkTitle":"Did the Machine Actually Read the Book?",
      "originalSourceHTMLSHA256":APPROVED_ARCHIVED_WORK_SOURCE_SHA256,
      "originalPrivateStageRouteSHA256":APPROVED_ARCHIVED_WORK_STAGE_SHA256,
      "currentEssayCount":5,"unchangedFirstReadingsCount":30,
      "archiveRoutePreserved":True,"originalWriterProseUnchanged":True,
      "ReaderShellUnchanged":True,"PressCompositorUnchanged":True,
      "privateMediaUnchanged":True,"stageOnly":True,
      "publicReleased":False,"fountainStoreAdmitted":False,
      "changedFileSHA256":APPROVED_ARCHIVE_FILES
    }
    if receipt != expected:
        raise UnadmittedReaderRoute("Wrong writer-approved archive decision or source commit")
    original_route = "estate/essays/to-read-is-not-to-remember/index.html"
    if (sha256(candidate / original_route) != APPROVED_ARCHIVED_WORK_STAGE_SHA256
        or sha256(predecessor / original_route) != APPROVED_ARCHIVED_WORK_STAGE_SHA256):
        raise UnadmittedReaderRoute("Archive altered original source-owned essay route")
    prior={p.relative_to(predecessor).as_posix():p
           for p in predecessor.rglob("*") if p.is_file()}
    next={p.relative_to(candidate).as_posix():p
          for p in candidate.rglob("*") if p.is_file()}
    if set(prior)!=set(next):
        raise UnadmittedReaderRoute("Archive changed site inventory without admission")
    changed=set()
    for rel,before_path in prior.items():
        after_path=next[rel]
        if after_path.is_symlink() or not after_path.is_file():
            raise UnadmittedReaderRoute("Unexpected link in archived stage: "+rel)
        if (before_path.stat().st_dev==after_path.stat().st_dev and
            before_path.stat().st_ino==after_path.stat().st_ino):
            continue
        if sha256(before_path)!=sha256(after_path):
            changed.add(rel)
    if changed != (set(APPROVED_ARCHIVE_FILES)|{"source-lock.json"}):
        raise UnadmittedReaderRoute("Archive changed other Reader/media/source files: "+
            str(sorted(changed-set(APPROVED_ARCHIVE_FILES)-{"source-lock.json"})[:4]))
    for rel,digest in APPROVED_ARCHIVE_FILES.items():
        if sha256(next[rel])!=digest:
            raise UnadmittedReaderRoute("Wrong archive Reader projection: "+rel)
    return {**inherited,**APPROVED_ARCHIVE_FILES}


# One artist-authorized Csound/SVG interlude, not a Reader replacement.
APPROVED_KINO_RELEASE = "shared-shell-20261105-v153-kino-interlude-bc53623"
APPROVED_KINO_SOURCE_COMMIT = "bc53623be7b5a94cf8b94cf88ff1c5f10931f21e"
APPROVED_KINO_LOCK_SHA256 = "35b2c50ef9efeba7c0ea992142984c77eb6c4ca33ef2e3e87ca7dd9c7fa257e8"
APPROVED_KINO_READER_SHA256 = "c37248c98329fcb5e9e6c36ddd400e617de509d4ca290073314891c974cd0532"
APPROVED_KINO_ROUTE = "teatro/interludes/kino/"
APPROVED_KINO_ADDENDUM = (
    '<p class="teatro-interlude-entry"><a href="/teatro/interludes/kino/" '
    'aria-label="Open Kino After Dark, the Teatro dance interlude">'
    'Interlude · Kino After Dark — a dance between readings</a></p>'
)


def approved_kino_interlude_files(baseline: Path, candidate: Path) -> dict[str, str]:
    """Admit only seven original Teatro files and one link on the v152 Reader."""
    if candidate.name != APPROVED_KINO_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_ARCHIVE_RELEASE
    inherited = approved_editorial_archive_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Missing accepted v152 Reader ancestry")
    if sha256(candidate / "source-lock.json") != APPROVED_KINO_LOCK_SHA256:
        raise UnadmittedReaderRoute("Wrong Kino stage source lock")
    after = json.loads((candidate / "source-lock.json").read_text())
    before = json.loads((predecessor / "source-lock.json").read_text())
    receipt = after.pop("teatroKinoInterludeAdmission", None)
    if before != after or not isinstance(receipt, dict):
        raise UnadmittedReaderRoute("Kino rewrote inherited publication identity")
    expected = {
        "schema": "fountain.teatro.csound-linotype-interlude.v1",
        "sourceOwner": "Fountain-Coach/teatro.fountain.coach",
        "sourceCommit": APPROVED_KINO_SOURCE_COMMIT,
        "predecessor": APPROVED_ARCHIVE_RELEASE,
        "release": APPROVED_KINO_RELEASE,
        "sourceReaderSHA256": APPROVED_ARCHIVE_FILES["estate/index.html"],
        "stagedReaderSHA256": APPROVED_KINO_READER_SHA256,
        "route": "/" + APPROVED_KINO_ROUTE,
        "originalReadingTextUnchanged": True,
        "originalReaderRuntimeUnchanged": True,
        "oneLinkInExistingFirstReadings": True,
        "stageOnly": True,
        "publicReleased": False,
        "nativeScenarioAdmitted": False,
    }
    if set(receipt) != set(expected) | {"filesSHA256"} or any(receipt[k] != v for k,v in expected.items()):
        raise UnadmittedReaderRoute("Kino stage intent/source identity differs")
    files = receipt["filesSHA256"]
    expected_paths = {
        APPROVED_KINO_ROUTE+"index.html", APPROVED_KINO_ROUTE+"manifest.json",
        *(APPROVED_KINO_ROUTE+"assets/"+n+".m4a" for n in ("kick","hat","bass","pad","spark"))
    }
    if not isinstance(files,dict) or set(files)!=expected_paths:
        raise UnadmittedReaderRoute("Wrong Csound interlude asset inventory")
    for rel,digest in files.items():
        p=candidate/rel
        if (not isinstance(digest,str) or not re.fullmatch(r"[a-f0-9]{64}",digest)
            or not p.is_file() or p.is_symlink() or sha256(p)!=digest):
            raise UnadmittedReaderRoute("Source/mix asset mismatch: "+rel)
    source=(predecessor/"estate/index.html").read_text()
    candidate_html=(candidate/"estate/index.html").read_text()
    start='<template data-reader-volume="first-readings">'
    if source.count(start)!=1:
        raise UnadmittedReaderRoute("First Readings source anchor missing")
    i=source.index(start); j=source.index("</template>",i)
    chunk=source[i:j]
    marker="</figure></article>"
    if chunk.count(marker)!=1:
        raise UnadmittedReaderRoute("First Readings Linotype markup changed")
    expected_html=source[:i]+chunk.replace(marker,"</figure>"+APPROVED_KINO_ADDENDUM+"</article>",1)+source[j:]
    if candidate_html != expected_html or sha256(candidate/"estate/index.html")!=APPROVED_KINO_READER_SHA256:
        raise UnadmittedReaderRoute("Kino altered the existing Press Reader outside the one interlude link")
    prior={p.relative_to(predecessor).as_posix():p for p in predecessor.rglob("*") if p.is_file()}
    next_files={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(next_files)!=set(prior)|expected_paths:
        raise UnadmittedReaderRoute("Unexpected added or removed stage file")
    for rel,p in prior.items():
        if rel in ("estate/index.html","source-lock.json"):
            continue
        q=next_files[rel]
        if q.is_symlink() or sha256(p)!=sha256(q):
            raise UnadmittedReaderRoute("Kino mutated unrelated Reader/estate asset: "+rel)
    return {**inherited,"estate/index.html":APPROVED_KINO_READER_SHA256}



# The writer rejected the v153 chord/stem arrangement. The v154 change touches
# ONLY the already-admitted Teatro interlude route. Reader bytes remain exact.
APPROVED_KINO_SAMPLER_RELEASE = "shared-shell-20261105-v154-kino-midi2-sampler-bb497e8"
APPROVED_KINO_SAMPLER_SOURCE_COMMIT = "bb497e83e479f50a3dc31ceb2c007b83f599fec7"
APPROVED_KINO_SAMPLER_LOCK_SHA256 = "78d4ff302577fbb29f2841e4054288c3f7c809c711d9b1d143f5cd56f8fdb6c3"
APPROVED_KINO_SAMPLER_ASSETS = {
    "assets/midi2-ump.mjs",
    "assets/sampler-v2.mjs",
    "assets/sampler-v2.css",
    "assets/sample-provenance.json",
    "assets/shaders-40479-extract.m4a",
}
APPROVED_KINO_SAMPLE_SHA256 = "eac66e8617f16cbae1c0a59cdb5cb3ec96ffd12d065babf307924383cb58bced"


def approved_kino_sampler_v2_files(baseline: Path, candidate: Path) -> dict[str,str]:
    if candidate.name != APPROVED_KINO_SAMPLER_RELEASE:
        return {}
    predecessor = candidate.parent / APPROVED_KINO_RELEASE
    inherited = approved_kino_interlude_files(baseline, predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Missing accepted v153 original-reader lineage")
    if sha256(candidate / "source-lock.json") != APPROVED_KINO_SAMPLER_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unexpected v154 source-lock")
    old = json.loads((predecessor/"source-lock.json").read_text())
    lock = json.loads((candidate/"source-lock.json").read_text())
    receipt = lock.pop("teatroKinoSamplerV2Admission", None)
    if old != lock or not isinstance(receipt,dict):
        raise UnadmittedReaderRoute("Kino v154 rewrote unrelated publication identity")
    expected = {
        "schema": "fountain.teatro.midi2-ump-touch-sampler-stage.v1",
        "sourceOwner": "Fountain-Coach/teatro.fountain.coach",
        "sourceCommit": APPROVED_KINO_SAMPLER_SOURCE_COMMIT,
        "predecessor": APPROVED_KINO_RELEASE,
        "release": APPROVED_KINO_SAMPLER_RELEASE,
        "firstReadingsReaderSHA256": APPROVED_KINO_READER_SHA256,
        "route": "/" + APPROVED_KINO_ROUTE,
        "removedRejectedStems":[APPROVED_KINO_ROUTE+"assets/"+x+".m4a" for x in ("bass","hat","kick","pad","spark")],
        "sourceSampleSHA256": APPROVED_KINO_SAMPLE_SHA256,
        "publishedSatzfunkOriginalUnchanged": True,
        "privateDerivativeRightsOnly": True,
        "onlyExistingReaderLink": True,
        "originalReaderRuntimeUnchanged": True,
        "midi2SoftwareUMPNativeHardwareClaim": False,
        "stageOnly": True,
        "publicReleased": False,
        "nativeTeatroScenarioAdmitted": False
    }
    if set(receipt) != set(expected) | {"filesSHA256"} or any(receipt[k]!=v for k,v in expected.items()):
        raise UnadmittedReaderRoute("Incorrect source-bound Kino v154 admission receipt")
    files=receipt["filesSHA256"]
    expected_paths={APPROVED_KINO_ROUTE+"index.html",APPROVED_KINO_ROUTE+"manifest.json",
                    *(APPROVED_KINO_ROUTE+x for x in APPROVED_KINO_SAMPLER_ASSETS)}
    if not isinstance(files,dict) or set(files)!=expected_paths or files.get(APPROVED_KINO_ROUTE+"assets/shaders-40479-extract.m4a")!=APPROVED_KINO_SAMPLE_SHA256:
        raise UnadmittedReaderRoute("Unexpected sampler source/media inventory")
    for path,digest in files.items():
        p=candidate/path
        if not p.is_file() or p.is_symlink() or not re.fullmatch(r"[a-f0-9]{64}",digest) or sha256(p)!=digest:
            raise UnadmittedReaderRoute("Corrupt or unadmitted Kino sample: "+path)
    metadata=json.loads((candidate/APPROVED_KINO_ROUTE/"assets/sample-provenance.json").read_text())
    if (metadata.get("stageOnly") is not True or metadata.get("publicDerivativeAuthorized") is not False or
        metadata.get("sampling",{}).get("sampleSHA256") != APPROVED_KINO_SAMPLE_SHA256):
        raise UnadmittedReaderRoute("Public derivative rights expanded without authority")
    old_files={p.relative_to(predecessor).as_posix():p for p in predecessor.rglob("*") if p.is_file()}
    new_files={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    removed={APPROVED_KINO_ROUTE+"assets/"+x+".m4a" for x in ("bass","hat","kick","pad","spark")}
    added={APPROVED_KINO_ROUTE+x for x in APPROVED_KINO_SAMPLER_ASSETS}
    if set(old_files)-set(new_files)!=removed or set(new_files)-set(old_files)!=added:
        raise UnadmittedReaderRoute("Unexpected stage file addition/removal")
    changed={rel for rel in old_files.keys()&new_files.keys() if sha256(old_files[rel])!=sha256(new_files[rel])}
    if changed!={"source-lock.json",APPROVED_KINO_ROUTE+"index.html",APPROVED_KINO_ROUTE+"manifest.json"}:
        raise UnadmittedReaderRoute("v154 changed other Reader or estate files: "+str(sorted(changed)[:5]))
    if sha256(candidate/"estate/index.html")!=APPROVED_KINO_READER_SHA256:
        raise UnadmittedReaderRoute("Existing First Readings Linotype changed")
    return inherited



# Private source-owned v155: actual Ear PCM -> MIDI2 CC74 loopback -> limited band echo.
APPROVED_KINO_EAR_RELEASE = "shared-shell-20261105-v155-kino-ear-band-echo-ea8fbaf"
APPROVED_KINO_EAR_SOURCE_COMMIT = "ea8fbaf53057691480510af6d87ca30645dae9d9"
APPROVED_KINO_EAR_LOCK_SHA256 = "d661bfc5288ff026036b6c259b5efcd65bcd86b2848fa3f641e3bc0bc6df82d3"
APPROVED_KINO_EAR_WORKLET_SHA256 = "4f1d800fd5518975c0bc98a5fb0ace93eaa726d8731bf330a8eff59a9d115427"
APPROVED_KINO_EAR_CHANGED = {APPROVED_KINO_ROUTE+x for x in (
    "index.html","manifest.json","assets/sampler-v2.mjs","assets/sampler-v2.css"
)}
APPROVED_KINO_EAR_ADDED = {APPROVED_KINO_ROUTE+x for x in (
    "assets/ear-original.js","assets/ear-band-echo.mjs"
)}
APPROVED_KINO_EAR_PRESERVED = {APPROVED_KINO_ROUTE+x for x in (
    "assets/midi2-ump.mjs","assets/sample-provenance.json",
    "assets/shaders-40479-extract.m4a"
)}


def approved_kino_ear_echo_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_EAR_RELEASE:
        return {}
    predecessor=candidate.parent/APPROVED_KINO_SAMPLER_RELEASE
    inherited=approved_kino_sampler_v2_files(baseline,predecessor)
    if not inherited:
        raise UnadmittedReaderRoute("Missing accepted v154 source/Reader ancestry")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_EAR_LOCK_SHA256:
        raise UnadmittedReaderRoute("Incorrect v155 source-lock")
    original=json.loads((predecessor/"source-lock.json").read_text())
    after=json.loads((candidate/"source-lock.json").read_text())
    receipt=after.pop("teatroKinoEarBandEchoAdmission",None)
    if after!=original or not isinstance(receipt,dict):
        raise UnadmittedReaderRoute("v155 altered inherited edition/source identity")
    expected={
      "schema":"fountain.teatro.ear-midi2-software-loopback-band-echo-stage.v1",
      "sourceOwner":"Fountain-Coach/teatro.fountain.coach",
      "sourceCommit":APPROVED_KINO_EAR_SOURCE_COMMIT,
      "predecessor":APPROVED_KINO_SAMPLER_RELEASE,
      "release":APPROVED_KINO_EAR_RELEASE,
      "route":"/"+APPROVED_KINO_ROUTE,
      "readerHTMLSHA256":APPROVED_KINO_READER_SHA256,
      "originalEarWorkletSHA256":APPROVED_KINO_EAR_WORKLET_SHA256,
      "earPCMMeasured":True,
      "midi2UMPControl":{"group":0,"channel":0,"controller":74,"valueBits":32,"minimumIntervalMilliseconds":75},
      "echoImplementation":"band-limited Web Audio tape echo emulation",
      "echoMaximumFeedback":0.44,
      "echoMaximumWet":0.43,
      "selfListeningFeedbackProhibited":True,
      "hardStopClosesLoop":True,
      "nativeCsoundAdmission":False,
      "publicProductionAffected":False,
      "publicDerivativeAuthorized":False,
      "ownerWLANOnly":True,
      "existingLinotypeReaderUnchanged":True,
      "newMIDIHardwarePeer":False
    }
    checks={"addedFileSHA256":APPROVED_KINO_EAR_ADDED,
            "changedFileSHA256":APPROVED_KINO_EAR_CHANGED,
            "preservedFileSHA256":APPROVED_KINO_EAR_PRESERVED}
    if set(receipt)!=set(expected)|set(checks) or any(receipt[k]!=v for k,v in expected.items()):
        raise UnadmittedReaderRoute("Wrong v155 Ear loopback identity/authorization")
    for kind,paths in checks.items():
        hashes=receipt[kind]
        if not isinstance(hashes,dict) or set(hashes)!=paths:
            raise UnadmittedReaderRoute("Unexpected v155 "+kind+" file set")
        for rel,digest in hashes.items():
            path=candidate/rel
            if (not path.is_file() or path.is_symlink() or
                not re.fullmatch(r"[a-f0-9]{64}",digest) or sha256(path)!=digest):
                raise UnadmittedReaderRoute("Unadmitted Ear/echo bytes: "+rel)
    if (receipt["addedFileSHA256"][APPROVED_KINO_ROUTE+"assets/ear-original.js"]!=APPROVED_KINO_EAR_WORKLET_SHA256
        or receipt["preservedFileSHA256"][APPROVED_KINO_ROUTE+"assets/shaders-40479-extract.m4a"]!=APPROVED_KINO_SAMPLE_SHA256):
        raise UnadmittedReaderRoute("Changed original Ear or Satzfunk sample provenance")
    prior={p.relative_to(predecessor).as_posix():p for p in predecessor.rglob("*") if p.is_file()}
    next={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(next)-set(prior)!=APPROVED_KINO_EAR_ADDED or set(prior)-set(next):
        raise UnadmittedReaderRoute("Unexpected change to stage inventory")
    for rel,path in prior.items():
        if rel in APPROVED_KINO_EAR_CHANGED|{"source-lock.json"}:
            continue
        revised=next[rel]
        if revised.is_symlink() or sha256(path)!=sha256(revised):
            raise UnadmittedReaderRoute("v155 mutated unrelated Reader/media asset: "+rel)
    if sha256(candidate/"estate/index.html")!=APPROVED_KINO_READER_SHA256:
        raise UnadmittedReaderRoute("Existing First Readings reader altered")
    return inherited




# Source-locked private v156 Csound hits + swing; NO Reader or public media change.
APPROVED_KINO_GROOVE_RELEASE="shared-shell-20261105-v157-kino-swing-aac-3b91ebb"
APPROVED_KINO_GROOVE_COMMIT="3b91ebb2409ca1e55d1c15b545bef422a5a560bf"
APPROVED_KINO_GROOVE_LOCK_SHA256="98d296bd70afc5617fd3cf9f3dbd7e5b0a766c0cc42aee62d4aa53990792b557"
APPROVED_KINO_GROOVE_ADDED={APPROVED_KINO_ROUTE+x for x in (
 "assets/groove-v156.mjs","assets/groove/bass-d2.m4a","assets/groove/hat-closed.m4a",
 "assets/groove/hat-open.m4a","assets/groove/sources.json")}
APPROVED_KINO_GROOVE_CHANGED={APPROVED_KINO_ROUTE+x for x in (
 "index.html","manifest.json","assets/ear-band-echo.mjs",
 "assets/sampler-v2.css","assets/sampler-v2.mjs")}
APPROVED_KINO_GROOVE_PRESERVED={APPROVED_KINO_ROUTE+x for x in (
 "assets/ear-original.js","assets/midi2-ump.mjs",
 "assets/sample-provenance.json","assets/shaders-40479-extract.m4a")}


def approved_kino_groove_v157_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_GROOVE_RELEASE:
        return {}
    old=candidate.parent/APPROVED_KINO_EAR_RELEASE
    inherited=approved_kino_ear_echo_files(baseline,old)
    if not inherited:
        raise UnadmittedReaderRoute("Missing accepted v155 Reader + Ear lineage")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_GROOVE_LOCK_SHA256:
        raise UnadmittedReaderRoute("Kino bass/hat SHA256 source-lock changed")
    previous=json.loads((old/"source-lock.json").read_text())
    now=json.loads((candidate/"source-lock.json").read_text())
    receipt=now.pop("teatroKinoGrooveV157Admission",None)
    if previous!=now or not isinstance(receipt,dict):
        raise UnadmittedReaderRoute("Unadmitted inherited source-lock mutation")
    if (receipt.get("sourceOwner")!="Fountain-Coach/teatro.fountain.coach" or
        receipt.get("sourceCommit")!=APPROVED_KINO_GROOVE_COMMIT or
        receipt.get("predecessor")!=APPROVED_KINO_EAR_RELEASE or
        receipt.get("release")!=APPROVED_KINO_GROOVE_RELEASE or
        receipt.get("readerHTMLSHA256")!=APPROVED_KINO_READER_SHA256 or
        receipt.get("noChords") is not True or receipt.get("noPads") is not True or
        receipt.get("originalCsoundRendered") is not True or
        receipt.get("originalSatzfunkDerivativeRemainsPrivate") is not True or
        receipt.get("publicReleased") is not False or
        receipt.get("ownerWLANOnly") is not True or
        receipt.get("nativeMIDI2HardwareClaim") is not False):
        raise UnadmittedReaderRoute("Wrong authored bass/hat/rights receipt")
    verify_sets={"addedFileSHA256":APPROVED_KINO_GROOVE_ADDED,
                 "changedFileSHA256":APPROVED_KINO_GROOVE_CHANGED,
                 "preservedFileSHA256":APPROVED_KINO_GROOVE_PRESERVED}
    for typ,paths in verify_sets.items():
        listing=receipt.get(typ)
        if not isinstance(listing,dict) or set(listing)!=paths:
            raise UnadmittedReaderRoute("Source delta file mismatch: "+typ)
        for rel,digest in listing.items():
            path=candidate/rel
            if (not isinstance(digest,str) or not re.fullmatch("[a-f0-9]{64}",digest) or
                not path.is_file() or path.is_symlink() or sha256(path)!=digest):
                raise UnadmittedReaderRoute("Modified source payload: "+rel)
    before={p.relative_to(old).as_posix():p for p in old.rglob("*") if p.is_file()}
    after={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(after)-set(before)!=APPROVED_KINO_GROOVE_ADDED or set(before)-set(after):
        raise UnadmittedReaderRoute("Unexpected route addition/deletion")
    for rel,path in before.items():
        if rel=="source-lock.json" or rel in APPROVED_KINO_GROOVE_CHANGED:
            continue
        new=after[rel]
        if new.is_symlink() or sha256(new)!=sha256(path):
            raise UnadmittedReaderRoute("Unrelated Reader/source altered: "+rel)
    source=json.loads((candidate/APPROVED_KINO_ROUTE/"assets/groove/sources.json").read_text())
    sounds=source.get("sounds")
    if not isinstance(sounds,list) or {s.get("name") for s in sounds}!={"bass-d2","hat-closed","hat-open"}:
        raise UnadmittedReaderRoute("Unsupported Csound groove sound inventory")
    for item in sounds:
        wav=candidate/APPROVED_KINO_ROUTE/item["file"]
        if sha256(wav)!=item["sha256"]:
            raise UnadmittedReaderRoute("Changed Csound-rendered hit: "+item["name"])
    if sha256(candidate/"estate/index.html")!=APPROVED_KINO_READER_SHA256:
        raise UnadmittedReaderRoute("Existing First Readings Reader changed")
    return inherited



# V158: former swing deck retires into a Csound acoustic memory room.
APPROVED_KINO_ATMOSPHERE_RELEASE="shared-shell-20261105-v158-kino-memory-room-edd6929"
APPROVED_KINO_ATMOSPHERE_SOURCE_COMMIT="edd6929866210adaeb98d4beae3dddeee942e9de"
APPROVED_KINO_ATMOSPHERE_LOCK_SHA256="c3ee668946d1145d18a74c5fb55b82c05e7451826f1d89dcd39612f7f14bb493"
APPROVED_KINO_ATMOSPHERE_ADDED={APPROVED_KINO_ROUTE+x for x in (
 "assets/ambience-v158.mjs","assets/ambient-v158.css",
 "assets/atmosphere/cinema-air.m4a","assets/atmosphere/film-dust.m4a",
 "assets/atmosphere/sources.json"
)}
APPROVED_KINO_ATMOSPHERE_CHANGED={
 APPROVED_KINO_ROUTE+"index.html",APPROVED_KINO_ROUTE+"manifest.json"
}


def approved_kino_atmosphere_v158_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_ATMOSPHERE_RELEASE:
        return {}
    previous=candidate.parent/APPROVED_KINO_GROOVE_RELEASE
    inherited=approved_kino_groove_v157_files(baseline,previous)
    if not inherited:
        raise UnadmittedReaderRoute("Absent accepted v157 Reader ancestry")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_ATMOSPHERE_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unexpected cinematic memory room source-lock")
    before=json.loads((previous/"source-lock.json").read_text())
    current=json.loads((candidate/"source-lock.json").read_text())
    receipt=current.pop("teatroKinoAtmosphereV158Admission",None)
    if current!=before or not isinstance(receipt,dict):
        raise UnadmittedReaderRoute("Memory room overwrote inherited Press identity")
    expected={
      "schema":"fountain.teatro.cinematic-acoustic-environment-stage.v1",
      "sourceOwner":"Fountain-Coach/teatro.fountain.coach",
      "sourceCommit":APPROVED_KINO_ATMOSPHERE_SOURCE_COMMIT,
      "predecessor":APPROVED_KINO_GROOVE_RELEASE,
      "release":APPROVED_KINO_ATMOSPHERE_RELEASE,
      "route":"/"+APPROVED_KINO_ROUTE,
      "readerHTMLSHA256":APPROVED_KINO_READER_SHA256,
      "originalCsoundAtmospheres":True,"nonPeriodicGrains":True,
      "bassAndHiHatNotScheduled":True,"sampleSliceUIRemoved":True,
      "archivalSourceOptInOnly":True,"archivalDefaultLevel":0,
      "earMidi2UMPControlChange74":True,"stopClosesEcho":True,
      "nativeCsoundScenarioAdmitted":False,"hardwareMidi2Transport":False,
      "publicDerivativeAuthorized":False,"ownerWLANOnly":True,
      "originalLinotypeReaderUnchanged":True
    }
    if set(receipt)!=set(expected)|{
        "addedFileSHA256","changedFileSHA256","preservedFileSHA256"
    } or any(receipt[k]!=value for k,value in expected.items()):
        raise UnadmittedReaderRoute("Altered Kino acoustic edition approval/rights")
    before_files={p.relative_to(previous).as_posix():p for p in previous.rglob("*") if p.is_file()}
    current_files={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(current_files)-set(before_files)!=APPROVED_KINO_ATMOSPHERE_ADDED or set(before_files)-set(current_files):
        raise UnadmittedReaderRoute("Unexpected added or removed estate file")
    preserved={p for p in before_files if p.startswith(APPROVED_KINO_ROUTE) and p not in APPROVED_KINO_ATMOSPHERE_CHANGED}
    categories={
      "addedFileSHA256":APPROVED_KINO_ATMOSPHERE_ADDED,
      "changedFileSHA256":APPROVED_KINO_ATMOSPHERE_CHANGED,
      "preservedFileSHA256":preserved
    }
    for field,expected_paths in categories.items():
        mapping=receipt[field]
        if not isinstance(mapping,dict) or set(mapping)!=expected_paths:
            raise UnadmittedReaderRoute("Unreviewed ambient media/source: "+field)
        for rel,digest in mapping.items():
            target=candidate/rel
            if not isinstance(digest,str) or not re.fullmatch("[a-f0-9]{64}",digest) or (
                not target.is_file() or target.is_symlink() or sha256(target)!=digest):
                raise UnadmittedReaderRoute("Source mismatch in atmospheric route: "+rel)
    for rel,p in before_files.items():
        if rel=="source-lock.json" or rel in APPROVED_KINO_ATMOSPHERE_CHANGED:
            continue
        current_file=current_files[rel]
        if current_file.is_symlink() or sha256(p)!=sha256(current_file):
            raise UnadmittedReaderRoute("Memory room altered unrelated Reader/estate: "+rel)
    sound=json.loads((candidate/APPROVED_KINO_ROUTE/"assets/atmosphere/sources.json").read_text())
    entries=sound.get("files",[])
    if {entry.get("name") for entry in entries}!={"cinema-air","film-dust"} or not sound.get("noBeat") or not sound.get("noChords"):
        raise UnadmittedReaderRoute("Unreviewed cinema audio evidence")
    for entry in entries:
        if sha256(candidate/APPROVED_KINO_ROUTE/entry["path"])!=entry["sha256"]:
            raise UnadmittedReaderRoute("Audio content differs from owner Csound render")
    text=(candidate/APPROVED_KINO_ROUTE/"index.html").read_text()
    if ("assets/ambience-v158.mjs" not in text or "sampler-v2.mjs" in text or
        '<section class="sampler"' in text or 'class="groove-strip"' in text or
        'id="traces" type="range" min="0" max="45" value="0"' not in text):
        raise UnadmittedReaderRoute("Intrusive former sampler/pattern still active")
    if sha256(candidate/"estate/index.html")!=APPROVED_KINO_READER_SHA256:
        raise UnadmittedReaderRoute("Original First Readings reader changed")
    return inherited



# V159 adds one source-authored soul-jazz memory; it cannot authorize copyrighted recordings.
APPROVED_KINO_MIDNIGHT_RELEASE="shared-shell-20261105-v159-kino-midnight-cylinder-e2f5dd2"
APPROVED_KINO_MIDNIGHT_COMMIT="e2f5dd2c89866d3ebc1265a2c56dc78338995cac"
APPROVED_KINO_MIDNIGHT_LOCK_SHA256="44f7285bb1d2d413d437e815f5decab6149eaf39e283ab7ec1e5984019abd99b"
APPROVED_KINO_MIDNIGHT_ADDED={APPROVED_KINO_ROUTE+x for x in (
    "assets/midnight/midnight-cylinder.m4a",
    "assets/midnight/sources.json",
)}
APPROVED_KINO_MIDNIGHT_CHANGED={APPROVED_KINO_ROUTE+x for x in (
    "assets/ambience-v158.mjs","index.html","manifest.json",
)}
APPROVED_KINO_MIDNIGHT_AUDIO_SHA256="682d574cea17f0f89f47a76b4f215ddc2413e085826d0a31effef3a4b59fb7a4"


def approved_kino_midnight_v159_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_MIDNIGHT_RELEASE:
        return {}
    prior=candidate.parent/APPROVED_KINO_ATMOSPHERE_RELEASE
    inherited=approved_kino_atmosphere_v158_files(baseline,prior)
    if not inherited:
        raise UnadmittedReaderRoute("Missing accepted v158 Reader and sound-room lineage")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_MIDNIGHT_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unexpected Midnight Cylinder source lock")
    previous=json.loads((prior/"source-lock.json").read_text())
    receipt_map=json.loads((candidate/"source-lock.json").read_text())
    receipt=receipt_map.pop("teatroKinoMidnightV159Admission",None)
    if receipt_map!=previous or not isinstance(receipt,dict):
        raise UnadmittedReaderRoute("Midnight Cylinder altered inherited source identity")
    expected={
        "schema":"fountain.teatro.original-jazz-memory-loop-stage.v1",
        "sourceOwner":"Fountain-Coach/teatro.fountain.coach",
        "sourceCommit":APPROVED_KINO_MIDNIGHT_COMMIT,
        "predecessor":APPROVED_KINO_ATMOSPHERE_RELEASE,
        "release":APPROVED_KINO_MIDNIGHT_RELEASE,
        "route":"/"+APPROVED_KINO_ROUTE,
        "readerHTMLSHA256":APPROVED_KINO_READER_SHA256,
        "originalCsoundAudio":True,
        "sourceRecordingSampled":False,
        "recordedMelodyTranscribed":False,
        "softLoopPlaybackRate":0.83,
        "defaultCylinderLevelPercent":18,
        "stopClosesJazzSourceAndEcho":True,
        "earMidi2CC74Unchanged":True,
        "publicDerivativeAuthorized":False,
        "originalLinotypeReaderUnchanged":True,
        "ownerWLANOnly":True,
        "nativeScenarioAdmitted":False,
        "hardwareMIDITransportClaim":False,
    }
    sets={
        "addedFileSHA256":APPROVED_KINO_MIDNIGHT_ADDED,
        "changedFileSHA256":APPROVED_KINO_MIDNIGHT_CHANGED,
    }
    if set(receipt)!=set(expected)|set(sets)|{"preservedFileSHA256"} or any(receipt[k]!=val for k,val in expected.items()):
        raise UnadmittedReaderRoute("Unreviewed Midnight Cylinder claim or authorization")
    prior_files={p.relative_to(prior).as_posix():p for p in prior.rglob("*") if p.is_file()}
    next_files={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(next_files)-set(prior_files)!=APPROVED_KINO_MIDNIGHT_ADDED or set(prior_files)-set(next_files):
        raise UnadmittedReaderRoute("Unexpected added or removed stage file")
    unchanged={path for path in prior_files if path.startswith(APPROVED_KINO_ROUTE) and path not in APPROVED_KINO_MIDNIGHT_CHANGED}
    if not isinstance(receipt["preservedFileSHA256"],dict) or set(receipt["preservedFileSHA256"])!=unchanged:
        raise UnadmittedReaderRoute("Unexpected altered prior Kino asset inventory")
    for field,paths in (("addedFileSHA256",APPROVED_KINO_MIDNIGHT_ADDED),
                        ("changedFileSHA256",APPROVED_KINO_MIDNIGHT_CHANGED),
                        ("preservedFileSHA256",unchanged)):
        digests=receipt[field]
        if not isinstance(digests,dict) or set(digests)!=paths:
            raise UnadmittedReaderRoute("Unknown Midnight Cylinder inventory "+field)
        for rel,digest in digests.items():
            file=candidate/rel
            if (not isinstance(digest,str) or not re.fullmatch("[a-f0-9]{64}",digest)
                or not file.is_file() or file.is_symlink() or sha256(file)!=digest):
                raise UnadmittedReaderRoute("Unadmitted Midnight sound/file "+rel)
    for rel,original in prior_files.items():
        if rel=="source-lock.json" or rel in APPROVED_KINO_MIDNIGHT_CHANGED:
            continue
        p=next_files[rel]
        if p.is_symlink() or sha256(original)!=sha256(p):
            raise UnadmittedReaderRoute("Midnight loop changed other Reader/media "+rel)
    src=json.loads((candidate/APPROVED_KINO_ROUTE/"assets/midnight/sources.json").read_text())
    if (src.get("sourceRecordingUsed") is not False or
        src.get("noTranscribedMelody") is not True or
        src.get("noChords") is not True or
        src.get("sha256")!=APPROVED_KINO_MIDNIGHT_AUDIO_SHA256):
        raise UnadmittedReaderRoute("Midnight source provenance or rights mismatch")
    manifest=json.loads((candidate/APPROVED_KINO_ROUTE/"manifest.json").read_text())
    if (manifest.get("originalJazzMemory",{}).get("sourceAudioSampled") is not False
        or manifest["originalJazzMemory"].get("defaultLevelPercent")!=18):
        raise UnadmittedReaderRoute("Midnight loop isn't the admitted original")
    html=(candidate/APPROVED_KINO_ROUTE/"index.html").read_text()
    if ('id="cylinder"' not in html or '<section class="sampler"' in html or
        'class="groove-strip"' in html or 'value="18" aria-label="Original jazz memory loop level"' not in html):
        raise UnadmittedReaderRoute("Intrusive sampler or unreviewed Cylinder control")
    runtime=(candidate/APPROVED_KINO_ROUTE/"assets/ambience-v158.mjs").read_text()
    if "source.loop=true" not in runtime or "stopCylinder();" not in runtime:
        raise UnadmittedReaderRoute("Original loop or bounded Stop missing")
    if sha256(candidate/"estate/index.html")!=APPROVED_KINO_READER_SHA256:
        raise UnadmittedReaderRoute("Existing First Readings reader changed")
    return inherited



APPROVED_PRESS_SOUND_V160_RELEASE="shared-shell-20261106-v160-press-sound-essay-proof-9d83302"
APPROVED_PRESS_SOUND_V160_LOCK_SHA256="c0b914586f4cfbd3312fe71b8579f2682de20479646252fdc65606d371553324"
APPROVED_PRESS_SOUND_V160_INDEX_SHA256="7cd67ccb9a8899230b887226a5bc628d23b88613c08385631a9112827518265e"
APPROVED_PRESS_SOUND_V160_APP_SHA256="83c83d45c1b11db03d0227b18f3daa6f6a481e757faeccc60b1fb1dd06d32cc9"
APPROVED_PRESS_SOUND_V160_RECEIPT_SHA256="e8f26a9672ec5cbedfe2799d43bd619e3abb9faca91d4fd8aa8b633073892d38"
APPROVED_PRESS_SOUND_V160_SOURCE_SHA256="53b5f7369f68548f211571bdaf5fa4d92bbc85b3fed30aedf8839eaf8e293b7c"
PRESS_SOUND_V160_MODIFIED={
    "estate/index.html":APPROVED_PRESS_SOUND_V160_INDEX_SHA256,
    "estate/assets/linotype/reading-first-app.js":APPROVED_PRESS_SOUND_V160_APP_SHA256,
}
PRESS_SOUND_V160_ADDED={
    "estate/evidence/press-sound-essay-proof-v160.json":APPROVED_PRESS_SOUND_V160_RECEIPT_SHA256,
}

def approved_press_sound_v160_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Exact private proof on the *existing* v159, production-derived Press Reader.

    This exception is nonpublic and cannot create a Bookshelf admission.
    It checks predecessor lineage and every byte, not a candidate self-claim.
    """
    if candidate.name!=APPROVED_PRESS_SOUND_V160_RELEASE:
        return {}
    prior=candidate.parent/APPROVED_KINO_MIDNIGHT_RELEASE
    inherited=approved_kino_midnight_v159_files(baseline,prior)
    if not inherited:
        raise UnadmittedReaderRoute("Missing accepted v159 predecessor and Reader lineage")
    if sha256(candidate/"source-lock.json")!=APPROVED_PRESS_SOUND_V160_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unrecognized private essay proof source lock")
    before=json.loads((prior/"source-lock.json").read_text())
    after=json.loads((candidate/"source-lock.json").read_text())
    admission=after.pop("pressSoundEssayV160Admission",None)
    expected={
        "schema":"fountain.press.sound-essay-editorial-proof-stage.v1",
        "sourceOwner":"Fountain-Coach/fountain.coach",
        "sourceCommit":"9d833024e202fa37653af3b46f9862d5fc2e82d8",
        "pressOwner":"Fountain-Coach/fountain-press",
        "pressCommit":"71bc32b7ed78798b886c865bb1168cd4f9027a92",
        "predecessor":APPROVED_KINO_MIDNIGHT_RELEASE,
        "release":APPROVED_PRESS_SOUND_V160_RELEASE,
        "sourceSHA256":APPROVED_PRESS_SOUND_V160_SOURCE_SHA256,
        "sourceStatus":"unadmitted-editorial-proof",
        "publicReleaseAuthorized":False,
        "governanceChapterAdmitted":False,
        "sourceCompositorReused":True,
        "existingEssaysMembershipUnchanged":True,
        "existingPrivateKinoUnchanged":True,
        "existingVoiceAssetsUnchanged":True,
        "changedFileSHA256":PRESS_SOUND_V160_MODIFIED,
        "addedFileSHA256":PRESS_SOUND_V160_ADDED,
    }
    if after!=before or admission!=expected:
        raise UnadmittedReaderRoute("Missing exact source-owned editorial proof admission")
    previous={p.relative_to(prior).as_posix():p for p in prior.rglob("*") if p.is_file()}
    proposed={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(proposed)-set(previous)!=set(PRESS_SOUND_V160_ADDED) or set(previous)-set(proposed):
        raise UnadmittedReaderRoute("Unexpected new/deleted file in editorial proof")
    for rel,path in proposed.items():
        if path.is_symlink():
            raise UnadmittedReaderRoute("Unexpected stage symlink in editorial proof "+rel)
        if rel=="source-lock.json":
            continue
        expected_sha=PRESS_SOUND_V160_MODIFIED.get(rel,PRESS_SOUND_V160_ADDED.get(rel))
        if expected_sha:
            if sha256(path)!=expected_sha:
                raise UnadmittedReaderRoute("Editorial proof file digest mismatch "+rel)
        elif sha256(path)!=sha256(previous[rel]):
            raise UnadmittedReaderRoute("Unapproved prior Reader/Kino mutation "+rel)
    receipt=json.loads((candidate/"estate/evidence/press-sound-essay-proof-v160.json").read_text())
    if (receipt.get("sourceSHA256")!=APPROVED_PRESS_SOUND_V160_SOURCE_SHA256
       or receipt.get("siteSourceCommit")!=expected["sourceCommit"]
       or receipt.get("pressAdapterCommit")!=expected["pressCommit"]
       or receipt.get("sourceStatus")!="verbatim-draft"
       or receipt.get("stagingOnly") is not True
       or receipt.get("publicRelease") is not False
       or receipt.get("governanceChapterAdmitted") is not False
       or receipt.get("otherAssetsPreservedFrom")!="v159"):
        raise UnadmittedReaderRoute("False editorial proof status or source provenance")
    book=(candidate/"estate/index.html").read_text()
    if ('data-reader-volume="essay--a-sound-must-earn-its-place"' not in book
       or 'data-editorial-state="proof"' not in book
       or 'Editorial proof · Unpublished draft' not in book
       or 'not an adopted Governance chapter' not in book):
        raise UnadmittedReaderRoute("Essay proof not inside accepted Reader with honest status")
    if sha256(candidate/"estate/assets/linotype/reading-first-press-engine.js")!=sha256(prior/"estate/assets/linotype/reading-first-press-engine.js"):
        raise UnadmittedReaderRoute("Second Reader or altered Press compositor")
    return {**inherited,**PRESS_SOUND_V160_MODIFIED,**PRESS_SOUND_V160_ADDED}


APPROVED_GOVERNANCE_V161_RELEASE="shared-shell-20261106-v161-governance-complete-9dfb0fc"
APPROVED_GOVERNANCE_V161_LOCK_SHA256="c852c8ea2d3e89a8c1edfa48aa7a69c8a3c1ac638dc81e2d3b0dd8a167fe983d"
APPROVED_GOVERNANCE_V161_INDEX_SHA256="c2b45a1743aac8f504a8011b62b3de76b19762af94f9ad998a3c1fa71063ebfd"
APPROVED_GOVERNANCE_V161_APP_SHA256="9fc914956045523522a1a4557721bb22a20fe995cb82f2f8c85c053f1f929f09"
APPROVED_GOVERNANCE_V161_RECEIPT_SHA256="cc88dab7dc8a9973b306401a47746508af4d4f23b841da003dafafd36fc09fbe"
GOVERNANCE_V161_CHANGED={
    "estate/index.html":APPROVED_GOVERNANCE_V161_INDEX_SHA256,
    "estate/assets/linotype/reading-first-app.js":APPROVED_GOVERNANCE_V161_APP_SHA256,
}
GOVERNANCE_V161_ADDED={
    "estate/evidence/press-governance-v161.json":APPROVED_GOVERNANCE_V161_RECEIPT_SHA256,
}


def approved_governance_v161_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Full canonical 160-chapter Governance proof with exact inherited Reader.

    This private WAN-independent staging exception does not edit the public
    Governance source, issue a Store admission or authorize production release.
    """
    if candidate.name!=APPROVED_GOVERNANCE_V161_RELEASE:
        return {}
    prior=candidate.parent/APPROVED_PRESS_SOUND_V160_RELEASE
    inherited=approved_press_sound_v160_files(baseline,prior)
    if not inherited:
        raise UnadmittedReaderRoute("Full Governance stage lacks accepted v160 Reader lineage")
    if sha256(candidate/"source-lock.json")!=APPROVED_GOVERNANCE_V161_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unexpected full Governance stage source-lock digest")
    before=json.loads((prior/"source-lock.json").read_text())
    after=json.loads((candidate/"source-lock.json").read_text())
    admission=after.pop("pressGovernanceV161Admission",None)
    expected={
        "schema":"fountain.press.governance-complete-wlan-admission.v1",
        "predecessor":APPROVED_PRESS_SOUND_V160_RELEASE,
        "release":APPROVED_GOVERNANCE_V161_RELEASE,
        "sourceOwner":"Fountain-Coach/governance.fountain.coach",
        "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
        "readerOwner":"Fountain-Coach/fountain.coach",
        "readerCommit":"80f09f059db61611925cf273ca0c3cd54cabe4eb",
        "pressOwner":"Fountain-Coach/fountain-press",
        "pressCommit":"9dfb0fcb1234879a84671ee514b631d4f286fe12",
        "sourceStatusSHA256":"48d563a4f0e7a03fb9ee27c63e00c0745b4b50364a73e91ba0c86cd4433482b3",
        "sourceChapterCount":160,
        "sourceCurrentCount":72,
        "sourceReferenceCount":88,
        "sourceOriginalFigures":70,
        "existingLinotypeCompositorUnchanged":True,
        "existingReaderAndPrivateMediaPreserved":True,
        "governanceSourceUnchanged":True,
        "privateWLANOnly":True,
        "publicReleaseAuthorized":False,
        "changedFileSHA256":GOVERNANCE_V161_CHANGED,
        "addedFileSHA256":GOVERNANCE_V161_ADDED,
    }
    if after!=before or admission!=expected:
        raise UnadmittedReaderRoute("Missing exact source-owned Governance edition admission")
    old={p.relative_to(prior).as_posix():p for p in prior.rglob("*") if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if (set(new)-set(old)!=set(GOVERNANCE_V161_ADDED) or set(old)-set(new)):
        raise UnadmittedReaderRoute("Unexpected added/removed file in complete Governance stage")
    for name,path in new.items():
        if path.is_symlink():
            raise UnadmittedReaderRoute("Symlink in source-locked Governance artifact "+name)
        if name=="source-lock.json":
            continue
        expected_hash=GOVERNANCE_V161_CHANGED.get(name,GOVERNANCE_V161_ADDED.get(name))
        if expected_hash:
            if sha256(path)!=expected_hash:
                raise UnadmittedReaderRoute("Unrecognized Governance reader/receipt bytes: "+name)
        elif sha256(path)!=sha256(old[name]):
            raise UnadmittedReaderRoute("Existing Reader, private media or canonical Governance route changed: "+name)
    record=json.loads((candidate/"estate/evidence/press-governance-v161.json").read_text())
    if (record.get("schema")!="fountain.press.governance-complete-wlan-stage.v1"
        or record.get("sourceCommit")!=expected["sourceCommit"]
        or record.get("pressCommit")!=expected["pressCommit"]
        or record.get("readerCommit")!=expected["readerCommit"]
        or record.get("chapterCount")!=160
        or record.get("chapterStatuses")!={"current":72,"reference":88}
        or record.get("governanceStatusSHA256")!=expected["sourceStatusSHA256"]
        or record.get("stageOnly") is not True
        or record.get("publicReleaseAuthorized") is not False
        or record.get("measuredLinotypeCompositorChanged") is not False
        or record.get("governanceSourceModified") is not False
        or record.get("privateAudioStagePreserved") is not True):
        raise UnadmittedReaderRoute("False Governance publication status or source identity")
    chapters=record.get("chapterSources")
    if not isinstance(chapters,list) or len(chapters)!=160 or len({c.get("slug") for c in chapters})!=160:
        raise UnadmittedReaderRoute("Incomplete or duplicate Governance corpus")
    if sum(c.get("status")=="current" for c in chapters)!=72 or sum(c.get("status")=="reference" for c in chapters)!=88:
        raise UnadmittedReaderRoute("Wrong historical/current source classification")
    html_source=(candidate/"estate/index.html").read_text()
    if html_source.count('data-reader-volume="governance--')!=160:
        raise UnadmittedReaderRoute("Not all 160 Governance chapters are in the original Reader")
    for entry in chapters:
        if (not re.fullmatch(r"[0-9]{2,3}-[a-z0-9-]+",entry.get("slug",""))
            or not re.fullmatch(r"[0-9a-f]{64}",entry.get("sourceSha256",""))
            or ('data-reader-volume="governance--'+entry["slug"]+'"') not in html_source
            or ('data-source-sha256="'+entry["sourceSha256"]+'"') not in html_source):
            raise UnadmittedReaderRoute("Unmatched canonical Governance source: "+str(entry.get("slug")))
    assets=record.get("figureAssetsSHA256")
    if not isinstance(assets,dict) or len(assets)!=70:
        raise UnadmittedReaderRoute("Governance figure inventory missing")
    for url,expected_hash in assets.items():
        if not re.fullmatch(r"/assets/illustrations/[a-z0-9_.-]+",url):
            raise UnadmittedReaderRoute("Unrecognized Governance asset path")
        asset=candidate/"governance"/url.lstrip("/")
        if (not asset.is_file() or asset.is_symlink()
            or not re.fullmatch("[0-9a-f]{64}",str(expected_hash))
            or sha256(asset)!=expected_hash):
            raise UnadmittedReaderRoute("Missing/stale original Governance art "+url)
    if sha256(candidate/"estate/assets/linotype/reading-first-press-engine.js")!=sha256(prior/"estate/assets/linotype/reading-first-press-engine.js"):
        raise UnadmittedReaderRoute("Second Governance compositor is not allowed")
    return {**inherited,**GOVERNANCE_V161_CHANGED,**GOVERNANCE_V161_ADDED}


APPROVED_GOVERNANCE_V162_RELEASE="shared-shell-20261106-v162-governance-link-fidelity-4d6046b"
APPROVED_GOVERNANCE_V162_LOCK_SHA256="4fbc867a0cc7e50211e2568402341682fd9110fce41c91f8ce30e9f688e4f99e"
APPROVED_GOVERNANCE_V162_INDEX_SHA256="35ade43f8c38ba56773e1130505d0262e11aec87b716f7d07614eebb13d7156c"
APPROVED_GOVERNANCE_V162_RECEIPT_SHA256="d69c9208dd03dce8b910271a75c4db664d8481200376f911243d58a0adb00343"
GOVERNANCE_V162_CHANGED={"estate/index.html":APPROVED_GOVERNANCE_V162_INDEX_SHA256}
GOVERNANCE_V162_ADDED={"estate/evidence/press-governance-v162.json":APPROVED_GOVERNANCE_V162_RECEIPT_SHA256}


def approved_governance_v162_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Preserve every original Governance href in the existing 160-chapter book.

    No other Reader, source, audio or Estate route may change from admitted v161.
    """
    if candidate.name!=APPROVED_GOVERNANCE_V162_RELEASE:
        return {}
    prior=candidate.parent/APPROVED_GOVERNANCE_V161_RELEASE
    inherited=approved_governance_v161_files(baseline,prior)
    if not inherited:
        raise UnadmittedReaderRoute("No accepted complete v161 Governance book lineage")
    if sha256(candidate/"source-lock.json")!=APPROVED_GOVERNANCE_V162_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unknown v162 Governance link-fidelity source-lock")
    before=json.loads((prior/"source-lock.json").read_text())
    after=json.loads((candidate/"source-lock.json").read_text())
    decision=after.pop("pressGovernanceV162Admission",None)
    expected={
        "schema":"fountain.press.governance-link-fidelity-wlan-admission.v1",
        "predecessor":APPROVED_GOVERNANCE_V161_RELEASE,
        "release":APPROVED_GOVERNANCE_V162_RELEASE,
        "sourceOwner":"Fountain-Coach/governance.fountain.coach",
        "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
        "pressOwner":"Fountain-Coach/fountain-press",
        "pressCommit":"4d6046b6fd2438e8e7f0bfe41f6469916922179d",
        "readerOwner":"Fountain-Coach/fountain.coach",
        "readerCommit":"82efaddeec7a149774e4611fca908354c1ed74a0",
        "chapterCount":160,
        "statusCurrent":72,
        "statusReference":88,
        "originalLinksPreserved":1132,
        "originalFiguresPreserved":70,
        "priorLinotypeEngineUnchanged":True,
        "governanceCanonicalSourceUnmodified":True,
        "privateWLANOnly":True,
        "publicReleaseAuthorized":False,
        "changedFileSHA256":GOVERNANCE_V162_CHANGED,
        "addedFileSHA256":GOVERNANCE_V162_ADDED,
    }
    if before!=after or decision!=expected:
        raise UnadmittedReaderRoute("Missing exact Governance link-fidelity admission")
    old={p.relative_to(prior).as_posix():p for p in prior.rglob("*") if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if (set(new)-set(old)!=set(GOVERNANCE_V162_ADDED)
        or set(old)-set(new)):
        raise UnadmittedReaderRoute("Additional Governance stage file mutation")
    for rel,path in new.items():
        if path.is_symlink():
            raise UnadmittedReaderRoute("Unreviewed v162 stage symlink "+rel)
        if rel=="source-lock.json":continue
        wanted=GOVERNANCE_V162_CHANGED.get(rel,GOVERNANCE_V162_ADDED.get(rel))
        if wanted:
            if sha256(path)!=wanted:
                raise UnadmittedReaderRoute("Unrecognized Governance link-fidelity bytes "+rel)
        elif sha256(path)!=sha256(old[rel]):
            raise UnadmittedReaderRoute("Prior Reader/Governance/Kino bytes changed "+rel)
    record=json.loads((candidate/"estate/evidence/press-governance-v162.json").read_text())
    if (record.get("schema")!="fountain.press.governance-link-fidelity-wlan-stage.v1"
        or record.get("sourceCommit")!=expected["sourceCommit"]
        or record.get("pressCommit")!=expected["pressCommit"]
        or record.get("readerCommit")!=expected["readerCommit"]
        or record.get("chapterCount")!=160
        or record.get("chapterStatuses")!={"current":72,"reference":88}
        or record.get("sourceLinksOriginal")!=1132
        or record.get("sourceLinksPreserved")!=1132
        or record.get("illustrationAssetsPreserved")!=70
        or record.get("indexSHA256")!=APPROVED_GOVERNANCE_V162_INDEX_SHA256
        or record.get("appSHA256")!=APPROVED_GOVERNANCE_V161_APP_SHA256
        or record.get("stageOnly") is not True
        or record.get("publicReleaseAuthorized") is not False
        or record.get("readerRuntimeUnchanged") is not True):
        raise UnadmittedReaderRoute("Untrue Governance original-link acceptance claims")
    current_html=(candidate/"estate/index.html").read_text()
    if (current_html.count('data-reader-volume="governance--')!=160
        or 'https://governance.fountain.coach/assets/social/133-csound-auv3-instrument-boundary.jpg' not in current_html
        or 'https://governance.fountain.coach/chapters/08-validation-and-acceptance/#cb2-1' not in current_html
        or sha256(candidate/"estate/assets/linotype/reading-first-app.js")!=APPROVED_GOVERNANCE_V161_APP_SHA256):
        raise UnadmittedReaderRoute("Lost original Governance link or modified Reader runtime")
    return {**inherited,**GOVERNANCE_V162_CHANGED,**GOVERNANCE_V162_ADDED}


APPROVED_GOVERNANCE_V163_RELEASE="shared-shell-20261106-v163-governance-inline-hero-cfc2745"
APPROVED_GOVERNANCE_V163_LOCK_SHA256="75198bfc5ae03f75d53a5fbc9c1a69b73bde0e5d0f563863d5fe8f73b7989091"
APPROVED_GOVERNANCE_V163_INDEX_SHA256="4c9298785fa505f8971429be9cf42b10682acc950b534194415193c87472e757"
APPROVED_GOVERNANCE_V163_RECEIPT_SHA256="8f0125958684dac0a9c2bf1c006f5e39b92e66b95ac43012da62c213745d871e"
GOVERNANCE_V163_CHANGED={"estate/index.html":APPROVED_GOVERNANCE_V163_INDEX_SHA256}
GOVERNANCE_V163_ADDED={"estate/evidence/press-governance-v163.json":APPROVED_GOVERNANCE_V163_RECEIPT_SHA256}


def approved_governance_v163_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Only original Governance image source anchors; no new engine or artwork."""
    if candidate.name!=APPROVED_GOVERNANCE_V163_RELEASE:return {}
    prior=candidate.parent/APPROVED_GOVERNANCE_V162_RELEASE
    inherited=approved_governance_v162_files(baseline,prior)
    if not inherited:
        raise UnadmittedReaderRoute("Governance hero stage lacks v162 accepted lineage")
    if sha256(candidate/"source-lock.json")!=APPROVED_GOVERNANCE_V163_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unknown v163 source-lock")
    before=json.loads((prior/"source-lock.json").read_text())
    after=json.loads((candidate/"source-lock.json").read_text())
    admission=after.pop("pressGovernanceV163Admission",None)
    expected={
        "schema":"fountain.press.governance-inline-hero-wlan-admission.v1",
        "release":APPROVED_GOVERNANCE_V163_RELEASE,
        "predecessor":APPROVED_GOVERNANCE_V162_RELEASE,
        "sourceOwner":"Fountain-Coach/governance.fountain.coach",
        "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
        "pressOwner":"Fountain-Coach/fountain-press",
        "pressCommit":"cfc2745772c8d3ea306f86e1cae8ac53f8805a9c",
        "readerOwner":"Fountain-Coach/fountain.coach",
        "readerCommit":"748ba55c38e167e9de90d6ec0572191dbcafa41e",
        "chapterCount":160,"statusCurrent":72,"statusReference":88,
        "sourceFigureCount":70,"sourceHeroCount":67,"sourceInlineCount":3,
        "allOriginalLinksUnchanged":True,"existingLinotypeEngineUnchanged":True,
        "privateWLANOnly":True,"publicReleaseAuthorized":False,
        "changedFileSHA256":GOVERNANCE_V163_CHANGED,
        "addedFileSHA256":GOVERNANCE_V163_ADDED,
    }
    if before!=after or admission!=expected:
        raise UnadmittedReaderRoute("Wrong Governance v163 source admission")
    old={p.relative_to(prior).as_posix():p for p in prior.rglob("*") if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(new)-set(old)!=set(GOVERNANCE_V163_ADDED) or set(old)-set(new):
        raise UnadmittedReaderRoute("Unexpected Governance v163 file additions/removals")
    for rel,path in new.items():
        if path.is_symlink():
            raise UnadmittedReaderRoute("Unreviewed v163 link "+rel)
        if rel=="source-lock.json":continue
        needed=GOVERNANCE_V163_CHANGED.get(rel,GOVERNANCE_V163_ADDED.get(rel))
        if needed:
            if sha256(path)!=needed:
                raise UnadmittedReaderRoute("Wrong v163 exact artifact: "+rel)
        elif sha256(path)!=sha256(old[rel]):
            raise UnadmittedReaderRoute("Unrelated Reader or private media mutated: "+rel)
    expected_html=(prior/"estate/index.html").read_text()
    new_html=(candidate/"estate/index.html").read_text()
    marker=(r' data-press-illustration-role="(?:hero|inline)"'
            r' data-source-illustration-id="[^"]+"'
            r' data-inline-after-paragraph="\d+"'
            r' data-source-paragraph-anchor="\d+"')
    markers=re.findall(marker,new_html)
    normalized=re.sub(marker,"",new_html)
    if (normalized!=expected_html or len(markers)!=70 or
        new_html.count('data-press-illustration-role="hero"')!=67 or
        new_html.count('data-press-illustration-role="inline"')!=3 or
        new_html.count('data-reader-volume="governance--')!=160):
        raise UnadmittedReaderRoute("Governance changes extend beyond 70 source-anchored art figures")
    record=json.loads((candidate/"estate/evidence/press-governance-v163.json").read_text())
    if (record.get("schema")!="fountain.press.governance-source-anchored-illustration-wlan-stage.v1"
        or record.get("sourceRevision")!=expected["sourceCommit"]
        or record.get("pressCommit")!=expected["pressCommit"]
        or record.get("readerCommit")!=expected["readerCommit"]
        or record.get("indexSHA256")!=APPROVED_GOVERNANCE_V163_INDEX_SHA256
        or record.get("appSHA256")!=APPROVED_GOVERNANCE_V161_APP_SHA256
        or record.get("figuresInSourceFlow")!=70
        or record.get("heroFigures")!=67
        or record.get("inlineFigures")!=3
        or record.get("existingLinotypeEngineUnchanged") is not True
        or record.get("unchangedPriorMarkupAfterRemovingOnlySourceAnchors") is not True
        or record.get("publicReleaseAuthorized") is not False
        or record.get("socialMediaImagePublicationStatus")!="not-modified-in-this-illustration-placement-fix"):
        raise UnadmittedReaderRoute("False Governance source illustration or social publishing witness")
    figures=record.get("anchoredSourceFigureIdentities")
    if not isinstance(figures,list) or len(figures)!=70 or len({f.get("id") for f in figures})!=70:
        raise UnadmittedReaderRoute("Incomplete original Governance illustration identities")
    for f in figures:
        if (f.get("role") not in ("hero","inline")
            or not isinstance(f.get("pressAnchorAfterParagraph"),int)
            or not isinstance(f.get("authoredParagraphCountBeforeFigure"),int)
            or f["pressAnchorAfterParagraph"]!=max(1,f["authoredParagraphCountBeforeFigure"])
            or ('data-source-illustration-id="'+f["id"]+'"') not in new_html):
            raise UnadmittedReaderRoute("Governance figure is not at its pinned source anchor")
    return {**inherited,**GOVERNANCE_V163_CHANGED,**GOVERNANCE_V163_ADDED}


APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE="shared-shell-20261106-v164-governance-social-b7b1dee"
APPROVED_GOVERNANCE_SOCIAL_V164_LOCK_SHA256="61703c3eb1271dd19461b6f79d09df21634efadfc1737d1c01735304e59b3771"
APPROVED_GOVERNANCE_SOCIAL_V164_MANIFEST_SHA256="07097d3f5d485644b4a28e849d6fbca9e6829daed811f9852efcb417943ce2bc"
APPROVED_GOVERNANCE_SOCIAL_V164_RECEIPT_SHA256="ea820fd6dd8b20dc888eec5e3494885a159598641df9852b17011c052a8c1244"

def approved_governance_social_v164_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Only original-source art and measured-page social derivatives; never another Reader."""
    if candidate.name != APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE:return {}
    previous=candidate.parent/APPROVED_GOVERNANCE_V163_RELEASE
    inherited=approved_governance_v163_files(baseline,previous)
    if not inherited:raise UnadmittedReaderRoute("No accepted v163 figure predecessor")
    if sha256(candidate/"source-lock.json")!=APPROVED_GOVERNANCE_SOCIAL_V164_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unpinned social source lock")
    original_lock=json.loads((previous/"source-lock.json").read_text())
    current_lock=json.loads((candidate/"source-lock.json").read_text())
    admission=current_lock.pop("pressGovernanceSocialV164Admission",None)
    expected={
        "schema":"fountain.press.governance.static-social-wlan-admission.v1",
        "release":APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE,
        "predecessor":APPROVED_GOVERNANCE_V163_RELEASE,
        "sourceOwner":"Fountain-Coach/governance.fountain.coach",
        "sourceCommit":"03f15306a018eddd85fab491e592d2fdffd61528",
        "pressOwner":"Fountain-Coach/fountain-press",
        "pressCommit":"b7b1deec4d42f249c0cacbb009709486bfc1154d",
        "readerOwner":"Fountain-Coach/fountain.coach",
        "readerCommit":"748ba55c38e167e9de90d6ec0572191dbcafa41e",
        "shareManifestSHA256":APPROVED_GOVERNANCE_SOCIAL_V164_MANIFEST_SHA256,
        "shareReceiptSHA256":APPROVED_GOVERNANCE_SOCIAL_V164_RECEIPT_SHA256,
        "shareDirectory":"estate/share/governance/",
        "shareSourceChapterCount":160,
        "heroDerivativeCount":68,
        "firstLandscapePageCount":92,
        "rightsRaisedForPublicUse":False,
        "readerAndSourceUnchanged":True,
        "privateWLANOnly":True,
        "publicReleaseAuthorized":False
    }
    if original_lock!=current_lock or admission!=expected:
        raise UnadmittedReaderRoute("Social admission changes v163 identity or grants new authority")
    prefix="estate/share/governance/"
    manifest_file=prefix+"manifest.json"
    receipt_file="estate/evidence/press-governance-social-v164.json"
    if (sha256(candidate/manifest_file)!=APPROVED_GOVERNANCE_SOCIAL_V164_MANIFEST_SHA256 or
        sha256(candidate/receipt_file)!=APPROVED_GOVERNANCE_SOCIAL_V164_RECEIPT_SHA256):
        raise UnadmittedReaderRoute("Unpinned image manifest/receipt")
    report=json.loads((candidate/manifest_file).read_text())
    receipt=json.loads((candidate/receipt_file).read_text())
    if (report.get("schema")!="fountain.press.governance.static-social-cards.v1" or
        report.get("sourceRevision")!=expected["sourceCommit"] or
        report.get("readerIndexSha256")!=APPROVED_GOVERNANCE_V163_INDEX_SHA256 or
        report.get("readerAppSha256")!=APPROVED_GOVERNANCE_V161_APP_SHA256 or
        report.get("counts")!={"chapters":160,"heroRaster":68,"firstLandscapeSpread":92,"current":72,"reference":88} or
        report.get("publicReleaseAuthorized") is not False or
        report.get("cardRightsNotElevated") is not True or
        len(report.get("entries",[]))!=160 or
        receipt.get("schema")!="fountain.press.governance.static-social-stage.v1" or
        receipt.get("pressCommit")!=expected["pressCommit"] or
        receipt.get("socialManifestSha256")!=APPROVED_GOVERNANCE_SOCIAL_V164_MANIFEST_SHA256 or
        receipt.get("stageOnly") is not True or receipt.get("publicReleaseAuthorized") is not False):
        raise UnadmittedReaderRoute("False social-source or publication metadata")
    prior_html=(previous/"estate/index.html").read_text()
    ids=re.findall(r'<template data-reader-volume="governance--([^"]+)"[^>]*data-source-sha256="([a-f0-9]{64})" data-governance-status="(current|reference)"',prior_html)
    if len(ids)!=160 or len({slug for slug,_,_ in ids})!=160:
        raise UnadmittedReaderRoute("Lost canonical Governance volume identities")
    extra={manifest_file:APPROVED_GOVERNANCE_SOCIAL_V164_MANIFEST_SHA256,
           receipt_file:APPROVED_GOVERNANCE_SOCIAL_V164_RECEIPT_SHA256}
    number_hero=0
    for (slug,source_sha,status),entry in zip(ids,report["entries"]):
        if (entry.get("slug")!=slug or entry.get("volumeId")!="governance--"+slug or
            entry.get("sourceSha256")!=source_sha or entry.get("status")!=status):
            raise UnadmittedReaderRoute("Chapter identity drift in social projection")
        volume=re.search(r'<template data-reader-volume="governance--'+re.escape(slug)+r'".*?</template>',prior_html,re.S)
        has_art=bool(volume and ('data-press-illustration-role="hero"' in volume.group() or 'gov-inline-svg' in volume.group()))
        if entry.get("mode")!=("original-hero-raster" if has_art else "first-landscape-spread"):
            raise UnadmittedReaderRoute("Image fallback contradicts original chapter")
        if has_art:number_hero+=1
        else:
            proof=entry.get("firstLandscapeComposition") or {}
            if (proof.get("firstFolioSourceId")!="work-governance-"+slug or
                proof.get("mode")!="spread" or
                proof.get("captureViewport")!={"width":1200,"height":630} or
                proof.get("stageClip")!={"width":1168,"height":518}):
                raise UnadmittedReaderRoute("First source landscape folio not witnessed")
        base=prefix+slug+"/"
        page=base+"index.html";card=base+"card.jpg"
        if (entry.get("staticHTMLPath")!=page or entry.get("cardPath")!=card or
            entry.get("cardWidth")!=1200 or entry.get("cardHeight")!=630 or
            entry.get("cardMime")!="image/jpeg" or
            not str(entry.get("rightsState","")).endswith("public-use-not-separately-authorized")):
            raise UnadmittedReaderRoute("Unapproved social file scope/rights")
        page_file=candidate/page;card_file=candidate/card
        if (not page_file.is_file() or not card_file.is_file() or
            page_file.is_symlink() or card_file.is_symlink() or
            sha256(page_file)!=entry.get("staticHTMLSha256") or
            sha256(card_file)!=entry.get("cardSha256")):
            raise UnadmittedReaderRoute("Different social image or HTML bytes")
        url="https://192.168.8.50:8243/"+base
        head=page_file.read_text()
        if (entry.get("stageShareURL")!=url or entry.get("stageImageURL")!=url+"card.jpg" or
            '<meta property="og:url" content="'+url+'">' not in head or
            '<meta property="og:image" content="'+url+'card.jpg">' not in head or
            '<meta name="twitter:image" content="'+url+'card.jpg">' not in head or
            '<meta property="og:image:width" content="1200">' not in head or
            '<meta property="og:image:height" content="630">' not in head or
            'fountain-coach-governance-estate.jpg' in head or
            not card_file.read_bytes().startswith(bytes((255,216)))):
            raise UnadmittedReaderRoute("Unrelated fallback or unaddressable crawler image")
        extra[page]=entry["staticHTMLSha256"];extra[card]=entry["cardSha256"]
    if number_hero!=68 or len(extra)!=322:
        raise UnadmittedReaderRoute("Not all 160 source cards were admitted")
    old={p.relative_to(previous).as_posix():p for p in previous.rglob("*") if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(new)-set(old)!=set(extra) or set(old)-set(new):
        raise UnadmittedReaderRoute("Unreviewed file in social release")
    for rel,p in new.items():
        if p.is_symlink():raise UnadmittedReaderRoute("Unreviewed symbolic link")
        if rel=="source-lock.json":continue
        if rel in extra:
            if sha256(p)!=extra[rel]:raise UnadmittedReaderRoute("Wrong new social file "+rel)
        elif sha256(p)!=sha256(old[rel]):
            raise UnadmittedReaderRoute("Existing Reader, audio or Governance modified "+rel)
    return {**inherited,**extra}




APPROVED_SOUND_CRAFT_V165_RELEASE="shared-shell-20261106-v165-satzfunk-csound-ab-eb45a85"
APPROVED_SOUND_CRAFT_V165_LOCK_SHA256="1f369206aef342b8423f959df437e1c069e0312c5ee75ac1f8a947ec4d0c3a36"
APPROVED_SOUND_CRAFT_V165_RECEIPT_SHA256="9e120b320e7f03206756d4a12d3d81b5bc94b6c1683259603616ef1f22cd0836"
APPROVED_SOUND_CRAFT_V165_SCORE_SHA256="21ae0eda6621d1b2ff90a1baaa792def576d7399da62cc90609022d854abda49"
APPROVED_SOUND_CRAFT_V165_REVISED_SHA256="b1da1f4c3651e84eb55e104d02d311ebd047278a046f427563600e091348ea44"
APPROVED_SOUND_CRAFT_V165_CHANGED={
    "estate/index.html":"5a2a8c084d806c515890e276be445fe34c21ca0243948d8cc088bcc70e65ab97",
    "estate/assets/linotype/reading-first-app.js":"46876ca7b54c5f26df2372f1ec037871e61f6773a406ff41ec32a634337b7831"
}
APPROVED_SOUND_CRAFT_V165_ADDED={
    "estate/media/kino/sound-craft/source-manifest.json":"712488ba5ae545692a7336f82a0b126b5165b85d62fcdf1d7ca91929c17786b7",
    "estate/media/kino/sound-craft/edition.json":"20ff8f8acfb30efe189ec6e9981fffd3c8297a80cd4ad08a34523c68956b9e0f",
    "estate/media/kino/sound-craft/a-literal.csd":"1f21a92ded2ceeaa699111254987c1d411bb740ebebfc140ef1b919ca9738ab7",
    "estate/media/kino/sound-craft/b-directed.csd":"928656e3a6e8a6a2edf7ea9fad55b844afca1b27bd4af94140a63b3b5850a202",
    "estate/media/kino/sound-craft/a-literal.m4a":"f8db7d1cee00b6e346fb400567c2868e99a97cf4c51007b3fe47fe542dbde427",
    "estate/media/kino/sound-craft/b-directed.m4a":"5413a93ba9a1c471e2178f93f099e412b464f2e25447b8a7f4ebb960b298d94b",
    "estate/evidence/press-sound-csound-v165.json":APPROVED_SOUND_CRAFT_V165_RECEIPT_SHA256
}

def approved_sound_craft_v165_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Preserve v164 byte-for-byte except a single edited essay and two Csound auditions."""
    if candidate.name!=APPROVED_SOUND_CRAFT_V165_RELEASE:return {}
    previous=candidate.parent/APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE
    inherited=approved_governance_social_v164_files(baseline,previous)
    if not inherited:
        raise UnadmittedReaderRoute("No complete v164 predecessor for audio proof")
    if sha256(candidate/"source-lock.json")!=APPROVED_SOUND_CRAFT_V165_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unapproved v165 source lock")
    old_lock=json.loads((previous/"source-lock.json").read_text())
    new_lock=json.loads((candidate/"source-lock.json").read_text())
    admission=new_lock.pop("pressSoundCsoundV165Admission",None)
    expected={
      "schema":"fountain.press.satzfunk-csound-editorial-audition.v1",
      "release":APPROVED_SOUND_CRAFT_V165_RELEASE,
      "predecessor":APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE,
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":"eb45a85d7485e7e8e4b093bc259e4f6c8075ec6d",
      "teatroOwner":"Fountain-Coach/teatro.fountain.coach",
      "teatroCommit":"1d8f6345ee0cb9fc7b8802cf2f3e0cdd6fc14b03",
      "editorialSourceSHA256":APPROVED_SOUND_CRAFT_V165_REVISED_SHA256,
      "csoundScoreSHA256":APPROVED_SOUND_CRAFT_V165_SCORE_SHA256,
      "readerIndexSHA256":APPROVED_SOUND_CRAFT_V165_CHANGED["estate/index.html"],
      "readerAppSHA256":APPROVED_SOUND_CRAFT_V165_CHANGED["estate/assets/linotype/reading-first-app.js"],
      "receiptSHA256":APPROVED_SOUND_CRAFT_V165_RECEIPT_SHA256,
      "privateWLANOnly":True,
      "publicReleaseAuthorized":False,
      "otherWorksPreserved":True,
      "nativeCsoundScenarioAdmissionClaimed":False
    }
    if old_lock!=new_lock or admission!=expected:
        raise UnadmittedReaderRoute("v165 source-lock changes unrelated book or grants authority")
    receipt=json.loads((candidate/"estate/evidence/press-sound-csound-v165.json").read_text())
    if (receipt.get("schema")!="fountain.press.satzfunk-csound-essay-stage.v165"
        or receipt.get("release")!=APPROVED_SOUND_CRAFT_V165_RELEASE
        or receipt.get("predecessor")!=APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE
        or receipt.get("editorialSourceSHA256")!=APPROVED_SOUND_CRAFT_V165_REVISED_SHA256
        or receipt.get("csoundSourceScoreSHA256")!=APPROVED_SOUND_CRAFT_V165_SCORE_SHA256
        or receipt.get("privateWLANOnly") is not True
        or receipt.get("publicReleaseAuthorized") is not False
        or receipt.get("artisticallyAccepted") is not False
        or receipt.get("nativeCsoundScenarioAdmitted") is not False
        or receipt.get("changedSHA256")!={**APPROVED_SOUND_CRAFT_V165_CHANGED,
              **{k:v for k,v in APPROVED_SOUND_CRAFT_V165_ADDED.items() if k!="estate/evidence/press-sound-csound-v165.json"}}):
        raise UnadmittedReaderRoute("v165 evidence does not match source and non-public rights")
    edition=json.loads((candidate/"estate/media/kino/sound-craft/edition.json").read_text())
    source=json.loads((candidate/"estate/media/kino/sound-craft/source-manifest.json").read_text())
    if (edition.get("schema")!="satzfunk.recorded-essay-rehearsal.v1"
        or edition.get("scoreSHA256")!=APPROVED_SOUND_CRAFT_V165_SCORE_SHA256
        or edition.get("mediaBasePrefix")!="/estate/"
        or source.get("sourceScoreSHA256")!=APPROVED_SOUND_CRAFT_V165_SCORE_SHA256
        or source.get("noOutsideRecordings") is not True
        or source.get("noNativeScenarioAdmissionClaim") is not True
        or len(edition.get("tracks",[]))!=2
        or len(source.get("files",[]))!=2
        or {t.get("id") for t in edition["tracks"]}!={"a-literal","b-directed"}
        or any(t.get("publicReleaseAuthorized") is not False or
               t.get("privateRehearsalAuthorized") is not True or
               t.get("sourceSHA256")!=APPROVED_SOUND_CRAFT_V165_SCORE_SHA256 for t in edition["tracks"])):
        raise UnadmittedReaderRoute("unverified media/source custody or a public grant")
    prev_html=(previous/"estate/index.html").read_text()
    new_html=(candidate/"estate/index.html").read_text()
    pattern=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    old_matches=re.findall(pattern,prev_html,re.S)
    new_matches=re.findall(pattern,new_html,re.S)
    if (len(old_matches)!=1 or len(new_matches)!=1 or
        new_html.replace(new_matches[0],old_matches[0],1)!=prev_html or
        new_matches[0].count("<satzfunk-player compact")!=2 or
        'data-source-sha256="'+APPROVED_SOUND_CRAFT_V165_REVISED_SHA256+'"' not in new_matches[0] or
        'It is ready when the work can answer for it.' not in new_matches[0]):
        raise UnadmittedReaderRoute("v165 changes unrelated reader content or old essay is still visible")
    app=(candidate/"estate/assets/linotype/reading-first-app.js").read_text()
    if ("const soundEditionPromise=" not in app or
        "const soundCraftPromise=" not in app or
        "if(volume===proofVolume)" not in app or
        app.count("function syncSatzfunkPlayer(){")!=1):
        raise UnadmittedReaderRoute("v165 must reuse the existing SatzfunkPlayer")
    old={p.relative_to(previous).as_posix():p for p in previous.rglob("*") if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(new)-set(old)!=set(APPROVED_SOUND_CRAFT_V165_ADDED) or set(old)-set(new):
        raise UnadmittedReaderRoute("v165 adds/removes unadmitted assets")
    for rel,p in new.items():
        if p.is_symlink():raise UnadmittedReaderRoute("v165 symbolic-link substitution")
        if rel=="source-lock.json":continue
        expected_hash=(APPROVED_SOUND_CRAFT_V165_CHANGED.get(rel) or
                       APPROVED_SOUND_CRAFT_V165_ADDED.get(rel))
        if expected_hash is not None:
            if sha256(p)!=expected_hash:
                raise UnadmittedReaderRoute("v165 source/file SHA mismatch "+rel)
        elif sha256(p)!=sha256(old[rel]):
            raise UnadmittedReaderRoute("v165 changes original Reader/other books "+rel)
    return {**inherited,**APPROVED_SOUND_CRAFT_V165_CHANGED,
            **APPROVED_SOUND_CRAFT_V165_ADDED}


# Source-owned two-figure addition to the already verified original sound essay.
# This is a reversible private stage publication, not a new Linotype edition,
# public rights grant, or native Csound Scenario.
APPROVED_KINO_FIGURES_V166_RELEASE="shared-shell-20261106-v166-essay-kino-figures-d79f9e0"
APPROVED_KINO_FIGURES_V166_LOCK_SHA256="3ed927bf7388694d85aeb9c3afba878288e8ade4e9654c44285df3a4d59464ee"
APPROVED_KINO_FIGURES_V166_SOURCE_SHA256="74d99a870040926c6e2ba86cb20e29b7c55585f385e9d0f56d6cc47b481f4432"
APPROVED_KINO_FIGURES_V166_INDEX_SHA256="2184719abcb24b13ae3ca2c795f2dbabef5419ab46b817343a487efe8407abe1"
APPROVED_KINO_FIGURES_V166_ADDED={
    "estate/essays/a-sound-must-earn-its-place/media/illustration-source.json":"3e40e8e014a66511cc23270ad8bd3e1ef7c693db1f855fac5e9d7c6bd325df9b",
    "estate/essays/a-sound-must-earn-its-place/media/kino-international-architectural-plate-20261106.jpg":"9bfa71540c6b54a4ac83696fbc0506e31ae58e47c681634d9b93dc4386d31a1c",
    "estate/essays/a-sound-must-earn-its-place/media/kino-international-night-20261106.jpg":"cb7b399aeb472a65a7156f9d9990b39564ba492337ef19365ed079c68ac1bc52",
    "estate/evidence/press-essay-kino-illustrations-v166.json":"53ca8c476c62fa8e95bbff3a566a58c4ce2de7db22aacb1d03c5a941bda3e3bc",
}
def approved_kino_figures_v166_files(baseline:Path,candidate:Path)->dict[str,str]:
    """Accept exactly two source-addressed figures; preserve original Reader/audio."""
    if candidate.name!=APPROVED_KINO_FIGURES_V166_RELEASE:return {}
    previous=candidate.parent/APPROVED_SOUND_CRAFT_V165_RELEASE
    inherited=approved_sound_craft_v165_files(baseline,previous)
    if not inherited:raise UnadmittedReaderRoute("Unaccepted v165 sound essay predecessor")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_FIGURES_V166_LOCK_SHA256:
        raise UnadmittedReaderRoute("Unadmitted v166 source lock")
    old_lock=json.loads((previous/"source-lock.json").read_text())
    new_lock=json.loads((candidate/"source-lock.json").read_text())
    grant=new_lock.pop("pressKinoFiguresV166Admission",None)
    if old_lock!=new_lock:raise UnadmittedReaderRoute("v166 changes unrelated source authority")
    expected={
      "schema":"fountain.press.kino-essay-illustrations.v166",
      "release":APPROVED_KINO_FIGURES_V166_RELEASE,
      "predecessor":APPROVED_SOUND_CRAFT_V165_RELEASE,
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":"d79f9e0704c143f41dbf5d06a7458997e016f3e1",
      "sourceSHA256":APPROVED_KINO_FIGURES_V166_SOURCE_SHA256,
      "previousIndexSHA256":APPROVED_SOUND_CRAFT_V165_CHANGED["estate/index.html"],
      "readerIndexSHA256":APPROVED_KINO_FIGURES_V166_INDEX_SHA256,
      "readerAppSHA256":APPROVED_SOUND_CRAFT_V165_CHANGED["estate/assets/linotype/reading-first-app.js"],
      "receiptSHA256":APPROVED_KINO_FIGURES_V166_ADDED["estate/evidence/press-essay-kino-illustrations-v166.json"],
      "figures":[
        {"id":"architectural-plate","sha256":APPROVED_KINO_FIGURES_V166_ADDED["estate/essays/a-sound-must-earn-its-place/media/kino-international-architectural-plate-20261106.jpg"]},
        {"id":"night-photograph","sha256":APPROVED_KINO_FIGURES_V166_ADDED["estate/essays/a-sound-must-earn-its-place/media/kino-international-night-20261106.jpg"]}],
      "publicReleaseAuthorized":False,"privateWLANOnly":True,
      "originalEssayProsePreserved":True,"originalSatzfunkPlayerPreserved":True,
      "measuredArchitecturalDrawingClaimed":False
    }
    if grant!=expected:raise UnadmittedReaderRoute("Unreviewed image provenance/admission")
    receipt=json.loads((candidate/"estate/evidence/press-essay-kino-illustrations-v166.json").read_text())
    manifest=json.loads((candidate/"estate/essays/a-sound-must-earn-its-place/media/illustration-source.json").read_text())
    if (receipt.get("schema")!="fountain.press.kino-essay-illustrations-stage-candidate.v1"
        or receipt.get("v3SourceSHA256")!=APPROVED_KINO_FIGURES_V166_SOURCE_SHA256
        or receipt.get("candidateIndexSHA256")!=APPROVED_KINO_FIGURES_V166_INDEX_SHA256
        or receipt.get("candidateAppUnchanged") is not True
        or receipt.get("essayBodyTextUnchanged") is not True
        or receipt.get("csoundSatzfunkTracksUnchanged") is not True
        or receipt.get("otherReaderVolumesUnchanged") is not True
        or receipt.get("figureCount")!=2
        or receipt.get("architecturePlateMeasured") is not False
        or receipt.get("publicRightsGranted") is not False
        or manifest.get("schema")!="fountain.press.essay-authored-illustrations.v1"
        or manifest.get("publicRightsGranted") is not False
        or len(manifest.get("figures",[]))!=2
        or [x.get("id") for x in manifest["figures"]]!=["architectural-plate","night-photograph"]
        or any(x.get("sha256")!=f["sha256"] or x.get("sourceAddress")!="a-sound-must-earn-its-place.figure."+str(i+1)
               for i,(x,f) in enumerate(zip(manifest["figures"],expected["figures"])))):
        raise UnadmittedReaderRoute("v166 no longer matches approved art/rights")
    old_html=(previous/"estate/index.html").read_text()
    new_html=(candidate/"estate/index.html").read_text()
    pat=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    a=re.findall(pat,old_html,re.S)
    b=re.findall(pat,new_html,re.S)
    if (len(a)!=1 or len(b)!=1 or new_html.replace(b[0],a[0],1)!=old_html
        or 'data-source-sha256="'+APPROVED_KINO_FIGURES_V166_SOURCE_SHA256+'"' not in b[0]
        or b[0].count('<satzfunk-player compact')!=2):
        raise UnadmittedReaderRoute("v166 changed unrelated Reader or audio")
    cleaned=b[0]
    for kind in ("architectural-plate","night-photograph"):
        pat=r'<figure[^>]*data-source-illustration-id="'+kind+r'"[^>]*>.*?</figure>'
        matches=re.findall(pat,cleaned,re.S)
        if len(matches)!=1:raise UnadmittedReaderRoute("Missing/duplicate source figure "+kind)
        cleaned=cleaned.replace(matches[0],"",1)
    cleaned=cleaned.replace(APPROVED_KINO_FIGURES_V166_SOURCE_SHA256,APPROVED_SOUND_CRAFT_V165_REVISED_SHA256,1)
    if cleaned!=a[0]:
        raise UnadmittedReaderRoute("Illustration insertion changed actual essay prose")
    old={p.relative_to(previous).as_posix():p for p in previous.rglob("*") if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob("*") if p.is_file()}
    if set(new)-set(old)!=set(APPROVED_KINO_FIGURES_V166_ADDED) or set(old)-set(new):
        raise UnadmittedReaderRoute("v166 adds unknown files or deletes source")
    for rel,path in new.items():
        if path.is_symlink():raise UnadmittedReaderRoute("Symlink injection")
        if rel=="source-lock.json":continue
        approved=APPROVED_KINO_FIGURES_V166_ADDED.get(rel)
        if rel=="estate/index.html":approved=APPROVED_KINO_FIGURES_V166_INDEX_SHA256
        if approved is not None:
            if sha256(path)!=approved:raise UnadmittedReaderRoute("v166 asset drift "+rel)
        elif sha256(path)!=sha256(old[rel]):
            raise UnadmittedReaderRoute("v166 changed other books/audio/Reader "+rel)
    return {**inherited,"estate/index.html":APPROVED_KINO_FIGURES_V166_INDEX_SHA256,
            **APPROVED_KINO_FIGURES_V166_ADDED}


# Source-preserving editorial reflow of the two already admitted Kino figures.
# V166 is immutable. V167 changes only their roles, anchoring and short captions.
APPROVED_KINO_COMPOSITION_V167_RELEASE="shared-shell-20261106-v167-essay-kino-composition-212cd57"
APPROVED_KINO_COMPOSITION_V167_SOURCE_SHA="044989721e76efb8d587d87893f4f623a2c106d10f9d6d929d23c795532cc585"
APPROVED_KINO_COMPOSITION_V167_SOURCE_COMMIT="212cd5730c83f796ed8af9cadaa9c3ed0f80860f"
APPROVED_KINO_COMPOSITION_V167_INDEX_SHA="33812b6e908e2f9ca26c9f09e7da7a5074bf20b5ccf43d19df41514b5cc30360"
APPROVED_KINO_COMPOSITION_V167_LOCK_SHA="7fd7cb08c4fa292abfa544a16e3053722ca84d2a15c075fdd4a7064e51b5b92f"
APPROVED_KINO_COMPOSITION_V167_MANIFEST_SHA="d80c728993716d5154daabe959e667a4f9090be108b630da23a8b79f4d4edb30"
APPROVED_KINO_COMPOSITION_V167_RECEIPT_PATH="estate/evidence/press-essay-kino-illustrations-v167.json"
APPROVED_KINO_COMPOSITION_V167_RECEIPT_SHA="98196c4dbbc41d32eefb29ac537792d052574426ab7180cb25f88358d7455129"
APPROVED_KINO_COMPOSITION_V167_MANIFEST_PATH="estate/essays/a-sound-must-earn-its-place/media/illustration-source.json"
def approved_kino_composition_v167_files(baseline:Path,candidate:Path)->dict[str,str]:
    if candidate.name!=APPROVED_KINO_COMPOSITION_V167_RELEASE:return {}
    previous=candidate.parent/APPROVED_KINO_FIGURES_V166_RELEASE
    inherited=approved_kino_figures_v166_files(baseline,previous)
    if not inherited:raise UnadmittedReaderRoute("Unaccepted immutable Kino figures predecessor")
    if sha256(candidate/"source-lock.json")!=APPROVED_KINO_COMPOSITION_V167_LOCK_SHA:
        raise UnadmittedReaderRoute("Unknown v167 source lock")
    old_lock=json.loads((previous/"source-lock.json").read_text())
    new_lock=json.loads((candidate/"source-lock.json").read_text())
    grant=new_lock.pop("pressKinoFiguresV167Admission",None)
    if new_lock!=old_lock:raise UnadmittedReaderRoute("Unrelated release/source lock changed")
    expected={
      "schema":"fountain.press.kino-essay-composition.v167",
      "release":APPROVED_KINO_COMPOSITION_V167_RELEASE,
      "predecessor":APPROVED_KINO_FIGURES_V166_RELEASE,
      "sourceOwner":"Fountain-Coach/fountain.coach",
      "sourceCommit":APPROVED_KINO_COMPOSITION_V167_SOURCE_COMMIT,
      "sourceSHA256":APPROVED_KINO_COMPOSITION_V167_SOURCE_SHA,
      "previousIndexSHA256":APPROVED_KINO_FIGURES_V166_INDEX_SHA256,
      "readerIndexSHA256":APPROVED_KINO_COMPOSITION_V167_INDEX_SHA,
      "readerAppSHA256":APPROVED_SOUND_CRAFT_V165_CHANGED["estate/assets/linotype/reading-first-app.js"],
      "receiptSHA256":APPROVED_KINO_COMPOSITION_V167_RECEIPT_SHA,
      "illustrationManifestSHA256":APPROVED_KINO_COMPOSITION_V167_MANIFEST_SHA,
      "architecturalPlateRole":"inline","nightPhotographRole":"social-lead",
      "nightPhotoFollowsParagraph":8,
      "publicReleaseAuthorized":False,"privateWLANOnly":True,
      "originalEssayProsePreserved":True,"originalSatzfunkPlayerPreserved":True
    }
    if grant!=expected:raise UnadmittedReaderRoute("Kino editorial revision identity/roles mismatched")
    manifest=json.loads((candidate/APPROVED_KINO_COMPOSITION_V167_MANIFEST_PATH).read_text())
    receipt=json.loads((candidate/APPROVED_KINO_COMPOSITION_V167_RECEIPT_PATH).read_text())
    figures=manifest.get("figures",[])
    if (len(figures)!=2 or
        [(f.get("id"),f.get("role")) for f in figures]!=
           [("architectural-plate","inline"),("night-photograph","social-lead")] or
        receipt.get("v3SourceSHA256")!=APPROVED_KINO_COMPOSITION_V167_SOURCE_SHA or
        receipt.get("candidateIndexSHA256")!=APPROVED_KINO_COMPOSITION_V167_INDEX_SHA or
        receipt.get("candidateAppUnchanged") is not True or
        receipt.get("essayBodyTextUnchanged") is not True or
        receipt.get("csoundSatzfunkTracksUnchanged") is not True or
        receipt.get("otherReaderVolumesUnchanged") is not True or
        receipt.get("socialLeadIllustrationID")!="night-photograph" or
        receipt.get("architecturalPlateInline") is not True or
        receipt.get("publicRightsGranted") is not False):
        raise UnadmittedReaderRoute("Unreviewed figures, rights or lead image")
    old_html=(previous/"estate/index.html").read_text()
    new_html=(candidate/"estate/index.html").read_text()
    pattern=r'<template data-reader-volume="essay--a-sound-must-earn-its-place"[^>]*>.*?</template>'
    old_templates=re.findall(pattern,old_html,re.S)
    new_templates=re.findall(pattern,new_html,re.S)
    if (len(old_templates)!=1 or len(new_templates)!=1 or
        new_html.replace(new_templates[0],old_templates[0],1)!=old_html):
        raise UnadmittedReaderRoute("Other Reader volumes were changed")
    t=new_templates[0]
    plate=t.find('data-source-illustration-id="architectural-plate"')
    photo=t.find('data-source-illustration-id="night-photograph"')
    p2=t.find('data-source-block="a-sound-must-earn-its-place.p2"')
    p3=t.find('data-source-block="a-sound-must-earn-its-place.p3"')
    p8=t.find('data-source-block="a-sound-must-earn-its-place.p8"')
    p9=t.find('data-source-block="a-sound-must-earn-its-place.p9"')
    audio=t.find('data-press-media="satzfunk-csound-kino-a-b"')
    if (not (0<=p2<plate<p3<p8<photo<p9<audio) or
        t.count('<satzfunk-player compact')!=2 or
        t.count('data-source-illustration-id="architectural-plate"')!=1 or
        t.count('data-source-illustration-id="night-photograph"')!=1 or
        'data-source-sha256="'+APPROVED_KINO_COMPOSITION_V167_SOURCE_SHA+'"' not in t):
        raise UnadmittedReaderRoute("Incorrect Kino source figure placement or A/B preservation")
    old={p.relative_to(previous).as_posix():p for p in previous.rglob('*') if p.is_file()}
    new={p.relative_to(candidate).as_posix():p for p in candidate.rglob('*') if p.is_file()}
    added={APPROVED_KINO_COMPOSITION_V167_RECEIPT_PATH}
    changed={'estate/index.html':APPROVED_KINO_COMPOSITION_V167_INDEX_SHA,
             APPROVED_KINO_COMPOSITION_V167_MANIFEST_PATH:APPROVED_KINO_COMPOSITION_V167_MANIFEST_SHA,
             APPROVED_KINO_COMPOSITION_V167_RECEIPT_PATH:APPROVED_KINO_COMPOSITION_V167_RECEIPT_SHA}
    if set(new)-set(old)!=added or set(old)-set(new):
        raise UnadmittedReaderRoute("Unexpected v167 file additions/removals")
    for rel,path in new.items():
        if path.is_symlink():raise UnadmittedReaderRoute("Symlink in stage artifact")
        if rel=='source-lock.json':continue
        expected_sha=changed.get(rel)
        if expected_sha:
            if sha256(path)!=expected_sha:raise UnadmittedReaderRoute("Altered v167 change: "+rel)
        elif sha256(path)!=sha256(old[rel]):
            raise UnadmittedReaderRoute("V167 changed unrelated Reader, image or audio: "+rel)
    return {**inherited,**changed}


class ReaderProvenanceGate:
    """The running server must not serve any unreviewed book HTML or engine.

    Existing accepted v140 Reader pages are grandfathered byte-for-byte.
    New or revised pages require a future reviewed source/production comparison
    AND a new pinned accepted baseline; they cannot opt in from the stage tree.
    """

    def __init__(self, baseline: Path, current: Path):
        self.baseline = baseline.resolve(strict=True)
        self.current = current.resolve(strict=True)
        if (self.baseline.name != ACCEPTED_STAGE or
                sha256(self.baseline / "source-lock.json") != ACCEPTED_SOURCE_LOCK_SHA256 or
                sha256(self.baseline / "estate/index.html") != ACCEPTED_BOOKSHELF_SHA256):
            raise UnadmittedReaderRoute("Unrecognized accepted Reader baseline")
        for name, expected in STAGE_READER.items():
            asset = self.baseline / "estate/assets/linotype" / name
            if sha256(asset) != expected:
                raise UnadmittedReaderRoute("Changed accepted Reader engine: " + name)
        inventory_digest, self.runtime_assets = linotype_inventory(self.baseline)
        if inventory_digest != ACCEPTED_LINOTYPE_TREE_SHA256:
            raise UnadmittedReaderRoute("Changed complete Linotype Reader asset inventory")
        self.approved_essay = approved_essay_files(self.baseline, self.current)
        if self.current.name == APPROVED_FIGURE_RELEASE:
            self.approved_essay = approved_balanced_essay_files(self.baseline, self.current)
        if self.current.name == APPROVED_WEB_READER_RELEASE:
            self.approved_essay = approved_web_reader_inset_files(self.baseline, self.current)
        if self.current.name == APPROVED_VERGIL_AUDITION_RELEASE:
            self.approved_essay = approved_private_vergil_audition_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_VERGIL_LISTENING_RELEASE:
            self.approved_essay = approved_private_vergil_listening_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_SELF_OUT_LOUD_RELEASE:
            self.approved_essay = approved_self_out_loud_essay_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_SPECIMEN_RELEASE:
            self.approved_essay = approved_typographic_specimen_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_NESTED_RELEASE:
            self.approved_essay = approved_nested_measure_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_FLUID_RELEASE:
            self.approved_essay = approved_fluid_nested_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_SPREAD_RELEASE:
            self.approved_essay = approved_semantic_spread_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_ARCHIVE_RELEASE:
            self.approved_essay = approved_editorial_archive_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_RELEASE:
            self.approved_essay = approved_kino_interlude_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_SAMPLER_RELEASE:
            self.approved_essay = approved_kino_sampler_v2_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_EAR_RELEASE:
            self.approved_essay = approved_kino_ear_echo_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_GROOVE_RELEASE:
            self.approved_essay = approved_kino_groove_v157_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_ATMOSPHERE_RELEASE:
            self.approved_essay = approved_kino_atmosphere_v158_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_MIDNIGHT_RELEASE:
            self.approved_essay = approved_kino_midnight_v159_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_PRESS_SOUND_V160_RELEASE:
            self.approved_essay = approved_press_sound_v160_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_GOVERNANCE_V161_RELEASE:
            self.approved_essay = approved_governance_v161_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_GOVERNANCE_V162_RELEASE:
            self.approved_essay = approved_governance_v162_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_GOVERNANCE_V163_RELEASE:
            self.approved_essay = approved_governance_v163_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE:
            self.approved_essay = approved_governance_social_v164_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_SOUND_CRAFT_V165_RELEASE:
            self.approved_essay = approved_sound_craft_v165_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_FIGURES_V166_RELEASE:
            self.approved_essay = approved_kino_figures_v166_files(
                self.baseline, self.current)
        if self.current.name == APPROVED_KINO_COMPOSITION_V167_RELEASE:
            self.approved_essay = approved_kino_composition_v167_files(
                self.baseline, self.current)

    def check(self, raw_url: str) -> None:
        rel = normalized_request_path(raw_url)
        if rel.startswith("private-auditions/"):
            target = self.current / rel
            if (self.current.name in (
                        APPROVED_VERGIL_LISTENING_RELEASE,
                        APPROVED_SELF_OUT_LOUD_RELEASE,
                        APPROVED_SPECIMEN_RELEASE,
                        APPROVED_NESTED_RELEASE,
                        APPROVED_FLUID_RELEASE,
                        APPROVED_SPREAD_RELEASE,
                        APPROVED_ARCHIVE_RELEASE,
                        APPROVED_KINO_RELEASE,
                            APPROVED_KINO_SAMPLER_RELEASE,
                            APPROVED_KINO_EAR_RELEASE,
                            APPROVED_KINO_GROOVE_RELEASE,
                            APPROVED_KINO_ATMOSPHERE_RELEASE,
                            APPROVED_KINO_MIDNIGHT_RELEASE,
                            APPROVED_PRESS_SOUND_V160_RELEASE,
                            APPROVED_GOVERNANCE_V161_RELEASE,
                            APPROVED_GOVERNANCE_V162_RELEASE,
                            APPROVED_GOVERNANCE_V163_RELEASE,
                            APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE,
                            APPROVED_SOUND_CRAFT_V165_RELEASE,
                            APPROVED_KINO_FIGURES_V166_RELEASE, APPROVED_KINO_COMPOSITION_V167_RELEASE)
                    and rel == APPROVED_VERGIL_LISTENING_ROUTE):
                if (not target.is_file() or target.is_symlink()
                        or git_blob_sha1(target) != APPROVED_VERGIL_LISTENING_GIT_BLOB):
                    raise UnadmittedReaderRoute("Altered private listening page")
                return
            expected = (APPROVED_VERGIL_AUDITION_ASSETS.get(rel)
                        if self.current.name in (
                            APPROVED_VERGIL_AUDITION_RELEASE,
                            APPROVED_VERGIL_LISTENING_RELEASE,
                            APPROVED_SELF_OUT_LOUD_RELEASE,
                            APPROVED_SPECIMEN_RELEASE,
                            APPROVED_NESTED_RELEASE,
                            APPROVED_FLUID_RELEASE,
                            APPROVED_SPREAD_RELEASE,
                            APPROVED_ARCHIVE_RELEASE,
                            APPROVED_KINO_RELEASE,
                            APPROVED_KINO_SAMPLER_RELEASE,
                            APPROVED_KINO_EAR_RELEASE,
                            APPROVED_KINO_GROOVE_RELEASE,
                            APPROVED_KINO_ATMOSPHERE_RELEASE,
                            APPROVED_KINO_MIDNIGHT_RELEASE,
                            APPROVED_PRESS_SOUND_V160_RELEASE,
                            APPROVED_GOVERNANCE_V161_RELEASE,
                            APPROVED_GOVERNANCE_V162_RELEASE,
                            APPROVED_GOVERNANCE_V163_RELEASE,
                            APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE,
                            APPROVED_SOUND_CRAFT_V165_RELEASE,
                            APPROVED_KINO_FIGURES_V166_RELEASE, APPROVED_KINO_COMPOSITION_V167_RELEASE)
                        else None)
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target) != expected:
                raise UnadmittedReaderRoute("Unknown or altered private audition asset")
            return
        if self.current.name in (APPROVED_GOVERNANCE_SOCIAL_V164_RELEASE, APPROVED_SOUND_CRAFT_V165_RELEASE, APPROVED_KINO_FIGURES_V166_RELEASE, APPROVED_KINO_COMPOSITION_V167_RELEASE) and rel.startswith("estate/share/governance/"):
            expected=self.approved_essay.get(rel)
            target=self.current/rel
            if (expected is None or not target.is_file() or target.is_symlink() or sha256(target)!=expected):
                raise UnadmittedReaderRoute("Unreviewed Governance static share artifact: "+rel)
            return
        if self.current.name in (APPROVED_SOUND_CRAFT_V165_RELEASE, APPROVED_KINO_FIGURES_V166_RELEASE, APPROVED_KINO_COMPOSITION_V167_RELEASE) and rel.startswith("estate/media/kino/sound-craft/"):
            expected=self.approved_essay.get(rel)
            target=self.current/rel
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target)!=expected:
                raise UnadmittedReaderRoute("Unreviewed Csound source audition: "+rel)
            return
        if self.current.name in (APPROVED_KINO_FIGURES_V166_RELEASE, APPROVED_KINO_COMPOSITION_V167_RELEASE) and rel.startswith(
            "estate/essays/a-sound-must-earn-its-place/media/"
        ):
            expected=self.approved_essay.get(rel)
            target=self.current/rel
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target)!=expected:
                raise UnadmittedReaderRoute("Unreviewed sound essay illustration: "+rel)
            return
        # Only the reviewed vector assets may exist under this work folder.
        # In particular, a new standalone index.html is NEVER an allowed
        # alternative Reader, even when the root source volume is admitted.
        if self.approved_essay and rel.startswith(
            "estate/essays/what-makes-a-page-modern/"
        ) and rel not in self.approved_essay:
            if (self.current / rel).exists():
                raise UnadmittedReaderRoute("Unreviewed independent essay route")
        # The editor's new SVG plates have their own pinned source digests;
        # this does not admit the rejected standalone essay HTML route.
        if rel.startswith(APPROVED_ESSAY_ASSET_DIR):
            expected = self.approved_essay.get(rel)
            target = self.current / rel
            if target.exists() and (
                expected is None or not target.is_file() or sha256(target) != expected
            ):
                raise UnadmittedReaderRoute("Unreviewed essay illustration")
        asset_dir = "estate/assets/linotype/"
        if rel.startswith(asset_dir):
            name = rel[len(asset_dir):]
            target = self.current / rel
            if target.exists():
                expected = self.approved_essay.get(rel, self.runtime_assets.get(name))
                if not target.is_file() or expected is None or sha256(target) != expected:
                    raise UnadmittedReaderRoute("Reader runtime changed without production parity: " + name)
        html_path = rel if protected_reader_html(rel) else reader_parent(rel)
        if html_path is None:
            return
        candidate = self.current / html_path
        if not candidate.exists():
            return  # The ordinary HTTP 404 remains authoritative.
        original = self.baseline / html_path
        # The v152 archival decision changes the existing Essays catalogue
        # but never the authored essay route. Admission remains exact-hash
        # and source-lock-bound, not a blanket exemption for nested HTML.
        admitted_catalogue=html_path in ("estate/index.html","estate/essays/index.html")
        if admitted_catalogue and self.approved_essay:
            expected=self.approved_essay.get(html_path)
            if expected is not None and sha256(candidate)==expected:
                return
        if not original.is_file() or sha256(candidate) != sha256(original):
            raise UnadmittedReaderRoute(
                "Unadmitted Reader route: production comparison and Fountain Press source reuse required"
            )

    @staticmethod
    def production_delta() -> dict[str, tuple[str, str]]:
        return {
            name: (prod, STAGE_READER[name])
            for name, prod in PRODUCTION_READER.items()
            if prod != STAGE_READER[name]
        }
