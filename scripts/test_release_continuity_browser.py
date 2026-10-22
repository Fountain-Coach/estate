#!/usr/bin/env python3
"""One automated browser-state scenario, not a manual browser matrix.

A: load pinned release; server atomically moves to B; old page must detect
staleness without losing local page state, user can deliberately navigate
to B; a new isolated context must immediately see B. Always restore A.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://192.168.8.50:8201"
STORE="/home/benedikt/estate-release-continuity-staging"
REMOTE="MacMiniDocker"

def run(command):
    result=subprocess.run(["ssh",REMOTE,command],capture_output=True,text=True,timeout=15)
    if result.returncode:raise RuntimeError(result.stderr+" "+result.stdout)
    return result.stdout.strip()

def promote(release):
    if len(release)!=64 or any(c not in "0123456789abcdef" for c in release):
        raise ValueError("invalid immutable release")
    run("python3 "+STORE+"/release_continuity.py verify --store "+STORE+" >/dev/null") # check current before swap
    run("test -f "+STORE+"/releases/"+release+"/release-manifest.json && "+
        "ln -s releases/"+release+" "+STORE+"/current.next && "+
        "mv -Tf "+STORE+"/current.next "+STORE+"/current")
    current=run("readlink "+STORE+"/current")
    if current!="releases/"+release:raise RuntimeError("pointer switch unconfirmed")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--release-a",required=True)
    ap.add_argument("--release-b",required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    proof={"scenario":"estate.browser-release-continuity","browser":"isolated Mac Chromium profile",
           "notNativeIPad":True,"publicPublished":False,"steps":[],"errors":[]}
    promote(args.release_a)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                headless=True,args=["--no-sandbox"])
            try:
                old=browser.new_context(service_workers="block",viewport={"width":1050,"height":780})
                page=old.new_page()
                page.goto(BASE+"/estate/",wait_until="domcontentloaded",timeout=20000)
                page.wait_for_function("document.documentElement.dataset.estateFreshness === 'fresh'",
                                        timeout=12000)
                assert page.locator("html").get_attribute("data-estate-release")==args.release_a
                proof["steps"].append({"name":"A fresh anonymous session","state":"fresh",
                                       "release":args.release_a})
                page.evaluate("window.__unsavedLocalWork='untouched-marker';")
                promote(args.release_b)
                # Same tab, with no browser-history clearing and no reload:
                state=page.evaluate("() => window.EstateReleaseContinuity.check()")
                assert state=="stale",("did not detect old loaded DOM",state)
                assert page.locator("html").get_attribute("data-estate-freshness")=="stale"
                assert page.locator("[data-estate-release-notice]").count()==1
                assert page.evaluate("window.__unsavedLocalWork")=="untouched-marker"
                assert page.locator("html").get_attribute("data-estate-release")==args.release_a
                page.screenshot(path=str(args.output/"stale-tab.png"),full_page=False)
                proof["steps"].append({"name":"Retained A tab detects B without reload",
                                      "state":"stale","pageStatePreserved":True})
                fresh=browser.new_context(service_workers="block")
                try:
                    page2=fresh.new_page()
                    page2.goto(BASE+"/estate/",wait_until="domcontentloaded",timeout=20000)
                    page2.wait_for_function("document.documentElement.dataset.estateFreshness === 'fresh'",
                                            timeout=12000)
                    assert page2.locator("html").get_attribute("data-estate-release")==args.release_b
                    proof["steps"].append({"name":"New isolated session starts B","state":"fresh"})
                finally:
                    fresh.close()
                page.locator("[data-estate-release-notice] button").click()
                page.wait_for_load_state("domcontentloaded",timeout=12000)
                page.wait_for_function("document.documentElement.dataset.estateFreshness === 'fresh'",
                                       timeout=12000)
                assert page.locator("html").get_attribute("data-estate-release")==args.release_b
                assert "estate_release="+args.release_b in page.url
                proof["steps"].append({"name":"Deliberate, ordinary navigation to B","state":"fresh",
                                      "historyPreserved":True})
                page.go_back(wait_until="domcontentloaded",timeout=15000)
                result=page.evaluate("() => window.EstateReleaseContinuity.check()")
                assert result in ("fresh","stale")
                server_release=page.locator("html").get_attribute("data-estate-current-release")
                assert server_release==args.release_b
                proof["steps"].append({"name":"Back navigation never claims old A current",
                                      "state":result,"serverRelease":server_release})
                # A loss of authority must never be interpreted as 'fresh'.
                page.route("**/__estate/current.json*",lambda route:route.abort())
                unknown=page.evaluate("() => window.EstateReleaseContinuity.check()")
                assert unknown in ("unverified","stale"),unknown
                proof["steps"].append({"name":"Disconnected authority refuses freshness",
                                      "state":unknown})
                old.close()
            finally:browser.close()
    except Exception as exc:
        proof["errors"].append(str(exc))
    finally:
        try:promote(args.release_a)
        except Exception as exc:proof["errors"].append("rollback: "+str(exc))
    proof["passed"]=not proof["errors"] and len(proof["steps"])==6
    screenshot=args.output/"stale-tab.png"
    if screenshot.exists():
        proof["staleScreenSHA256"]=hashlib.sha256(screenshot.read_bytes()).hexdigest()
    (args.output/"witness.json").write_text(json.dumps(proof,indent=2)+"\n")
    print(json.dumps({"passed":proof["passed"],"checks":proof["steps"],
                      "errors":proof["errors"]},indent=2))
    return 0 if proof["passed"] else 1

if __name__=="__main__":raise SystemExit(main())
