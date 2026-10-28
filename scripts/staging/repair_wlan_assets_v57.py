#!/usr/bin/env python3
"""Apply source-proven static route/asset link corrections to a disposable
owner-WLAN editorial candidate. No outside-host write or publication.
"""
from pathlib import Path
import re,json,hashlib
root=Path("/tmp/fc-editorial-v57-20261028/candidate")
changes={}
for page in sorted(root.rglob("index.html")):
    data=page.read_text(encoding="utf-8",errors="replace")
    new=data
    relative=page.relative_to(root).as_posix()
    if relative.startswith("book/"):
        for old,rep in [
            ('href="/assets/estate-core.css"','href="/book/assets/estate-core.css"'),
            ('src="/assets/estate-core.js"','src="/book/assets/estate-core.js"'),
            ('href="/assets/fountain-coach-logo-transparent.png"','href="/book/assets/fountain-coach-logo-transparent.png"'),
            ('src="/assets/fountain-coach-logo-transparent.png"','src="/book/assets/fountain-coach-logo-transparent.png"'),
        ]:
            new=new.replace(old,rep)
    if relative=="estate/essays/index.html":
        new=new.replace("https://192.168.8.11:8443/fountain.coach/essays/","/estate/essays/")
    if not re.search(r'<link\b[^>]*\brel=["\'](?:shortcut )?icon["\']',new,re.I):
        new=new.replace("</head>",'<link rel="icon" type="image/png" href="/assets/estate-shell-logo.png"></head>',1)
    if data!=new:
        page.write_text(new,encoding="utf-8")
        changes[relative]=[hashlib.sha256(data.encode()).hexdigest(),hashlib.sha256(new.encode()).hexdigest()]
# Public source-owned ground artwork was omitted from the old stage and
# public HTTPS presentation. Its actual upstream Git original is fetched by
# a separate read-only network command and matched to this manifest.
asset=root/"book/assets/ground-live-ulysses-circe-20260809.png"
assert (root/"book/assets/estate-core.css").is_file()
assert (root/"book/assets/estate-core.js").is_file()
assert (root/"book/assets/fountain-coach-logo-transparent.png").is_file()
print("STAGE_LINK_REPAIRS",len(changes),"stale_html_links_removed",
      "192.168.8.11" not in (root/"estate/essays/index.html").read_text(),
      "upstream_art_exists",asset.is_file())
(root.parent/"acceptance/stage-asset-link-delta.json").write_text(
    json.dumps({"stageOnly":True,"sourceOwner":"Fountain-Coach/book-of-reframe",
                "upstreamOriginalAsset":"site/assets/ground-live-ulysses-circe-20260809.png",
                "links":changes},indent=2)+"\n")
