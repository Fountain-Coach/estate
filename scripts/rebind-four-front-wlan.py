#!/usr/bin/env python3
"""Repair a disposable Fountain Coach WLAN preview when its former bind IP vanished.

Only updates the staging release's absolute local links, the locally installed
three-front preview server's IP, and the protected archive's local return links.
Never writes Git-owned source sites, media, host DNS, Caddy, or production Store.
"""
import argparse
import ipaddress
import json
from pathlib import Path
from shutil import copy2

ROOT=Path("/home/benedikt/estate-three-front-staging")
ARCHIVE=Path("/home/benedikt/services/satzfunk-private-video-browser/archive/browser")
OLD="192.168.8.249"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--release",type=Path,required=True)
    p.add_argument("--bind",default="192.168.8.50")
    a=p.parse_args()
    ip=ipaddress.IPv4Address(a.bind)
    if not ip in ipaddress.IPv4Network("192.168.8.0/24"):
        raise SystemExit("Expected owner-managed LAN address")
    rel=a.release.resolve()
    if rel.parent != ROOT / "releases":
        raise SystemExit("Refusing anything outside disposable release")
    if (ROOT/"current").resolve()!=rel:
        raise SystemExit("Refusing non-current local release")
    src=f"http://{OLD}:"
    dst=f"http://{ip}:"
    changes={}
    for site in ("fountain","solstice","teatro"):
        edited=[]
        for file in (rel/site).rglob("*"):
            if file.suffix not in (".html",".js",".json",".css",".mjs") or not file.is_file():
                continue
            if file.name=="source-lock.json":
                continue
            s=file.read_text(encoding="utf-8")
            if src not in s:
                continue
            file.write_text(s.replace(src,dst),encoding="utf-8")
            edited.append(str(file.relative_to(rel)))
        changes[site]=len(edited)
    script=ROOT/"serve-wlan-staging.py"
    original=script.read_text()
    oldline='IP = "'+OLD+'"'
    newline='IP = "'+str(ip)+'"'
    if oldline in original:
        backup=ROOT/("serve-wlan-staging.py.pre-four-front-"+OLD)
        if backup.exists():
            raise SystemExit("Existing server backup must be inspected")
        copy2(script,backup)
        script.write_text(original.replace(oldline,newline))
    elif newline not in original:
        raise SystemExit("Unexpected staging server binding; no mutation")
    for name in ("index.html","7vst-originals.html"):
        file=ARCHIVE/name
        s=file.read_text()
        if 'data-estate-stage="four-front-v1"' not in s:
            raise SystemExit("Expected approved Satzfunk local navigation")
        if src in s:
            file.write_text(s.replace(src,dst))
    lockfile=rel/"source-lock.json"
    lock=json.loads(lockfile.read_text())
    if lock.get("productionPublished") is not False:
        raise SystemExit("Not a local stage")
    lock["localEstateAddition"]["estateBindIP"]=str(ip)
    lock["localEstateAddition"]["retargetedLocalLinks"]=changes
    lock["localEstateAddition"]["legacyBindIP"]=OLD
    lockfile.write_text(json.dumps(lock,indent=2)+"\n")
    print(json.dumps({"bind":str(ip),"localLinks":changes,
                      "sourceMediaUntouched":True,"previousConfigPreserved":True},indent=2))
if __name__=="__main__":
    main()
