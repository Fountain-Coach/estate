#!/usr/bin/env python3
"""Private route-by-route WLAN candidate headmast/reel/footer acceptance.
Uses the retained canonical reel only. Does not publish archive route names.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json
root=Path("/tmp/fc-editorial-v57-20261028/candidate")
entry=json.loads(Path("/tmp/fc-editorial-v57-20261028/estate/navigation/canonical-reel.v1.json").read_text())["entries"]
ids=[x["id"] for x in entry]
labels={x["id"]:x["label"] for x in entry}
urls={x["id"]:x["url"] for x in entry}
assert len(ids)==9 and "status" not in ids
rows=[]
footer_shas=set()
for page in sorted(root.rglob("index.html")):
    s=BeautifulSoup(page.read_text(encoding="utf-8",errors="replace"),"html.parser")
    route=page.relative_to(root).as_posix()
    host=route.split("/",1)[0]
    errs=[]
    head=s.select("header.fc-estate-shell[data-estate-slot=masthead]")
    nav=s.select("header.fc-estate-shell nav.fc-shell-reel")
    foot=s.select("footer.fc-estate-shell[data-footer-contract]")
    if len(head)!=1: errs.append("HEADMAST_COUNT:"+str(len(head)))
    if len(nav)!=1: errs.append("REEL_COUNT:"+str(len(nav)))
    if len(foot)!=1: errs.append("FOOTER_COUNT:"+str(len(foot)))
    if len(nav)==1:
        anchors=nav[0].select("a[data-estate-id]")
        if [x.get("data-estate-id") for x in anchors]!=ids: errs.append("REEL_MEMBERSHIP_ORDER")
        for a in anchors:
            ident=a.get("data-estate-id")
            if a.get("aria-label")!=labels[ident]: errs.append("REEL_LABEL:"+ident)
            if a.get("data-canonical-href")!=urls[ident]:errs.append("REEL_DESTINATION:"+ident)
            if a.get("data-icon-id")!=ident:errs.append("REEL_ICON_ID:"+ident)
        if len(nav[0].select("a.estate-info[href='#footer']"))!=1:errs.append("REEL_INFO")
        actives=[x.get("data-estate-id") for x in anchors if x.get("aria-current")=="page"]
        if actives!=([host] if host in ids else []):errs.append("REEL_ACTIVE:"+str(actives))
    if len(foot)==1:
        if "status.fountain.coach" not in str(foot[0]):errs.append("FOOTER_STATUS")
        if not foot[0].select_one('[data-footer-slot="provenance"]'):errs.append("FOOTER_PROVENANCE")
        footer_shas.add(hashlib.sha256(str(foot[0]).encode()).hexdigest())
    if len(s.select("#footer"))!=1:errs.append("DUPLICATE_FOOTER_ID")
    if not s.head.select_one('link[href="/assets/estate-shell.css"]'):
        errs.append("SHARED_CSS_MISSING")
    if not s.head.select_one('script[src="/assets/estate-shell-state.js"]'):
        errs.append("SHARED_STATE_MISSING")
    if s.select_one('header nav.estate-nav'):errs.append("LEGACY_GLOBAL_REEL_DUPLICATE")
    rows.append(dict(host=host,route=route,state="PASS" if not errs else "FAIL",findings=errs))
counts={}
for row in rows:counts[row["state"]]=counts.get(row["state"],0)+1
summary={"schema":"fountain.estate.author-led-v57-route-acceptance.v1",
         "total":len(rows),"counts":counts,"footerVariantCount":len(footer_shas),
         "allRoutesAccepted":len(rows)==509 and counts.get("FAIL",0)==0,
         "productionReleased":False,"stageActivated":False,
         "stagingPredecessor":"shared-shell-20261028-v56-modell-wirklichkeit-e3753d7",
         "routes":rows}
output=root.parent/"acceptance"
output.mkdir(exist_ok=True)
(output/"all-stage-routes.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
md=["# Author-led estate, complete staged-source route audit","",
 "Scope: private prebuilt v57 candidate, **not an activated stage or public release**.","",
 f"Routes: **{len(rows)}**. PASS **{counts.get('PASS',0)}**. FAIL **{counts.get('FAIL',0)}**. Footer variants **{len(footer_shas)}**.","",
 "| Host | Route | Result | Findings |","| --- | --- | --- | --- |"]
for row in rows:
    md.append("| "+row["host"]+" | "+row["route"]+" | "+row["state"]+" | "+"; ".join(row["findings"])+" |")
(output/"all-stage-routes.md").write_text("\n".join(md)+"\n")
print("ALL_ROUTE_STRUCTURAL_ACCEPTANCE",json.dumps({k:v for k,v in summary.items() if k!="routes"}))
if not summary["allRoutesAccepted"]: raise SystemExit(1)
