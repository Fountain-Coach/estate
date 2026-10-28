#!/usr/bin/env python3
"""Project the already-adopted direct-static EstateShell over a disposable copy
of the canonical private WLAN release. No network writes or production effects.

Local authored material, original article/bibliography text, reader controls,
and all media bytes stay within their original DOM or byte paths.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
import hashlib, json, sys
from copy import deepcopy

root=Path(sys.argv[1]).resolve(strict=True)
template=BeautifulSoup((root/"estate/index.html").read_text(),"html.parser")
common_header=template.select_one("header.fc-estate-shell")
common_footer=template.select_one("footer.fc-estate-shell")
assert common_header and common_footer
EXPECTED=("estate","book","governance","midi2","instruments","teatro","satzfunk","works","solstice")
assert tuple(x["data-estate-id"] for x in common_header.select("[data-estate-id]"))==EXPECTED
assert common_footer.select_one('[data-footer-slot="legal"]')
counts=Counter()
records=[]

for f in sorted(root.rglob("index.html")):
    original=f.read_text(encoding="utf-8",errors="replace")
    soup=BeautifulSoup(original,"html.parser")
    relative=f.relative_to(root)
    host=relative.parts[0]
    if not soup.body or not soup.head:
        records.append(dict(path=str(relative),status="INVALID_DOCUMENT"))
        counts["INVALID_DOCUMENT"]+=1
        continue
    before_main=soup.main.get_text() if soup.main else None
    source_ids={t.get("id") for t in soup.select("button[id],input[id],textarea[id]")}
    original_asset_links=[(x.name,x.get("src")) for x in soup.select("main [src]") if x.get("src")]
    before_body_text=soup.body.get_text(" ",strip=True)
    # Canonical estate chrome is inherited from an independently tested page.
    # The local original site header remains to identify its article/edition,
    # but remove only the older global estate reel and local Info.
    for hdr in list(soup.select("header.fc-estate-shell")): hdr.decompose()
    for foot in list(soup.select("footer.fc-estate-shell")): foot.decompose()
    for nav in list(soup.select("header nav.estate-nav,header nav.fc-shell-reel")):
        nav.decompose()
    # A reader's page-navigation footer is a real control, not a legal footer.
    # Preserve it; preserve all old legal credit text as an original-source aside.
    for foot in list(soup.find_all("footer")):
        if "book-pagination" in foot.get("class",[]) or foot.get("aria-label","").lower().startswith("book pagination"):
            continue
        foot.name="aside"
        foot.attrs.pop("id",None)
        foot["data-original-publisher-footer"]="retained"
        foot["aria-label"]="Original source credits"
    # Attach one global shell without altering the source text or reading UI.
    hdr=BeautifulSoup(str(common_header),"html.parser").header
    footer=BeautifulSoup(str(common_footer),"html.parser").footer
    if host in EXPECTED:
        identity=host
    elif host=="pointer":
        identity="pointer archive"
    elif host=="status":
        identity="status"
    else:
        identity=host
    canonical=json.loads((Path(__file__).resolve().parents[2]/"navigation/canonical-reel.v1.json").read_text())
    by_id={item["id"]:item for item in canonical["entries"]}
    for anchor in hdr.select("[data-estate-id]"):
        item=by_id[anchor["data-estate-id"]]
        anchor["aria-label"]=item["label"]
        anchor["data-canonical-href"]=item["url"]
        anchor["data-icon-id"]=item["id"]
    hdr["data-estate-identity"]=identity
    label=hdr.select_one(".fc-site-identity")
    if label:label.string=identity.upper().replace("-"," ")
    active=host if host in EXPECTED else None
    for a in hdr.select("[data-estate-id]"):
        if a.get("data-estate-id")==active:
            a["aria-current"]="page"
        else:
            a.attrs.pop("aria-current",None)
    soup.body.insert(0,hdr)
    soup.body.append(footer)
    for path,tag in [("/assets/estate-shell.css","link"),("/assets/estate-shell-state.js","script")]:
        exists=any(x.get("href")==path or x.get("src")==path for x in soup.head.select("link,script"))
        if not exists:
            t=soup.new_tag(tag)
            if tag=="link":
                t["rel"]="stylesheet"
                t["href"]=path
            else:
                t["src"]=path
                t["defer"]=""
            soup.head.append(t)
    # Add a source-specific role only where missing; never misstate publication.
    if not soup.head.select_one('meta[name="fountain:publication-role"]'):
        r=soup.new_tag("meta")
        r["name"]="fountain:publication-role"
        r["content"]="original source-owned "+host+" document, private WLAN editorial projection"
        soup.head.append(r)
    if soup.main and soup.main.get_text()!=before_main:
        raise AssertionError("Authored main text changed: "+str(relative))
    if not source_ids.issubset({x.get("id") for x in soup.select("button[id],input[id],textarea[id]")}):
        raise AssertionError("Reader/application control removed: "+str(relative))
    after_assets=[(x.name,x.get("src")) for x in soup.select("main [src]") if x.get("src")]
    if after_assets!=original_asset_links:
        raise AssertionError("Main media reference changed: "+str(relative))
    if soup.body.get_text(" ",strip=True).count("Fountain Coach")<1:
        raise AssertionError("Missing publisher identity")
    result=str(soup)
    f.write_text(result,encoding="utf-8")
    counts["PROJECTED"]+=1
    records.append(dict(path=str(relative),status="PROJECTED",identity=identity,
             sourceSHA256=hashlib.sha256(original.encode()).hexdigest(),
             projectedSHA256=hashlib.sha256(result.encode()).hexdigest(),
             sourceControls=len(source_ids),sourceMediaReferences=len(original_asset_links)))
summary=dict(schema="fountain.estate.private-wlan-author-led-projection.v1",
    candidateRoot=str(root),changed=counts["PROJECTED"],
    invalid=counts["INVALID_DOCUMENT"],expectedReel=EXPECTED,
    previousActiveRelease="shared-shell-20261028-v56-modell-wirklichkeit-e3753d7",
    productionMutation=False,stageActivated=False,
    records=records)
dest=root.parent/"chrome-projection-receipt.json"
dest.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
print("PRIVATE_CHROME_COMPOSITION",json.dumps({k:v for k,v in summary.items() if k!="records"},ensure_ascii=False))
