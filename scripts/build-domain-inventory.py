#!/usr/bin/env python3
"""Owner-grounded estate source inventory and independent, read-only HTTPS witnesses."""
import argparse
import concurrent.futures
import gzip
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from urllib.parse import urljoin, urlsplit

ROOT=Path(__file__).resolve().parents[1]
DEV=Path(os.environ.get('FOUNTAIN_DEV_ROOT',ROOT.parents[1])).resolve()
MANIFEST=ROOT/'manifest.json'
OUTPUT=ROOT/'inventory'
SCHEMA='fountain.estate.source-inventory.v1'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(path,*args,allow_failure=False):
    p=subprocess.run(['git',*args],cwd=path,capture_output=True,text=True)
    if p.returncode and not allow_failure:raise RuntimeError('git '+str(args)+' '+p.stderr[:300])
    return p.stdout.strip()

def committed_bytes(path,name,revision='HEAD'):
    read=subprocess.run(['git','show',revision+':'+name],cwd=path,capture_output=True)
    if read.returncode:raise ValueError('Unresolvable committed Git file '+str(path)+' '+name)
    return read.stdout

def remote_repo(path):
    u=git(path,'remote','get-url','origin')
    m=re.search(r'github[.]com[:/]([^/]+/[^/]+?)(?:[.]git)?$',u)
    if not m:raise ValueError('Unrecognized Git origin '+str(path)+' '+u)
    return m.group(1)

def checkouts(required):
    locations=[DEV/'estate-domain-owners',DEV/'press-source-checkouts',DEV]
    result={}
    for parent in locations:
        if not parent.is_dir():continue
        for path in sorted(parent.iterdir()):
            if not path.is_dir() or not (path/'.git').exists():continue
            repo=remote_repo(path)
            if repo not in required:continue
            if repo in result:raise ValueError('Ambiguous checkout '+repo)
            result[repo]=path
    return result

def domains_from_manifest():
    m=json.loads(MANIFEST.read_text());result={}
    for entry in m['frontDoors']:
        planned=entry['id']=='first-reading'
        host=entry['futureHost'] if planned else urlsplit(entry['url']).hostname
        if host in result:raise ValueError('Duplicate host '+host)
        result[host]=dict(host=host,sourceRepo=entry['sourceRepo'],role=entry['role'],
                          lifecycle='planned' if planned else 'active',delegations=[])
    for entry in m['supportingDomains']:
        host=entry['host']
        if host in result:raise ValueError('Duplicate host '+host)
        result[host]=dict(host=host,sourceRepo=entry['sourceRepo'],role=entry['role'],
                          lifecycle='archived' if 'archiv' in entry['status'] else 'active',
                          delegations=entry.get('delegatedPublications',[]))
    repos={e['sourceRepo'] for e in result.values()}
    for entry in result.values():
        for d in entry['delegations']:
            if d['sourceRepo'] not in repos or not d['pathPrefix'].startswith('/'):
                raise ValueError('Invalid source delegation '+entry['host'])
    return result

class Links(HTMLParser):
    def __init__(self):super().__init__();self.values=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('a','link'):
            value=dict(attrs).get('href')
            if value:self.values.append(value)

def parse_links(data,host,route,hosts):
    p=Links();p.feed(data.decode('utf8','replace'))
    counted={}
    for href in p.values:
        if href.startswith(('mailto:','tel:','javascript:','data:')):continue
        u=urlsplit(urljoin('https://'+host+route,href))
        target=u.hostname or host
        key=(target,u.path or '/',u.fragment or '')
        counted[key]=counted.get(key,0)+1
    result=[]
    for (target,path,fragment),count in sorted(counted.items()):
        result.append(dict(host=host,fromRoute=route,targetHost=target,targetPath=path,
                           fragment=fragment or None,kind='internal' if target==host else
                           'estate' if target in hosts else 'external',occurrences=count))
    return result

def source_root(path,repo,edition):
    if repo=='Fountain-Coach/midi2':return None
    if repo=='Fountain-Coach/works-benedikt-eickhoff':value='.'
    elif repo=='Fountain-Coach/book-of-reframe':value='site'
    else:value=edition.get('publicationRoot')
    if not value:return None
    if value.startswith('/') or '..' in PurePosixPath(value).parts:raise ValueError('Unsafe publication root')
    directory=path/value
    if not directory.is_dir():raise ValueError('Missing source root '+str(directory))
    return directory

def inventory(pinned_revisions=None):
    domains=domains_from_manifest()
    required={v['sourceRepo'] for v in domains.values()}
    paths=checkouts(required)
    if required-set(paths):raise ValueError('Missing owner checkout: '+str(sorted(required-set(paths))))
    sources=[];routes=[];edges=[];risks=[]
    for repo in sorted(required):
        path=paths[repo]
        if remote_repo(path)!=repo:raise ValueError('Wrong repo '+repo)
        locked=(pinned_revisions or {}).get(repo)
        head=locked['head'] if locked else git(path,'rev-parse','HEAD')
        git(path,'cat-file','-e',head+'^{commit}')
        upstream=locked['localOriginMain'] if locked else git(path,'rev-parse','--verify','refs/remotes/origin/main',allow_failure=True)
        clean=locked['clean'] if locked else not git(path,'status','--porcelain')
        if not clean:risks.append(dict(type='dirty-owner-checkout',repository=repo))
        if upstream and upstream!=head:risks.append(dict(type='revision-differs-from-local-origin-main',repository=repo))
        files=[x for x in git(path,'ls-tree','-r','--name-only','-z',head).split('\x00') if x]
        info=json.loads(committed_bytes(path,'edition.json',head)) if 'edition.json' in files else {}
        if info.get('repository',info.get('authority',repo))!=repo:raise ValueError('Edition owner disagreement '+repo)
        base=source_root(path,repo,info)
        prefix=base.relative_to(path).as_posix() if base else None
        in_git=set(files)
        selected=sorted(x for x in in_git if not prefix or prefix=='.' or x.startswith(prefix+'/'))
        htmls=[x for x in selected if x.endswith(('.html','.htm'))]
        docs=[x for x in files if x.endswith(('.md','.tei','.xml','.markdown'))]
        origin_hosts=sorted(k for k,v in domains.items() if v['sourceRepo']==repo)
        committed={name:committed_bytes(path,name,head) for name in selected}
        filehash={name:digest(body) for name,body in committed.items()}
        inv_state='not-provided'
        inv_file=path/'publication-files.sha256'
        if 'publication-files.sha256' in files:
            entries={}
            for line in committed_bytes(path,'publication-files.sha256',head).decode().splitlines():
                h,sep,name=line.partition('  ')
                if not sep or name in entries:raise ValueError('Malformed SHA inventory '+repo)
                entries[name]=h
            if base and base.name=='site':
                actual={name[len(prefix)+1:]:filehash[name] for name in selected if name.startswith(prefix+'/')}
                inv_state='verified' if entries==actual else 'mismatch'
                if inv_state=='mismatch':risks.append(dict(type='source-file-inventory-mismatch',repository=repo))
            else:inv_state='source-snapshot-not-comparable'
        sources.append(dict(repository=repo,github='https://github.com/'+repo,
                  localCheckout=path.relative_to(DEV).as_posix(),head=head,localOriginMain=upstream or None,
                  headMatchesLocalOriginMain=(head==upstream if upstream else None),
                  clean=clean,sourceRoot=prefix,trackedFiles=len(files),
                  trackedHTML=len(htmls),trackedDocuments=len(docs),
                  trackedContentSHA256=digest(json.dumps(filehash,sort_keys=True).encode()),
                  sourceInventoryStatus=inv_state,editionState=info.get('publicationState',info.get('editionStatus')),
                  hosts=origin_hosts))
        if base is None:
            risks.append(dict(type='no-tracked-static-publication-root',repository=repo))
            continue
        for rel in htmls:
            inside=rel[len(prefix)+1:] if prefix and prefix!='.' else rel
            route=('/' if inside=='index.html' else '/'+inside[:-10] if inside.endswith('/index.html') else '/'+inside)
            for host in origin_hosts:
                routes.append(dict(host=host,owner=repo,route=route,sourceFile=rel,
                    sourceSHA256=filehash[rel],provenance='git-tracked-source'))
                edges.extend(parse_links(committed[rel],host,route,set(domains)))
    for host,value in sorted(domains.items()):
        for delegated in value['delegations']:
            prefix=delegated['pathPrefix'].rstrip('/')
            upstream=delegated['sourceDomain']
            matched=[r for r in routes if r['host']==upstream and r['owner']==delegated['sourceRepo']]
            owner_sources={row['repository']:row for row in sources}
            for r in matched:
                hosted_route=prefix+r['route']
                routes.append(dict(r,host=host,route=hosted_route,
                                   provenance='git-tracked-delegated-source',delegatedFrom=upstream))
                checkout=DEV/owner_sources[delegated['sourceRepo']]['localCheckout']
                revision=next(row['head'] for row in sources if row['repository']==delegated['sourceRepo'])
                edges.extend(parse_links(committed_bytes(checkout,r['sourceFile'],revision),host,hosted_route,set(domains)))
            if not matched:risks.append(dict(type='delegated-source-unavailable',host=host))
    routes.sort(key=lambda r:(r['host'],r['route'],r['owner']))
    edges.sort(key=lambda e:(e['host'],e['fromRoute'],e['targetHost'],e['targetPath'],e['fragment'] or ''))
    seen=set()
    for r in routes:
        k=(r['host'],r['route'])
        if k in seen:risks.append(dict(type='route-collision',host=k[0],route=k[1]))
        seen.add(k)
    for host,d in domains.items():
        if d['lifecycle']=='planned':risks.append(dict(type='planned-host-no-publication-assertion',host=host))
    result=dict(schema=SCHEMA,manifestSHA256=digest(MANIFEST.read_bytes()),
        principles={'source':'Git owner is authority for source; not for deployment state',
                    'hosting':'Independent live HTTPS readback is required for release',
                    'navigation':'Bookshelf is a projection, never the estate inventory'},
        domains=[dict(d,sourceCommit=next(s['head'] for s in sources if s['repository']==d['sourceRepo']),
                      sourceHTMLRoutes=sum(1 for r in routes if r['host']==host))
                 for host,d in sorted(domains.items())],
        sources=sources,risks=risks,
        counts=dict(hosts=len(domains),sourceRepositories=len(sources),gitHTMLRoutes=len(routes),
                    gitNavigationEdges=len(edges),riskFindings=len(risks)))
    return result,routes,edges

def emit(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n')

def persist(data,routes,edges,verify=False):
    for name,value in [('domain-ownership.json',data),('source-routes.json',routes)]:
        p=OUTPUT/name
        expected=json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
        if verify:
            if not p.exists() or p.read_text()!=expected:raise ValueError('STALE INVENTORY '+str(p))
        else:p.write_text(expected)
    # Every link is retained, including intra-chapter governance navigation,
    # but losslessly compressed for a small, stable, versioned Git artifact.
    compressed=gzip.compress((json.dumps(edges,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode(),compresslevel=9,mtime=0)
    p=OUTPUT/'navigation-edges.json.gz'
    if verify:
        if not p.exists() or p.read_bytes()!=compressed:raise ValueError('STALE INVENTORY '+str(p))
    else:p.write_bytes(compressed)
    # Accessible, compact listing of cross-domain relationships for reviews.
    associations={}
    for edge in edges:
        if edge['kind']!='estate':continue
        key=(edge['host'],edge['targetHost'])
        row=associations.setdefault(key,dict(fromHost=key[0],toHost=key[1],links=0,uniqueRoutes=set()))
        row['links']+=edge['occurrences']
        row['uniqueRoutes'].add(edge['fromRoute'])
    cross=[dict(fromHost=row['fromHost'],toHost=row['toHost'],links=row['links'],originRouteCount=len(row['uniqueRoutes'])) for row in associations.values()]
    cross.sort(key=lambda item:(item['fromHost'],item['toHost']))
    p=OUTPUT/'estate-relations.json'
    expected=json.dumps(cross,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if verify:
        if not p.exists() or p.read_text()!=expected:raise ValueError('STALE INVENTORY '+str(p))
    else:p.write_text(expected)
    print('ESTATE_INVENTORY_'+('VERIFIED' if verify else 'BUILT'),json.dumps(data['counts']))

def sample_routes(routes,host):
    values=sorted({r['route'] for r in routes if r['host']==host and r['route']!='/'})
    result=[]
    for prefix in ['/essays/','/chapters/','/editions/','/solstice/editions/first-reading/','/posts/','/instruments/']:
        choice=next((x for x in values if x.startswith(prefix)),None)
        if choice and choice not in result:result.append(choice)
    for value in values:
        if len(result)>=3:break
        if value not in result:result.append(value)
    return result[:3]

def request(url):
    with tempfile.TemporaryDirectory(prefix='estate-readback-') as tmp:
        file=Path(tmp)/'body'
        p=subprocess.run(['curl','-L','-sS','--max-time','14','--connect-timeout','5',
              '-o',str(file),'-w','%{http_code}|%{url_effective}|%{content_type}',url],
              capture_output=True,text=True)
        fields=p.stdout.strip().split('|',2)
        code=int(fields[0]) if fields and fields[0].isdigit() else 0
        row=dict(url=url,httpStatus=code,effectiveUrl=fields[1] if len(fields)>1 else None,
                 contentType=fields[2] if len(fields)>2 else None,
                 transportError=p.stderr.strip()[:300] if p.returncode else None)
        if file.exists():
            body=file.read_bytes()
            row.update(bytes=len(body),sha256=digest(body))
            if 'html' in (row['contentType'] or '') and len(body)<5_000_000:
                parser=Links();parser.feed(body.decode('utf8','replace'))
                row['anchorCount']=len(parser.values)
                row['linkedHosts']=sorted({urlsplit(urljoin(url,a)).hostname for a in parser.values
                       if urlsplit(urljoin(url,a)).hostname})
        return row

def probe(data,routes,edges):
    requests={}
    for domain in data['domains']:
        if domain['lifecycle']=='archived':continue
        host=domain['host']
        for route in ['/']+sample_routes(routes,host):
            requests[(host,route)]='https://'+host+route
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures={key:pool.submit(request,url) for key,url in requests.items()}
        values={key:f.result() for key,f in futures.items()}
    hashes={(r['host'],r['route']):r['sourceSHA256'] for r in routes}
    observations=[]
    for domain in data['domains']:
        host=domain['host'];checks=[]
        if domain['lifecycle']!='archived':
            for route in ['/']+sample_routes(routes,host):
                value=values[(host,route)];value['route']=route
                sourcehash=hashes.get((host,route));value['sourceSHA256']=sourcehash
                value['sameBytesAsCurrentSource']=(value.get('sha256')==sourcehash) if sourcehash else None
                if route=='/' and 'linkedHosts' in value and sourcehash:
                    allowed={item['host'] for item in data['domains']}
                    live_links=set(value['linkedHosts']) & allowed - {host}
                    source_links={e['targetHost'] for e in edges if e['host']==host and e['fromRoute']=='/' and e['kind']=='estate'}
                    value['publicEstateLinks']=sorted(live_links)
                    value['sourceEstateLinks']=sorted(source_links)
                    value['publicEstateLinksMissingFromSource']=sorted(live_links-source_links)
                if host=='fountain.coach' and route=='/':
                    source=next(s for s in data['sources'] if s['repository']==domain['sourceRepo'])
                    checkout=DEV/source['localCheckout']
                    metadata=json.loads((checkout/'edition.json').read_text())
                    revision=metadata.get('baselineGitCommit')
                    if revision:
                        raw=subprocess.run(['git','show',revision+':site/index.html'],cwd=checkout,capture_output=True)
                        if raw.returncode==0:
                            value['baselineGitCommit']=revision
                            value['sameBytesAsHistoricalBaseline']=digest(raw.stdout)==value.get('sha256')
                checks.append(value)
        observations.append(dict(host=host,lifecycle=domain['lifecycle'],checks=checks))
    result=dict(schema='fountain.estate.public-readback.v1',
       observedAt=datetime.now(timezone.utc).isoformat(timespec='seconds'),
       manifestSHA256=data['manifestSHA256'],scope='Sample of HTTPS root and max three routes per host; not complete public crawl',
       domains=observations)
    emit(OUTPUT/'public-readback.json',result)
    for row in observations:
        first=row['checks'][0] if row['checks'] else None
        print('HTTPS',row['host'],(first['httpStatus'] if first else 'archived'),
              'source-match',first.get('sameBytesAsCurrentSource') if first else None)
    return result

def make_report(data,witness):
    byhost={r['host']:r for r in witness['domains']} if witness else {}
    lines=['# Fountain Coach estate inventory','',
        'Machine-generated from owner Git checkouts and the Estate domain registry.',
        'No publishing, DNS, Caddy or Git mutation. Source ownership is not proof of deployment.','',
        '| Host | Owner | Role | Git HTML routes | Public root | Root matches current source |',
        '|---|---|---|---:|---|---|']
    for d in data['domains']:
        live=byhost.get(d['host']);root=(live['checks'][0] if live and live['checks'] else None)
        status=str(root['httpStatus']) if root else d['lifecycle']
        same=('yes' if root['sameBytesAsCurrentSource'] else 'no' if root['sameBytesAsCurrentSource'] is False else 'unverified') if root else 'unverified'
        lines.append('| '+' | '.join([d['host'],d['sourceRepo'],d['role'],
                      str(d['sourceHTMLRoutes']),status,same])+' |')
    lines+=['','## Critical boundaries','',
       f'- Complete tracked HTML routes are in source-routes.json; all {data["counts"]["gitNavigationEdges"]:,} navigation edges are preserved losslessly in navigation-edges.json.gz and cross-domain relations are summarized in estate-relations.json.',
       '- The public readback is a bounded sample; no false claim of exhaustive public routing.',
       '- The works.benedikt-eickhoff.de parent hostname is owned by works-benedikt-eickhoff; its /solstice/ subtree delegates to the Solstice source repository.',
       '- The MIDI2 code/documentation repository has no tracked deployed site root in this checkout; its live website must be read back independently.',
       '- Archived Tennis must not be counted as a live estate member. The planned Solstice hostname is not assumed to resolve.',
       '- A source revision differing from production is not a reason to replace a public estate homepage with a new bookshelf.',
       '','## Public deployment reconciliation','']
    if witness:
        for row in witness['domains']:
            root=row['checks'][0] if row['checks'] else None
            if root and root.get('httpStatus')==0:
                lines.append('- '+row['host']+': no successful HTTPS response; do not claim this host is published')
            elif root and root.get('sameBytesAsCurrentSource') is False:
                suffix=('; matches historical root Git baseline' if root.get('sameBytesAsHistoricalBaseline') else '')
                lines.append('- '+row['host']+': live HTTPS differs from current checked-out source'+suffix)
            if root and root.get('publicEstateLinksMissingFromSource'):
                lines.append('- '+row['host']+': public estate root links absent from current candidate navigation: '+', '.join(root['publicEstateLinksMissingFromSource']))
    lines+=['','## Repository-side risks','']
    lines += ['- '+r['type']+': '+str(r.get('host',r.get('repository',''))) for r in data['risks']]
    lines+=['','## Controls','',
       'Build source inventory: npm run inventory:build',
       'Check source inventory without modification: npm run inventory:verify',
       'Read back public HTTPS samples: npm run inventory:probe',
       '',
       'Human review and governed publishing remain separate steps.']
    (OUTPUT/'README.md').write_text('\n'.join(lines)+'\n')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['build','verify','probe'])
    mode=parser.parse_args().mode
    OUTPUT.mkdir(exist_ok=True)
    pinned=None
    if mode=='verify':
        recorded=OUTPUT/'domain-ownership.json'
        if not recorded.exists():raise ValueError('Missing source lock: build inventory first')
        pinned={item['repository']:item for item in json.loads(recorded.read_text())['sources']}
    data,routes,edges=inventory(pinned)
    persist(data,routes,edges,mode=='verify')
    witness=probe(data,routes,edges) if mode=='probe' else (
       json.loads((OUTPUT/'public-readback.json').read_text()) if (OUTPUT/'public-readback.json').exists() else None)
    if mode!='verify':make_report(data,witness)

if __name__=='__main__':main()
