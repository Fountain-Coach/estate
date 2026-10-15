#!/usr/bin/env python3
"""Read-only compare Git-tracked historical estate projection files with live HTTP.

This is an evidentiary audit, not approval to replace canonical owner sources.
"""
import argparse
import concurrent.futures
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
DEV=Path(os.environ.get('FOUNTAIN_DEV_ROOT',ROOT.parents[1])).resolve()
ARCHIVE=DEV/'solstice-caddy-20261012'
OUT=ROOT/'recovery'
REPORT=OUT/'historical-projection-audit.json'
DOC=OUT/'historical-projection-audit.md'
REF='aba0a0ea941a886642bb4d87df5bfd99f674c6d3'
PROJECTION='Fountain-Coach/midi2-gpu-fabric'
MAX_FILE_BYTES=30_000_000
SUBJECTS=(
  ('book.fountain.coach','book.fountain.coach','/'),
  ('midi2.fountain.coach','midi2.fountain.coach','/'),
  ('solstice.fountain.coach','works.benedikt-eickhoff.de','/solstice/'),
)
def digest(data):return hashlib.sha256(data).hexdigest()
def git(*args,as_bytes=False):
    proc=subprocess.run(['git',*args],cwd=ARCHIVE,capture_output=True)
    if proc.returncode:raise RuntimeError('Git archive query failed: '+repr(args)+' '+proc.stderr.decode('utf8','replace')[:160])
    return proc.stdout if as_bytes else proc.stdout.decode().strip()
def source_files(subject,revision=None):
    root='estate/sites/'+subject
    output=git('ls-tree','-r','--format=%(objectmode) %(objecttype) %(objectname) %(path)',revision or REF,'--',root)
    rows=[]
    for line in output.splitlines():
        parts=line.split(' ',3)
        if len(parts)!=4 or parts[1]!='blob':continue
        mode,kind,oid,path=parts
        rel=path[len(root)+1:]
        data=git('cat-file','blob',oid,as_bytes=True)
        rows.append(dict(sourcePath=path,relativePath=rel,sourceGitBlob=oid,
                         sourceSHA256=digest(data),sourceBytes=len(data)))
    return rows
def request(row,host,prefix):
    relative=row['relativePath']
    url_path='/'.join(quote(segment,safe='-._~') for segment in relative.split('/'))
    if relative=='index.html':url_path=''
    elif relative.endswith('/index.html'):url_path=url_path[:-10]
    url='https://'+host+prefix+url_path
    with tempfile.TemporaryDirectory(prefix='estate-audit-') as tmp:
        target=Path(tmp)/'body'
        cmd=['curl','--location','--silent','--show-error','--max-time','24',
             '--connect-timeout','5','--max-filesize',str(MAX_FILE_BYTES),
             '--header','Accept-Encoding: identity','--output',str(target),
             '--write-out','%{http_code}|%{url_effective}|%{content_type}',url]
        try:
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
        except subprocess.TimeoutExpired:
            return dict(row,publicUrl=url,httpStatus=0,publicBytes=None,
                        publicSHA256=None,comparison='TRANSPORT_TIMEOUT')
        fields=proc.stdout.strip().rsplit('|',2)
        http=int(fields[0]) if len(fields)>0 and fields[0].isdigit() else 0
        effective=fields[1] if len(fields)>1 else ''
        content_type=fields[2] if len(fields)>2 else ''
        actual_host=urlsplit(effective).hostname
        body=target.read_bytes() if target.is_file() else b''
        if proc.returncode:
            comparison='TRANSPORT_ERROR' if not body else 'INCOMPLETE_RESPONSE'
        elif actual_host!=host:
            comparison='UNEXPECTED_REDIRECT_HOST'
        elif http!=200:
            comparison='NOT_HTTP_200'
        elif digest(body)==row['sourceSHA256']:
            comparison='EXACT'
        else:
            comparison='DIFFERENT'
        return dict(row,publicUrl=url,effectiveUrl=effective,httpStatus=http,
                    contentType=content_type,publicBytes=len(body),
                    publicSHA256=digest(body) if body else None,comparison=comparison,
                    error=proc.stderr[:220].strip() if proc.returncode else None)
def report(data):
    lines=['# Historical estate projection: public artifact comparison','',
           '**Archive evidence only — no ownership reassignment or release admission.**',
           '', 'Git source: ['+PROJECTION+'](https://github.com/'+PROJECTION+'/tree/'+REF+'/estate/sites) at immutable commit `'+REF+'`.',
           '', 'This audit reads the committed Git blobs, not the old worktree. Public files are fetched via bounded GET requests and compared byte-for-byte. Git-tracked archived pages are **not necessarily public obligations**; HTTP 404 can indicate never-published staging material.',
           '','| Public target | Tracked blobs | Exactly matching | Different bytes | HTTP missing | Transport/error |',
           '|---|---:|---:|---:|---:|---:|']
    for s in data['subjects']:
        c=s['counts']
        lines.append('| '+s['publicHost']+s['publicPrefix']+' | '+str(c['total'])+
        ' | '+str(c['EXACT'])+' | '+str(c['DIFFERENT'])+' | '+str(c['NOT_HTTP_200'])+
        ' | '+str(c['TRANSPORT_ERROR']+c['TRANSPORT_TIMEOUT']+c['INCOMPLETE_RESPONSE']+c['UNEXPECTED_REDIRECT_HOST'])+' |')
    lines+=['','## Recoverability decision','',
      '**Still BLOCKED.** An exact archival blob match proves one historical projection contains the observed bytes. It does not prove that the canonical owning repository can regenerate them or that the complete release inventory, offsite backups and dynamic dependencies exist.',
      'Do not migrate content ownership to midi2-gpu-fabric merely because the root was found there.',
      'The live `works.benedikt-eickhoff.de/solstice/` prefix is delegated content; `solstice.fountain.coach` is not assumed publicly reachable.',
      'Diffs are evidence of divergent publication revisions, not a signal to overwrite either side.',
      '',
      '## Unmatched public observations','']
    for s in data['subjects']:
        lines+=['### '+s['publicHost']+s['publicPrefix'],'']
        discrepancies=[f for f in s['files'] if f['comparison']!='EXACT']
        for f in discrepancies[:40]:
            lines.append('- `'+f['relativePath']+'`: '+f['comparison']+' (HTTP '+str(f['httpStatus'])+')')
        if len(discrepancies)>40:lines.append('- … and '+str(len(discrepancies)-40)+' additional unmatched tracked blobs (see JSON)')
        if not discrepancies:lines.append('- All tracked blobs in this archival projection match, but public completeness is not established.')
        lines.append('')
    lines+=['## Safety and scope','',
       'Only the three named archival projection trees are checked. Public URLs are allowed only beneath their fixed configured host/prefix. Every request is capped at '+str(MAX_FILE_BYTES)+' bytes, 24 seconds, and moderate concurrency. No live files or credentials are uploaded. Results store only paths, checksums, HTTP evidence and Git identifiers. No SSH, DNS, Caddy, tunnel or production mutation.',
       '',
       'Refresh observed bytes: `npm run recovery:archive-probe`; verify frozen report against the current Git blob identities: `npm run recovery:archive-verify`. Re-running the probe may produce different results if publication changes.',
       '']
    return '\n'.join(lines)
def audit():
    actual=git('remote','get-url','origin')
    if 'Fountain-Coach/midi2-gpu-fabric' not in actual:
        raise RuntimeError('Untrusted archive origin '+actual)
    git('cat-file','-e',REF+'^{commit}')
    total=[]
    for source,public,prefix in SUBJECTS:
        files=source_files(source)
        if not files:raise RuntimeError('Missing archival source '+source)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            future=[pool.submit(request,row,public,prefix) for row in files]
            checked=[f.result() for f in future]
        checked.sort(key=lambda x:x['relativePath'])
        codes=('EXACT','DIFFERENT','NOT_HTTP_200','TRANSPORT_ERROR','TRANSPORT_TIMEOUT','INCOMPLETE_RESPONSE','UNEXPECTED_REDIRECT_HOST')
        counts=dict(total=len(checked),**{code:sum(f['comparison']==code for f in checked) for code in codes})
        print('ARCHIVAL_COMPARISON',public+prefix,counts,flush=True)
        total.append(dict(archivalHost=source,publicHost=public,publicPrefix=prefix,
                          sourceRoot='estate/sites/'+source,counts=counts,files=checked))
    return dict(schema='fountain.estate.archival-artifact-witness.v1',
                recordedAt=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                archivalRepo=PROJECTION,archivalRevision=REF,
                admission='BLOCKED',ownerTransferAuthorized=False,
                auditScope='All Git-tracked archival projection blobs for three surfaces, not all public routes',
                subjects=total)
def verify():
    data=json.loads(REPORT.read_text())
    if data['archivalRevision']!=REF or data['archivalRepo']!=PROJECTION or data['admission']!='BLOCKED':
        raise RuntimeError('Untrusted archived report')
    if data['ownerTransferAuthorized'] is not False:raise RuntimeError('Unsafe owner transfer')
    if len(data['subjects'])!=len(SUBJECTS):raise RuntimeError('Missing archival subject')
    for s in data['subjects']:
        files=source_files(s['archivalHost'])
        by_path={f['relativePath']:f for f in files}
        if len(by_path)!=len(s['files']):raise RuntimeError('Stale archival source paths')
        for f in s['files']:
            current=by_path[f['relativePath']]
            if any(current[key]!=f[key] for key in ('sourceSHA256','sourceGitBlob','sourceBytes')):
                raise RuntimeError('Stale archival Git source file '+f['relativePath'])
        if s['counts']['total']!=len(files):raise RuntimeError('Wrong archived count')
        for code in ('EXACT','DIFFERENT','NOT_HTTP_200','TRANSPORT_ERROR','TRANSPORT_TIMEOUT','INCOMPLETE_RESPONSE','UNEXPECTED_REDIRECT_HOST'):
            if s['counts'][code]!=sum(f['comparison']==code for f in s['files']):raise RuntimeError('Wrong result count')
    if DOC.read_text()!=report(data):raise RuntimeError('Human-readable archive witness stale')
    print('ARCHIVAL_AUDIT_VERIFIED',sum(s['counts']['total'] for s in data['subjects']),'blobs')
def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=('probe','verify'))
    args=p.parse_args()
    if args.mode=='verify':verify();return
    data=audit()
    OUT.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    DOC.write_text(report(data))
    print('ARCHIVAL_AUDIT_RECORDED',len(data['subjects']),'surfaces')
if __name__=='__main__':main()
