#!/usr/bin/env python3
"""Fail-closed public EstateShell structural admission gate.

Checks ALL eight publicly hosted editorial owners and EVERY Governance HTML
route, not only the three WLAN demo fronts. This is not WebKit approval or a
production-release receipt and cannot activate anything.
"""
import argparse
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup

PUBLIC_OWNERS=('estate','book','governance','midi2','instruments','teatro','pointer','solstice')
ALL_IDS=('estate','book','governance','midi2','instruments','teatro','satzfunk','pointer','solstice')
SLOTS=('imprint','provenance','legal','release-state')
LEGAL_REQUIRED={
    'https://governance.fountain.coach/legal/',
    'https://governance.fountain.coach/privacy/',
    'https://governance.fountain.coach/accessibility/',
    'https://governance.fountain.coach/copyright/',
    'https://governance.fountain.coach/compliance/',
    'https://status.fountain.coach/',
}

def hash_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_page(html, owner, canonical):
    soup=BeautifulSoup(html,'html.parser')
    errors=[]
    def require(test,msg):
        if not test:errors.append(msg)
    headers=soup.select('header.fc-estate-shell[data-estate-shell-version]')
    navs=soup.select('nav.fc-shell-reel[aria-label="Fountain Coach publication estate"]')
    footers=soup.select('footer.estate-footer.fc-estate-shell#footer')
    require(len(headers)==1,'one versioned masthead')
    require(len(navs)==1,'one canonical reel')
    require(len(footers)==1,'one shared legal footer')
    require(len(soup.select('img.estate-logo'))==1,'one publisher logo')
    require(not soup.select('meta[name="robots"][content*="noindex"]'),'public projection is noindex')
    version=headers[0].get('data-estate-shell-version') if len(headers)==1 else None
    if len(headers)==1:
        require(headers[0].get('data-estate-identity')==owner,'wrong owner identity')
    if len(footers)==1:
        footer=footers[0]
        require(footer.get('data-estate-shell-version')==version,'footer version drift')
        require(footer.get('data-footer-contract')=='fountain.estate.canonical-footer.v1','footer contract drift')
        slots=[s.get('data-footer-slot') for s in footer.select('[data-footer-slot]')]
        require(tuple(slots)==SLOTS,'four footer slots missing or wrong order')
        urls={a.get('href') for a in footer.select('a[href]')}
        require(LEGAL_REQUIRED.issubset(urls),'legal/footer links missing')
        require(not footer.select('footer'),'duplicate nested footer')
    if len(navs)==1:
        n=navs[0]
        require(n.get('data-reel-contract')=='fountain.estate.canonical-reel.v1','canonical reel drift')
        items=n.select('[data-estate-id]')
        require(tuple(x.get('data-estate-id') for x in items)==ALL_IDS,'nine editorial identities/order incorrect')
        require(not n.select('[data-estate-id="status"]'),'Status wrongly in top reel')
        require(len(n.select('a.estate-info[href="#footer"]'))==1,'Info/footer missing')
        active=[x.get('data-estate-id') for x in items if x.get('aria-current')=='page']
        require(active==[owner],'wrong active editorial identity')
        for x in items:
            ident=x.get('data-estate-id')
            expected=next((e for e in canonical['entries'] if e['id']==ident),None)
            if expected is None:continue
            require(x.get('data-icon-id')==ident,'wrong icon '+ident)
            if ident=='satzfunk':
                require(x.name=='span' and x.get('aria-disabled')=='true' and x.get('role')=='link','unpublished Satzfunk not inert')
                require(x.get('href') is None,'unpublished Satzfunk linked publicly')
                require(x.get('data-canonical-href')==expected['url'],'unpublished Satzfunk canonical identity lost')
            else:
                require(x.name=='a' and x.get('href')==expected['url'],'incorrect URL '+ident)
                require(x.get('aria-label')==expected['label'],'incorrect label '+ident)
        for link in n.select('a[href]'):
            require(not any(private in link.get('href','') for private in ('192.168.','10.0.','127.0.0.1','localhost')),'private WLAN link exposed')
    return {'passed':not errors,'errors':errors,'owner':owner,'version':version}

def check_candidate(canonical, owner_pages, css_paths, logo_paths, governance_root=None, route_manifest=None):
    if tuple(e['id'] for e in canonical['entries'])!=ALL_IDS:
        raise ValueError('canonical reel source changed')
    if set(owner_pages)!=set(PUBLIC_OWNERS):
        raise ValueError('all eight public editorial owners required')
    if set(css_paths)!=set(PUBLIC_OWNERS) or set(logo_paths)!=set(PUBLIC_OWNERS):
        raise ValueError('shared CSS and mark must cover every owner')
    results=[]
    for owner in PUBLIC_OWNERS:
        results.append({'route':'/',**check_page(Path(owner_pages[owner]).read_text(),owner,canonical)})
    if governance_root is None or route_manifest is None:
        raise ValueError('Governance complete deep-route coverage required')
    root=Path(governance_root)
    routes=json.loads(Path(route_manifest).read_text())
    if routes.get('host')!='governance.fountain.coach' or not routes.get('routes'):
        raise ValueError('invalid Governance route authority')
    declared={p.lstrip('/') for item in routes['routes'] for p in item['publicPaths'] if p.endswith('/index.html')}
    actual={p.relative_to(root).as_posix() for p in root.rglob('*.html')}
    if not declared.issubset(actual):
        raise ValueError('missing declared Governance HTML routes')
    if len(actual)<len(declared):
        raise ValueError('Governance chapter inventory incomplete')
    for path in sorted(actual):
        if path=='index.html': continue
        results.append({'route':'/'+path,**check_page((root/path).read_text(),'governance',canonical)})
    css={hash_file(css_paths[i]) for i in PUBLIC_OWNERS}
    logos={hash_file(logo_paths[i]) for i in PUBLIC_OWNERS}
    versions={x['version'] for x in results}
    checks={'sameCSS':len(css)==1,'sameLogo':len(logos)==1,
            'oneVersion':len(versions)==1 and None not in versions,
            'allRoutesPassed':all(x['passed'] for x in results)}
    return {'passed':all(checks.values()),'checks':checks,'routesTested':len(results),
            'failures':[x for x in results if not x['passed']],
            'nativeSafariAccepted':False,'publicReleased':False,
            'boundary':'source/DOM checks only; no WebKit, legal admission or HTTPS release proof'}

def mapping(args):
    out={}
    for x in args:
        if '=' not in x:raise ValueError('expected owner=path')
        k,v=x.split('=',1)
        if k in out:raise ValueError('duplicate owner '+k)
        out[k]=v
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--manifest',required=True,type=Path)
    p.add_argument('--site',action='append',required=True)
    p.add_argument('--css',action='append',required=True)
    p.add_argument('--logo',action='append',required=True)
    p.add_argument('--governance-root',type=Path,required=True)
    p.add_argument('--governance-route-manifest',type=Path,required=True)
    opts=p.parse_args()
    try:
        result=check_candidate(json.loads(opts.manifest.read_text()),mapping(opts.site),
                               mapping(opts.css),mapping(opts.logo),opts.governance_root,
                               opts.governance_route_manifest)
    except (OSError,ValueError,KeyError,AssertionError) as err:
        result={'passed':False,'error':str(err),'publicReleased':False}
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
