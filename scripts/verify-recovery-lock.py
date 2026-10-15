#!/usr/bin/env python3
"""Validate fail-closed semantics of proposed disaster-recovery publication lock."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'recovery/candidate-release-lock.json').read_text())
inventory=json.loads((ROOT/'inventory/domain-ownership.json').read_text())
assert lock['schema']=='fountain.estate.candidate-public-release-lock.v1'
assert lock['releaseAdmitted'] is False
assert lock['allowRecoveryDeployment'] is False
assert lock['requiredOwnerApproval'] is True
assert lock['matchedPublicationRoots']<lock['publicationSurfaces']
assert lock['blockers']
assert lock['hostCount']==len(inventory['domains'])
assert lock['publicationSurfaces']==len(lock['domains'])
assert all(not row['releaseAdmitted'] for row in lock['domains'])
supplemental=lock['supplementaryHistoricalBlobEvidence']
assert supplemental['authority'].startswith('historical Git blob evidence')
assert supplemental['publicArtifactCounts']['ROOT_REVISION_EXACT']==170
assert supplemental['publicArtifactCounts']['OTHER_GIT_REVISION_EXACT']==7
assert supplemental['publicArtifactCounts']['PUBLIC_BYTES_NOT_LOCATED']==5
assert supplemental['publicArtifactCounts']['ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL']==2
host_names={r['host'] for r in inventory['domains']}
surfaces={(r['publicHost'],r.get('routePrefix','')):r for r in lock['domains']}
assert len(surfaces)==len(lock['domains'])
assert {name for name,_ in surfaces}==host_names
for row in inventory['domains']:
    entries=[x for x in lock['domains'] if x['publicHost']==row['host']]
    assert entries
    if row['lifecycle'] in ('archived','planned'):
        assert all(x['readiness']=='NOT_PUBLIC_RECOVERY_TARGET' for x in entries)
    else:
        assert entries[0]['readiness']=='BLOCKED'
        assert 'FULL_LAST_PUBLIC_RELEASE_AND_ASSET_PROOF_NOT_ESTABLISHED' in entries[0]['blockers']
for row in lock['domains']:
    if row['readiness']=='NOT_PUBLIC_RECOVERY_TARGET':continue
    assert row['blockers'] and row['readiness']=='BLOCKED'
    if row['candidateRevision']:
        assert len(row['candidateRevision'])==40
        assert row['candidateRevision'] in row['matchedHistoricalRevisions']
        assert row['sourceAssetManifestSHA256'] and row['candidateSourceRootTree']
        assert row['sourceFiles'] and len(row['sourceFiles'])==row['gitTrackedBlobCount']
        assert row['sampleRoutes']
        assert row['sampleRoutes'][0]['matches'] is True
        assert all(len(x['blobGitObject'])>=40 for x in row['sourceFiles'])
        assert len({x['path'] for x in row['sourceFiles']})==len(row['sourceFiles'])
    else:
        assert any(code in row['blockers'] for code in [
            'NO_EXACT_GIT_COMMIT_MATCHING_LIVE_DOCUMENT',
            'MISSING_GIT_TRACKED_DEPLOYMENT_ROOT',
            'NO_SUCCESSFUL_VERIFIED_LIVE_ROOT_WITNESS'])
for name in ('book.fountain.coach','midi2.fountain.coach'):
    assert surfaces[(name,'/')]['candidateRevision'] is None
assert surfaces[('works.benedikt-eickhoff.de','/solstice/')]['ownerRepo']=='Fountain-Coach/solstice.fountain.coach'
assert surfaces[('works.benedikt-eickhoff.de','/')]['ownerRepo']=='Fountain-Coach/works-benedikt-eickhoff'
assert surfaces[('fountain.coach','/')]['candidateRevision'].startswith('420be0c')
assert surfaces[('fountain.coach','/')]['candidateRevision']!=surfaces[('fountain.coach','/')]['currentOwnerHead']
assert all(x['matches'] for x in surfaces[('works.benedikt-eickhoff.de','/')]['sampleRoutes'])
print('RECOVERY_CANDIDATE_CONTRACT_VERIFIED',len(lock['domains']),'surfaces',lock['matchedPublicationRoots'],'root-matches',len(lock['blockers']),'blockers')
