from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote
import mimetypes, re, ssl

ROOT = Path("/home/benedikt/estate-wlan-staging/20260926-semantic")
HOST = "192.168.8.11"
PORT = 8443
DOMAINS = [
    "fountain.coach",
    "governance.fountain.coach",
    "book.fountain.coach",
    "teatro.fountain.coach",
    "midi2.fountain.coach",
    "instruments.fountain.coach",
    "status.fountain.coach",
    "tennis.fountain.coach",
    "benedikt-eickhoff.de",
]
TEXT_TYPES = {".html", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".webmanifest"}

def staging_url(domain, path=""):
    return f"https://{HOST}:{PORT}/{domain}/" + path.lstrip("/")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), fmt % args), flush=True)

    def do_GET(self):
        raw = unquote(self.path.split("?",1)[0].split("#",1)[0])
        if raw == "/fountain-coach-local-wlan-ca.cer":
            data=(ROOT/"fountain-coach-local-wlan-ca.cer").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type","application/x-x509-ca-cert")
            self.send_header("Content-Disposition","attachment; filename=Fountain-Coach-Local-WLAN-CA.cer")
            self.send_header("Content-Length",str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if raw == "/":
            self.send_response(302)
            self.send_header("Location", "/fountain.coach/")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return

        parts = raw.lstrip("/").split("/",1)
        domain = parts[0]
        if domain not in DOMAINS or not (ROOT/domain).exists():
            self.send_error(404)
            return
        sub = parts[1] if len(parts) > 1 else ""
        target = (ROOT/domain/sub).resolve()
        base = (ROOT/domain).resolve()
        if not str(target).startswith(str(base)):
            self.send_error(403)
            return
        if target.is_dir():
            target = target/"index.html"
        if not target.exists() or not target.is_file():
            self.send_error(404)
            return

        data = target.read_bytes()
        ext = target.suffix.lower()
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"

        if ext in TEXT_TYPES:
            text = data.decode("utf-8", "replace")
            for d in DOMAINS:
                text = text.replace(f"https://{d}/", staging_url(d))
                text = text.replace(f"http://{d}/", staging_url(d))
            prefix = f"/{domain}/"
            if ext in {".html", ".svg"}:
                text = re.sub(r'((?:href|src|srcset|action)=["\'])/(?!/)', r'\1' + prefix, text)
                text = re.sub(r'(url\(["\']?)/(?!/)', r'\1' + prefix, text)
            elif ext == ".css":
                text = re.sub(r'(url\(["\']?)/(?!/)', r'\1' + prefix, text)
            data = text.encode("utf-8")

        # Binary media needs byte ranges for browser seek. Text transformations
        # above retain their existing behavior and are never sliced by this path.
        is_audio = ext in {".mp3", ".m4a", ".wav", ".ogg", ".flac", ".aac"}
        requested_range = self.headers.get("Range") if is_audio else None
        if requested_range:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested_range.strip())
            size = len(data)
            valid = bool(match and any(match.groups()) and size)
            if valid:
                first, last = match.groups()
                if first:
                    start = int(first)
                    end = min(int(last), size - 1) if last else size - 1
                else:
                    suffix = int(last)
                    start, end = max(0, size - suffix), size - 1
                    valid = suffix > 0
                valid = valid and 0 <= start <= end < size
            if not valid:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            payload = data[start:end + 1]
            self.send_response(206)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(200)
        if is_audio:
            self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text/") else ""))
        self.send_header("Cache-Control","no-store")
        self.send_header("Content-Length",str(len(data)))
        self.end_headers()
        self.wfile.write(data)

server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("/etc/fountain-store/tls/local-wlan/fullchain.pem", "/etc/fountain-store/tls/local-wlan/privkey.pem")
server.socket = ctx.wrap_socket(server.socket, server_side=True)
server.serve_forever()
