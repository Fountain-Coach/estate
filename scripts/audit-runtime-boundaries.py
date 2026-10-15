#!/usr/bin/env python3
"""Inspect frozen publicly served assets for browser/runtime dependency indicators.

Read-only, deterministic, no network. These are code-presence hints, not proof
that a capability is currently active or restorable.
"""
import argparse
from collections import Counter
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import urljoin,urlsplit

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'recovery'
ARCHIVE=REC/'bundles/estate-public-observed-20261015.tar.gz'
MANIFEST=REC/'bundles/estate-public-observed-20261015.manifest.json'
OUTPUT=REC/'runtime-boundary-witness.json'
DOC=REC/'runtime-boundary-witness.md'
TOKENS={
 'browser_audio':r'AudioContext|webkitAudioContext|OfflineAudioContext',
 'midi_browser_api':r'navigator[.]requestMIDIAccess|MIDIAccess|MIDIOutput',
 'csound_browser':r'Csound|csound|@csound/',
 'camera_or_microphone':r'getUserMedia|mediaDevices',
 'websocket_or_sse':r'WebSocket\s*\(|EventSource\s*\(',
 'fetch_api':r'\bfetch\s*\(',
 'persistent_browser_storage':r'localStorage|indexedDB|sessionStorage',
 'service_worker':r'serviceWorker\b',
 'wasm':r'WebAssembly\b|[.]wasm',
 'oauth_or_external_identity':r'OAuth|openid|authorization_code|client_id',
}
class Sources(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        for k in ('href','src','poster','action'):
            if d.get(k):self.refs.append(d[k])
def sha(b):return hashlib.sha256(b).hexdigest()
def gather():
    manifest=json.loads(MANIFEST.read_text())
    files={}
    with tarfile.open(ARCHIVE,'r:gz') as tar:
        for member in tar:
            if not member.isfile() or not member.name.startswith('sites/'):continue
            if member.name.endswith(('.js','.html','.css','.htm','.json')):
                files[member.name]=tar.extractfile(member).read()
    byhost={}
    records=manifest['records']
    for host in manifest['hostnames']:
        items=[e for e in records if urlsplit(e['url']).hostname==host]
        counts=Counter()
        codes={}
        external_urls=set()
        for e in items:
            extension=Path(urlsplit(e['url']).path).suffix.lower() or 'route'
            counts[extension]+=1
            key=e['bundlePath']
            if key not in files:continue
            content=files[key].decode('utf8','replace')
            matches=sorted(name for name,pattern in TOKENS.items() if re.search(pattern,content,re.I))
            if matches:codes[key]=matches
            if extension in ('.html','.htm','route'):
                parser=Sources()
                parser.feed(content)
                for link in parser.refs:
                    if link.startswith(('data:','mailto:','tel:','javascript:','#')):continue
                    result=urlsplit(urljoin(e['url'],link))
                    if result.hostname and result.hostname!=host:
                        external_urls.add(result.hostname)
        indicators={}
        for kind in TOKENS:
            examples=sorted(path for path,labels in codes.items() if kind in labels)
            if examples:indicators[kind]=dict(fileCount=len(examples),examplePaths=examples[:6])
        byhost[host]=dict(publicResources=len(items),fileExtensions=dict(sorted(counts.items())),
            browserCodeIndicators=indicators,externalHtmlLinkHosts=sorted(external_urls)[:50],
            httpResponseReplayProof='PASS_BOUNDED',
            browserRuntimeBehaviorProof='NOT_TESTED',
            serverSideApiRecoveryProof='NOT_TESTED')
    return dict(schema='fountain.estate.public-browser-runtime-indicators.v1',
        bundleSHA256=sha(ARCHIVE.read_bytes()),
        staticResourceBytesVerified=True,
        inferenceLimit='Presence of words or script references is not evidence of functioning or deployed external service. Missing signs cannot prove absence.',
        deviceOrBrowserInteractionTested=False,
        privateStoreRestoreProven=False,serverAPIsRestored=False,
        hosts=byhost)
def human(d):
    lines=['# Browser and server-runtime continuity evidence','',
        '**This is a static-source inspection, not an interactive browser or service test.**',
        '', 'The recovered public artifact has 600 byte-verifiable HTTP-200 responses and is served by Caddy on Ubuntu. That proves only the bytes. This inspection records browser API/library indicators and external HTML reference hosts; the presence of a token does not prove a working API, and absence does not prove no runtime dependency.',
        '', '| Public host | Resources | Browser code indicators | Runtime accepted? |',
        '|---|---:|---|---|']
    for host,row in d['hosts'].items():
        labels=', '.join(sorted(row['browserCodeIndicators'])) or 'none detected'
        lines.append('| '+host+' | '+str(row['publicResources'])+' | '+labels+' | Not tested |')
    lines+=['','## Why dynamic recovery is not admitted','',
        'Browser MIDI, Csound, AudioContext, service workers and network APIs may require device activation, hardware permissions, audio assets, cross-domain origin policies or external services. The static archive cannot reproduce private FountainStore operations, OAuth state, authenticated services or past user data. The app/service owners must furnish independently backed runtime/service state and endpoint health contracts.',
        '', 'For each actual interactive service, a later acceptance test needs an independent client (including iPad for the reading/performance UX), correct canonical Host/TLS identity, permission grants and an observed end-to-end result—not only a GET 200.',
        '', 'Detailed per-host evidence and limited path examples are in [runtime-boundary-witness.json](runtime-boundary-witness.json). Run npm run recovery:runtime:build to refresh from the frozen public bundle, and npm run recovery:runtime:verify to detect drift without network requests.',
        '']
    return '\n'.join(lines)
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=('build','verify'))
    mode=p.parse_args().mode
    result=gather()
    data=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    report=human(result)
    if mode=='verify':
        if OUTPUT.read_text()!=data or DOC.read_text()!=report:
            raise RuntimeError('STALE_RUNTIME_BOUNDARY_WITNESS')
    else:
        OUTPUT.write_text(data);DOC.write_text(report)
    print('RUNTIME_BOUNDARY_'+mode.upper(),len(result['hosts']),'hosts',
          sum(bool(v['browserCodeIndicators']) for v in result['hosts'].values()),'with indicators',
          'dynamic service recovery',result['serverAPIsRestored'])
if __name__=='__main__':main()
