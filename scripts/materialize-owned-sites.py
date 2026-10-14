#!/usr/bin/env python3
"""Source-first scoped materialization into an existing EstatePublisher checkout.

Owning GitHub repositories are authority; the old estate/sites folders are
derived projections. This performs NO public release, Caddy mutation or Git
remote mutation. --apply is explicit and preserves unrecognized extra assets.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=json.loads((ROOT/'manifest.json').read_text())
FEATURED={'fountain.coach','teatro.fountain.coach','solstice.fountain.coach'}

def digest(value):
    return hashlib.sha256(value).hexdigest()

def get_owner(host,checkouts):
    owner=checkouts/host
    site=owner/'site'
    edition=owner/'edition.json'
    inv=owner/'publication-files.sha256'
    if not owner.is_dir() or not site.is_dir() or not edition.is_file() or not inv.is_file():
        raise ValueError('No complete Git owner checkout for '+host)
    remote=subprocess.check_output(['git','-C',str(owner),'remote','get-url','origin'],text=True).strip()
    if 'Fountain-Coach/'+host+'.git' not in remote and not remote.endswith('Fountain-Coach/'+host):
        raise ValueError('Owner Git remote identity unexpected '+host+': '+remote)
    sha=subprocess.check_output(['git','-C',str(owner),'rev-parse','HEAD'],text=True).strip()
    edition_info=json.loads(edition.read_text())
    if edition_info['repository']!='Fountain-Coach/'+host:raise ValueError('Edition claims unexpected owner')
    required={}
    for line in inv.read_text().splitlines():
        itemhash,sep,name=line.partition('  ')
        if not sep or name in required or '..' in Path(name).parts:
            raise ValueError('Broken inventory in '+host)
        required[name]=itemhash
    source={x.relative_to(site).as_posix():digest(x.read_bytes()) for x in site.rglob('*') if x.is_file()}
    if source!=required or digest(inv.read_bytes())!=edition_info['sourceSha256Inventory']:
        raise ValueError('Owning Git source digest mismatch for '+host)
    return owner,sha,source

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('--checkouts',type=Path,required=True)
    cli.add_argument('--estate',type=Path,required=True)
    cli.add_argument('--host',action='append',choices=sorted(FEATURED))
    cli.add_argument('--apply',action='store_true')
    args=cli.parse_args()
    hosts=args.host or sorted(FEATURED)
    records=[]
    for host in hosts:
        source,revision,files=get_owner(host,args.checkouts)
        estate=args.estate.resolve()
        target=estate/'estate'/'sites'/host
        if target.resolve()!=target or not target.is_dir() or target.parent.name!='sites':
            raise ValueError('Invalid exact derived target '+str(target))
        # Generated print proof bundles were never admitted as source files.
        differences=[name for name,sha in files.items() if not (target/name).is_file() or digest((target/name).read_bytes())!=sha]
        print('OWNER',host,revision,'tracked',len(files),'diff',len(differences),'APPLY',args.apply)
        if args.apply:
            for name in differences:
                dst=target/name;dst.parent.mkdir(parents=True,exist_ok=True)
                temp=dst.with_name(dst.name+'.git-owner-temp')
                shutil.copyfile(source/'site'/name,temp)
                os.replace(temp,dst)
            assert all(digest((target/name).read_bytes())==sha for name,sha in files.items())
        records.append(dict(host=host,sourceRepo='Fountain-Coach/'+host,sourceRevision=revision,
                            files=len(files),differences=len(differences),materialized=args.apply,
                            derivedRoot='estate/sites/'+host))
    if args.apply:
        lock=estate/'estate'/'github-source-lock.json'
        previous=json.loads(lock.read_text()) if lock.exists() else {'schema':'fountain.estate.github-source-lock.v1','owners':{}}
        for row in records:
            previous['owners'][row['host']]={k:v for k,v in row.items() if k not in ('differences','materialized')}
        previous['registry']='Fountain-Coach/estate'
        previous['releaseStatus']='derived-local-only; not a production release'
        lock.write_text(json.dumps(previous,indent=2)+'\n')
        print('GITHUB_OWNED_DERIVED_LOCK',str(lock))
    return 0
if __name__=='__main__':raise SystemExit(main())
