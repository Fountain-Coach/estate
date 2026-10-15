#!/usr/bin/env python3
"""Verify owner-Git custody for previously missing public publication bytes.

Pinned commits and public-response SHA-256 are checked offline. No publishing.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
DEV=ROOT.parents[1]
REC=ROOT/'recovery'
LOCK=REC/'owner-readback-custody.json'
EVIDENCE=REC/'public-byte-provenance.json'
CENSUS=REC/'public-route-census.json'
OWNERS={
 'Fountain-Coach/book-of-reframe':DEV/'press-source-checkouts/book-of-reframe',
 'Fountain-Coach/midi2':DEV/'press-source-checkouts/midi2',
 'Fountain-Coach/solstice.fountain.coach':DEV/'estate-domain-owners/solstice.fountain.coach',
}
def digest(data):return hashlib.sha256(data).hexdigest()
def git(path,*args):
    r=subprocess.run(['git',*args],cwd=path,capture_output=True)
    if r.returncode:raise RuntimeError('Missing pinned Git object '+str(args))
    return r.stdout
def public_evidence():
    data=json.loads(EVIDENCE.read_text())
    if data['releaseAdmitted'] or not data['owningSourcesUntouched']:raise RuntimeError('Invalid historic publication evidence')
    previous={}
    for section in data['sections']:
        owner=section['canonicalOwnerRepo']
        if owner in ('Fountain-Coach/book-of-reframe','Fountain-Coach/midi2'):
            rows=[r for r in section['files'] if r['state']=='PUBLIC_BYTES_NOT_LOCATED']
            previous[owner]={r['publicUrl']:r['publicSHA256'] for r in rows}
    assert set(previous)==set(OWNERS)-{'Fountain-Coach/solstice.fountain.coach'}
    assert sum(len(group) for group in previous.values())==5
    census=json.loads(CENSUS.read_text())
    live={r['url']:r for r in census['results'] if r['status']==200 and r['sha256']}
    return previous,live
def owner_check(repo):
    path=OWNERS[repo]
    origin=git(path,'remote','get-url','origin').decode().strip()
    if not origin.endswith(repo+'.git') and not origin.endswith(repo):
        raise RuntimeError('Unexpected Git source owner origin '+origin)
    return path
def source_blob(path,rev,p):
    return git(path,'show',rev+':'+p)
def verify_receipt(row,previous,live):
    repo=row['ownerRepo'];rev=row['commit']
    if repo not in OWNERS or len(rev)!=40 or not all(c in '0123456789abcdef' for c in rev):
        raise RuntimeError('Unrecognized owner or Git revision')
    path=owner_check(repo)
    doc='publication-recovery/2026-10-15/receipt.json'
    rec=json.loads(source_blob(path,rev,doc))
    if rec['ownerRepository']!=repo:raise RuntimeError('Receipt owner mismatch')
    if repo=='Fountain-Coach/solstice.fountain.coach':
        items=rec['artifacts']
        if len(items)!=5:raise RuntimeError('Missing Solstice public proofs')
        for item in items:
            public=item['publicUrl']
            if not public.startswith('https://works.benedikt-eickhoff.de/solstice/'):raise RuntimeError('Invalid Solstice public domain')
            if public not in live or item['sha256']!=live[public]['sha256']:raise RuntimeError('Solstice witness mismatch')
            data=source_blob(path,rev,item['ownerSnapshotPath'])
            if digest(data)!=item['sha256'] or len(data)!=item['bytes']:
                raise RuntimeError('Solstice Git blob mismatch')
    else:
        items=rec['documents']
        if len(items)!=len(previous[repo]):raise RuntimeError('Incomplete owner readback')
        for item in items:
            public=item['publicUrl']
            if public not in previous[repo] or item['sha256']!=previous[repo][public]:
                raise RuntimeError('Owner publication readback mismatch')
            data=source_blob(path,rev,item['recoveryPath'])
            if digest(data)!=item['sha256'] or len(data)!=item['bytes']:
                raise RuntimeError('Owner HTML Git blob mismatch')
    return len(items)
def verify_solstice_direct_assets(rev,live):
    owner='Fountain-Coach/solstice.fountain.coach'
    path=owner_check(owner);items=[]
    for relative in ('assets/press-accepted.css','assets/press-accepted.js'):
        public='https://works.benedikt-eickhoff.de/solstice/'+relative
        data=source_blob(path,rev,'site/'+relative)
        sha=digest(data)
        if public not in live or live[public]['sha256']!=sha:
            raise RuntimeError('Solstice direct source asset differs from public witness: '+relative)
        items.append(dict(ownerRepo=owner,revision=rev,gitPath='site/'+relative,publicUrl=public,sha256=sha))
    return items
def make(records):
    previous,live=public_evidence()
    if len(records)!=3 or set(r['ownerRepo'] for r in records)!=set(OWNERS):
        raise RuntimeError('Incomplete owning repositories')
    count=sum(verify_receipt(r,previous,live) for r in records)
    if count!=10:raise RuntimeError('Incomplete public owner byte custody')
    solstice=next(r for r in records if r['ownerRepo']=='Fountain-Coach/solstice.fountain.coach')
    assets=verify_solstice_direct_assets(solstice['commit'],live)
    return dict(schema='fountain.estate.owner-public-byte-custody.v2',
       sourceHTMLProvenanceSHA256=digest(EVIDENCE.read_bytes()),
       publicCensusSHA256=digest(CENSUS.read_bytes()),
       capturedDate='2026-10-15',ownerSnapshotCount=count,
       exactOwnerGitAssetCount=len(assets),
       ownerRecords=records,ownerDirectGitAssets=assets,
       sourceOwnershipUnchanged=True,releaseAdmitted=False,allowDeployment=False,
       completePublicReleaseProof=False,
       explanation='Ten public readbacks and two owner source assets pinned to committed owner Git objects; not a full approved static release')
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['build','verify'])
    p.add_argument('--book-commit');p.add_argument('--midi-commit');p.add_argument('--solstice-commit')
    args=p.parse_args()
    if args.action=='build':
        if not all((args.book_commit,args.midi_commit,args.solstice_commit)):
            raise RuntimeError('All three owner commits must be explicitly pinned')
        records=[
          dict(ownerRepo='Fountain-Coach/book-of-reframe',commit=args.book_commit,integration='main'),
          dict(ownerRepo='Fountain-Coach/midi2',commit=args.midi_commit,integration='main-squash-merge-pr-193'),
          dict(ownerRepo='Fountain-Coach/solstice.fountain.coach',commit=args.solstice_commit,integration='main')]
    else:
        if not LOCK.exists():raise RuntimeError('Custody record absent')
        records=json.loads(LOCK.read_text())['ownerRecords']
    result=make(records)
    encoded=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.action=='build':LOCK.write_text(encoded)
    elif LOCK.read_text()!=encoded:raise RuntimeError('Stale/tampered custody lock')
    print('OWNER_GIT_CUSTODY_'+('BUILT' if args.action=='build' else 'VERIFIED'),
          result['ownerSnapshotCount'],'public snapshots,',
          result['exactOwnerGitAssetCount'],'source assets, admitted',result['releaseAdmitted'])
if __name__=='__main__':main()
