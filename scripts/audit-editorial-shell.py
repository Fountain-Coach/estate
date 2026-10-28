#!/usr/bin/env python3
"""Complete source-route and canonical WLAN-stage shell audit.

No mutation of publication servers. Every registered HTML route receives a
row, including explicit exceptions, unavailable mappings and HTTP failures.
Run from the existing Estate owner checkout with adjacent owner repositories.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import os
import subprocess
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEV = Path(os.environ.get("FOUNTAIN_DEV_ROOT", ROOT.parents[1])).resolve()
ROUTES = ROOT / "inventory/source-routes.json"
OWNERS = ROOT / "inventory/domain-ownership.json"
REEL = ROOT / "navigation/canonical-reel.v1.json"
STAGE = ROOT / "staging/environment.json"
PUBLIC_ONLY = [
    "/essays/the-door-is-a-score/",
    "/essays/the-composable-book/",
]
ROLE_TO_HOST = {
    "estate": "fountain.coach", "book": "book.fountain.coach",
    "governance": "governance.fountain.coach", "midi2": "midi2.fountain.coach",
    "instruments": "instruments.fountain.coach", "teatro": "teatro.fountain.coach",
    "pointer": "benedikt-eickhoff.de",
    "solstice": "solstice.fountain.coach",
}
STAGE_ROLE = {
    "fountain.coach": "estate", "book.fountain.coach": "book",
    "governance.fountain.coach": "governance", "midi2.fountain.coach": "midi2",
    "instruments.fountain.coach": "instruments", "teatro.fountain.coach": "teatro",
    "benedikt-eickhoff.de": "pointer", "solstice.fountain.coach": "solstice",
    "works.benedikt-eickhoff.de": "works", "status.fountain.coach": "status",
}
REQUIRED_FOOTER = (
    "status.fountain.coach", "/legal/", "/privacy/",
    "/accessibility/", "/copyright/", "/compliance/"
)

class Document(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.reel = []
        self.footer = []
        self.has_html = False
        self.banners = 0
        self.mains = 0
        self.footers = 0
        self.heading_count = 0
        self.role = ""
        self.skip = False
        self.info = False
        self.brand = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        classes = set(d.get("class", "").split())
        if tag == "html": self.has_html = True
        if tag == "meta" and d.get("name") == "fountain:publication-role":
            self.role = d.get("content", "")
        if tag == "header" and ("site-header" in classes or "fc-estate-shell" in classes or "topbar" in classes or d.get("data-estate-slot") == "masthead" or d.get("role") == "banner"):
            self.banners += 1
        if tag == "main": self.mains += 1
        if tag == "footer": self.footers += 1
        if tag == "h1": self.heading_count += 1
        self.stack.append((tag, d))
        is_reel = any(t == "nav" and ("estate-nav" in a.get("class","").split() or "fc-shell-reel" in a.get("class","").split() or
                           "estate" in a.get("aria-label","").lower()) for t,a in self.stack)
        is_footer = any(t == "footer" for t,a in self.stack)
        is_header = any(t == "header" for t,a in self.stack)
        if tag == "a":
            href = d.get("href", "")
            if "skip-link" in classes and href.startswith("#"): self.skip = True
            if is_header and ("fc-publisher" in classes or "brand" in classes or "wordmark" in classes or d.get("data-canonical-href") == "https://fountain.coach/"):
                self.brand = True
            if is_reel and "estate-info" in classes: self.info = True
            if is_reel:
                identity = d.get("data-estate-id")
                if identity: self.reel.append((identity,href))
            if is_footer: self.footer.append(href)
            if is_header and (href == "/" or href == "https://fountain.coach/"):
                self.brand = True
        if tag == "button" and is_reel and ("estate-info" in classes or
                "info" in d.get("aria-label","").lower()): self.info = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for n in range(len(self.stack)-1,-1,-1):
            if self.stack[n][0] == tag:
                del self.stack[n:]
                break

def baseline():
    owners = json.loads(OWNERS.read_text())
    routes = json.loads(ROUTES.read_text())
    reel = json.loads(REEL.read_text())
    stage = json.loads(STAGE.read_text())["surfaces"]
    current = stage[json.loads(STAGE.read_text())["canonicalEntrySurface"]]
    source = {x["repository"]:x for x in owners["sources"]}
    domains = {x["host"]:x for x in owners["domains"]}
    return routes,source,domains,reel["entries"],current

def stage_path(row, stage_routes):
    host, route = row["host"],row["route"]
    if host == "works.benedikt-eickhoff.de" and route.startswith("/solstice/"):
        prefix = stage_routes.get("solstice")
        if not prefix: return None
        suffix = route[len("/solstice/"):]
    else:
        role = STAGE_ROLE.get(host)
        prefix = stage_routes.get(role) if role else None
        suffix = route.lstrip("/")
    if not prefix: return None
    return prefix.rstrip("/") + "/" + suffix

def read_source(row, owners, fountain_ref=None):
    repo = row["owner"]
    src = owners[repo]
    revision = fountain_ref if repo == "Fountain-Coach/fountain.coach" and fountain_ref else src["head"]
    root = DEV / src["localCheckout"]
    cmd = ["git", "-C", str(root), "show", revision + ":" + row["sourceFile"]]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode("utf-8","replace")[:240])
    return p.stdout.decode("utf-8","replace")

def read_stage(url, timeout):
    req = Request(url, headers={"User-Agent":"FountainCoach-EstateChrome-Audit/1.0"})
    try:
        with urlopen(req,timeout=timeout) as answer:
            return answer.status, answer.read(4_000_000).decode("utf-8","replace")
    except Exception as e:
        return 0, type(e).__name__ + ": " + str(e)[:180]

def assess(html, entries, row, stage_mode):
    doc = Document(html)
    if not doc.has_html:
        return "FRAGMENT", ["Source fragment; not a complete route HTML document"],{}
    expected = [x["id"] for x in entries]
    found = [x[0] for x in doc.reel]
    errors = []
    if doc.banners != 1: errors.append("HEADMAST: expected one semantic masthead, got " + str(doc.banners))
    if not doc.brand: errors.append("HEADMAST: no author/publisher link home")
    if doc.mains != 1: errors.append("LANDMARK: expected one main element")
    if doc.heading_count != 1: errors.append("HEADING: expected one H1")
    if not doc.skip: errors.append("AX: missing skip navigation")
    if found != expected: errors.append("REEL: expected " + ",".join(expected) + " found " + ",".join(found))
    if not doc.info: errors.append("REEL: missing Info action")
    if doc.footers != 1: errors.append("FOOTER: expected one footer")
    ftext = " ".join(doc.footer)
    for required in REQUIRED_FOOTER:
        if required not in ftext: errors.append("FOOTER: missing " + required)
    if not doc.role and not any(x in html for x in ("data-estate-identity=", "data-publication-role=", "name=\"fountain:publication-role\"")):
        errors.append("ROLE: no explicit publication role")
    evidence = {
      "headmastCount":doc.banners,"mainCount":doc.mains,"h1Count":doc.heading_count,
      "reelIDs":found,"footerLinks":doc.footer,"publicationRole":doc.role,
      "hasInfo":doc.info,"hasSkip":doc.skip
    }
    return ("FAIL" if errors else "PASS"),errors,evidence

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("source","stage"),required=True)
    ap.add_argument("--stage-base",default="http://benedikt-Macmini.local:8200")
    ap.add_argument("--fountain-ref",help="Pinned author-led source branch or 40-character Git SHA")
    ap.add_argument("--output",required=True,help="Local JSON report, no publication effect")
    ap.add_argument("--workers",type=int,default=8)
    ap.add_argument("--timeout",type=float,default=5.0)
    ap.add_argument("--report-only",action="store_true",help="Do not fail on findings")
    a = ap.parse_args()
    rows,owners,domains,entries,stage = baseline()
    rows = list(rows)
    known = {(r["host"],r["route"]) for r in rows}
    for path in PUBLIC_ONLY:
        if ("fountain.coach",path) not in known:
            rows.append(dict(host="fountain.coach",route=path,
                owner="Fountain-Coach/fountain.coach",sourceFile=None,
                provenance="public-HTTPS-route-not-present-in-Git-inventory"))
    stage_routes = stage["editorialRoutes"]
    def inspect(row):
        host, route = row["host"],row["route"]
        state = domains.get(host,{}).get("lifecycle","unregistered")
        base = dict(host=host,route=route,owner=row["owner"],
                    sourceFile=row.get("sourceFile"),lifecycle=state,mode=a.mode,
                    provenance=row.get("provenance"),findings=[])
        if state in ("planned","archived") and not (
            host == "works.benedikt-eickhoff.de" and route.startswith("/solstice/")):
            return dict(base,result="OUTSIDE_PUBLIC_SCOPE",
                findings=["Host declared " + state + "; not asserted as publicly served"])
        if a.mode == "source":
            if not row.get("sourceFile"):
                return dict(base,result="MISSING_SOURCE_CUSTODY",
                    findings=["Publicly observed essay is absent from tracked source inventory"])
            try: html = read_source(row, owners,a.fountain_ref)
            except Exception as e: return dict(base,result="ERROR",findings=[str(e)])
            result,findings,evidence = assess(html,entries,row,False)
            return dict(base,result=result,findings=findings,evidence=evidence,
                        contentSHA256=sha256(html.encode()).hexdigest())
        mapped = stage_path(row,stage_routes)
        if mapped is None:
            return dict(base,result="UNMAPPED",findings=["No canonical stage route declared for this host"])
        url = a.stage_base.rstrip("/") + mapped
        status,html = read_stage(url,a.timeout)
        base.update(stageURL=url,httpStatus=status)
        if status != 200:
            return dict(base,result="ERROR",findings=["Stage HTTP status " + str(status) + " " + html[:160]])
        result,findings,evidence=assess(html,entries,row,True)
        return dict(base,result=result,findings=findings,evidence=evidence,
                    contentSHA256=sha256(html.encode()).hexdigest())
    with ThreadPoolExecutor(max_workers=max(1,min(16,a.workers))) as pool:
        results = list(pool.map(inspect,rows))
    counts = {}
    for x in results: counts[x["result"]] = counts.get(x["result"],0)+1
    summary = dict(schema="fountain.estate.editorial-shell-audit.v1",
        generatedAt=datetime.now(timezone.utc).isoformat(),
        mode=a.mode, canonicalStageEntry=stage.get("entryURL"),
        sourceRouteInventoryCount=len(known),
        additionalPublicRoutes=[r for r in PUBLIC_ONLY if ("fountain.coach",r) not in known],
        checkedRoutes=len(results), counts=counts,
        verdict="PASS" if all(x["result"] in ("PASS","FRAGMENT","OUTSIDE_PUBLIC_SCOPE") for x in results)
                else "NOT_ACCEPTED",
        routes=results)
    dest = Path(a.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    # A second human-readable route register is derived from the same evidence.
    md = ["# Estate chrome route-by-route acceptance",
          "", "Mode: `"+a.mode+"` | Verdict: **"+summary["verdict"]+"** | Routes: "+str(len(results)),
          "", "This is source or private WLAN evidence, never a public release receipt.",
          "Planned and archived hosts are represented without pretending they serve a public page.",
          "", "## Result counts", ""]
    for name,count in sorted(counts.items()): md.append("- "+name+": "+str(count))
    md += ["", "## Routes", "", "| Host | Route | Result | Findings |",
           "| --- | --- | --- | --- |"]
    for item in sorted(results,key=lambda x:(x["host"],x["route"])):
        msg = "; ".join(item["findings"]).replace("|","\\|").replace("\n"," ")
        md.append("| "+item["host"]+" | `"+item["route"].replace("|","\\|")+
                  "` | "+item["result"]+" | "+msg+" |")
    dest.with_suffix(".md").write_text("\n".join(md)+"\n")
    print("ESTATE_CHROME_AUDIT",a.mode,summary["verdict"],"routes",len(results),
          json.dumps(counts,sort_keys=True),"report",dest)
    if summary["verdict"] != "PASS" and not a.report_only: raise SystemExit(1)

if __name__ == "__main__":
    main()
