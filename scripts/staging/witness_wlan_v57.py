#!/usr/bin/env python3
"""Independent HTTP witness of every HTML route in the WLAN staging release."""
from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import hashlib, json, datetime, collections

ROOT=Path("/tmp/fc-editorial-v57-20261028")
M=json.loads((ROOT/"release-inventory.json").read_text())
ENTRY=json.loads((ROOT/"estate/navigation/canonical-reel.v1.json").read_text())["entries"]
EXPECTED=[x["id"] for x in ENTRY]
assert len(EXPECTED)==9 and "works" in EXPECTED and "satzfunk" in EXPECTED
URL="http://192.168.8.50:8200/"
HOSTS=collections.Counter()
HTML=[x for x in M["files"] if x["path"].endswith("/index.html")]

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack=[]
        self.header=0;self.footer=0;self.reel=[];self.footerStatus=0
        self.footerLegal=0;self.footerProvenance=0;self.info=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.stack.append((tag,d))
        if tag=="header" and "fc-estate-shell" in d.get("class","").split():self.header+=1
        if tag=="footer" and "fc-estate-shell" in d.get("class","").split():self.footer+=1
        in_reel=any(t=="nav" and "fc-shell-reel" in x.get("class","").split() for t,x in self.stack)
        in_footer=any(t=="footer" and "fc-estate-shell" in x.get("class","").split() for t,x in self.stack)
        if tag=="a" and in_reel and "data-estate-id" in d:self.reel.append(d["data-estate-id"])
        if tag=="a" and in_reel and "estate-info" in d.get("class","").split():self.info+=1
        if tag=="a" and in_footer and "status.fountain.coach" in d.get("href",""):self.footerStatus+=1
        if in_footer and d.get("data-footer-slot")=="legal":self.footerLegal+=1
        if in_footer and d.get("data-footer-slot")=="provenance":self.footerProvenance+=1
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs);self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:]
                break

def witness(item):
    path=item["path"];route="/"+path[:-len("index.html")]
    req=Request(URL+route,headers={"User-Agent":"Fountain-Coach-Private-WLAN-Release-Witness/1.0","Cache-Control":"no-cache"})
    result={"path":path,"route":route,"state":"FAILED"}
    try:
        with urlopen(req,timeout=15) as resp:
            body=resp.read()
            result["httpStatus"]=resp.status
            result["contentType"]=resp.headers.get("Content-Type","")
        result["bytes"]=len(body)
        result["sha256"]=hashlib.sha256(body).hexdigest()
        issues=[]
        if result["httpStatus"]!=200:issues.append("HTTP_NOT_200")
        expected=item["sha256"]
        if path=="pointer/index.html":
            expected=hashlib.sha256((ROOT/"candidate/works/index.html").read_bytes()).hexdigest()
            result["servedAlias"]="/works/"
        if result["sha256"]!=expected:issues.append("BYTES_DIFFER")
        if "text/html" not in result["contentType"]:issues.append("CONTENT_TYPE")
        doc=Inspect()
        doc.feed(body.decode("utf-8","replace"))
        if doc.header!=1:issues.append("MASTHEAD_COUNT")
        if doc.footer!=1:issues.append("FOOTER_COUNT")
        if doc.reel!=EXPECTED:issues.append("CANONICAL_REEL")
        if doc.info!=1:issues.append("INFO_ACTION")
        if doc.footerStatus<1:issues.append("STATUS_LINK")
        if doc.footerLegal!=1:issues.append("LEGAL_SLOT")
        if doc.footerProvenance!=1:issues.append("PROVENANCE_SLOT")
        result["findings"]=issues
        result["state"]="PASS" if not issues else "FAIL"
        result["reelCount"]=len(doc.reel)
        result["footerCount"]=doc.footer
        result["headerCount"]=doc.header
    except Exception as e:
        result["findings"]=[type(e).__name__+": "+str(e)[:180]]
    return result

with ThreadPoolExecutor(max_workers=12) as pool:
    results=list(pool.map(witness,HTML))
counts=collections.Counter(x["state"] for x in results)
for x in results:HOSTS[x["path"].split("/",1)[0]]+=1
summary={"schema":"fountain.estate.wlan-stage-509-http-readback.v1",
 "date":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "release":M["release"],"entry":URL+"estate/",
 "sourceInventorySHA256":M["inventorySHA256"],"tests":len(results),
 "statusCounts":counts,"hosts":HOSTS,"complete":len(results)==509 and counts["PASS"]==509,
 "productionReleased":False,"results":results}
out=ROOT/"acceptance"
out.mkdir(exist_ok=True)
(out/"wlan-http-509.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
lines=["# Independent HTTP readback — private WLAN v57","",
 "URL: "+URL+"estate/  | Release: "+M["release"],"",
 "Tested 509 exact HTML routes against the immutable SHA-256 file inventory, shared masthead, full reel, Info action, legal footer and provenance slot.",
 "",
 "| Result | Count |","| --- | ---: |",
 *["| "+name+" | "+str(count)+" |" for name,count in sorted(counts.items())],
 "","| Host | Route | Result | Findings |","| --- | --- | --- | --- |"]
for row in results:
    lines.append("| "+row["path"].split("/",1)[0]+" | "+row["route"]+" | "+row["state"]+" | "+"; ".join(row.get("findings",[]))+" |")
(out/"wlan-http-509.md").write_text("\n".join(lines)+"\n")
print("INDEPENDENT_WLAN_HTTP_READBACK",json.dumps({k:v for k,v in summary.items() if k!="results"},default=dict,ensure_ascii=False))
if not summary["complete"]:raise SystemExit(1)
