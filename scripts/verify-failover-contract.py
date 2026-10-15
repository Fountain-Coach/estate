#!/usr/bin/env python3
"""Enforce fail-closed provider-loss and browser-runtime coverage contracts."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'recovery'
owners=json.loads((ROOT/'inventory/domain-ownership.json').read_text())
manifest=json.loads((REC/'bundles/estate-public-observed-20261015.manifest.json').read_text())
dns=json.loads((REC/'failover-dns-witness.json').read_text())
gate=json.loads((REC/'failover-readiness.json').read_text())
runtime=json.loads((REC/'runtime-boundary-witness.json').read_text())
livehosts=set(manifest['hostnames'])
assert len(livehosts)==9
assert dns['schema']=='fountain.estate.provider-loss-dns-witness.v1'
assert gate['schema']=='fountain.estate.provider-loss-readiness.v1'
assert runtime['schema']=='fountain.estate.public-browser-runtime-indicators.v1'
assert gate['dnsWitnessSHA256']==hashlib.sha256((REC/'failover-dns-witness.json').read_bytes()).hexdigest()
assert runtime['bundleSHA256']==hashlib.sha256((REC/'bundles/estate-public-observed-20261015.tar.gz').read_bytes()).hexdigest()
assert set(runtime['hosts'])==livehosts
assert {x['host'] for x in gate['knownHosts']}==livehosts
assert gate['status']=='NOT_READY_FOR_CANONICAL_PROVIDER_LOSS_FAILOVER'
assert gate['publiclyObservedStaticReconstruction']=='PASS_BOUNDED'
assert gate['editionIsAuthorApproved'] is False
assert gate['releaseAdmitted'] is False
assert gate['authorizedDNSFailover'] is False
assert gate['automaticDNSMutationAllowed'] is False
assert gate['scenarioSimulation']['originalIpAvailable'] is False
assert gate['scenarioSimulation']['hetznerDnsControlAvailable'] is False
assert gate['scenarioSimulation']['canonicalEstateAccessible'] is False
assert dns['zoneCompletenessClaim'] is False
assert dns['ownerRegistrarSessionVerified'] is False
assert runtime['deviceOrBrowserInteractionTested'] is False
assert runtime['serverAPIsRestored'] is False
assert runtime['privateStoreRestoreProven'] is False
assert sum(row['public200Resources'] for row in gate['knownHosts'])==600
assert sum(row['publicResources'] for row in runtime['hosts'].values())==600
zones={z['zone']:z for z in dns['zones']}
assert set(zones)=={'fountain.coach','benedikt-eickhoff.de'}
assert all('hetzner' in s for s in zones['fountain.coach']['delegatedNameservers'])
assert all('hetzner' not in s for s in zones['benedikt-eickhoff.de']['delegatedNameservers'])
assert all(not z['completeZoneTransfer'] and not z['registrarControlVerified'] for z in zones.values())
assert any('mail.icloud.com' in v['value'] for name in zones['benedikt-eickhoff.de']['authoritativeQueries']
           for a in name['rrtypes'].values() for v in a['answers'] if v['type']=='MX')
allgate={x['id']:x for x in gate['serviceAndAuthorityGates']}
assert allgate['ubuntu-static-origin']['status']=='PASS_BOUNDED'
for name in ['fountain-authoritative-dns-independent-of-hetzner',
             'founder-zone-and-icloud-mail-preserved',
             'complete-public-release',
             'private-fountainstore-state',
             'canonical-nine-host-ingress-and-tls',
             'owner-auth-domain-trust-and-secrets',
             'recovery-rto-rpo-and-failback']:
    assert allgate[name]['status']=='BLOCKED'
assert any(x['status']=='UNDETERMINED' for x in allgate.values())
assert all(x['canonicalDNSCutover']=='NOT_AUTHORIZED' for x in gate['knownHosts'])
assert all(x['browserRuntimeBehaviorProof']=='NOT_TESTED' for x in runtime['hosts'].values())
print('FAILOVER_CONTRACT_VERIFIED',len(livehosts),'domains',len(allgate),
      'gates; production failover remains blocked')
