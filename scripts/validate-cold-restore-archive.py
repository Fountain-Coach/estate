#!/usr/bin/env python3
"""Validate and safely unpack a public, immutable recovery-candidate bundle.

The archive is NOT an authorized production release. Operates only in a new,
isolated target directory; no network calls, Caddy changes, DNS or credentials.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

EXPECTED_SCHEMA="fountain.estate.public-static-cold-restore-snapshot.v1"
MAX_UNPACKED_BYTES=1_000_000_000

def sha_stream(path):
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--sha256",required=True)
    args=parser.parse_args()
    if sha_stream(args.archive)!=args.sha256:
        raise SystemExit("REJECTED: archive SHA-256 differs")
    target=args.target.resolve()
    if target.exists():
        raise SystemExit("REJECTED: target must not exist")
    target.mkdir(parents=True,mode=0o700)
    extracted=set()
    total=0
    with tarfile.open(args.archive,"r:gz") as bundle:
        for member in bundle:
            name=member.name
            path=PurePosixPath(name)
            if not member.isfile() or path.is_absolute() or ".." in path.parts or "." in path.parts:
                raise SystemExit("REJECTED: unsafe archive member "+name)
            if path.as_posix() not in ("manifest.json","Caddyfile") and (
                 len(path.parts)<3 or path.parts[0]!="sites"):
                raise SystemExit("REJECTED: unexpected recovery member "+name)
            if name in extracted:
                raise SystemExit("REJECTED: duplicate archive entry "+name)
            if member.size>30_000_000:
                raise SystemExit("REJECTED: oversized member "+name)
            total+=member.size
            if total>MAX_UNPACKED_BYTES:
                raise SystemExit("REJECTED: archive exceeds size limit")
            destination=target.joinpath(*path.parts)
            destination.parent.mkdir(parents=True,exist_ok=True)
            with bundle.extractfile(member) as src, destination.open("xb") as dst:
                digest=hashlib.sha256()
                count=0
                for chunk in iter(lambda: src.read(1024*1024),b""):
                    dst.write(chunk);digest.update(chunk);count+=len(chunk)
                if count!=member.size:
                    raise SystemExit("REJECTED: incomplete archive member "+name)
            extracted.add(name)
    manifest=json.loads((target/"manifest.json").read_text())
    if manifest["schema"]!=EXPECTED_SCHEMA or manifest["releaseAdmitted"] is not False or manifest["authorizedForProduction"] is not False:
        raise SystemExit("REJECTED: not an unadmitted public snapshot")
    hostnames=set(manifest["hostnames"])
    if len(hostnames)!=9:
        raise SystemExit("REJECTED: unexpected public host set")
    observed={}
    for record in manifest["records"]:
        name=record["bundlePath"]
        if name not in extracted or not name.startswith("sites/"):
            raise SystemExit("REJECTED: missing or unsafe resource "+name)
        if name in observed and observed[name]!=record["sha256"]:
            raise SystemExit("REJECTED: conflicting aliases "+name)
        observed[name]=record["sha256"]
    if len(manifest["records"])!=manifest["public200EvidenceCount"] or len(observed)!=manifest["uniqueFilesOnDisk"]:
        raise SystemExit("REJECTED: manifest count mismatch")
    if extracted!=set(observed).union({"Caddyfile","manifest.json"}):
        raise SystemExit("REJECTED: manifest does not enumerate all archived data")
    for path,expected in observed.items():
        if path.split("/")[1] not in hostnames or sha_stream(target/path)!=expected:
            raise SystemExit("REJECTED: unverified restored file "+path)
    caddy=(target/"Caddyfile").read_text()
    if "admin off" not in caddy or "auto_https off" not in caddy or ":18480" not in caddy:
        raise SystemExit("REJECTED: unexpected Caddy listener/control configuration")
    print("LOCAL_RESTORE_ARCHIVE_VERIFIED",len(hostnames),"hosts",
          len(manifest["records"]),"public URLs",len(observed),"unique files",
          total,"unpacked bytes")
    print("RECOVERY_ROOT",target)
    print("RELEASE_ADMITTED",manifest["releaseAdmitted"])

if __name__=="__main__":
    main()
