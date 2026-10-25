#!/usr/bin/env python3
"""Prepare an immutable, source-locked public EstateShell candidate; never deploy.

Use exactly the existing Git owner's PUBLIC site directory and SHA inventory.
No network, no new service, no Store dependency, and no public effects.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

from project_public_estate_shell import project_public
from estate_shell import manifest, VERSION

def sha(data):
    return hashlib.sha256(data).hexdigest()

def exact_public_source(site: Path, sha_file: Path):
    recorded={}
    for line in sha_file.read_text().splitlines():
        digest, sep, rel=line.partition('  ')
        if not sep or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('invalid SHA-256 source inventory')
        p=Path(rel)
        if any(part == '.git' or part.startswith('.env') or part in ('secrets','private') for part in p.parts) or p.suffix in ('.key','.p12','.pem'):
            raise ValueError('private files forbidden in public source')
        if p.is_absolute() or '..' in p.parts or not p.parts or rel in recorded:
            raise ValueError('untrusted source inventory path')
        recorded[rel]=digest
    current={}
    for p in site.rglob('*'):
        if p.is_symlink():raise ValueError('source symlink forbidden')
        if p.is_file():
            rel=p.relative_to(site).as_posix()
            if rel not in recorded:raise ValueError('unlisted public source: '+rel)
            current[rel]=sha(p.read_bytes())
    if current!=recorded:
        missing=set(recorded)-set(current)
        wrong={p for p in recorded.keys()&current.keys() if recorded[p]!=current[p]}
        raise ValueError('source inventory differs: missing='+str(sorted(missing))+' wrong='+str(sorted(wrong)))
    return recorded

def prepare(site_root, sha_manifest, owner, canonical, source_revision,
            output, receipt, assets_dir, route_manifest=None):
    site_root=Path(site_root).resolve()
    output=Path(output).resolve()
    receipt=Path(receipt).resolve()
    if len(source_revision)!=40 or any(x not in '0123456789abcdef' for x in source_revision):
        raise ValueError('source revision must be the exact 40-char Git commit SHA')
    if owner not in ('estate','book','governance','midi2','instruments','teatro','pointer','solstice'):
        raise ValueError('not a public editorial source owner')
    if output.exists() or receipt.exists():raise ValueError('immutable candidate or receipt already exists')
    if output == site_root or site_root in output.parents or output in site_root.parents:
        raise ValueError('candidate must be outside source-owned site root')
    if receipt == site_root or site_root in receipt.parents or output == receipt or output in receipt.parents:
        raise ValueError('receipt must not write into source or served candidate')
    original=exact_public_source(site_root,Path(sha_manifest))
    if not any(p.endswith('.html') for p in original):raise ValueError('site has no HTML routes')
    if owner=='governance' and route_manifest is None:
        raise ValueError('Governance route manifest required')
    if route_manifest is not None:
        routes=json.loads(Path(route_manifest).read_text())
        owner_hosts={'estate':'fountain.coach','book':'book.fountain.coach',
                     'governance':'governance.fountain.coach','midi2':'midi2.fountain.coach',
                     'instruments':'instruments.fountain.coach','teatro':'teatro.fountain.coach',
                     'pointer':'benedikt-eickhoff.de','solstice':'works.benedikt-eickhoff.de'}
        if routes.get('host')!=owner_hosts[owner]:
            raise ValueError('route manifest host mismatch')
        required={p.lstrip('/') for row in routes['routes'] for p in row['publicPaths']}
        if not required.issubset(original):raise ValueError('declared public routes missing from source')
    if output.parent == Path('/'):raise ValueError('unsafe output destination')
    assets_dir=Path(assets_dir).resolve()
    if output == assets_dir or assets_dir in output.parents:
        raise ValueError('candidate may not mutate EstateShell source')
    estate_assets={
        'assets/estate-shell.css': assets_dir/'estate-shell.css',
        'assets/estate-shell-state.js':assets_dir/'estate-shell-state.js',
        'assets/estate-shell-logo.png':assets_dir/'assets/estate-shell-logo.png',
    }
    if set(original)&set(estate_assets):raise ValueError('source already owns common shell asset: abort')
    if not all(x.is_file() and not x.is_symlink() for x in estate_assets.values()):
        raise ValueError('versioned shared shell assets missing')
    asset_names={
        name:'/assets/'+Path(name).stem+'-'+sha(asset.read_bytes())[:16]+Path(name).suffix
        for name,asset in estate_assets.items()
    }
    if len(set(asset_names.values()))!=3:
        raise ValueError('shared asset fingerprint collision')
    if any(name.lstrip('/') in original for name in asset_names.values()):
        raise ValueError('source already owns a fingerprinted shell asset')
    asset_urls={'/'+k:v for k,v in asset_names.items()}
    output.mkdir(parents=True)
    source_receipts={}
    try:
        for rel in sorted(original):
            source=site_root/rel
            target=output/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            if source.suffix.lower()=='.html':
                projected,info=project_public(source.read_text(encoding='utf8'),owner,canonical,asset_urls=asset_urls)
                target.write_text(projected,encoding='utf8')
                source_receipts[rel]=info
            else:
                shutil.copy2(source,target)
        for rel,source in estate_assets.items():
            target=output/asset_names[rel].lstrip('/')
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
        results={p.relative_to(output).as_posix():sha(p.read_bytes())
                 for p in output.rglob('*') if p.is_file()}
        record={
            'schema':'fountain.estate.public-candidate.v1',
            'releaseIntent':'CANDIDATE-ONLY',
            'publicReleased':False,'publisherApproval':None,
            'owner':owner,'sourceRevision':source_revision,
            'sourceFileCount':len(original),'projectedHTMLCount':len(source_receipts),
            'sourceInventorySHA256':sha(Path(sha_manifest).read_bytes()),
            'shellVersion':VERSION,
            'sharedCSSSHA256':results[asset_names['assets/estate-shell.css'].lstrip('/')],
            'sharedLogoSHA256':results[asset_names['assets/estate-shell-logo.png'].lstrip('/')],
            'sharedAssetURLs':asset_urls,
            'retainedAuthoredWorkSHA256':{p:r['sourceWorkSHA256'] for p,r in source_receipts.items()},
            'candidateFilesSHA256':results,
            'rollbackRelease':None,
            'nativeWebKitAccepted':False,
            'independentHTTPSReadback':False,
        }
        receipt.parent.mkdir(parents=True,exist_ok=True)
        receipt.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        return record
    except BaseException:
        shutil.rmtree(output)
        raise

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--site',type=Path,required=True)
    p.add_argument('--source-manifest',type=Path,required=True)
    p.add_argument('--source-revision',required=True)
    p.add_argument('--identity',required=True)
    p.add_argument('--reel',type=Path,required=True)
    p.add_argument('--shell',type=Path,default=Path(__file__).resolve().parents[1]/'shell')
    p.add_argument('--route-manifest',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--receipt',type=Path,required=True)
    a=p.parse_args()
    try:
        result=prepare(a.site,a.source_manifest,a.identity,manifest(a.reel),
                       a.source_revision,a.out,a.receipt,a.shell,a.route_manifest)
        print(json.dumps({key:result[key] for key in (
            'owner','sourceRevision','sourceFileCount','projectedHTMLCount',
            'sharedCSSSHA256','shellVersion','publicReleased')},indent=2))
    except (ValueError,OSError,KeyError) as err:
        print('REFUSED:',err,file=sys.stderr)
        return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
