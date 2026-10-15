#!/usr/bin/env python3
"""Bounded, read-only public HTTPS route and asset discoverability census.

No Caddy/SSH/DNS/tunnel mutation. This is a bounded link crawl, not a proof
that unlinked or dynamic public resources do not exist.
"""
import argparse
import concurrent.futures
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urljoin,urlsplit,urlunsplit,unquote

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recovery/public-route-census.json'
HUMAN=ROOT/'recovery/public-route-census.md'
ACTIVE={
 'fountain.coach','book.fountain.coach','governance.fountain.coach',
 'midi2.fountain.coach','instruments.fountain.coach',
 'status.fountain.coach','teatro.fountain.coach',
 'benedikt-eickhoff.de','works.benedikt-eickhoff.de'
}
MAX_BYTES=25_000_000
MAX_URLS=2200
MAX_PER_HOST=600
MAX_HTML=2_000_000
class Refs(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('a','link','script','img','source','video','audio','iframe'):
            for key in ('href','src','poster'):
                if a.get(key):self.urls.append(a[key])
            if a.get('srcset'):
                self.urls.extend(x.strip().split(' ')[0] for x in a['srcset'].split(','))
def safe_url(url,base=''):
    if not url or url.startswith(('mailto:','tel:','data:','blob:','javascript:','#')):
        return None
    parsed=urlsplit(urljoin(base,url))
    if parsed.scheme!='https' or parsed.hostname not in ACTIVE:return None
    path=parsed.path or '/'
    if any(x in ('..','.') for x in path.split('/')):return None
    if len(path)>700:return None
    return urlunsplit(('https',parsed.hostname,path,'',''))
def root_and_seeds():
    inv=json.loads((ROOT/'inventory/domain-ownership.json').read_text())
    locked={d['host']:d for d in inv['domains']}
    if not ACTIVE.issubset(locked):raise ValueError('Estate registry lacks a public host')
    seeds={'https://'+host+'/' for host in ACTIVE}
    source=json.loads((ROOT/'inventory/source-routes.json').read_text())
    for item in source:
        host=item['host']
        if host in ACTIVE:seeds.add('https://'+host+item['route'])
    for name in ('root-matched-historical-artifacts.json',):
        witness=json.loads((ROOT/'recovery'/name).read_text())
        for section in witness['subjects']:
            for file in section['files']:
                u=safe_url(file['publicUrl'])
                if u:seeds.add(u)
    return sorted(seeds)
def request(url):
    with tempfile.TemporaryDirectory(prefix='estate-crawl-') as folder:
        dest=Path(folder)/'body';headers=Path(folder)/'headers'
        cmd=['curl','--silent','--show-error','--max-time','20','--connect-timeout','5',
             '--header','Accept-Encoding: identity','--max-filesize',str(MAX_BYTES),
             '-D',str(headers),'-o',str(dest),'-w','%{http_code}|%{content_type}|%{url_effective}',url]
        try:r=subprocess.run(cmd,capture_output=True,text=True,timeout=25)
        except subprocess.TimeoutExpired:
            return dict(url=url,status=0,outcome='TIMEOUT',discovered=[],bytes=None,sha256=None)
        fields=r.stdout.strip().split('|',2)
        status=int(fields[0]) if fields and fields[0].isdigit() else 0
        content_type=fields[1] if len(fields)>1 else ''
        effective=fields[2] if len(fields)>2 else ''
        body=dest.read_bytes() if dest.exists() else b''
        hd=headers.read_text(errors='replace') if headers.exists() else ''
        location=re.findall(r'^location:\s*(.+)$',hd,re.M|re.I)
        redirects=[safe_url(location[-1].strip(),url)] if location else []
        discovered=[]
        if status==200 and r.returncode==0:
            if 'html' in content_type.lower() and len(body)<=MAX_HTML:
                parser=Refs();parser.feed(body.decode('utf8','replace'))
                discovered=[x for x in (safe_url(h,url) for h in parser.urls) if x]
            elif 'css' in content_type.lower() and len(body)<=MAX_HTML:
                raw=body.decode('utf8','replace')
                values=re.findall(r'url\(\s*[^)]*?\)',raw,re.I)
                for val in values:
                    val=val[4:-1].strip(' \"\'')
                    dest_url=safe_url(val,url)
                    if dest_url:discovered.append(dest_url)
        found=sorted(set(discovered+redirects))
        return dict(url=url,status=status,outcome='OK' if r.returncode==0 else 'CURL_ERROR',
            contentType=content_type,bytes=len(body) if dest.exists() else None,
            sha256=hashlib.sha256(body).hexdigest() if dest.exists() else None,
            redirects=redirects,discovered=found,
            error=r.stderr.strip()[:140] if r.returncode else None,
            finalUrl=effective)
def walk():
    seeds=root_and_seeds()
    queue=list(seeds)
    visited=set();rows=[]
    pending_counts={}
    for s in seeds:
        host=urlsplit(s).hostname
        pending_counts[host]=pending_counts.get(host,0)+1
    if len(queue)>MAX_URLS:raise ValueError('Seed list exceeds bound')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures={}
        def schedule():
            while queue and len(futures)<10 and len(visited)+len(futures)<MAX_URLS:
                url=queue.pop(0)
                if url in visited:continue
                host=urlsplit(url).hostname
                if sum(urlsplit(x).hostname==host for x in visited)>=MAX_PER_HOST:continue
                visited.add(url)
                futures[pool.submit(request,url)]=url
        schedule()
        while futures:
            completed=next(concurrent.futures.as_completed(futures))
            url=futures.pop(completed)
            row=completed.result();rows.append(row)
            for child in row['discovered']:
                host=urlsplit(child).hostname
                if child not in visited and child not in queue and pending_counts.get(host,0)<MAX_PER_HOST:
                    queue.append(child);pending_counts[host]=pending_counts.get(host,0)+1
            if len(rows)%100==0:print('CENSUS_PROGRESS',len(rows),'queued',len(queue),flush=True)
            schedule()
    rows.sort(key=lambda item:item['url'])
    counts={}
    for host in sorted(ACTIVE):
        relevant=[x for x in rows if urlsplit(x['url']).hostname==host]
        counts[host]=dict(probed=len(relevant),ok200=sum(x['status']==200 for x in relevant),
            not2xx=sum(x['status']!=200 for x in relevant),
            html=sum(x['status']==200 and 'html' in x['contentType'] for x in relevant),
            errors=sum(x['outcome']!='OK' for x in relevant))
    return dict(schema='fountain.estate.bounded-live-route-census.v1',witnessBasis='read-only HTTPS GET, no deployment state mutated',
       includesAllPublicAssets=False,limits=dict(maxUrlCount=MAX_URLS,maxPerHost=MAX_PER_HOST,maxResponseBytes=MAX_BYTES),
       seedCount=len(seeds),sampleCount=len(rows),uncrawledQueueCount=len(queue),
       hosts=counts,results=rows)
def report(c):
    lines=['# Public estate: bounded route and asset census','',
        'Read-only HTTPS GET discovery from all nine known currently public estate host roots, their Git-owned HTML route candidates, and known archival publication assets. This is **not** an exhaustive public filesystem inventory. Unlinked routes, dynamic services and resources larger than the size cap may not appear.',
        '', '| Public hostname | Fetched | HTTP 200 | Other HTTP | HTML 200 | Request errors |',
        '|---|---:|---:|---:|---:|---:|']
    for host,count in c['hosts'].items():
        lines.append('| '+host+' | '+str(count['probed'])+' | '+str(count['ok200'])+
          ' | '+str(count['not2xx'])+' | '+str(count['html'])+' | '+str(count['errors'])+' |')
    lines+=['', '**Across all hosts:** '+str(c['sampleCount'])+' fetched URLs; '+str(c['uncrawledQueueCount'])+' URLs still queued when bounded crawl ended.',
        '', 'Every fetched URL has a status, response content hash where available, and discovered on-estate links/assets in [public-route-census.json](public-route-census.json).',
        '',
        '## Coverage limits','',
        '- A URL returning 200 does not prove identical content exists in the canonical owner source. Independent blob provenance and full release receipts are required.',
        '- Only nine live hostnames are followed; planned Solstice and archived Tennis are excluded.',
        '- Canonical ownership and delegated Solstice route identity remain unchanged.',
        '- Relative URLs, scripts, images and CSS url() references are followed, subject to fixed host/size/count restrictions. Redirects are recorded.',
        '- URLs with query strings are collapsed to the same path. Interactive API, signed/private endpoints, JavaScript-generated requests, and nonlinked documents may not be discovered.',
        '- No GitHub branch, Ubuntu service, public DNS, tunnel or Caddy deployment is changed.',
        '','Run: npm run recovery:crawl:probe to refresh; npm run recovery:crawl:verify checks the frozen witness structure offline (not the present live site).']
    return '\n'.join(lines)+'\n'
def verify():
    c=json.loads(OUT.read_text())
    if c['schema']!='fountain.estate.bounded-live-route-census.v1':raise ValueError('Wrong census contract')
    if set(c['hosts'])!=ACTIVE:raise ValueError('Missing estate domain')
    if c['sampleCount']!=len(c['results']) or c['sampleCount']>MAX_URLS:raise ValueError('Wrong count')
    if len({x['url'] for x in c['results']})!=len(c['results']):raise ValueError('Duplicate URL')
    for row in c['results']:
        if safe_url(row['url'])!=row['url']:raise ValueError('Unsafe URL in census')
        if row['status']==200 and row['outcome']=='OK' and not row['sha256']:raise ValueError('Missing response digest')
    for host,count in c['hosts'].items():
        rows=[x for x in c['results'] if urlsplit(x['url']).hostname==host]
        if count['probed']!=len(rows):raise ValueError('Wrong host count')
    if HUMAN.read_text()!=report(c):raise ValueError('Stale human report')
    print('PUBLIC_CENSUS_VERIFIED',c['sampleCount'],'URLs',len(c['hosts']),'hosts')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['probe','verify'])
    args=ap.parse_args()
    if args.action=='verify':verify();return
    c=walk()
    OUT.write_text(json.dumps(c,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    HUMAN.write_text(report(c))
    print('PUBLIC_CENSUS_PROBED',c['sampleCount'],'URLs',len(c['hosts']),'hosts')
if __name__=='__main__':main()
