#!/usr/bin/env python3
"""Read-only DNS and public continuity gate for the Fountain Coach estate.

No zone transfers, no credentials, no DNS mutation. DNS records are observed
only for an explicit set of known names and common email labels. No claim of a
complete DNS zone export or registrar ownership verification is possible.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recovery'
SNAP=OUT/'failover-dns-witness.json'
PLAN=OUT/'failover-readiness.json'
REPORT=OUT/'failover-readiness.md'
ZONES=('fountain.coach','benedikt-eickhoff.de')
RR_TYPES=('A','AAAA','CNAME','MX','TXT','CAA','NS','SOA')
PROBE_NAMES=('','_dmarc','selector1._domainkey','selector2._domainkey')
SCHEMA='fountain.estate.provider-loss-dns-witness.v1'
READINESS_SCHEMA='fountain.estate.provider-loss-readiness.v1'

def sha(b):return hashlib.sha256(b).hexdigest()
def load(name):return json.loads((ROOT/name).read_text())
def dig(name,rrtype,server=None):
    cmd=['dig','+time=3','+tries=1','+noall','+answer',name,rrtype]
    if server:cmd.insert(1,'@'+server)
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=8)
    except subprocess.TimeoutExpired:
        return dict(error='TIMEOUT',answers=[])
    if p.returncode or 'no servers could be reached' in p.stdout+p.stderr:
        return dict(error='NO_RESPONSE',answers=[])
    answers=[]
    for line in p.stdout.splitlines():
        parts=line.split(None,4)
        if len(parts)<5 or parts[2]!='IN':continue
        answers.append(dict(name=parts[0].rstrip('.').lower(),
            ttl=int(parts[1]),type=parts[3],
            value=parts[4].strip()))
    return dict(error=None,answers=answers)
def zonefor(host):
    matches=[z for z in ZONES if host==z or host.endswith('.'+z)]
    if not matches:raise ValueError('Host outside known registrar zones '+host)
    return max(matches,key=len)
def capture():
    inv=load('inventory/domain-ownership.json')
    hosts=sorted({d['host'] for d in inv['domains'] if d['lifecycle']=='active'})
    if len(hosts)!=9:raise ValueError('Expected 9 active observed HTTPS hosts')
    selected={z:set([z]) for z in ZONES}
    for h in hosts:selected[zonefor(h)].add(h)
    for z in ZONES:
        for prefix in PROBE_NAMES[1:]:selected[z].add(prefix+'.'+z)
    zones=[]
    for z in ZONES:
        ns=dig(z,'NS')
        name_servers=sorted({row['value'].rstrip('.').lower() for row in ns['answers'] if row['type']=='NS'})
        if not name_servers:raise RuntimeError('No authoritative nameservers discovered for '+z)
        witness=[]
        for name in sorted(selected[z]):
            # All selected names are sampled against primary authoritative NS,
            # with a second NS for A/NS to detect split / unavailable DNS.
            probes={}
            for t in RR_TYPES:
                if name!=z and t in ('NS','SOA','MX','CAA'):continue
                if name.startswith('_') and t not in ('TXT','CNAME'):continue
                first=dig(name,t,server=name_servers[0])
                if first['error'] and len(name_servers)>1:
                    backup=dig(name,t,server=name_servers[-1])
                    backup['retryAfterPrimaryError']=first['error']
                    probes[t]=backup
                else:probes[t]=first
            witness.append(dict(name=name,rrtypes=probes))
        cross=[]
        for t in ('A','NS'):
            first=dig(z,t,server=name_servers[0])
            second=dig(z,t,server=name_servers[-1])
            cross.append(dict(type=t,primary=first,secondary=second))
        zones.append(dict(zone=z,delegatedNameservers=name_servers,
                     discoveredViaRecursiveNS=ns,
                     observedRecordNames=sorted(selected[z]),
                     authoritativeQueries=witness,consistencySamples=cross,
                     completeZoneTransfer=False,registrarControlVerified=False))
        print('DNS_WITNESS',z,'nameservers',','.join(name_servers),
            'sampleNames',len(selected[z]),flush=True)
    return dict(schema=SCHEMA,observedAt=datetime.now(timezone.utc).isoformat(timespec='seconds'),
       method='Read-only dig against listed authoritative nameservers for explicit host and email labels',
       scope='selected existing estate hostnames and common mail labels only',
       zoneCompletenessClaim=False,ownerRegistrarSessionVerified=False,
       zones=zones)
def answers(zone,name,t):
    w=next(x for x in zone['authoritativeQueries'] if x['name']==name)
    return w['rrtypes'].get(t,dict(error='NOT_SAMPLED',answers=[]))
def check_dns(witness):
    if witness['schema']!=SCHEMA or witness['zoneCompletenessClaim'] or witness['ownerRegistrarSessionVerified']:
        raise ValueError('Untrusted DNS capture metadata')
    if {x['zone'] for x in witness['zones']}!=set(ZONES):raise ValueError('Incomplete zone witness')
    f=next(x for x in witness['zones'] if x['zone']=='fountain.coach')
    b=next(x for x in witness['zones'] if x['zone']=='benedikt-eickhoff.de')
    if not all('hetzner' in s for s in f['delegatedNameservers']):
        raise ValueError('DNS recovery assumption changed, re-audit required')
    if all('hetzner' in s for s in b['delegatedNameservers']):
        raise ValueError('Founder zone no longer independently delegated')
    if not any('mail.icloud.com' in x['value'] for x in answers(b,b['zone'],'MX')['answers']):
        raise ValueError('Expected founder mail preservation requirement lost')
    return f,b
def make(witness):
    f,b=check_dns(witness)
    inv=load('inventory/domain-ownership.json')
    allhosts={d['host']:d for d in inv['domains']}
    public=load('recovery/public-git-coverage.json')
    proof=load('recovery/ubuntu-cold-restore-witness-20261015.json')
    bundle=load('recovery/bundles/estate-public-observed-20261015.manifest.json')
    if public['releaseAdmitted'] or proof['releaseAdmitted'] or bundle['releaseAdmitted']:
        raise ValueError('Unsafe published-state source')
    if proof['staticRestore']['sha256VerifiedResponses']!=600:
        raise ValueError('Partial static restore')
    if set(bundle['hostnames'])!={h for h,d in allhosts.items() if d['lifecycle']=='active'}:
        raise ValueError('Unrecognized public estate hosts')
    source_hashes=sum(public['counts'].get(s,0) for s in (
        'EXACT_HISTORICAL_PROJECTION_GIT','EXACT_OWNER_GIT_ASSET',
        'EXACT_OWNER_PUBLIC_READBACK_SNAPSHOT','EXACT_OWNING_GIT_REVISION'))
    if source_hashes!=600:raise ValueError('Public Git coverage incomplete')
    active=[]
    for name in sorted(bundle['hostnames']):
        zone=zonefor(name)
        z=f if zone=='fountain.coach' else b
        address=answers(z,name,'A')
        cname=answers(z,name,'CNAME')
        active.append(dict(host=name,zone=zone,
             sourceRepo=allhosts[name]['sourceRepo'],
             liveA=sorted({x['value'] for x in address['answers'] if x['type']=='A'}),
             liveCNAME=sorted({x['value'] for x in cname['answers'] if x['type']=='CNAME'}),
             public200Resources=sum(x['httpStatus']==200 and x['url'].startswith('https://'+name+'/') for x in public['results']),
             staticHTTPByteRestore='PASS_BOUNDED',
             interactiveBehavior='NOT_VERIFIED',
             dynamicHostServices='NOT_ESTABLISHED',
             canonicalDNSCutover='NOT_AUTHORIZED'))
    gates=[
      dict(id='immutable-public-bundle',status='PASS_BOUNDED',
           reason='600/600 observed HTTP-200 files retrieved from GitHub and hash verified on Ubuntu; SHA-pin protects integrity but GitHub release is not policy-immutable'),
      dict(id='ubuntu-static-origin',status='PASS_BOUNDED',
           reason='Isolated local Caddy on loopback 18480 answered 600/600 resource bytes for all nine original Host headers'),
      dict(id='cloudflare-single-host',status='PASS_BOUNDED',
           reason='Temporary uncredentialed Cloudflare URL returned exact fountain.coach root over public HTTPS, not the original canonical hostname'),
      dict(id='complete-public-release',status='BLOCKED',
           reason='621 bounded URLs observed; unlinked public resources, complete source release admission and source owner signature unknown'),
      dict(id='fountain-authoritative-dns-independent-of-hetzner',status='BLOCKED',
           reason='Current NS delegation entirely to Hetzner; registrar-level NS migration/access not exercised'),
      dict(id='founder-zone-and-icloud-mail-preserved',status='BLOCKED',
           reason='Different registrar DNS; existing iCloud mail MX/TXT must survive; public observation does not establish full zone contents'),
      dict(id='zone-inventory-exhaustive',status='BLOCKED',
           reason='Known-host and common mail-label DNS readback is not a complete zone enumeration and does not prove registrar credentials'),
      dict(id='canonical-nine-host-ingress-and-tls',status='BLOCKED',
           reason='Named tunnel, per-host hostname ingress, canonical-domain TLS, control-token custody and rollback not tested'),
      dict(id='owner-auth-domain-trust-and-secrets',status='BLOCKED',
           reason='No independently recoverable owner key or SecretStore custody proof'),
      dict(id='private-fountainstore-state',status='BLOCKED',
           reason='Git static publication does not include private Store durable state or a verified off-provider encrypted restore'),
      dict(id='browser-runtime-and-interactive-audio',status='BLOCKED',
           reason='Caddy byte equality does not test iPad reader interaction, browser Csound, MIDI2 performance, playback or user consent'),
      dict(id='external-api-and-service-identities',status='UNDETERMINED',
           reason='Public static URL census cannot establish active OAuth, BotCast, API, email integrations or other external runtime state'),
      dict(id='off-home-network-witness',status='BLOCKED',
           reason='Quick Tunnel tested via internet by Mac, not independently accepted on a separate ISP/device'),
      dict(id='recovery-rto-rpo-and-failback',status='BLOCKED',
           reason='No timed authorized full cutover or rollback; private data loss objective undefined')
    ]
    hypothetical=dict(scenario='hetzner-origin-and-authoritative-dns-lost',
        originalIpAvailable=False,hetznerDnsControlAvailable=False,
        ubuntuHostAvailable=True,githubPublicReleaseAvailable=True,
        canonicalEstateAccessible=False,
        reason='GitHub plus Ubuntu restore the observed static bytes, but fountain.coach registrar delegation still points to lost Hetzner nameservers. Domain routing cannot be asserted without separate NS authority.')
    return dict(schema=READINESS_SCHEMA,dnsWitnessSHA256=sha(SNAP.read_bytes()),
        editionIsAuthorApproved=False,authorizedDNSFailover=False,
        automaticDNSMutationAllowed=False,releaseAdmitted=False,
        status='NOT_READY_FOR_CANONICAL_PROVIDER_LOSS_FAILOVER',
        publiclyObservedStaticReconstruction='PASS_BOUNDED',
        knownHosts=active,serviceAndAuthorityGates=gates,
        scenarioSimulation=hypothetical,
        nextMilestone='Prepare complete alternative authoritative DNS zone and test owner registrar delegation in a separately authorized plan, without modifying production in this run')
def markdown(w):
    lines=['# Hetzner-provider-loss recovery readiness','',
        '**Result: '+w['status']+'**',
        '', 'The existing Ubuntu/Caddy origin successfully reconstructs the 600 observed static public bytes. This report evaluates the separate canonical-domain, DNS, identity and dynamic-state boundaries. It is a **read-only** exercise: no registrar session, zone import, named tunnel, live routing, secrets or production Caddy configuration was modified.',
        '', '## Public DNS authority and dependencies','',
        '| DNS zone | Observed delegated nameservers | Operational concern |',
        '|---|---|---|']
    for zone in json.loads(SNAP.read_text())['zones']:
        issue='Provider-loss single point of failure' if zone['zone']=='fountain.coach' else 'iCloud Mail records and adjacent literary domain must be preserved'
        lines.append('| '+zone['zone']+' | '+', '.join(zone['delegatedNameservers'])+' | '+issue+' |')
    lines+=['','This is **not a complete DNS zone export**. A small known-host record census cannot enumerate every unlisted DKIM selector, private verification subdomain, SRV or third-party integration. At a later authorized migration, obtain a complete zone export through its owning provider/registrar and compare every record before a nameserver change.',
        '', '## Observed public hosts','',
        '| Host | Known source owner | Current A (sample) | Public responses recovered |',
        '|---|---|---|---:|']
    for item in w['knownHosts']:
        lines.append('| '+item['host']+' | '+item['sourceRepo']+' | '+(', '.join(item['liveA']) or ('CNAME' if item['liveCNAME'] else 'no sampled A'))+
            ' | '+str(item['public200Resources'])+' |')
    lines+=['','## Failover and runtime gates','',
        '| Gate | State | Reason |',
        '|---|---|---|']
    for gate in w['serviceAndAuthorityGates']:
        lines.append('| '+gate['id']+' | '+gate['status']+' | '+gate['reason']+' |')
    lines+=['','## Explicit provider-loss simulation','',
        'In the assumed disaster (Hetzner server/IP unavailable **and** Hetzner authoritative DNS unavailable), the reconstructed files continue to exist on Ubuntu, but **fountain.coach is not demonstrated to remain publicly reachable**. Until the registrar directs queries to functioning independent nameservers, an HTTP-healthy origin cannot rescue a DNS-dead domain.',
        '', 'Next action: independently prepare and verify alternative DNS ownership, exact complete zones, Cloudflare named tunnel/hostname control and protected token custody. Test with delegated nonproduction zones and only then seek explicit owner authority for canonical-domain migration.',
        '', '## Limitations','',
        '- Per-host HTTP 200 static equality does not attest live service API, FountainStore, OAuth, BotCast, interactive iPad reader or MIDI2 performance continuity.',
        '- The historical static release remains explicitly **unadmitted** as production.',
        '- TXT records are public DNS data but may include third-party verification tokens; no secrets/private backup content was queried.',
        '- Public DNS observation cannot prove registrar login, ability to move delegation, domain expiry/transfer status or complete zone contents.',
        '- The simulation is deliberately fail-closed and must not be described as a performed DNS failover.',
        '', 'Refresh public DNS witness: `npm run recovery:failover:probe`. Verify pinned snapshot without network: `npm run recovery:failover:verify`.']
    return '\n'.join(lines)+'\n'
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['probe','verify']);args=p.parse_args()
    if args.mode=='probe':
        witness=capture();SNAP.write_text(json.dumps(witness,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
    else:
        if not SNAP.exists():raise RuntimeError('No pinned DNS witness')
        witness=json.loads(SNAP.read_text())
    result=make(witness)
    encoded=json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    human=markdown(result)
    if args.mode=='verify':
        if PLAN.read_text()!=encoded or REPORT.read_text()!=human:
            raise RuntimeError('STALE_FAILOVER_READINESS_EVIDENCE')
    else:PLAN.write_text(encoded);REPORT.write_text(human)
    print('FAILOVER_'+args.mode.upper(),result['status'],
        'domains',len(result['knownHosts']),
        'gates',len(result['serviceAndAuthorityGates']))
if __name__=='__main__':main()
