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

    def check(self, raw_url: str) -> None:
        rel = normalized_request_path(raw_url)
        if rel.startswith("private-auditions/"):
            target = self.current / rel
            if (self.current.name in (
                        APPROVED_VERGIL_LISTENING_RELEASE,
                        APPROVED_SELF_OUT_LOUD_RELEASE,
                        APPROVED_SPECIMEN_RELEASE)
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
                            APPROVED_SPECIMEN_RELEASE)
                        else None)
            if expected is None or not target.is_file() or target.is_symlink() or sha256(target) != expected:
                raise UnadmittedReaderRoute("Unknown or altered private audition asset")
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
        if html_path == "estate/index.html" and self.approved_essay:
            if sha256(candidate) == self.approved_essay[html_path]:
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
