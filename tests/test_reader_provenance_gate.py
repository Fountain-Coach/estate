"""Regress the November 4 invented-Reader incident on the EXISTING preview server."""
import hashlib
import json
import shutil
import threading
import urllib.error
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import reader_provenance_gate as gate
from serve_shared_shell_preview import Handler


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
            patch.object(gate, "ACCEPTED_LINOTYPE_TREE_SHA256", gate.linotype_inventory(self.base)[0]),
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

    def test_new_edition_routes_and_reader_html_outside_essays_are_refused(self):
        for path in ("estate/read/first-readings/index.html",
                     "estate/editions/a/new-chapter.html",
                     "book/chapters/a/index.html",
                     "solstice/editions/first-reading/new.html"):
            put(self.stage, path, "<html>invented reader</html>")
            with self.subTest(path=path), self.assertRaises(gate.UnadmittedReaderRoute):
                self.guard.check("/" + path)

    def test_legacy_reader_compositor_asset_cannot_be_swapped(self):
        rel = "estate/assets/linotype/book.js"
        original = put(self.base, rel, "accepted older Linotype book.js")
        candidate = put(self.stage, rel, original.read_text())
        with patch.object(gate, "ACCEPTED_LINOTYPE_TREE_SHA256",
                          gate.linotype_inventory(self.base)[0]):
            refreshed = gate.ReaderProvenanceGate(self.base, self.stage)
            self.assertIsNone(refreshed.check("/" + rel))
            candidate.write_text("invented new compositor")
            with self.assertRaisesRegex(gate.UnadmittedReaderRoute, "runtime changed"):
                refreshed.check("/" + rel)
            put(self.stage, "estate/assets/linotype/invented-reader.js", "reader")
            with self.assertRaises(gate.UnadmittedReaderRoute):
                refreshed.check("/estate/assets/linotype/invented-reader.js")

    def test_unreviewed_audio_module_is_refused(self):
        put(self.stage, "estate/assets/linotype/teatro-vergil-hearing.mjs", "another module")
        with self.assertRaisesRegex(gate.UnadmittedReaderRoute, "runtime changed"):
            self.guard.check("/estate/assets/linotype/teatro-vergil-hearing.mjs")

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

    def test_live_http_handler_rejects_unadmitted_reader_get_and_head(self):
        put(self.stage, "estate/essays/new-reader/index.html", "<html>unadmitted</html>")
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(
            Handler, root=self.stage, personal_works_landing=False,
            reader_gate=self.guard))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = "http://127.0.0.1:" + str(server.server_port)
            with urllib.request.urlopen(base + "/estate/editions/essays-continuing/", timeout=3) as r:
                self.assertEqual(r.status, 200)
            for method in ("GET", "HEAD"):
                request = urllib.request.Request(
                    base + "/estate/essays/new-reader/", method=method)
                with self.subTest(method=method), self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(request, timeout=3)
                self.assertEqual(error.exception.code, 403)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


    def test_exact_new_essay_admission_and_runtime_mutation_refusal(self):
        candidate = Path(self.temp.name) / gate.APPROVED_ESSAY_RELEASE
        shutil.copytree(self.base, candidate)
        index = put(candidate, "estate/index.html", "<html>Accepted real v140 Reader plus source volume</html>")
        app = put(candidate, "estate/assets/linotype/reading-first-app.js",
                  "Original v140 Reader app, same algorithm, six essays")
        images = {}
        for name in gate.APPROVED_ESSAY_ASSETS:
            namepath = gate.APPROVED_ESSAY_ASSET_DIR + name
            images[namepath] = digest(put(candidate, namepath, "<svg>" + name + "</svg>"))
        files = {
            "estate/index.html": digest(index),
            "estate/assets/linotype/reading-first-app.js": digest(app),
            **images,
        }
        admission = dict(
            schema="fountain.press.existing-reader.essay-addition.v1",
            sourceOwner="Fountain-Coach/fountain.coach",
            sourceCommit=gate.APPROVED_ESSAY_SOURCE_COMMIT,
            sourcePDFSHA256=gate.APPROVED_ESSAY_PDF_SHA256,
            predecessor=gate.ACCEPTED_STAGE,
            release=gate.APPROVED_ESSAY_RELEASE,
            stageOnly=True, publicReleased=False, fountainStoreAdmitted=False,
            readerRuntimeUnchangedExceptGalleryMembership=True,
            notAnAlternateReader=True, fileSHA256=files,
        )
        original = json.loads((self.base / "source-lock.json").read_text())
        source_lock = put(candidate, "source-lock.json", json.dumps({
            **original, "modernPageExistingReaderAdmission": admission
        }, ensure_ascii=False, indent=2) + "\n")
        patches = [
            patch.object(gate, "APPROVED_ESSAY_LOCK_SHA256", digest(source_lock)),
            patch.object(gate, "APPROVED_ESSAY_INDEX_SHA256", digest(index)),
            patch.object(gate, "APPROVED_ESSAY_APP_SHA256", digest(app)),
        ]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)
        approved = gate.ReaderProvenanceGate(self.base, candidate)
        self.assertEqual(len(approved.approved_essay), 15)
        for path in ("/estate/", "/estate/editions/essays-continuing/",
                     "/estate/assets/linotype/reading-first-app.js",
                     "/estate/essays/what-makes-a-page-modern/assets/question.svg"):
            self.assertIsNone(approved.check(path))
        self.assertIsNone(approved.check("/estate/essays/what-makes-a-page-modern/"))
        # A previously absent standalone Reader and any replaced illustration
        # must still fail even after the new SOURCE has been admitted.
        put(candidate, "estate/essays/what-makes-a-page-modern/index.html",
            "<html>another invented reader</html>")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            approved.check("/estate/essays/what-makes-a-page-modern/")
        (candidate / "estate/essays/what-makes-a-page-modern/index.html").unlink()
        put(candidate, gate.APPROVED_ESSAY_ASSET_DIR+"question.svg", "<svg>tampered</svg>")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            approved.check("/estate/essays/what-makes-a-page-modern/assets/question.svg")
        put(candidate, gate.APPROVED_ESSAY_ASSET_DIR+"question.svg", "<svg>question.svg</svg>")
        put(candidate, "estate/assets/linotype/reading-first-app.js", "new runtime")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            approved.check("/estate/assets/linotype/reading-first-app.js")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            gate.ReaderProvenanceGate(self.base, candidate)
        put(candidate, "estate/assets/linotype/reading-first-app.js",
            "Original v140 Reader app, same algorithm, six essays")
        put(candidate, "estate/essays/what-makes-a-page-modern/assets/new-reader.js", "unauthorized")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            gate.ReaderProvenanceGate(self.base, candidate)

    def test_v143_exact_balanced_figures_admission_and_refusal(self):
        # Create two source-bound release snapshots, each independently copied,
        # as proof that the corrected figure does not replace the Reader.
        root = Path(self.temp.name)
        previous = root / gate.APPROVED_ESSAY_RELEASE
        candidate = root / gate.APPROVED_FIGURE_RELEASE
        shutil.copytree(self.base, previous)
        prior_index = put(previous, "estate/index.html", "<html>v142 original Reader</html>")
        prior_app = put(previous, "estate/assets/linotype/reading-first-app.js",
                        "original Reader with the sixth essay")
        prior_images = {}
        for name in gate.APPROVED_ESSAY_ASSETS:
            loc = gate.APPROVED_ESSAY_ASSET_DIR + name
            prior_images[loc] = digest(put(previous, loc, "<svg>old " + name + "</svg>"))
        prior_files = {
            "estate/index.html": digest(prior_index),
            "estate/assets/linotype/reading-first-app.js": digest(prior_app),
            **prior_images,
        }
        prev_lock_data = json.loads((self.base / "source-lock.json").read_text())
        prev_lock_data["modernPageExistingReaderAdmission"] = {
            "schema": "fountain.press.existing-reader.essay-addition.v1",
            "sourceOwner": "Fountain-Coach/fountain.coach",
            "sourceCommit": gate.APPROVED_ESSAY_SOURCE_COMMIT,
            "sourcePDFSHA256": gate.APPROVED_ESSAY_PDF_SHA256,
            "predecessor": gate.ACCEPTED_STAGE,
            "release": gate.APPROVED_ESSAY_RELEASE,
            "stageOnly": True,
            "publicReleased": False,
            "fountainStoreAdmitted": False,
            "readerRuntimeUnchangedExceptGalleryMembership": True,
            "notAnAlternateReader": True,
            "fileSHA256": prior_files,
        }
        prev_lock = put(previous, "source-lock.json",
                        json.dumps(prev_lock_data, ensure_ascii=False, indent=2) + "\n")

        shutil.copytree(previous, candidate)
        new_index = put(candidate, "estate/index.html", "<html>v143 same Reader, corrected figures</html>")
        revised_images = {}
        for name in gate.APPROVED_ESSAY_ASSETS:
            loc = gate.APPROVED_ESSAY_ASSET_DIR + name
            revised_images[loc] = digest(put(candidate, loc, "<svg>balanced " + name + "</svg>"))
        revised_files = {"estate/index.html": digest(new_index), **revised_images}
        new_lock_data = json.loads(prev_lock.read_text())
        new_lock_data["modernPageFigureBalanceAdmission"] = {
            "schema": "fountain.press.figure-balance.existing-reader.v1",
            "sourceOwner": "Fountain-Coach/fountain.coach",
            "sourceCommit": gate.APPROVED_FIGURE_SOURCE_COMMIT,
            "sourcePDFSHA256": gate.APPROVED_ESSAY_PDF_SHA256,
            "predecessor": gate.APPROVED_ESSAY_RELEASE,
            "release": gate.APPROVED_FIGURE_RELEASE,
            "stageOnly": True,
            "publicReleased": False,
            "fountainStoreAdmitted": False,
            "readerRuntimeUnchanged": True,
            "originalManuscriptUnchanged": True,
            "visibleFrameAlignedToText": True,
            "fileSHA256": revised_files,
        }
        lock = put(candidate, "source-lock.json",
                   json.dumps(new_lock_data, ensure_ascii=False, indent=2) + "\n")
        expected = {name[len(gate.APPROVED_ESSAY_ASSET_DIR):]: value
                    for name, value in revised_images.items()}
        constants = [
            patch.object(gate, "APPROVED_ESSAY_LOCK_SHA256", digest(prev_lock)),
            patch.object(gate, "APPROVED_ESSAY_INDEX_SHA256", digest(prior_index)),
            patch.object(gate, "APPROVED_ESSAY_APP_SHA256", digest(prior_app)),
            patch.object(gate, "APPROVED_FIGURE_LOCK_SHA256", digest(lock)),
            patch.object(gate, "APPROVED_FIGURE_HTML_SHA256", digest(new_index)),
            patch.object(gate, "APPROVED_FIGURE_ASSET_SHA256", expected),
        ]
        for p in constants:
            p.start()
            self.addCleanup(p.stop)
        original = gate.ReaderProvenanceGate(self.base, previous)
        self.assertEqual(len(original.approved_essay), 15)
        accepted = gate.ReaderProvenanceGate(self.base, candidate)
        self.assertEqual(len(accepted.approved_essay), 15)
        for route in ("/estate/", "/estate/editions/essays-continuing/",
                      "/estate/assets/linotype/reading-first-app.js",
                      "/estate/essays/what-makes-a-page-modern/assets/question.svg"):
            self.assertIsNone(accepted.check(route))
        put(candidate, gate.APPROVED_ESSAY_ASSET_DIR+"question.svg", "<svg>tampered</svg>")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            accepted.check("/estate/essays/what-makes-a-page-modern/assets/question.svg")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            gate.ReaderProvenanceGate(self.base, candidate)
        put(candidate, gate.APPROVED_ESSAY_ASSET_DIR+"question.svg",
            "<svg>balanced question.svg</svg>")
        put(candidate, "estate/essays/what-makes-a-page-modern/index.html",
            "<html>alternate reader</html>")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            accepted.check("/estate/essays/what-makes-a-page-modern/")
        with self.assertRaises(gate.UnadmittedReaderRoute):
            gate.ReaderProvenanceGate(self.base, candidate)

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
                             {"reading-first-app.js", "teatro-vergil-hearing.mjs",
                              "vergil-prologue-hearing.mjs"})


if __name__ == "__main__":
    unittest.main()
