#!/usr/bin/env python3
"""Fail-closed last-published release candidate planner. Never deploys or mutates sources.

An exact HTML match identifies ONE file of an historical Git tree. It does not
approve that tree as an entire previously published release.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
DEV=Path(os.environ.get('FOUNTAIN_DEV_ROOT', ROOT.parents[1])).resolve()
INV=ROOT/'inventory'
OUT=ROOT/'recovery'
LOCK=OUT/'candidate-release-lock.json'
REPORT=OUT/'README.md'

def sha(b):return hashlib.sha256(b).hexdigest()
def raw_git(directory,*args):
    p=subprocess.run(['git',*args],cwd=directory,capture_output=True)
    if p.returncode:raise RuntimeError('Git source unavailable: '+str(directory)+' '+str(args)+' '+p.stderr.decode('utf8','replace')[:120])
    return p.stdout
def git(directory,*args):return raw_git(directory,*args).decode().strip()
def checked_identity(directory):
    u=git(directory,'remote','get-url','origin')
    m=re.search(r'github[.]com[:/]([^/]+/[^/]+?)(?:[.]git)?$',u)
    if not m:raise RuntimeError('Not a GitHub owner checkout: '+str(directory))
    return m.group(1)
def committed(directory,ref,path):
    p=subprocess.run(['git','show',ref+':'+path],cwd=directory,capture_output=True)
    return p.stdout if p.returncode==0 else None
def committed_tree(directory,ref,prefix):
    args=['ls-tree','-r','--format=%(objectmode) %(objecttype) %(objectname) %(path)',ref]
    if prefix!='.':args+=['--',prefix]
    output=git(directory,*args)
    rows=[]
    for line in output.splitlines():
        m=re.match(r'^([0-9]{6}) (blob) ([0-9a-f]+) (.+)$',line)
        if not m:continue
        rows.append(dict(path=m.group(4),blobGitObject=m.group(3),mode=m.group(1)))
    return rows
def sample_path(public_route,prefix):
    if not public_route.startswith(prefix):return None
    part=public_route[len(prefix):].lstrip('/')
    if not part or public_route.endswith('/'):part=part+'index.html'
    return part
def source_file(public_route,root,public_prefix):
    if root is None:return None
    part=sample_path(public_route,public_prefix)
    if part is None:return None
    return ((root.rstrip('/')+'/' if root!='.' else '')+part)

def history_candidates(directory,root_file,want_sha,pinned_head):
    # 'git log PINNED_SHA' selects immutable blobs from the frozen owner graph,
    # including historical snapshots. A HEAD working-tree file is never read.
    history=git(directory,'log',pinned_head,'--format=%H','--',root_file).splitlines()
    head=pinned_head
    candidates=list(dict.fromkeys([head]+history))
    matches=[]
    for revision in candidates:
        blob=committed(directory,revision,root_file)
        if blob is not None and sha(blob)==want_sha:matches.append(revision)
    return matches,len(candidates)

def host_rows():
    own=json.loads((INV/'domain-ownership.json').read_text())
    witnessed=json.loads((INV/'public-readback.json').read_text())
    reg=json.loads((ROOT/'manifest.json').read_text())
    hosts={r['host']:r for r in own['domains']}
    sources={r['repository']:r for r in own['sources']}
    observed={r['host']:r for r in witnessed['domains']}
    return hosts,sources,observed,reg,witnessed

def plan():
    hosts,sources,observed,reg,witnessed=host_rows()
    if set(hosts)!=set(observed):raise RuntimeError('Mismatch between host registry and witness list')
    domains=[];blockers=[]
    def evaluation(host, owner, root, exposed_prefix, witness_host, witness_route, deployment_role, excluded_prefixes=()):
        checkout=DEV/sources[owner]['localCheckout']
        if checked_identity(checkout)!=owner:raise RuntimeError('Git owner remote mismatch: '+owner)
        row=observed[witness_host]
        witness=next((x for x in row['checks'] if x['route']==witness_route),None)
        result=dict(publicHost=host,routePrefix=exposed_prefix,ownerRepo=owner,
                    owningRepository='https://github.com/'+owner,
                    deploymentRole=deployment_role,publicWitnessHost=witness_host,
                    rootWitnessRoute=witness_route,
                    gitSourceRoot=root,
                    sourceDocument=source_file(witness_route,root,exposed_prefix),
                    publicWitnessStatus=witness['httpStatus'] if witness else None,
                    publicWitnessSHA256=witness.get('sha256') if witness else None,
                    currentOwnerHead=sources[owner]['head'],
                    matchedHistoricalRevisions=[],
                    candidateRevision=None,candidateSourceRootTree=None,
                    sourceAssetManifestSHA256=None,sourceFiles=[],
                    sampleRoutes=[],releaseAdmitted=False,blockers=[])
        def fail(code):
            result['blockers'].append(code)
            blockers.append(dict(host=host,routePrefix=exposed_prefix,code=code))
        if not root or not result['sourceDocument']:
            fail('MISSING_GIT_TRACKED_DEPLOYMENT_ROOT')
        elif not witness or witness['httpStatus']!=200 or not witness.get('sha256'):
            fail('NO_SUCCESSFUL_VERIFIED_LIVE_ROOT_WITNESS')
        else:
            matching,count=history_candidates(checkout,result['sourceDocument'],witness['sha256'],sources[owner]['head'])
            result['historicalRootRevisionCandidatesExamined']=count
            result['matchedHistoricalRevisions']=matching
            if not matching:fail('NO_EXACT_GIT_COMMIT_MATCHING_LIVE_DOCUMENT')
            else:
                rev=matching[0]
                result['candidateRevision']=rev
                tree=committed_tree(checkout,rev,root)
                if not tree:fail('EMPTY_GIT_SOURCE_TREE')
                else:
                    result['candidateSourceRootTree']=git(checkout,'rev-parse',rev+':'+root) if root!='.' else git(checkout,'rev-parse',rev+'^{tree}')
                    result['sourceFiles']=tree
                    result['sourceAssetManifestSHA256']=sha(json.dumps(tree,sort_keys=True,separators=(',',':')).encode())
                    result['gitTrackedBlobCount']=len(tree)
                    result['gitTrackedHTMLCount']=sum(x['path'].endswith(('.html','.htm')) for x in tree)
                    # Compare only successful observed pages; 404/401 staged routes
                    # do not establish approved publication obligations.
                    for sample in row['checks']:
                        if sample['httpStatus']!=200 or not sample['route'].startswith(exposed_prefix):continue
                        if any(sample['route'].startswith(x) for x in excluded_prefixes):continue
                        rel=source_file(sample['route'],root,exposed_prefix)
                        blob=committed(checkout,rev,rel)
                        observed_hash=sample.get('sha256')
                        matching_hash=sha(blob) if blob is not None else None
                        result['sampleRoutes'].append(dict(route=sample['route'],sourceFile=rel,publicSHA256=observed_hash,
                            candidateSHA256=matching_hash,matches=(matching_hash==observed_hash) if observed_hash else None))
                    if not result['sampleRoutes']:fail('NO_POSITIVE_SAMPLED_PUBLIC_ROUTES')
                    if any(x['matches'] is False for x in result['sampleRoutes']):
                        fail('CANDIDATE_MISMATCHES_PUBLIC_SAMPLED_ROUTES')
        if sources[owner]['sourceInventoryStatus']=='mismatch':
            fail('OWNER_CURRENT_SOURCE_HASH_LEDGER_MISMATCH')
        # Unconditionally block admission until a full route/asset release receipt
        # is independently validated. This guard may never be skipped based on a homepage.
        fail('FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED')
        result['readiness']='BLOCKED' if result['blockers'] else 'READY'
        return result

    for host in sorted(hosts):
        row=hosts[host]
        if row['lifecycle'] in ('archived','planned'):
            domains.append(dict(publicHost=host,ownerRepo=row['sourceRepo'],deploymentRole=row['role'],
                lifecycle=row['lifecycle'],readiness='NOT_PUBLIC_RECOVERY_TARGET',
                blockers=[],releaseAdmitted=False))
            continue
        owner=row['sourceRepo']
        root=sources[owner]['sourceRoot']
        if root is None:
            domains.append(evaluation(host,owner,None,'/',host,'/',row['role'],
                    tuple(d['pathPrefix'] for d in row.get('delegations',[]))))
        else:
            domains.append(evaluation(host,owner,root,'/',host,'/',row['role'],
                    tuple(d['pathPrefix'] for d in row.get('delegations',[]))))
        for delegation in row.get('delegations',[]):
            # A host owns /, a different Git owner owns the delegated /solstice/.
            prefix=delegation['pathPrefix']
            delegated=delegation['sourceRepo']
            witness_route=prefix.rstrip('/')+'/editions/first-reading/'
            domains.append(evaluation(host,delegated,sources[delegated]['sourceRoot'],
                                      prefix,host,witness_route,'delegated-literary-publication'))

    supplementary=None
    evidence=OUT/'public-byte-provenance.json'
    if evidence.exists():
        recorded=json.loads(evidence.read_text())
        if recorded.get('schema')!='fountain.estate.public-byte-provenance.v1' or recorded.get('releaseAdmitted'):
            raise ValueError('Unsafe supplemental Git blob evidence')
        totals={status:sum(s['counts'][status] for s in recorded['sections']) for status in
                ('ROOT_REVISION_EXACT','OTHER_GIT_REVISION_EXACT','PUBLIC_BYTES_NOT_LOCATED','ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL')}
        supplementary=dict(evidencePath='recovery/public-byte-provenance.json',
                           evidenceSHA256=sha(evidence.read_bytes()),archivalOwner='Fountain-Coach/midi2-gpu-fabric',
                           authority='historical Git blob evidence, not canonical owner, not release admission',
                           publicArtifactCounts=totals)
    return dict(schema='fountain.estate.candidate-public-release-lock.v1',
         authority='evidence-only; neither publication approval nor deploy permission',
         releaseAdmitted=False,allowRecoveryDeployment=False,
         sourceInventorySHA256=sha((INV/'domain-ownership.json').read_bytes()),
         publicReadbackSHA256=sha((INV/'public-readback.json').read_bytes()),
         manifestSHA256=sha((ROOT/'manifest.json').read_bytes()),
         observedAt=witnessed['observedAt'],
         requiredOwnerApproval=True,supplementaryHistoricalBlobEvidence=supplementary,
         proofBoundary='Exact matching of observed HTML is not proof of complete asset/route recovery; receipts and full readback missing',
         hostCount=len(hosts),publicationSurfaces=len(domains),
         matchedPublicationRoots=sum(bool(x.get('candidateRevision')) for x in domains),
         blockers=blockers,domains=domains)

def markdown(lock):
    lines=['# Candidate release lock — cold restore, evidence only','',
      '**Blocked:** this is a read-only reconstruction plan, not a complete last-public release or authority to start a tunnel.',
      '', 'Recorded public HTTPS witness: '+lock['observedAt'],
      '', '| Public host / path | Source owner | Exact live-document Git revision | Sampled routes | Recovery status |',
      '|---|---|---|---|---|']
    for x in lock['domains']:
        samples=x.get('sampleRoutes',[])
        score=str(sum(y['matches'] is True for y in samples))+'/'+str(len(samples)) if samples else '—'
        lines.append('| '+x['publicHost']+x.get('routePrefix','')+' | '+x['ownerRepo']+
          ' | '+(x.get('candidateRevision') or 'not found')[:12]+' | '+score+' | '+x['readiness']+' |')
    supplemental=lock.get('supplementaryHistoricalBlobEvidence')
    if supplemental:
        counts=supplemental['publicArtifactCounts']
        lines+=['','## Cross-repository historical byte provenance','',
          f"{counts['ROOT_REVISION_EXACT']+counts['OTHER_GIT_REVISION_EXACT']} archival public file responses have exact Git blob provenance ({counts['ROOT_REVISION_EXACT']} in their matching historical root trees; {counts['OTHER_GIT_REVISION_EXACT']} in other historical commits). {counts['PUBLIC_BYTES_NOT_LOCATED']} publicly responding files remain unmatched; {counts['ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL']} archival files returned HTTP 404.",
          '', 'See [public-byte-provenance.md](public-byte-provenance.md) and [root-matched-historical-artifacts.md](root-matched-historical-artifacts.md). This is evidence from midi2-gpu-fabric, **not** a change to domain source ownership or an approved static recovery release.']
    lines+=['','## Public-byte custody and bounded site census','',
      'The five previously unmatched public HTML documents were preserved as SHA-256-verified recovery snapshots in their canonical Book of Reframe and MIDI2 owner repositories (MIDI2 through protected PR #193, squash-merged). Five additional Solstice HTML/PDF proofs were preserved in its source owner, and its two previously unmatched styles/scripts exactly match committed owner Git assets.',
      'The [owner custody](owner-readback-custody.json) verifies ten captured published files and two additional owner Git assets. The [nine-domain public-route census](public-route-census.md) verified 621 URLs, of which 600 returned HTTP 200. [Public Git coverage](public-git-coverage.md) assigns exact Git-byte provenance to all 600 successful public responses in that bounded crawl; 21 URLs returned other HTTP statuses.',
      '**None of this is an exhaustive estate crawl, complete last-published release, private-state backup, or authority to deploy.** Unknown unlinked assets and dynamic/public API boundaries remain outside coverage.']
    lines+=['','## Findings and next steps','',
      'Only Git objects of pinned candidate commits are inspected, never uncommitted working-tree files.',
      'A match is per public HTML document. Some hosts also have sampled route matches; none has an independently certified complete public static asset manifest.',
      'The candidate lock lists Git blobs/tree objects for reconstruction but does not claim these are all the bytes presently published.',
      'A 404 or 401 for a staging-only route does not imply the public historic release should contain it.',
      'The MIDI2 owning repository has no verified static publication root; a separate historical estate projection may contain an exact homepage copy, but that projection is **not yet** an approved Git-owned recovery input.',
      'The Solstice First Reading is delegated under works.benedikt-eickhoff.de/solstice/ and must have an independent content/source match.',
      'Before any deployment, prove every required public route/asset, identify remaining web or dynamic state, authorize a full last-published lock, and verify the existing Ubuntu host is isolated.',
      '',
      '## Blocking conditions','']
    for row in lock['blockers']:
        lines.append('- '+row['host']+row['routePrefix']+': '+row['code'])
    lines+=['','## Reproducibility','','Run: npm run recovery:plan, then npm run recovery:verify.',
     'No SSH, DNS mutation, Caddy reload, tunnel, secrets, public deployment or Git owner modifications.']
    return '\n'.join(lines)+'\n'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['plan','verify'])
    args=ap.parse_args()
    expected=plan()
    b=json.dumps(expected,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    report=markdown(expected)
    if args.action=='plan':
        OUT.mkdir(exist_ok=True)
        LOCK.write_text(b)
        REPORT.write_text(report)
    else:
        if not LOCK.is_file() or not REPORT.is_file() or LOCK.read_text()!=b or REPORT.read_text()!=report:
            raise RuntimeError('RECOVERY_LOCK_STALE: regenerate from owner Git objects and public-readback witness')
        if expected['allowRecoveryDeployment'] or expected['releaseAdmitted']:
            raise RuntimeError('RECOVERY_LOCK_UNSAFE')
        if not expected['blockers']:raise RuntimeError('Unjustified admission of unreconciled public release')
    print('RECOVERY_PLAN_'+('VERIFIED' if args.action=='verify' else 'BUILT'),
          'surfaces',len(expected['domains']),'matching-roots',expected['matchedPublicationRoots'],
          'blockers',len(expected['blockers']),'admitted',expected['releaseAdmitted'])

if __name__=='__main__':main()
