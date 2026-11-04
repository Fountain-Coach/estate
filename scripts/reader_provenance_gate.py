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

    def check(self, raw_url: str) -> None:
        rel = normalized_request_path(raw_url)
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
