#!/usr/bin/env python3
"""Build/verify a frozen PUBLIC static estate snapshot from independent Git evidence.

Do not treat as a last-public release admission. Includes only byte-exact
HTTP 200 assets recorded by the nine-host 2026-10-15 public census. Does not
copy private runtime source, unpublished assets, credentials or Store state.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
DEV=ROOT.parents[1]
REC=ROOT/'recovery'
OUT=REC/'bundles'
BUNDLE=OUT/'estate-public-observed-20261015.tar.gz'
MANIFEST=OUT/'estate-public-observed-20261015.manifest.json'
REPORT=OUT/'README.md'
COVERAGE=REC/'public-git-coverage.json'
CENSUS=REC/'public-route-census.json'
OWNERS=ROOT/'inventory/domain-ownership.json'
ARCHIVE=DEV/'solstice-caddy-20261012'
MAX_SOURCE_FILE=25_000_000

def digest(b):return hashlib.sha256(b).hexdigest()
def git(path,*argv):
    result=subprocess.run(['git',*argv],cwd=path,capture_output=True)
    if result.returncode:
        raise RuntimeError('Unavailable pinned Git object '+str(argv)+' '+result.stderr.decode('utf8','replace')[:200])
    return result.stdout
def path_for_url(url):
    u=urlsplit(url)
    if u.scheme!='https' or not u.hostname or u.query or u.fragment or u.username:
        raise ValueError('Invalid public URL '+url)
    raw=unquote(u.path or '/')
    if '\\' in raw or '\x00' in raw or not raw.startswith('/') or '//' in raw:raise ValueError('Unsafe path '+raw)
    parts=raw.lstrip('/').split('/')
    if any(s in ('.','..') for s in parts):raise ValueError('Traversal in '+url)
    relative=raw.lstrip('/')
    if relative=='' or relative.endswith('/'):relative+='index.html'
    if relative.startswith('.') and not relative.startswith('.well-known/'):
        raise ValueError('Unapproved hidden public destination '+relative)
    return 'sites/'+u.hostname+'/'+relative
def caddyfile(hosts):
    lines=['{','  admin off','  auto_https off','}',':18480 {']
    for i,host in enumerate(hosts):
        lines+=['  @host'+str(i)+' host '+host,'  handle @host'+str(i)+' {',
          '    root * /srv/recovery/sites/'+host,
          '    file_server','  }']
    lines+=['  respond "Recovery host not admitted" 421','}']
    return ('\n'.join(lines)+'\n').encode()
def files():
    coverage=json.loads(COVERAGE.read_text())
    census=json.loads(CENSUS.read_text())
    owners=json.loads(OWNERS.read_text())
    candidates={s['repository']:(DEV/s['localCheckout']) for s in owners['sources']}
    if coverage['releaseAdmitted'] or coverage['allowDeployment']:
        raise RuntimeError('Coverage claims unsafe publication admission')
    if coverage['publicCensusSHA256']!=digest(CENSUS.read_bytes()):
        raise RuntimeError('Unmatched census witness digest')
    if coverage['counts'].get('PUBLIC_200_NOT_PROVEN_IN_PINNED_GIT',0):
        raise RuntimeError('Unverified public 200 resources')
    matches=[entry for entry in coverage['results'] if entry['httpStatus']==200]
    if len(matches)!=600:raise RuntimeError('Expected 600 exact public readback bytes, got '+str(len(matches)))
    paths={}
    records=[]
    for item in matches:
        matched=item.get('gitMatch')
        if not matched or not matched.get('gitRevision') or not matched.get('gitPath'):
            raise RuntimeError('Incomplete Git provenance '+item['url'])
        owner=matched['owner']
        base=ARCHIVE if matched['kind']=='EXACT_HISTORICAL_PROJECTION_GIT' else candidates.get(owner)
        if base is None:raise RuntimeError('Unknown owner for public artifact '+owner)
        data=git(base,'show',matched['gitRevision']+':'+matched['gitPath'])
        expected=item['liveSHA256']
        if digest(data)!=expected or matched['sha256']!=expected:
            raise RuntimeError('Git/public digest mismatch '+item['url'])
        if not data or len(data)>MAX_SOURCE_FILE:
            raise RuntimeError('Unexpected public asset size '+item['url'])
        dest=path_for_url(item['url'])
        if dest in paths and paths[dest]!=data:
            raise RuntimeError('Conflicting URL aliases at '+dest)
        paths[dest]=data
        records.append(dict(url=item['url'],bundlePath=dest,sha256=expected,bytes=len(data),
                    evidenceCategory=matched['kind'],gitOwner=owner,
                    gitCommit=matched['gitRevision'],gitPath=matched['gitPath']))
    hosts=sorted(census['hosts'])
    if len(hosts)!=9:raise RuntimeError('Expected nine public website hosts')
    paths['Caddyfile']=caddyfile(hosts)
    manifest=dict(schema='fountain.estate.public-static-cold-restore-snapshot.v1',
        basis='Frozen public HTTPS GET witness and byte-for-byte Git provenance, 2026-10-15',
        sourceCensusSHA256=digest(CENSUS.read_bytes()),sourceCoverageSHA256=digest(COVERAGE.read_bytes()),
        releaseAdmitted=False,authorizedForProduction=False,containsPrivateRuntimeState=False,
        sourceCompleteness='bounded 621 URL crawl, not exhaustive public release',
        hostnames=hosts,public200EvidenceCount=len(records),uniqueFilesOnDisk=len(paths)-1,
        non200Observations=sum(x['httpStatus']!=200 for x in coverage['results']),
        records=sorted(records,key=lambda r:r['url']))
    paths['manifest.json']=(json.dumps(manifest,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    return paths,manifest
def gzip_tar(paths):
    out=io.BytesIO()
    with gzip.GzipFile(fileobj=out,mode='wb',filename='',mtime=0,compresslevel=7) as gz:
        with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as tar:
            for name in sorted(paths):
                content=paths[name]
                meta=tarfile.TarInfo(name)
                meta.size=len(content);meta.mtime=0;meta.uid=meta.gid=0
                meta.uname=meta.gname=''
                meta.mode=0o644
                tar.addfile(meta,io.BytesIO(content))
    return out.getvalue()
def report(manifest,archive_len,archive_sha):
    return ('# Immutable observed public estate recovery candidate\n\n'
      '**Not approved for production deployment.** No dynamic/private state is represented.\n\n'
      'This tarball preserves exactly '+str(manifest['public200EvidenceCount'])+
      ' byte-verified public HTTPS resources under host-rooted paths and '+str(manifest['uniqueFilesOnDisk'])+
      ' unique filesystem destinations, with a Caddy origin file and SHA-256 manifest. '
      'The public crawl observed '+str(manifest['non200Observations'])+
      ' additional non-200 URLs and cannot prove absent/unlinked URLs, an atomic published release, or live API state.\n\n'
      'Artifact: '+BUNDLE.name+' ('+str(archive_len)+' compressed bytes)\n\n'
      'Archive SHA-256: `'+archive_sha+'`\n\n'
      'Generated from committed historical Git objects only; the archive may only contain files '
      'whose bytes were served publicly and match the frozen census digest. A public user can '
      'retrieve this artifact without any access to the private development source tree. '
      'The archive is a recovery **candidate** and must not become the canonical estate until '
      'an explicit owner-admitted release and cutover authority exist.\n\n'
      'The included Caddyfile serves only a loopback-published Docker port 18480 when used with '
      'the documented external runtime; host routing uses the original domain Host header. '
      'The Caddyfile itself does not configure the host Docker port mapping.\n\n'
      'Reproduce from historical owning Git objects: `npm run recovery:bundle:build`. '
      'Verify immutable bytes: `npm run recovery:bundle:verify`. '
      'For the first LAN-only rehearsal, use the isolated Ubuntu verification scenario '
      'without changing production DNS, TLS, or existing Caddy services.\n')
def execute(action):
    if action=='verify' and (not BUNDLE.exists() or not MANIFEST.exists() or not REPORT.exists()):
        raise RuntimeError('Missing bundle artifacts')
    data,manifest=files()
    serialized=(json.dumps(manifest,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
    tar_bytes=gzip_tar(data)
    tar_hash=digest(tar_bytes)
    text=report(manifest,len(tar_bytes),tar_hash)
    if action=='build':
        OUT.mkdir(parents=True,exist_ok=True)
        BUNDLE.write_bytes(tar_bytes)
        MANIFEST.write_text(serialized)
        REPORT.write_text(text)
    else:
        if digest(BUNDLE.read_bytes())!=tar_hash:raise RuntimeError('Rebuilt bundle digest differs')
        if MANIFEST.read_text()!=serialized or REPORT.read_text()!=text:
            raise RuntimeError('Stale bundle manifest or report')
    print('STATIC_RECOVERY_'+action.upper(),'PUBLIC_BYTES',manifest['public200EvidenceCount'],
        'UNIQUE_FILES',manifest['uniqueFilesOnDisk'],'ARCHIVE_BYTES',len(tar_bytes),
        'ARCHIVE_SHA',tar_hash,'RELEASE_ADMITTED',manifest['releaseAdmitted'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['build','verify'])
    execute(p.parse_args().action)
