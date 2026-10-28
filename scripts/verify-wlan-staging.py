#!/usr/bin/env python3
"""Read-only acceptance for the *current* owner-WLAN estate staging service.

Unlike verify-wlan-staging-legacy-8180.py this checks the source-registered
8200 service, its actual active symlink and exact release file inventory.
It emits an explicit verdict and one row for every staged HTML route.
No server or Git mutation.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from collections import Counter
import argparse
import datetime
import hashlib
import json
import shlex
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"staging/environment.json"
REEL=ROOT/"navigation/canonical-reel.v1.json"

class Chrome(HTMLParser):
    def __init__(self,html):
        super().__init__(convert_charrefs=True)
        self.stack=[]
        self.masthead=0
        self.reel=[]
        self.info=0
        self.footer=0
        self.status=0
        self.legal=0
        self.provenance=0
        self.ids=[]
        self.feed(html)

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        self.stack.append((tag,a))
        css=a.get("class","").split()
        if tag=="header" and "fc-estate-shell" in css:self.masthead+=1
        if tag=="footer" and "fc-estate-shell" in css:self.footer+=1
        if a.get("id")=="footer":self.ids.append("footer")
        in_reel=any(t=="nav" and "fc-shell-reel" in x.get("class","").split() for t,x in self.stack)
        in_foot=any(t=="footer" and "fc-estate-shell" in x.get("class","").split() for t,x in self.stack)
        if tag=="a" and in_reel:
            if a.get("data-estate-id"):self.reel.append(a)
            if "estate-info" in css and a.get("href")=="#footer":self.info+=1
        if tag=="a" and in_foot and "status.fountain.coach" in a.get("href",""):self.status+=1
        if in_foot and a.get("data-footer-slot")=="legal":self.legal+=1
        if in_foot and a.get("data-footer-slot")=="provenance":self.provenance+=1
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs);self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:]
                break

def ssh(alias,command):
    p=subprocess.run(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=5",alias,command],
       text=True,capture_output=True,timeout=40)
    if p.returncode:
        raise RuntimeError("SSH read-only witness failed: "+p.stderr[-360:])
    return p.stdout.strip()

def run():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ssh-alias",default="MacMiniDocker")
    parser.add_argument("--manifest",type=Path,help="Existing local copy of an exact active release inventory")
    parser.add_argument("--output",type=Path,default=Path("/tmp/fountain-estate-current-wlan-readback.json"))
    parser.add_argument("--workers",type=int,default=12)
    args=parser.parse_args()
    registry=json.loads(REGISTRY.read_text())
    surface=registry["surfaces"][registry["canonicalEntrySurface"]]
    entry=surface.get("observedDirectAddressURL",surface["entryURL"])
    parsed=urlsplit(entry)
    base=parsed.scheme+"://"+parsed.netloc+"/"
    release=surface["observedRelease"]
    root=surface["activeReleaseSymlink"]
    actual=ssh(args.ssh_alias,"readlink "+shlex.quote(root))
    if actual!="releases/"+release:
        raise RuntimeError("Active release changed. Registry="+release+" actual="+actual)
    service=ssh(args.ssh_alias,"systemctl --user is-active fountain-shell-acceptance-preview.service")
    if service!="active":raise RuntimeError("WLAN preview service is not active: "+service)
    rec=surface.get("authorLedEditorialReleaseV58",surface["authorLedEditorialReleaseV57"])["typedPrivateReceipt"]
    remote_manifest=str(Path(rec).with_name("release-inventory.json"))
    manifest=json.loads(args.manifest.read_text() if args.manifest else
                        ssh(args.ssh_alias,"cat "+shlex.quote(remote_manifest)))
    if manifest["release"]!=release:raise RuntimeError("Release inventory mismatch")
    if manifest.get("publicAuthorized") is not False:raise RuntimeError("Refuse public manifest")
    files={x["path"]:x for x in manifest["files"]}
    html=[x for x in manifest["files"] if x["path"].endswith("/index.html")]
    if len(html)!=manifest["htmlCount"]:raise RuntimeError("HTML inventory mismatch")
    reel=json.loads(REEL.read_text())["entries"]
    ids=[r["id"] for r in reel]
    if ids!=["estate","book","governance","midi2","instruments","teatro","satzfunk","works","solstice"]:
        raise RuntimeError("Unreviewed canonical reel identity set")
    lookup={r["id"]:r for r in reel}

    def inspect(item):
        path=item["path"]
        route="/"+path[:-len("index.html")]
        row=dict(route=route,path=path,state="FAIL",findings=[])
        request=Request(base+route,headers={"Cache-Control":"no-cache",
                           "User-Agent":"FountainCoach-WLAN-stage-audit/2.0"})
        try:
            with urlopen(request,timeout=18) as reply:
                data=reply.read()
                row["httpStatus"]=reply.status
                row["contentType"]=reply.headers.get("Content-Type","")
            digest=hashlib.sha256(data).hexdigest()
            row["sha256"]=digest
            expected=item["sha256"]
            if path=="pointer/index.html":
                expected=files["works/index.html"]["sha256"]
                row["routeAlias"]="/works/"
            if digest!=expected:row["findings"].append("HTML_SHA256")
            if row["httpStatus"]!=200:row["findings"].append("HTTP_STATUS")
            if "text/html" not in row["contentType"]:row["findings"].append("CONTENT_TYPE")
            parsed=Chrome(data.decode("utf-8","replace"))
            if parsed.masthead!=1:row["findings"].append("MASTHEAD_COUNT")
            if parsed.footer!=1:row["findings"].append("FOOTER_COUNT")
            if len(parsed.ids)!=1:row["findings"].append("FOOTER_ID")
            if [v.get("data-estate-id") for v in parsed.reel]!=ids:
                row["findings"].append("REEL_ORDER")
            else:
                for a in parsed.reel:
                    v=lookup[a["data-estate-id"]]
                    if a.get("aria-label")!=v["label"]:row["findings"].append("REEL_LABEL:"+v["id"])
                    if a.get("data-icon-id")!=v["id"]:row["findings"].append("REEL_ICON:"+v["id"])
                    if a.get("data-canonical-href")!=v["url"]:
                        row["findings"].append("REEL_DESTINATION:"+v["id"])
            if parsed.info!=1:row["findings"].append("INFO_ACTION")
            if parsed.status<1:row["findings"].append("FOOTER_STATUS")
            if parsed.legal!=1:row["findings"].append("FOOTER_LEGAL")
            if parsed.provenance!=1:row["findings"].append("FOOTER_PROVENANCE")
        except Exception as e:
            row["findings"].append(type(e).__name__+": "+str(e)[:160])
        if not row["findings"]:row["state"]="PASS"
        return row

    with ThreadPoolExecutor(max_workers=max(1,min(16,args.workers))) as pool:
        results=list(pool.map(inspect,html))
    counts=dict(Counter(x["state"] for x in results))
    # Route-local stylesheets are NOT implied by a passing HTML/reel check.
    # The Composable Book CSS returned 404 on v56/v57 despite 509 green HTML
    # results. Verify this exact production-sourced stylesheet on the running stage.
    asset_checks=[]
    css_proof=surface.get("authorLedEditorialReleaseV58")
    if css_proof and release==css_proof["activeRelease"]:
        asset_path="estate/essays/the-composable-book/assets/essay.css"
        expected_css=css_proof["cssSHA256"]
        assert files[asset_path]["sha256"]==expected_css, "CSS manifest/source mismatch"
        row={"path":asset_path,"expectedSHA256":expected_css,"state":"FAIL"}
        try:
            req=Request(base+asset_path,headers={"Cache-Control":"no-cache"})
            with urlopen(req,timeout=18) as reply:
                content=reply.read()
                row["httpStatus"]=reply.status
                row["contentType"]=reply.headers.get("Content-Type","")
            row["bytes"]=len(content)
            row["sha256"]=hashlib.sha256(content).hexdigest()
            ok=(row["httpStatus"]==200 and row["contentType"].startswith("text/css")
                and row["bytes"]==css_proof["cssBytes"]
                and row["sha256"]==expected_css)
            row["state"]="PASS" if ok else "FAIL"
        except Exception as error:
            row["error"]=str(error)[:200]
        asset_checks.append(row)
    report={"schema":"fountain.estate.wlan-stage-live-route-check.v2",
      "generatedAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "release":release,"predecessor":manifest["priorRelease"],
      "url":entry,"inventorySHA256":manifest["inventorySHA256"],
      "routes":len(results),"counts":counts,"assetChecks":asset_checks,
      "accepted":len(results)==manifest["htmlCount"] and counts.get("PASS")==len(results)
         and all(x["state"]=="PASS" for x in asset_checks),
      "publicPublished":False,"rows":results}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    lines=["# Verified owner-WLAN stage routes","",
        "Release: "+release+" | Entry: "+entry+" | Accepted: "+str(report["accepted"]),
        "","| Route | Status | Findings |","| --- | --- | --- |"]
    for row in results:
        lines.append("| "+row["route"]+" | "+row["state"]+" | "+"; ".join(row["findings"])+" |")
    args.output.with_suffix(".md").write_text("\n".join(lines)+"\n")
    print("CURRENT_WLAN_STAGE",json.dumps({k:v for k,v in report.items() if k!="rows"},ensure_ascii=False))
    if not report["accepted"]:raise SystemExit(1)

if __name__=="__main__":
    run()
