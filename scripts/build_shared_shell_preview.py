#!/usr/bin/env python3
"""Capture the actual published pages, compose a common shell and build a LAN preview.

Reads public bytes only. No page publication, rights admission, Store write,
authorization, DNS or live domain mutation. Reframe Bookshelf admission is not
an EstatePublisher release.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,sys
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

sys.path.insert(0,str(Path(__file__).parent))
from estate_shell import manifest,contract,project,VERSION

SITES={
 "estate":"https://fountain.coach/",
 "teatro":"https://teatro.fountain.coach/",
 "solstice":"https://works.benedikt-eickhoff.de/solstice/editions/first-reading/",
}
def get(source):
 req=Request(source,headers={"User-Agent":"FountainCoach-EstateShell-Staging/1.0"})
 with urlopen(req,timeout=17) as f:
  if f.status!=200 or f.url!=source:
   raise RuntimeError("unexpected redirect/status: "+source)
  return f.read().decode("utf-8")

def resolve_original_assets(html,base):
 """Preserve the published content; link original page assets from its own host."""
 soup=BeautifulSoup(html,"html.parser")
 for item in soup.find_all(["script","img","link","source","video"]):
  for key in ("src","href","poster"):
   value=item.get(key)
   if not value or value.startswith(("#","data:","blob:","mailto:","javascript:")):
    continue
   if value.startswith(("http://","https://")):
    continue
   item[key]=urljoin(base,value)
 return str(soup)

def build(out:Path,manifest_path:Path):
 if out.exists():
  raise RuntimeError("refuse overwrite of previous staging release: "+str(out))
 m=manifest(manifest_path)
 out.mkdir(parents=True)
 (out/"assets").mkdir()
 root=manifest_path.parent.parent
 css=root/"shell/estate-shell.css"
 mark=root/"shell/assets/estate-shell-logo.png"
 assert css.is_file() and mark.is_file()
 shutil.copy2(css,out/"assets"/"estate-shell.css")
 shutil.copy2(mark,out/"assets"/"estate-shell-logo.png")
 locks={}
 for ident,url in SITES.items():
  original=get(url)
  source=resolve_original_assets(original,url)
  html,receipt=project(source,ident,m,logo="/assets/estate-shell-logo.png")
  (out/ident).mkdir()
  (out/ident/"index.html").write_text(html,encoding="utf-8")
  receipt["exactPublicSourceSHA256"]=hashlib.sha256(original.encode()).hexdigest()
  receipt["originalSourceURL"]=url
  receipt["sourceAssetsRepointedToAuthoritativeHost"]=True
  locks[ident]=receipt
 (out/"contract.json").write_text(json.dumps(contract(m),indent=2)+"\n")
 lock={"status":"WLAN-PREVIEW-NOT-PUBLIC","templateVersion":VERSION,
       "sites":locks,"sharedCSSSHA256":hashlib.sha256(css.read_bytes()).hexdigest(),
       "sharedLogoSHA256":hashlib.sha256(mark.read_bytes()).hexdigest(),
       "noPrivateArchiveBytes":True,"domainDeploymentAuthorized":False,
       "sourceRightsOrAuthorApprovalImplied":False}
 (out/"source-lock.json").write_text(json.dumps(lock,indent=2)+"\n")
 return lock
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--out",type=Path,required=True)
 p.add_argument("--manifest",type=Path,default=Path(__file__).parent.parent/"navigation/canonical-reel.v1.json")
 o=p.parse_args()
 print(json.dumps(build(o.out,o.manifest),indent=2))
