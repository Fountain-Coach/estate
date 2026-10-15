#!/usr/bin/env python3
"""Validate all 600 frozen public HTTP-200 resources against loopback Caddy.

Runs on the dedicated Ubuntu recovery machine. No remote URLs are requested,
no DNS/prod mutation, all redirects must be relative paths on localhost.
"""
import collections
import hashlib
import http.client
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path('/home/benedikt/fountain-recovery-cold-20261015/payload')
manifest=json.loads((ROOT/'manifest.json').read_text())
hosts=set(manifest['hostnames'])
if len(hosts)!=9 or len(manifest['records'])!=600 or manifest['releaseAdmitted']:
    raise RuntimeError('Invalid recovery proof manifest')
conn=http.client.HTTPConnection('127.0.0.1',18480,timeout=10)
failures=[]
verified=0
redirected=0
counts=collections.Counter()
for record in manifest['records']:
    url=urlsplit(record['url'])
    if url.scheme!='https' or url.hostname not in hosts or url.query or url.fragment:
        raise RuntimeError('Unverified target')
    path=url.path or '/'
    response=None
    for attempt in range(3):
        conn.request('GET',path,headers={'Host':url.hostname,'Accept-Encoding':'identity'})
        response=conn.getresponse()
        status=response.status
        body=response.read()
        if status in (301,302,307,308):
            location=response.getheader('Location','')
            if not location.startswith('/') or location.startswith('//') or '?' in location:
                failures.append(dict(url=record['url'],status=status,problem='UNSAFE_REDIRECT',location=location))
                break
            if location==path:
                failures.append(dict(url=record['url'],status=status,problem='REDIRECT_LOOP'))
                break
            redirected+=1
            path=location
            continue
        sha=hashlib.sha256(body).hexdigest()
        counts[url.hostname]+=1
        if status!=200 or sha!=record['sha256'] or len(body)!=record['bytes']:
            failures.append(dict(url=record['url'],status=status,sha=sha,expected=record['sha256'],
                                 actualBytes=len(body),expectedBytes=record['bytes'],problem='BYTE_MISMATCH'))
        else:verified+=1
        break
    else: failures.append(dict(url=record['url'],problem='TOO_MANY_REDIRECTS'))
conn.close()
print('RESTORE_LOOPBACK_VERIFIED',verified,'OF',len(manifest['records']),
      'REDIRECT_HOPS',redirected)
print('PER_HOST',json.dumps(dict(sorted(counts.items())),sort_keys=True))
print('FAILURES',len(failures))
for f in failures[:25]:print(json.dumps(f))
if failures or verified!=len(manifest['records']):raise SystemExit(1)
