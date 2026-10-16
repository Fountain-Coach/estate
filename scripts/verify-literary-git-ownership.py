#!/usr/bin/env python3
"""Verify Git-owned literary source identities and bounded source-only recovery.

Never treats a Git object as a restored FountainStore, published book or
authorization. Never exports private manuscripts to public Estate Git.
"""
import argparse
import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'inventory/literary-git-ownership.json'
REPO_ROOT=ROOT.parents[1]
CHECKOUTS={
 'Fountain-Coach/works-benedikt-eickhoff':'werke-benedikt-eickhoff-de',
 'Fountain-Coach/solstice.fountain.coach':'estate-domain-owners/solstice.fountain.coach',
 'Fountain-Coach/fountain.coach':'estate-domain-owners/fountain.coach',
 'Fountain-Coach/teatro.fountain.coach':'estate-domain-owners/teatro.fountain.coach'
}
SCHEMA='fountain.estate.literary-git-ownership.v1'
REQUIRED_RECORD={'id','kind','title','ownerRepository','ownerCommit','sourcePath',
 'gitBlob','sourceSHA256','storeCorpusID','sourceState','storeRecoveryState',
 'publicationAdmission','detail'}
KINDS={'work','edition','corpus'}
OWNER_RE=re.compile(r'^Fountain-Coach/[A-Za-z0-9_.-]+$')
HEX40=re.compile(r'^[0-9a-f]{40}$')
HEX64=re.compile(r'^[0-9a-f]{64}$')
ID_RE=re.compile(r'^[a-z0-9][a-z0-9-]{1,100}$')
class Refusal(ValueError): pass

def refuse(why):
    raise Refusal(why)

def digest(value):
    return hashlib.sha256(value).hexdigest()

def validate(manifest):
    if not isinstance(manifest,dict) or manifest.get('schema')!=SCHEMA:
        refuse('invalid literary owner schema')
    expected={'schema','asOf','governingDecision','authority','gitSourceAuthority',
      'storeLiveTransactionalAuthority','gitDoesNotAuthorizePublication',
      'completeLibraryInventory','anyFountainStoreRestored',
      'independentCompleteStoreBackupVerified','records'}
    if set(manifest)!=expected or manifest['authority']!='Fountain-Coach/estate':
        refuse('unexpected authority / fields')
    for key in ('gitSourceAuthority','storeLiveTransactionalAuthority',
                'gitDoesNotAuthorizePublication'):
        if manifest[key] is not True:
            refuse('source/runtime/publication authorities conflated: '+key)
    for key in ('completeLibraryInventory','anyFountainStoreRestored',
                'independentCompleteStoreBackupVerified'):
        if manifest[key] is not False:
            refuse('unsupported acceptance claim: '+key)
    if manifest['governingDecision']!='docs/decisions/004-git-owned-literary-sources-and-fountainstore-recovery.md':
        refuse('unknown authority decision')
    rows=manifest['records']
    if not isinstance(rows,list) or not rows:
        refuse('no work ownership records')
    ids=set()
    for row in rows:
        if not isinstance(row,dict) or set(row)!=REQUIRED_RECORD:
            refuse('unrecognized source record fields')
        ident=row['id']
        if not isinstance(ident,str) or not ID_RE.fullmatch(ident) or ident in ids:
            refuse('missing/duplicate work ID')
        ids.add(ident)
        if row['kind'] not in KINDS or not isinstance(row['title'],str) or not row['title'].strip():
            refuse(ident+': invalid title/kind')
        if row['publicationAdmission']!='NOT_ASSERTED' or row['storeRecoveryState']!='UNVERIFIED':
            refuse(ident+': unsupported admission / Store restore')
        if not isinstance(row['detail'],str) or len(row['detail'])>260:
            refuse(ident+': invalid rationale')
        gitfields=('ownerRepository','ownerCommit','sourcePath','gitBlob','sourceSHA256')
        if row['sourceState']=='GIT_OBJECT_VERIFIED_LOCAL':
            if any(not row.get(key) for key in gitfields):
                refuse(ident+': incomplete Git source identity')
            if not OWNER_RE.fullmatch(row['ownerRepository']) or not HEX40.fullmatch(row['ownerCommit']):
                refuse(ident+': unrecognized Git owner/ref')
            if not HEX40.fullmatch(row['gitBlob']) or not HEX64.fullmatch(row['sourceSHA256']):
                refuse(ident+': invalid Git object or source digest')
            if row['sourcePath'].startswith('/') or any(x in ('','..') for x in row['sourcePath'].split('/')) or '\\' in row['sourcePath']:
                refuse(ident+': unsafe path')
        elif row['sourceState']=='STORE_SOURCE_ONLY_UNMIRRORED':
            if row['kind']!='corpus' or any(row.get(k) is not None for k in gitfields) or row['storeCorpusID']!=ident:
                refuse(ident+': Store-only source cannot fake Git ownership')
        else: refuse(ident+': unrecognized source status')
        if row['storeCorpusID'] is not None and not ID_RE.fullmatch(row['storeCorpusID']):
            refuse(ident+': unrecognized corpus ID')
    return manifest

def owner_checkout(row):
    name=row['ownerRepository']
    if name not in CHECKOUTS:
        refuse('Git owner checkout not independently registered')
    path=REPO_ROOT/CHECKOUTS[name]
    origin=subprocess.check_output(['git','-C',str(path),'remote','get-url','origin'],text=True).strip()
    if name+'.git' not in origin and not origin.endswith(name):
        refuse('Git remote does not match declared owner')
    return path

def local_verify(manifest):
    # The original-author source repository now owns a machine-readable
    # work manifest. A downstream Estate entry must match that Git-authored
    # owner declaration; the Estate cannot independently rename a source.
    originals_repo='Fountain-Coach/works-benedikt-eickhoff'
    originals_path=owner_checkout({'ownerRepository':originals_repo})
    authored=json.loads(subprocess.check_output(
        ['git','-C',str(originals_path),'show','HEAD:literary/works.json']))
    if authored.get('schema')!='fountain.literary.source-owner.v1' or authored.get('sourceOwner')!=originals_repo:
        refuse('invalid canonical author Git manifest')
    authored_works={w['workID']:w for w in authored.get('works',[])}
    if len(authored_works)!=len(authored.get('works',[])):
        refuse('duplicate canonical author work identity')
    count=0
    for row in manifest['records']:
        if row['sourceState']!='GIT_OBJECT_VERIFIED_LOCAL':continue
        if row['ownerRepository']==originals_repo:
            own=authored_works.get(row['id'])
            if own is None or (own['title']!=row['title'] or
                own['originalPath']!=row['sourcePath'] or
                own['sourceGitBlob']!=row['gitBlob'] or
                own['sourceSHA256']!=row['sourceSHA256']):
                refuse('Estate literary metadata diverged from owning Git work: '+row['id'])
        path=owner_checkout(row)
        revision=row['ownerCommit']
        ref=revision+':'+row['sourcePath']
        obj=subprocess.check_output(['git','-C',str(path),'rev-parse',ref],text=True).strip()
        if obj!=row['gitBlob']:refuse('Git blob changed: '+row['id'])
        body=subprocess.check_output(['git','-C',str(path),'show',ref])
        if digest(body)!=row['sourceSHA256']:refuse('source SHA-256 changed: '+row['id'])
        count+=1
    return count

def github_recovery(manifest,source_id,destination):
    """GitHub remote independent of local checkout; reconstruct one author source.

    Download from the GitHub blob API using configured user's authorization.
    Does not import into FountainStore and does not write into this public repo.
    """
    row=next((r for r in manifest['records'] if r['id']==source_id),None)
    if row is None or row['sourceState']!='GIT_OBJECT_VERIFIED_LOCAL':
        refuse('unowned source not eligible for remote recovery')
    repo=row['ownerRepository']
    endpoint='repos/'+repo+'/git/blobs/'+row['gitBlob']
    payload=json.loads(subprocess.check_output(['gh','api',endpoint],text=True))
    if payload.get('encoding')!='base64' or payload.get('sha')!=row['gitBlob']:
        refuse('remote GitHub object identity mismatch')
    data=base64.b64decode(payload['content'],validate=False)
    git_hash=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if git_hash!=row['gitBlob'] or digest(data)!=row['sourceSHA256']:
        refuse('remote GitHub source integrity mismatch')
    dest=Path(destination)
    if dest.exists():refuse('refusing to overwrite any existing recovery source')
    dest.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    dest.write_bytes(data)
    dest.chmod(0o600)
    if digest(dest.read_bytes())!=row['sourceSHA256']:
        dest.unlink(missing_ok=True)
        refuse('reconstructed artifact failed independent disk readback')
    return {'id':source_id,'gitOwner':repo,'gitBlob':git_hash,
            'sha256':digest(data),'bytes':len(data),
            'result':'SOURCE_OBJECT_RECONSTRUCTED_ONLY',
            'storeRestore':'NOT_ATTEMPTED','publication':'NOT_AUTHORIZED'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=('verify','local-verify','github-recover'))
    parser.add_argument('--source-id')
    parser.add_argument('--output')
    args=parser.parse_args()
    manifest=validate(json.loads(MANIFEST.read_text()))
    if args.mode=='local-verify':
        print('LOCAL_GIT_SOURCE_OBJECTS_VERIFIED',local_verify(manifest))
    elif args.mode=='github-recover':
        if not args.source_id or not args.output:
            refuse('remote drill requires exact source and private output destination')
        print(json.dumps(github_recovery(manifest,args.source_id,args.output),sort_keys=True))
    else: print('LITERARY_GIT_OWNERSHIP_METADATA_VALID',len(manifest['records']))
if __name__=='__main__':
    try:main()
    except (Refusal,subprocess.CalledProcessError) as exc:
        raise SystemExit('BLOCKED: '+str(exc))
