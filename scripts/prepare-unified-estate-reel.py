#!/usr/bin/env python3
"""Capture nine *published* estate entrances and project one identical reel.

This creates a disposable LAN proof, not a source owner, domain release, or
archive permission. The rendered pages retain their existing HTML and styles.
Only the top navigation and preview asset links change.
"""
from __future__ import annotations

import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

HOSTS = {
    "estate": "https://fountain.coach/",
    "book": "https://book.fountain.coach/",
    "governance": "https://governance.fountain.coach/",
    "midi2": "https://midi2.fountain.coach/",
    "instruments": "https://instruments.fountain.coach/",
    "status": "https://status.fountain.coach/",
    "teatro": "https://teatro.fountain.coach/",
    "pointer": "https://benedikt-eickhoff.de/",
    "solstice": "https://works.benedikt-eickhoff.de/solstice/",
}
STAGE = "http://192.168.8.50:8198/"
RADIO = "http://192.168.8.50:8194/"
NAV_RE = re.compile(r'(<nav\b[^>]*class="[^"]*\bestate-nav\b[^"]*"[^>]*>).*?(</nav>)', re.S)
REF_RE = re.compile(r'(?P<pre>\b(?:href|src)=)(?P<quote>["\x27])(?P<value>.*?)(?P=quote)', re.S)
CSS_REF = re.compile(r'url\(\s*[\x27"]?(.*?)[\x27"]?\s*\)', re.I)

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in {"img", "script"} and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("href") and any(t in (a.get("rel") or "") for t in ("stylesheet","icon","preload","modulepreload")):
            self.assets.append(a["href"])

def get(url):
    r=Request(url,headers={"User-Agent":"FountainCoach-Canonical-Reel-Audit/1.0"})
    with urlopen(r,timeout=12) as response:
        if response.status!=200 or response.url!=url:
            raise ValueError("source changed/redirected "+url)
        data=response.read(12000000)
        if len(data)>=12000000:
            raise ValueError("too-large asset "+url)
        return data

def make_nav(identity, entries):
    pieces=[]
    for entry in entries:
        id=entry["id"]
        url=RADIO if id=="satzfunk" else STAGE+id+"/"
        curr=' aria-current="page"' if identity==id else ""
        path=escape(entry["path"],quote=True)
        label=escape(entry["label"])
        pieces.append(
            '<a class="estate-icon" data-estate-id="'+id+'" href="'+url+'"'
            ' aria-label="'+label+'"'+curr+'><svg class="estate-symbol" viewBox="0 0 24 24"'
            ' aria-hidden="true"><path d="'+path+'"/></svg><span>'+label+'</span></a>')
    # The existing Info action stays at the end of the reel and points to the current document.
    pieces.append('<a class="estate-icon estate-info" href="#footer" aria-label="Info">'
                  '<svg viewBox="0 0 24 24" class="estate-symbol" aria-hidden="true">'
                  '<circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor"/>'
                  '<path d="M12 8.5v.1m0 3v4" fill="none" stroke="currentColor"/></svg>'
                  '<span>Info</span></a>')
    return "".join(pieces)

def transform(html, identity, entries, public):
    if html.count("estate-nav") < 1:
        raise ValueError("missing public estate navigation on "+identity)
    # Preserve original non-navigation links (the whole site remains live on the web).
    def anchor(m):
        tag=m.group(0)
        def rewrite(a):
            u=a.group("value")
            if not u or u.startswith(("#","mailto:","tel:","javascript:","http:","https:","data:")):
                return a.group(0)
            return a.group("pre")+a.group("quote")+urljoin(public,u)+a.group("quote")
        return REF_RE.sub(rewrite,tag)
    html=re.sub(r'<a\b[^>]*>',anchor,html)
    def nav(m):
        opening=m.group(1).replace("estate-nav", "estate-nav",1)
        return opening+make_nav(identity,entries)+m.group(2)
    html,n=NAV_RE.subn(nav,html)
    if n!=1:
        raise ValueError("expected unique estate-nav, found "+str(n)+" at "+identity)
    # Source page metadata and original work stay intact. This is clearly a WLAN preview.
    html=html.replace("<head>","<head>\n<meta name=\"robots\" content=\"noindex,nofollow\">"
                      '<meta name="fountain:local-reel-projection" content="2026-10-21">',1)
    html=html.replace("<html ", '<html data-reel-preview-identity="'+identity+'" ',1)
    # Existing estate-core.js recognizes public domains, not an IP: restore correct
    # active marking only in the disposable proof after original scripts have run.
    html=html.replace("</body>",
      '<script>document.addEventListener("DOMContentLoaded",()=>{'
      'for(const a of document.querySelectorAll(".estate-nav a[data-estate-id]")){'
      'if(a.dataset.estateId===document.documentElement.dataset.reelPreviewIdentity)'
      'a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");}'
      '});</script></body>',1)
    assert html.count('data-estate-id="satzfunk"')==1
    assert len(re.findall(r'data-estate-id="([^"]+)"',NAV_RE.search(html).group()))==len(entries)
    return html

def local_asset(public,raw):
    if not raw or raw.startswith(("data:","#","blob:","javascript:")):
        return None
    full=urljoin(public,raw)
    if urlparse(full).netloc!=urlparse(public).netloc:
        return None
    pathname=urlparse(full).path
    base=urlparse(public).path
    rel=pathname[len(base):] if pathname.startswith(base) else pathname.lstrip("/")
    if not rel or ".." in Path(rel).parts or not rel.startswith(("assets/","favicon.","site.")):
        return None
    return (full,rel)

def capture(identity,public,entries,root):
    raw=get(public)
    source=raw.decode("utf-8")
    dest=root/identity
    dest.mkdir(parents=True)
    html=transform(source,identity,entries,public)
    parser=Assets()
    parser.feed(source)
    queue=list(parser.assets)
    mapping={}
    copied=[]
    seen=set()
    while queue and len(copied)<65:
        item=queue.pop(0)
        asset=local_asset(public,item)
        if not asset:
            continue
        url,rel=asset
        if url in seen:
            continue
        seen.add(url)
        try:
            data=get(url)
        except Exception as e:
            # Only optional assets may fail; stylesheet and script must resolve.
            if rel.endswith((".css",".js")):
                raise
            continue
        target=dest/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():
            raise ValueError("asset name collision "+str(target))
        target.write_bytes(data)
        copied.append({"path":rel,"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)})
        mapping[item]="/"+identity+"/"+rel
        if rel.endswith(".css"):
            css=data.decode("utf-8","replace")
            queue.extend(x.strip().strip("'\\"") for x in CSS_REF.findall(css) if x)
    # Turn root-absolute assets into corresponding scoped preview paths; relative
    # assets work naturally at /<id>/. Internal anchor links remain public.
    for original,new in mapping.items():
        if original.startswith("/"):
            html=html.replace('href="'+original+'"','href="'+new+'"')
            html=html.replace('src="'+original+'"','src="'+new+'"')
            html=html.replace("href='"+original+"'","href='"+new+"'")
            html=html.replace("src='"+original+"'","src='"+new+"'")
    (dest/"index.html").write_text(html)
    return {"identity":identity,"public":public,
            "sourceSHA256":hashlib.sha256(raw).hexdigest(),
            "copiedAssets":copied,"htmlSHA256":hashlib.sha256(html.encode()).hexdigest(),
            "reelEntries":[e["id"] for e in entries]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--release",type=Path,required=True)
    args=p.parse_args()
    if args.release.exists():
        raise SystemExit("Refusing overwrite")
    if args.release.parent.name!="releases" or args.release.parent.parent.name!="estate-unified-reel-staging":
        raise SystemExit("Refusing non-staging target")
    manifest=json.loads(args.manifest.read_text())
    assert manifest["schema"]=="fountain.estate.canonical-reel.v1"
    entries=manifest["entries"]
    assert len(entries)==10 and len({e["id"] for e in entries})==10
    args.release.mkdir(parents=True)
    out=[]
    for ident,public in HOSTS.items():
        out.append(capture(ident,public,entries,args.release))
        print("CAPTURED",ident,"assets",len(out[-1]["copiedAssets"]),flush=True)
    lock={"schema":"fountain.estate.unified-reel-preview.v1",
          "origin":"actual live HTTPS pages captured individually",
          "canonicalManifestSHA256":hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
          "sites":out,"localReel":STAGE,"privateArchive":RADIO,
          "privateMediaCopied":False,"publicationChanged":False}
    (args.release/"capture-lock.json").write_text(json.dumps(lock,indent=2)+"\n")
    print(json.dumps({"staged":len(out),"identities":len(entries),
                      "status":"LOCAL_ONLY","root":str(args.release)},indent=2))
if __name__=="__main__":
    main()
