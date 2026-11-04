"""Fail-closed guard for the existing EstateShell WLAN preview Reader routes.

A copied/rewritten HTML page is not an admitted Fountain Press Reader.
The accepted v140 reader and public production asset comparison are pinned
below. No staged source-lock or newly copied page can whitelist itself.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ACCEPTED_STAGE = "shared-shell-20261103-v140-same-folio-return"
ACCEPTED_SOURCE_LOCK_SHA256 = "d263837865d282f495de905e3c43833be3b118faf0332529f61564b137bfaebc"
ACCEPTED_BOOKSHELF_SHA256 = "69e656346b219be35c030e437100e72338f54d3a70abecbe6030971773cb1c01"

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

    def check(self, raw_url: str) -> None:
        rel = normalized_request_path(raw_url)
        asset_dir = "estate/assets/linotype/"
        if rel.startswith(asset_dir):
            name = rel[len(asset_dir):]
            if name in STAGE_READER:
                target = self.current / rel
                if target.exists() and sha256(target) != STAGE_READER[name]:
                    raise UnadmittedReaderRoute("Reader runtime changed without production parity: " + name)
        html_path = rel if protected_reader_html(rel) else reader_parent(rel)
        if html_path is None:
            return
        candidate = self.current / html_path
        if not candidate.exists():
            return  # The ordinary HTTP 404 remains authoritative.
        original = self.baseline / html_path
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
