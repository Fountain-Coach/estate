"""The existing HTTPS stage transport shares the exact Reader guard with HTTP."""
import tempfile
import threading
import urllib.error
import urllib.request
import unittest
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from serve_shared_shell_preview_https import SecureStageHandler
from reader_provenance_gate import UnadmittedReaderRoute


class FakeAcceptedGate:
    def __init__(self):
        self.requests = []

    def check(self, path):
        self.requests.append(path)
        if "/invented/" in path:
            raise UnadmittedReaderRoute("Not admitted")


class SecureStageReaderGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "estate").mkdir()
        (self.root / "estate/index.html").write_text("Existing Reader page")
        media = self.root / "estate/media/first-readings"
        media.mkdir(parents=True)
        (media / "teatro-vergil-auto-corrected-v2.mp3").write_bytes(b"original-media-bytes")
        (self.root / "estate/invented").mkdir()
        (self.root / "estate/invented/index.html").write_text("new Reader")
        self.gate = FakeAcceptedGate()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(
            SecureStageHandler, root=self.root, personal_works_landing=False,
            reader_gate=self.gate
        ))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def get(self, path, method="GET", headers=None):
        req = urllib.request.Request(
            "http://127.0.0.1:" + str(self.server.server_port) + path,
            headers=headers or {}, method=method
        )
        return urllib.request.urlopen(req, timeout=3)

    def test_html_and_head_use_guard(self):
        for method in ("GET", "HEAD"):
            with self.get("/estate/", method) as response:
                self.assertEqual(response.status, 200)
            with self.assertRaises(urllib.error.HTTPError) as exc:
                self.get("/estate/invented/", method)
            self.assertEqual(exc.exception.code, 403)
            exc.exception.close()
        self.assertIn("/estate/", self.gate.requests)
        self.assertIn("/estate/invented/", self.gate.requests)

    def test_byte_range_uses_same_guard(self):
        path = "/estate/media/first-readings/teatro-vergil-auto-corrected-v2.mp3"
        with self.get(path, headers={"Range": "bytes=2-6"}) as response:
            self.assertEqual(response.status, 206)
            self.assertEqual(response.read(), b"igina")
        self.assertIn(path, self.gate.requests)

    def test_missing_gate_fails_closed(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(
            SecureStageHandler, root=self.root, personal_works_landing=False,
            reader_gate=None
        ))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:" + str(server.server_port) + "/estate/"
            )
            with self.assertRaises(urllib.error.HTTPError) as exc:
                urllib.request.urlopen(req, timeout=3)
            self.assertEqual(exc.exception.code, 403)
            exc.exception.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)
