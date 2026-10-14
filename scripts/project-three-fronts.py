#!/usr/bin/env python3
"""Project the three-front editorial nav into owning Git site source files.

Read-only by default; --apply requires an exact canonical owner checkout.
Does not deploy, alter text outside estate-nav, or edit derived estate trees.
"""
import argparse,re,json
from pathlib import Path
NAV=re.compile(r'(<nav\b[^>]*\bclass="[^"]*\bestate-nav\b[^"]*"[^>]*>)(.*?)(</nav>)',re.S)
LINK=re.compile(r'<a\b(?=[^>]*\bdata-estate-id="([^"]+)")[^>]*>.*?</a>',re.S)
INFO=re.compile(r'<a\b[^>]*\bclass="[^"]*\bestate-info\b[^"]*"[^>]*>.*?</a>',re.S)
IDS=('estate','solstice','teatro')
FR='https://works.benedikt-eickhoff.de/solstice/editions/first-reading/'
ALLOWED={'fountain.coach','teatro.fountain.coach','solstice.fountain.coach'}
def rewrite(raw,host):
    spans=list(NAV.finditer(raw))
    if not spans:return raw,False
    if len(spans)!=1:raise ValueError('Unexpected multiple estate navs')
    match=spans[0];body=match.group(2)
    links={m.group(1):m.group() for m in LINK.finditer(body)}
    if 'solstice' not in links and 'first-reading' in links:
        links['solstice']=links['first-reading']
    if not set(IDS)<=set(links):raise ValueError('Required front identities missing: '+str(set(IDS)-set(links)))
    retained=[]
    for ident in IDS:
        link=re.sub(r'\s+aria-current="page"','',links[ident])
        if ident=='solstice':
            link=re.sub(r'data-estate-id="solstice"','data-estate-id="first-reading"',link)
            link=re.sub(r'href="https://(?:solstice\.fountain\.coach|works\.benedikt-eickhoff\.de/solstice)(?:/editions/first-reading)?/"',f'href="{FR}"',link)
            link=re.sub(r'aria-label="Solstice[^"]*"','aria-label="First Reading"',link)
            link=link.replace('<span>Solstice</span>','<span>First Reading</span>')
        active={'fountain.coach':'estate','teatro.fountain.coach':'teatro','solstice.fountain.coach':'solstice'}[host]
        if ident==active:link=link.replace('<a ', '<a aria-current="page" ',1)
        retained.append(link)
    info=INFO.search(body)
    if info:retained.append(info.group())
    joined=''.join(retained)
    new=raw[:match.start(2)]+joined+raw[match.end(2):]
    return new,new!=raw
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True,type=Path)
 p.add_argument('--host',required=True,choices=sorted(ALLOWED))
 p.add_argument('--apply',action='store_true')
 a=p.parse_args()
 src=a.source.resolve()
 if src.name!='site' or src.parent.name!=a.host or not (src.parent/'edition.json').is_file():
    raise ValueError('Edit only an owning Git checkout site/ matching requested host')
 changed=present=0
 for file in sorted(src.rglob('index.html')):
    raw=file.read_text()
    out,dirty=rewrite(raw,a.host)
    present+=bool(NAV.search(raw));changed+=dirty
    if dirty and a.apply:file.write_text(out)
 print(json.dumps({'host':a.host,'scanned':len(list(src.rglob('index.html'))),
                   'navPages':present,'changed':changed,'applied':a.apply},indent=2))
if __name__=='__main__':main()
