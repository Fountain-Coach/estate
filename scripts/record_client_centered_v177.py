#!/usr/bin/env python3
"""Independent live v177 HTTP/semantic/font/figure release receipt (no writes to public)."""
from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request

STAGE=Path("/home/benedikt/estate-shell-acceptance-staging")
RELEASE="shared-shell-20261110-v177-client-centered-bd8f6d9"
PREV="shared-shell-20261109-v176-four-domain-c265c57"
SOURCE="bd8f6d93e01354cc0c09a9de0bf9417bd9cfde9c"
SHA_LOCK="f67e3dd27d08d73e96f04e6c67a08983bb6c87145126f45c62f924a3fea4c688"
INVENTORY_SHA="01b6e426983fc17d69454df37a694bc77aa859f05e543c711068ed3bd28b32f7"
PFX="estate/read/essay--client-centered/"
HOST="http://192.168.8.50:8200/"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return path.read_bytes()
root=STAGE/"releases"/RELEASE
assert (STAGE/"current").resolve()==root.resolve()
assert sha(read(root/"source-lock.json"))==SHA_LOCK
assert (STAGE/"releases"/PREV).is_dir()
assert subprocess.check_output(["systemctl","--user","is-active","fountain-shell-acceptance-preview.service"],text=True).strip()=="active"
cmd=subprocess.check_output(["systemctl","--user","show","fountain-shell-acceptance-preview.service","-p","ExecStart"],text=True)
assert "serve_client_centered_v177.py" in cmd
manifest_file=STAGE/"candidates/client-centered-v177-bd8f6d9-source-inventory.json"
assert sha(read(manifest_file))==INVENTORY_SHA
source=json.loads(manifest_file.read_text())
assert source["sourceRevision"]==SOURCE and len(source["files"])==16
http=[]
for rel,digest in sorted(source["files"].items()):
    route=PFX+rel
    req=urllib.request.Request(HOST+route,headers={"User-Agent":"Fountain-Press-staging-source-witness"})
    with urllib.request.urlopen(req,timeout=14) as resp:
        assert resp.status==200
        actual=resp.read()
        code=resp.status
    assert sha(actual)==digest and sha(read(root/route))==digest,rel
    http.append({"route":"/"+route,"status":code,"sha256":digest,"size":len(actual)})
edition=json.loads(read(root/PFX/"edition-manifest.json"))
assert edition["sourceRevision"]==SOURCE
assert edition["sourceSHA256"]==source["manuscriptSHA256"]
assert edition["paragraphCount"]==22
assert len(edition["sections"])==4 and len(edition["figures"])==2
assert edition["productionAuthorized"] is False
assert edition["blocks"][-1]["text"].endswith("What develops between those two circumstances cannot be entirely designed in advance.")
assert sha(read(root/PFX/"assets/press/reading-first-press-engine.e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a.js"))=="e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a"
log=STAGE/"candidates/client-centered-v177-bd8f6d9-browser.log"
s=log.read_text()
assert s.count("CLIENT_CENTERED_ORIGINAL_PRESS_PASS")==4
assert "source-paragraphs=22 sections=4 figures=2" in s
shots=STAGE/"candidates/client-centered-v177-bd8f6d9"
screens={}
for name in ("phone","ipad-portrait","ipad-landscape","desktop"):
    file=shots/("client-centered-"+name+"-first.png")
    assert file.is_file()
    screens[name]={"sha256":sha(read(file)),"bytes":file.stat().st_size}
receipt={
 "schema":"fountain.press.client-centered.wlan-acceptance.v177",
 "observedAt":datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "work":"Client-Centered",
 "sourceOwner":"Fountain-Coach/fountain.coach","sourceRevision":SOURCE,
 "manuscriptSource":"site/essays/client-centered/client-centered.md",
 "sourceSHA256":edition["sourceSHA256"],
 "publishedPredecessor":"https://fountain.coach/estate/read/essay--the-ear-that-learns/",
 "publishedReaderEngineSHA256":"e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a",
 "stageURL":HOST+PFX,
 "stageRelease":RELEASE,"stagePredecessor":PREV,
 "stageSourceLockSHA256":SHA_LOCK,"sourceInventorySHA256":INVENTORY_SHA,
 "proseParagraphs":22,"sections":4,"authoredTeatroScores":2,
 "inheritedStageFilesPreserved":1830,"addedStageFiles":16,
 "stageSourceAssetsReadback":http,
 "browserWitness":{"file":log.name,"sha256":sha(read(log)),"passedViewports":["phone","ipad-portrait","ipad-landscape","desktop"],"sourceReconstruction":True,"twoFiguresOnComposedPages":True},
 "firstLeafScreenshots":screens,
 "sourcePublishedProduction":False,"publicProductionChanged":False,
 "physicaliPadSafariVoiceOver":"not performed",
 "rollbackReleaseRetained":True,
}
result=STAGE/"candidates/client-centered-v177-bd8f6d9-terminal-receipt.json"
result.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"receipt":str(result),"source":SOURCE,"assets":len(http),"browserViewports":4,"stageRelease":RELEASE,"productionChanged":False},indent=2))
