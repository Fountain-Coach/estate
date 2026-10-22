#!/usr/bin/env python3
"""Compile a *stage-only* release-continuity witness from independent HTTP readbacks.

Never authorizes a production deployment. Fails closed on incomplete browser,
release identity, immutable asset, rollback or no-store evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request,urlopen

SCHEMA="fountain.estate.browser-release-continuity.stage-certificate.v1"
STEPS=(
  "A fresh anonymous session",
  "Retained A tab detects B without reload",
  "New isolated session starts B",
  "Deliberate, ordinary navigation to B",
  "Back navigation never claims old A current",
  "Disconnected authority refuses freshness"
)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def fetch(origin,path):
    req=Request(origin+path,headers={"Cache-Control":"no-cache","Accept":"*/*"})
    with urlopen(req,timeout=8) as response:
        if response.geturl()!=origin+path or response.status!=200:
            raise ValueError("readback redirect or status mismatch")
        return dict(response.headers.items()),response.read()

def certify(origin,a,b,witness_dir):
    if origin != "http://192.168.8.50:8201":
        raise ValueError("only verified author-LAN origin admitted")
    if not a or not b or a==b or any(len(x)!=64 or not all(c in "0123456789abcdef" for c in x) for x in (a,b)):
        raise ValueError("invalid independent release IDs")
    report=json.loads((witness_dir/"witness.json").read_text())
    if report.get("scenario")!="estate.browser-release-continuity" or report.get("passed") is not True or report.get("errors"):
        raise ValueError("failed or incompatible browser witness")
    observed=report.get("steps",[])
    if tuple(x.get("name") for x in observed)!=STEPS:
        raise ValueError("incomplete ordered state transition")
    if (observed[0].get("release")!=a or observed[1].get("state")!="stale" or
        observed[1].get("pageStatePreserved") is not True or
        observed[3].get("historyPreserved") is not True or
        observed[4].get("serverRelease")!=b or
        observed[5].get("state")!="unverified"):
        raise ValueError("browser-state causality not established")
    screenshot=witness_dir/"stale-tab.png"
    if not screenshot.is_file() or report.get("staleScreenSHA256")!=sha(screenshot.read_bytes()):
        raise ValueError("missing or changed stale-page visual witness")
    pointer_headers,pointer=fetch(origin,"/__estate/current.json?receipt="+a[:8])
    state=json.loads(pointer)
    if (state.get("schema")!="fountain.estate.release-continuity.v1" or
        state.get("releaseId")!=a or state.get("publicPublished") is not False or
        pointer_headers.get("X-Estate-Release")!=a or
        pointer_headers.get("X-Estate-Authority")!="source-locked" or
        "no-store" not in pointer_headers.get("Cache-Control","")):
        raise ValueError("origin is not safely rolled back to A")
    html_headers,html=fetch(origin,"/estate/")
    if (html_headers.get("X-Estate-Release")!=a or
        "no-store" not in html_headers.get("Cache-Control","") or
        ("data-estate-release=\""+a+"\"").encode() not in html):
        raise ValueError("HTML not bound to current source-locked release")
    asset_headers,asset=fetch(origin,"/__estate/"+a+"/estate-release-continuity.js")
    if (asset_headers.get("X-Estate-Release")!=a or
        "immutable" not in asset_headers.get("Cache-Control","") or len(asset)<500):
        raise ValueError("immutable state client not read back")
    older_headers,_=fetch(origin,"/__estate/"+b+"/estate-shell.css")
    if "immutable" not in older_headers.get("Cache-Control",""):
        raise ValueError("promoted B assets did not survive rollback")
    return {
      "schema":SCHEMA,"status":"STAGE_ONLY_VERIFIED",
      "publicPromotionAuthorized":False,"productionEstatePublisherReceipt":None,
      "sourceHost":"author LAN Mac mini","sourceOrigin":origin,
      "activeReleaseAfterRollback":a,"simulatedPromotedRelease":b,
      "transitionSteps":[x["name"] for x in observed],
      "browserWitnessSHA256":sha((witness_dir/"witness.json").read_bytes()),
      "staleScreenshotSHA256":sha(screenshot.read_bytes()),
      "originHTMLSHA256":sha(html),
      "continuityAssetSHA256":sha(asset),
      "noStoreDocumentVerified":True,"noStoreAuthorityVerified":True,
      "immutableReleaseAssetsVerified":True,"rollbackVerified":True,
      "nativeIPadSafariAccepted":False,"fullPublicDomainAcceptance":False
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--origin",default="http://192.168.8.50:8201")
    p.add_argument("--release-a",required=True)
    p.add_argument("--release-b",required=True)
    p.add_argument("--witness",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    x=p.parse_args()
    cert=certify(x.origin,x.release_a,x.release_b,x.witness)
    if x.out.exists():raise SystemExit("refusing to overwrite a versioned witness")
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(cert,indent=2)+"\n")
    print(json.dumps({"status":cert["status"],"steps":len(cert["transitionSteps"]),
                      "publicPromotionAuthorized":False,"output":str(x.out)},indent=2))
