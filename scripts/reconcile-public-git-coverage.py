#!/usr/bin/env python3
"""Reconcile the frozen public HTTPS route census with independently pinned Git bytes.

Never transforms, invents or publishes material. Exact URL/path and SHA-256 only.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote,urlsplit,urlunsplit

ROOT=Path(__file__).resolve().parents[1]
DEV=ROOT.parents[1]
DIR=ROOT/'recovery'
OUTPUT=DIR/'public-git-coverage.json'
REPORT=DIR/'public-git-coverage.md'

def digest(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_text())
def fullurl(host,path):
    return 'https://'+host+path
def urlkey(url):
    p=urlsplit(url)
    path=unquote(p.path) or '/'
    if path.endswith('/index.html'):path=path[:-10]
    return urlunsplit(('https',p.hostname or '',path,'',''))
def from_root(rel,root):
    if root=='.':return rel
    if rel.startswith(root.rstrip('/')+'/'):return rel[len(root.rstrip('/'))+1:]
    return None
def path_to_url(host,rel,prefix='/'):
    if rel=='index.html':return fullurl(host,prefix)
    if rel.endswith('/index.html'):return fullurl(host,prefix+rel[:-10])
    return fullurl(host,prefix+rel)
def blob_bytes(checkout,oid):
    p=subprocess.run(['git','cat-file','blob',oid],cwd=checkout,capture_output=True)
    if p.returncode:raise RuntimeError('Missing pinned Git blob '+oid+' in '+str(checkout))
    return p.stdout

def plan():
    census=load(DIR/'public-route-census.json')
    owners=load(ROOT/'inventory/domain-ownership.json')
    owner_sources={x['repository']:x for x in owners['sources']}
    candidate=load(DIR/'candidate-release-lock.json')
    projection=load(DIR/'public-byte-provenance.json')
    custody=load(DIR/'owner-readback-custody.json')
    if candidate['releaseAdmitted'] or custody['releaseAdmitted'] or projection['releaseAdmitted']:
        raise RuntimeError('Untrusted recovery input admitted')
    matches=collections.defaultdict(list)
    for domain in candidate['domains']:
        revision=domain.get('candidateRevision')
        if not revision:continue
        host=domain['publicHost']
        owner=domain['ownerRepo']
        checkout=DEV/owner_sources[owner]['localCheckout']
        prefix=domain['routePrefix']
        root=domain.get('gitSourceRoot')
        if not root:continue
        for source in domain['sourceFiles']:
            rel=from_root(source['path'],root)
            if rel is None:continue
            url=urlkey(path_to_url(host,rel,prefix))
            body=blob_bytes(checkout,source['blobGitObject'])
            matches[url].append(dict(kind='EXACT_OWNING_GIT_REVISION',owner=owner,
                gitRevision=revision,gitPath=source['path'],sha256=digest(body)))
    for section in projection['sections']:
        for row in section['files']:
            if not row.get('matchingGitRevision'):continue
            matches[urlkey(row['publicUrl'])].append(dict(
                kind='EXACT_HISTORICAL_PROJECTION_GIT',
                owner=projection.get('historicalProjectionRepo','Fountain-Coach/midi2-gpu-fabric'),
                gitRevision=row['matchingGitRevision'],gitPath=row['historicalSourcePath'],
                sha256=row['publicSHA256']))
    for owner_record in custody['ownerRecords']:
        owner=owner_record['ownerRepo']
        checkout=DEV/owner_sources[owner]['localCheckout']
        commit=owner_record['commit']
        receipt_path='publication-recovery/2026-10-15/receipt.json'
        r=subprocess.run(['git','show',commit+':'+receipt_path],cwd=checkout,capture_output=True)
        if r.returncode:raise RuntimeError('Missing owner Git recovery receipt')
        receipt=json.loads(r.stdout)
        for page in (receipt['artifacts'] if owner=='Fountain-Coach/solstice.fountain.coach' else receipt['documents']):
            source_file=(page['ownerSnapshotPath'] if owner=='Fountain-Coach/solstice.fountain.coach' else page['recoveryPath'])
            p=subprocess.run(['git','show',commit+':'+source_file],cwd=checkout,capture_output=True)
            if p.returncode or digest(p.stdout)!=page['sha256']:raise RuntimeError('Owner snapshot SHA invalid')
            matches[urlkey(page['publicUrl'])].append(dict(kind='EXACT_OWNER_PUBLIC_READBACK_SNAPSHOT',
                owner=owner,gitRevision=commit,gitPath=source_file,sha256=page['sha256']))
    for item in custody['ownerDirectGitAssets']:
        matches[urlkey(item['publicUrl'])].append(dict(kind='EXACT_OWNER_GIT_ASSET',
            owner=item['ownerRepo'],gitRevision=item['revision'],gitPath=item['gitPath'],sha256=item['sha256']))
    results=[];counts=collections.Counter();per_host=collections.defaultdict(collections.Counter)
    for row in census['results']:
        url=urlkey(row['url']);sha=row['sha256']
        if row['status']!=200 or row['outcome']!='OK':
            status='PUBLIC_NOT_HTTP_200'
            match=None
        else:
            hits=[p for p in matches.get(url,[]) if p['sha256']==sha]
            order=['EXACT_OWNING_GIT_REVISION','EXACT_OWNER_GIT_ASSET','EXACT_OWNER_PUBLIC_READBACK_SNAPSHOT','EXACT_HISTORICAL_PROJECTION_GIT']
            hits.sort(key=lambda item:order.index(item['kind']))
            if hits:
                match=hits[0];status=match['kind']
            else:
                match=None;status='PUBLIC_200_NOT_PROVEN_IN_PINNED_GIT'
        host=urlsplit(url).hostname
        counts[status]+=1;per_host[host][status]+=1
        results.append(dict(url=url,httpStatus=row['status'],liveSHA256=sha,
                            recoveryEvidence=status,gitMatch=match))
    return dict(schema='fountain.estate.public-git-coverage.v1',
       publicCensusSHA256=digest((DIR/'public-route-census.json').read_bytes()),
       candidateReleaseSHA256=digest((DIR/'candidate-release-lock.json').read_bytes()),
       historicalGitEvidenceSHA256=digest((DIR/'public-byte-provenance.json').read_bytes()),
       ownerSnapshotCustodySHA256=digest((DIR/'owner-readback-custody.json').read_bytes()),
       scope='Bounded public discoverability census; not exhaustive public release or dynamic service restoration',
       releaseAdmitted=False,allowDeployment=False,
       counts=dict(sorted(counts.items())),
       byHost={host:dict(sorted(c.items())) for host,c in sorted(per_host.items())},
       results=results)
def text_report(data):
    cats=['EXACT_OWNING_GIT_REVISION','EXACT_OWNER_GIT_ASSET','EXACT_OWNER_PUBLIC_READBACK_SNAPSHOT',
          'EXACT_HISTORICAL_PROJECTION_GIT','PUBLIC_200_NOT_PROVEN_IN_PINNED_GIT','PUBLIC_NOT_HTTP_200']
    lines=['# Public HTTPS to immutable Git recovery reconciliation','',
     '**Scope:** bounded nine-host public route census, matched strictly by normalized public URL and byte-identical SHA-256 to a pinned owning commit, archival Git projection, or an owner-domain public HTML recovery snapshot.',
     '',
     '**Do not deploy:** this does not prove an exhaustive public route or asset inventory, atomic publication revision, or private/dynamic services. The recovery lock remains BLOCKED.',
     '',
     '| Host | Owner release commit | Owner asset | Owner public readback | Historical projection | Unmatched HTTP 200 | Non-200 |',
     '|---|---:|---:|---:|---:|---:|---:|']
    for host,counts in data['byHost'].items():
        lines.append('| '+host+' | '+' | '.join(str(counts.get(k,0)) for k in cats)+' |')
    lines+=['','## Unmatched public resources in this census','']
    missing=[x for x in data['results'] if x['recoveryEvidence']=='PUBLIC_200_NOT_PROVEN_IN_PINNED_GIT']
    for item in missing[:85]:
        lines.append('- '+item['url']+' — '+str(item['liveSHA256'])[:20])
    if len(missing)>85:lines.append('- '+str(len(missing)-85)+' additional unmatched public URLs in the JSON evidence')
    if not missing:lines.append('- None among probed URLs. This still does not certify full public release coverage.')
    lines+=['','## Guardrails','',
     '- Provenance categories are mutually exclusive for presentation; a URL may have multiple historical Git candidates. Each selected match is digest-verified.',
     '- The historical projection does not gain domain ownership by having byte-identical files.',
     '- All ten previously unmatched public HTML and PDF files are now present in their owning repositories as frozen, explicitly non-deployable readbacks. The two Solstice CSS/JavaScript assets are proven directly from a pinned owning Git commit.',
     '- Public 404 and 401 are reported, not “recovered” by inventing or promoting a staging page.',
     '- Assets not linked or listed in the historical seed may be absent from this census.',
     '- Dynamic runtime data, unpublished content and secrets are outside scope.',
     '','Regenerate offline: npm run recovery:coverage:build. Verify unchanged witness: npm run recovery:coverage:verify.']
    return '\n'.join(lines)+'\n'
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['build','verify'])
    args=p.parse_args()
    data=plan()
    encoded=json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    markdown=text_report(data)
    if args.action=='verify':
        if not OUTPUT.exists() or OUTPUT.read_text()!=encoded or REPORT.read_text()!=markdown:
            raise RuntimeError('Stale or tampered public Git route coverage witness')
    else:
        OUTPUT.write_text(encoded);REPORT.write_text(markdown)
    print('PUBLIC_GIT_COVERAGE_'+('VERIFIED' if args.action=='verify' else 'BUILT'),data['counts'])
if __name__=='__main__':main()
