#!/usr/bin/env python3
"""Resolve public-byte provenance into immutable Git blobs where possible.

Read-only; uses frozen HTTPS audit and committed Git history; no web calls.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recovery'
AUDIT=OUT/'root-matched-historical-artifacts.json'
RESULT=OUT/'public-byte-provenance.json'
DOC=OUT/'public-byte-provenance.md'
SCHEMA='fountain.estate.public-byte-provenance.v1'
SPEC=importlib.util.spec_from_file_location('archive_source',ROOT/'scripts/audit-historical-projection.py')
archive=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive)
OWNER={
 'book.fountain.coach':'Fountain-Coach/book-of-reframe',
 'midi2.fountain.coach':'Fountain-Coach/midi2',
 'solstice.fountain.coach':'Fountain-Coach/solstice.fountain.coach',
}
def sha(b):return hashlib.sha256(b).hexdigest()
def blob_match(path,expected):
    history=archive.git('log',archive.REF,'--format=%H','--',path).splitlines()
    for revision in history:
        body=archive.git('show',revision+':'+path,as_bytes=True)
        if sha(body)==expected:
            oid=archive.git('rev-parse',revision+':'+path)
            return dict(revision=revision,gitBlob=oid)
    return None
def generate():
    evidence=json.loads(AUDIT.read_text())
    if evidence['releaseAdmitted'] or evidence['ownershipTransferred']:
        raise ValueError('Untrusted root matched release witness')
    sections=[]
    for source in sorted(OWNER):
        original=next(x for x in evidence['subjects'] if x['archivalSourceHost']==source)
        rows=[]
        for item in original['files']:
            status=item['comparison']
            base=dict(publicUrl=item['publicUrl'],relativePath=item['relativePath'],
                      publicSHA256=item['publicSHA256'],httpStatus=item['httpStatus'],
                      rootMatchingRevision=original['revision'],historicalSourcePath=item['sourcePath'])
            if status=='EXACT':
                match=dict(revision=original['revision'],gitBlob=item['sourceGitBlob'])
                state='ROOT_REVISION_EXACT'
            elif status=='DIFFERENT':
                match=blob_match(item['sourcePath'],item['publicSHA256'])
                state='OTHER_GIT_REVISION_EXACT' if match else 'PUBLIC_BYTES_NOT_LOCATED'
            elif status=='NOT_HTTP_200':
                match=None;state='ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL'
            else:
                match=None;state='INCOMPLETE_HTTP_EVIDENCE'
            if match:
                contents=archive.git('cat-file','blob',match['gitBlob'],as_bytes=True)
                if sha(contents)!=item['publicSHA256']:
                    raise ValueError('Bad Git blob candidate '+item['sourcePath'])
            rows.append(dict(base,state=state,matchingGitRevision=match['revision'] if match else None,
                             matchingGitBlob=match['gitBlob'] if match else None))
        states=['ROOT_REVISION_EXACT','OTHER_GIT_REVISION_EXACT','PUBLIC_BYTES_NOT_LOCATED',
                'ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL','INCOMPLETE_HTTP_EVIDENCE']
        counts={s:sum(row['state']==s for row in rows) for s in states}
        counts['archivalFileCount']=len(rows)
        sections.append(dict(archivalHost=source,publicHost=original['publicHost'],
                             publicPrefix=original['publicPrefix'],
                             canonicalOwnerRepo=OWNER[source],historicalProjectionRepo=archive.PROJECTION,
                             selectedRootRevision=original['revision'],counts=counts,files=rows))
    return dict(schema=SCHEMA,sourceAuditSHA256=sha(AUDIT.read_bytes()),gitSearchBoundary=archive.REF,
                owningSourcesUntouched=True,completePublicRecoveryProof=False,
                releaseAdmitted=False,allowDeployment=False,sections=sections)
def report(d):
    lines=['# Public-byte provenance: Git historical composition','',
        '**Evidence-only: no recovery release admitted and no source ownership reassignment.**','',
        'The exact public HTML roots were found in historical Git commits of an archival estate projection. For each file that differs from its root-matched tree, this report searches all commits ancestral to the fixed archival witness commit for the exact public SHA-256. This locates independently recoverable historical blobs **without downloading or committing live content**.',
        '', '| Public target | Root-tree exact | Exact blob in another historical revision | Public bytes not found in Git search | Archive URL not HTTP 200 |',
        '|---|---:|---:|---:|---:|']
    for sec in d['sections']:
        c=sec['counts']
        lines.append('| '+sec['publicHost']+sec['publicPrefix']+' | '+str(c['ROOT_REVISION_EXACT'])+
                     ' | '+str(c['OTHER_GIT_REVISION_EXACT'])+' | '+str(c['PUBLIC_BYTES_NOT_LOCATED'])+
                     ' | '+str(c['ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL'])+' |')
    total={key:sum(sec['counts'][key] for sec in d['sections']) for key in d['sections'][0]['counts']}
    lines+=['','**Across this limited archived-file set:** '+str(total['ROOT_REVISION_EXACT']+total['OTHER_GIT_REVISION_EXACT'])+
            ' public responses have exact Git blob provenance out of '+str(total['archivalFileCount']-total['ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL'])+
            ' files returning HTTP 200. This is not a denominator for all public site files; unlisted routes/assets remain unknown.',
            '', '## Files still lacking exact historical Git bytes','']
    for sec in d['sections']:
        missing=[row for row in sec['files'] if row['state']=='PUBLIC_BYTES_NOT_LOCATED']
        if not missing:continue
        lines.append('### '+sec['publicHost']+sec['publicPrefix'])
        for row in missing:lines.append('- `'+row['relativePath']+'` — '+row['publicSHA256'])
        lines.append('')
    lines+=['## Not-public or unverified archival URLs','']
    for sec in d['sections']:
        excluded=[row for row in sec['files'] if row['state'] in ('ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL','INCOMPLETE_HTTP_EVIDENCE')]
        for row in excluded:lines.append('- '+sec['publicHost']+sec['publicPrefix']+row['relativePath']+': '+row['state']+' (HTTP '+str(row['httpStatus'])+')')
    lines+=['','## Authority and release gate','',
        '- Source owner remains the domain registry owner. Historical projection repository entries are cross-repository **evidence**, not alternate domain owners.',
        '- A mixture of historical Git blobs is **not** a proven atomic published release. Exact blob provenance is necessary but insufficient for a full release manifest.',
        '- The data is based on a bounded earlier live HTTPS observation and on Git commits available from the pinned archival ancestry. The archive must also be proven retrievable from remote GitHub for provider-loss recovery.',
        '- Do not copy unknown public bytes into Git to make an audit pass; first establish source ownership, editorial scope and authority.',
        '- No permission for SSH, Caddy, tunnel, DNS or recovery deployment follows from this audit.',
        '', 'Build/refresh: `npm run recovery:blob-plan`; independently verify: `npm run recovery:blob-verify`.']
    return '\n'.join(lines)+'\n'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['plan','verify'])
    args=parser.parse_args()
    obj=generate()
    serialized=json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    human=report(obj)
    if args.action=='plan':
        RESULT.write_text(serialized);DOC.write_text(human)
    elif not RESULT.exists() or RESULT.read_text()!=serialized or not DOC.exists() or DOC.read_text()!=human:
        raise ValueError('STALE_GIT_BLOB_PROVENANCE')
    totals={key:sum(s['counts'][key] for s in obj['sections']) for key in ('ROOT_REVISION_EXACT','OTHER_GIT_REVISION_EXACT','PUBLIC_BYTES_NOT_LOCATED','ARCHIVAL_FILE_NOT_PUBLIC_AT_PROBED_URL')}
    print('BLOB_PROVENANCE_'+('PLANNED' if args.action=='plan' else 'VERIFIED'),totals,'admitted',obj['releaseAdmitted'])
if __name__=='__main__':main()
