#!/usr/bin/env python3
"""Build one source-preserving common shell against live public owner pages.

Copies only publicly served assets to disposable staging. Never mirrors private
Satzfunk, mutates public DNS, or authorizes Reframe Bookshelf to release to web.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,sys,re
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
sys.path.insert(0,str(Path(__file__).parent))
from estate_shell import manifest,contract,project,VERSION

SITES={
 "estate": ("https://fountain.coach/", ""),
 "teatro": ("https://teatro.fountain.coach/", ""),
 "solstice": ("https://works.benedikt-eickhoff.de/solstice/editions/first-reading/","solstice/")
}
STAGE_BINDINGS = {
 "estate": "http://192.168.8.50:8200/estate/",
 "teatro": "http://192.168.8.50:8200/teatro/",
 "solstice": "http://192.168.8.50:8200/solstice/editions/first-reading/",
 "satzfunk": "https://satzfunk.fountain.coach/",
 "works": "http://192.168.8.50:8200/works/"
}
MAX_COPY=70*1024*1024
def get(url):
 req=Request(url,headers={"User-Agent":"FountainCoach-EstateShell-Staging/1.0"})
 with urlopen(req,timeout=17) as r:
  if r.status!=200 or r.url!=url:raise RuntimeError("Unexpected public response "+url)
  data=r.read(18*1024*1024)
  if len(data)>=18*1024*1024:raise RuntimeError("asset size limit "+url)
  return data

def build(output,manifest_path):
 if output.exists():raise RuntimeError("refuse overwrite, keep rollback snapshot")
 m=manifest(manifest_path)
 output.mkdir(parents=True)
 (output/"assets").mkdir()
 root=manifest_path.parent.parent
 css=root/"shell/estate-shell.css";logo=root/"shell/assets/estate-shell-logo.png"
 assert css.is_file() and logo.is_file()
 shutil.copy2(css,output/"assets"/"estate-shell.css")
 shutil.copy2(logo,output/"assets"/"estate-shell-logo.png")
 shutil.copy2(root/"shell/estate-shell-state.js",output/"assets"/"estate-shell-state.js")
 shutil.copy2(root/"shell/estate-shell-stage-nav.js",output/"assets"/"estate-shell-stage-nav.js")
 evidence={}
 for ident,(url,site_prefix) in SITES.items():
  original=get(url).decode('utf8')
  soup=BeautifulSoup(original,"html.parser")
  seen=set();missing=[];total=0;copies=[]
  site=output/ident
  # Site paths preserve original URL-relative paths, including Solstice's
  # strict-CSP book.css and book.js, without inventing a second reader.
  def admit(asset_url):
   nonlocal total
   remote=urljoin(url,asset_url)
   if urlparse(remote).netloc != urlparse(url).netloc:return
   part=urlparse(remote).path.lstrip("/")
   if site_prefix:
    if not part.startswith(site_prefix):return
    part=part[len(site_prefix):]
   if not part or '..' in Path(part).parts or remote in seen:return
   if len(copies)>=100 or total>=MAX_COPY:return
   seen.add(remote)
   try:data=get(remote)
   except Exception as exc:
    missing.append({"url":remote,"reason":str(exc)[:120]});return
   target=site/part;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
   total+=len(data)
   copies.append({"path":part,"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)})
   if part.endswith(".css"):
    content=data.decode("utf8","replace")
    for token in re.findall(r'url\(\s*["\x27]?(.*?)["\x27]?\s*\)',content):
     token=token.strip().strip('"').strip("'")
     if token and not token.startswith(("data:","#")):admit(urljoin(remote,token))
   # Imported JS chunks are discovered only when statically import-declared.
   if part.endswith(".js"):
    content=data.decode("utf8","replace")
    for token in re.findall(r'(?:from\s*|import\s*)["\x27](\./[^"\x27]+)["\x27]',content):
     admit(urljoin(remote,token))
  for tag in soup.find_all(["script","link","img","source"]):
   for attr in ("src","href","srcset"):
    asset=tag.get(attr)
    if not asset or not isinstance(asset,str):continue
    if tag.name=="link" and not any(x in tag.get("rel",[]) for x in ("stylesheet","icon","preload","modulepreload")):continue
    if tag.name=="source" and attr=="srcset":
     for part in asset.split(","):
      piece=part.strip().split(" ")[0]
      if piece:admit(piece)
     continue
    admit(asset)
    if asset.startswith("/"):
     if site_prefix and asset.startswith("/"+site_prefix):
      tag[attr]="/"+ident+asset[len(site_prefix)+1:]
     elif not site_prefix:
      tag[attr]="/"+ident+asset
  # Copy source-owned HTML with only asset URLs adjusted for stage identity.
  source=str(soup)
  html,receipt=project(source,ident,m,logo="/assets/estate-shell-logo.png")
  # Explicit, stage-only LAN destinations. Keep the original canonical
  # URL as evidence; do not modify the source-owned public manifest.
  projected=BeautifulSoup(html,"html.parser")
  for owner,url in STAGE_BINDINGS.items():
   link=projected.select_one('nav.fc-shell-reel a[data-estate-id="'+owner+'"]')
   assert link and link.get("href","").startswith("https://")
   link["data-canonical-href"]=link["href"]
   link["data-stage-binding"]="wlan-only"
   link["href"]=url
  html=str(projected)
  page=site/"editions"/"first-reading"/"index.html" if ident=="solstice" else site/"index.html"
  page.parent.mkdir(parents=True,exist_ok=True)
  html=html.replace("</body>",'<script defer src="/assets/estate-shell-stage-nav.js"></script></body>',1)
  page.write_text(html)
  if ident=="solstice":
   (site/"index.html").write_text('<!doctype html><meta name="robots" content="noindex">'
      '<meta http-equiv="refresh" content="0;url=editions/first-reading/">'
      '<a href="editions/first-reading/">First Reading</a>')
  receipt.update({"exactPublicSourceSHA256":hashlib.sha256(original.encode()).hexdigest(),
                  "originalPublicURL":url,"assetCount":len(copies),
                  "assetBytes":total,"assetReceipts":copies,"missingAssets":missing,
                  "stageURLPrefix":"/"+ident+"/"})
  evidence[ident]=receipt
 (output/"contract.json").write_text(json.dumps(contract(m),indent=2)+"\n")
 result={"status":"WLAN-PREVIEW-NOT-PUBLIC","templateVersion":VERSION,
         "sites":evidence,"cssSHA256":hashlib.sha256(css.read_bytes()).hexdigest(),
         "logoSHA256":hashlib.sha256(logo.read_bytes()).hexdigest(),
         "archiveMediaCopied":False,"authorPublished":False,"releaseReceipt":None,
         "stageBindings":STAGE_BINDINGS,"canonicalManifestUnchanged":True}
 (output/"source-lock.json").write_text(json.dumps(result,indent=2)+"\n")
 return {"version":VERSION,"sources":{k:{"sha256":v["exactPublicSourceSHA256"],
     "files":v["assetCount"],"bytes":v["assetBytes"],"missing":len(v["missingAssets"])} for k,v in evidence.items()},
    "staged":str(output),"published":False}
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--out",required=True,type=Path)
 p.add_argument("--manifest",type=Path,default=Path(__file__).parent.parent/"navigation/canonical-reel.v1.json")
 o=p.parse_args();print(json.dumps(build(o.out,o.manifest),indent=2))
