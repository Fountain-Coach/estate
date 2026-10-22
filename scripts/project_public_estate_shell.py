#!/usr/bin/env python3
"""Public-candidate adapter for the ONE existing EstateShell renderer.

Pure source projection: no SSH, DNS, credentials, Store or publication effects.
The old author-owned page remains the source; the writer's main content is
rejected on drift. Satzfunk's unpublished identity is visible but inert.
"""
import argparse
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup
from estate_shell import project, manifest, work_digest, VERSION

PUBLIC_IDS = ('estate','book','governance','midi2','instruments','teatro','satzfunk','pointer','solstice')

def project_public(source: str, identity: str, reel: dict, logo='/assets/estate-shell-logo.png'):
    original = BeautifulSoup(source,'html.parser')
    if not original.head or not original.body:
        raise ValueError('public source must be complete HTML')
    if original.select('[data-estate-shell-version]'):
        raise ValueError('already versioned: refuse double shell')
    if original.select('meta[name="robots"][content*="noindex"]'):
        raise ValueError('private or noindex source cannot be made public')
    old_work = work_digest(original)
    # Legacy Governance uses header.topbar, other owners header.site-header.
    # Normalize the header *in memory* for the existing source-preserving
    # renderer. This does not change its Git-owned editorial main or assets.
    heads = original.select('header.topbar,header.site-header')
    if len(heads)>1:
        raise ValueError('ambiguous publisher headers')
    if heads and 'site-header' not in heads[0].get('class',[]):
        heads[0]['class']=['site-header']
    stage_html, stage_receipt = project(str(original), identity, reel, logo)
    p = BeautifulSoup(stage_html,'html.parser')
    generated_robots = p.select('meta[name="robots"][content="noindex,nofollow"]')
    if len(generated_robots)!=1:
        raise AssertionError('unexpected staging robots directive')
    generated_robots[0].decompose()
    nav = p.select_one('nav.fc-shell-reel')
    if not nav:
        raise AssertionError('common publisher navigation absent')
    satz = nav.select_one('a[data-estate-id="satzfunk"]')
    if not satz or satz.get('href')!='https://satzfunk.fountain.coach/':
        raise AssertionError('canonical unpublished Satzfunk contract changed')
    satz.name = 'span'
    satz.attrs = {
        'class':['fc-reel-link','fc-reel-unavailable'],
        'data-estate-id':'satzfunk',
        'data-icon-id':'satzfunk',
        'data-canonical-href':'https://satzfunk.fountain.coach/',
        'role':'link','aria-disabled':'true',
        'aria-label':'Satzfunk — not yet public',
        'title':'Satzfunk — not yet public',
    }
    # Preserve the shared four-slot schema. Public candidate text must not
    # falsely say "private preview" or assert a completed HTTPS release.
    state = p.select_one('[data-footer-slot="release-state"] p')
    if not state:
        raise AssertionError('shared publication-state slot missing')
    state.string = ('Public editorial projection; independent release evidence '
                    'is maintained separately.')
    legal = p.select_one('[data-footer-slot="legal"] .fc-legal-links')
    if not legal:
        raise AssertionError('shared legal slot missing')
    if not legal.select_one('a[href="https://governance.fountain.coach/compliance/"]'):
        a=p.new_tag('a',href='https://governance.fountain.coach/compliance/')
        a.string='EU compliance'; legal.append(a)
    ids = [x['data-estate-id'] for x in nav.select('[data-estate-id]')]
    if tuple(ids)!=PUBLIC_IDS:
        raise AssertionError('missing or reordered editorial identity')
    if len(nav.select('.estate-info[href="#footer"]'))!=1:
        raise AssertionError('Info destination mismatch')
    if len(p.select('header.fc-estate-shell'))!=1 or len(p.select('footer.estate-footer#footer'))!=1:
        raise AssertionError('ambiguous common shell')
    if old_work!=work_digest(p):
        raise AssertionError('authored main changed during projection')
    html=str(p)
    return html,{
        'profile':'public-candidate','shellVersion':VERSION,
        'identity':identity,'sourceSHA256':hashlib.sha256(source.encode()).hexdigest(),
        'sourceWorkSHA256':old_work,'projectionSHA256':hashlib.sha256(html.encode()).hexdigest(),
        'unpublishedSatzfunk':True,'publicReleased':False,
        'stageProjectionReceipt':stage_receipt['projectionSHA256'],
    }

def main():
    parser=argparse.ArgumentParser(description='Pure public EstateShell projection; no deploy')
    parser.add_argument('--manifest',required=True,type=Path)
    parser.add_argument('--source',required=True,type=Path)
    parser.add_argument('--identity',required=True)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--receipt',required=True,type=Path)
    parser.add_argument('--logo',default='/assets/estate-shell-logo.png')
    args=parser.parse_args()
    if args.output.exists() or args.receipt.exists():
        raise SystemExit('refuse overwrite of candidate or evidence')
    content,evidence=project_public(args.source.read_text(encoding='utf8'),args.identity,
                                    manifest(args.manifest),args.logo)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(content,encoding='utf8')
    args.receipt.write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n')
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
