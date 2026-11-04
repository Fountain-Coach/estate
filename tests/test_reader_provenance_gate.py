"""Regress the November 4 invented-Reader incident on the EXISTING preview server."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import reader_provenance_gate as gate


def put(root, rel, value):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReaderProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.actual_stage_witness = dict(gate.STAGE_READER)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.base = root / "accepted-v140"
        self.stage = root / "candidate-v141"
        self.base.mkdir()
        self.stage.mkdir()
        self.lock = put(self.base, "source-lock.json", '{"status":"WLAN-PREVIEW-NOT-PUBLIC"}')
        self.home = put(self.base, "estate/index.html", "<html>One established Reader</html>")
        self.known = "estate/editions/essays-continuing/index.html"
        put(self.base, self.known, "<html>Source-bound edition</html>")
        put(self.stage, self.known, "<html>Source-bound edition</html>")
        put(self.stage, "estate/index.html", self.home.read_text())
        originals = {}
        for name in gate.PRODUCTION_READER:
            rel = "estate/assets/linotype/" + name
            original = put(self.base, rel, "accepted=" + name)
            put(self.stage, rel, original.read_text())
            originals[name] = digest(original)
        self.patches = [
            patch.object(gate, "ACCEPTED_STAGE", "accepted-v140"),
            patch.object(gate, "ACCEPTED_SOURCE_LOCK_SHA256", digest(self.lock)),
            patch.object(gate, "ACCEPTED_BOOKSHELF_SHA256", digest(self.home)),
            patch.object(gate, "STAGE_READER", originals),
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)
        self.guard = gate.ReaderProvenanceGate(self.base, self.stage)

    def test_existing_source_exact_pages_and_assets_remain_usable(self):
        for url in ("/estate/", "/estate/editions/essays-continuing/",
                    "/estate/assets/linotype/reading-first-app.js",
                    "/teatro/experiments/"):
            self.assertIsNone(self.guard.check(url))

    def test_new_invented_book_reader_is_refused(self):
        put(self.stage, "estate/essays/what-makes-a-page-modern/index.html",
            '<body class="book-app"><script src="/estate/assets/linotype/book.js"></script></body>')
        with self.assertRaisesRegex(gate.UnadmittedReaderRoute, "Unadmitted"):
            self.guard.check("/estate/essays/what-makes-a-page-modern/")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            self.guard.check("/estate/essays/what-makes-a-page-modern/index.html")
        put(self.stage, "estate/essays/what-makes-a-page-modern/assets/proof.svg", "<svg/>")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            self.guard.check("/estate/essays/what-makes-a-page-modern/assets/proof.svg")

    def test_similar_html_using_the_right_reader_still_requires_admission(self):
        put(self.stage, "estate/essays/another/index.html",
            '<script src="/estate/assets/linotype/reading-first-app.js"></script>')
        with self.assertRaises(gate.UnadmittedReaderRoute):
            self.guard.check("/estate/essays/another/")

    def test_mutated_existing_reader_and_runtime_are_refused(self):
        put(self.stage, self.known, "<html>A new reader, same pathname</html>")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            self.guard.check("/estate/editions/essays-continuing/")
        put(self.stage, "estate/assets/linotype/reading-first-app.js", "another reader")
        with self.assertRaisesRegex(gate.UnadmittedReaderRoute, "runtime changed"):
            self.guard.check("/estate/assets/linotype/reading-first-app.js")

    def test_unrelated_staging_routes_remain_allowed(self):
        put(self.stage, "teatro/example/index.html", "<html>Teatro retained</html>")
        self.assertIsNone(self.guard.check("/teatro/example/"))
        self.assertIsNone(self.guard.check("/nonexistent/"))
        self.assertIsNone(self.guard.check("/estate/essays/missing/"))

    def test_forged_baseline_cannot_admit_new_reader(self):
        put(self.base, "source-lock.json", '{"changed":true}')
        with self.assertRaisesRegex(gate.UnadmittedReaderRoute, "Unrecognized"):
            gate.ReaderProvenanceGate(self.base, self.stage)

    def test_encoded_path_traversal_is_refused(self):
        for path in ("/estate/%2e%2e/editions/new/", "/estate/essays/x/../../other/"):
            with self.assertRaises(gate.UnadmittedReaderRoute):
                self.guard.check(path)

    def test_production_reader_asset_difference_is_explicit(self):
        with patch.object(gate, "STAGE_READER", self.actual_stage_witness):
            self.assertEqual(set(gate.ReaderProvenanceGate.production_delta()),
                             {"reading-first-app.js"})


if __name__ == "__main__":
    unittest.main()
