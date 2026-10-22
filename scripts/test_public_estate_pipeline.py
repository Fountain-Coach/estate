#!/usr/bin/env python3
"""Public release negative tests; no deployment, no new framework."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from estate_shell import project, work_digest
from project_public_estate_shell import project_public
from build_public_estate_candidate import prepare
from check_public_estate_shell import check_candidate,PUBLIC_OWNERS,ALL_IDS

URLS={'estate':'https://fountain.coach/','book':'https://book.fountain.coach/',
'governance':'https://governance.fountain.coach/','midi2':'https://midi2.fountain.coach/',
'instruments':'https://instruments.fountain.coach/','teatro':'https://teatro.fountain.coach/',
'satzfunk':'https://satzfunk.fountain.coach/','pointer':'https://benedikt-eickhoff.de/',
'solstice':'https://works.benedikt-eickhoff.de/solstice/'}
M={'schema':'fountain.estate.canonical-reel.v1','entries':[
{'id':x,'label':x.title(),'url':URLS[x],'path':'M4 4 L20 20'} for x in ALL_IDS]}

def legacy(kind='topbar'):
    nav='<nav class="estate-nav" aria-label="Fountain Coach publication estate">'+''.join(
        '<a data-estate-id="'+x+'" href="'+URLS[x]+'">'+x+'</a>' for x in ALL_IDS if x!='satzfunk')+'</nav>'
    head=('<header class="'+kind+'" role="banner">'+nav+'</header>') if kind else ''
    return ('<!doctype html><html lang="en"><head><title>Governance</title></head><body>'+head+
        '<main><h1>Governance</h1><article><p>Source-owned manuscript unchanged.</p></article>'+
        '<div class="book-toolbar"><button id="next-leaf">Next</button></div>'+
        '<footer class="footer" id="footer" role="contentinfo"><p>Original rights, author and credits.</p></footer>'+
        '</main></body></html>')

class PublicEstatePipeline(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_legacy_governance_mastheads_preserved(self):
        for kind in ('topbar','site-header'):
            src=legacy(kind)
            html,r=project_public(src,'governance',M)
            p=BeautifulSoup(html,'html.parser')
            self.assertEqual(len(p.select('header.fc-estate-shell')),1)
            self.assertEqual(len(p.select('footer.estate-footer#footer')),1)
            self.assertEqual(work_digest(BeautifulSoup(src,'html.parser')),work_digest(p))
            self.assertIsNotNone(p.select_one('#next-leaf'))
            self.assertTrue(r['legacyImprintRetained'])
            self.assertIn('Original rights, author and credits',
                          p.select_one('details.fc-owner-imprint').get_text(' ',strip=True))
            self.assertFalse(r['publicReleased'])

    def test_real_instruments_and_solstice_legacy_shapes(self):
        # Public Instruments has header[role=banner] but no .site-header.
        instruments=legacy('topbar').replace('class="topbar" role="banner"','role="banner"')
        instruments=instruments.replace('<main><h1>','<main><header class="catalog-heading">Catalog</header><h1>')
        html,_=project_public(instruments,'instruments',M)
        page=BeautifulSoup(html,'html.parser')
        self.assertEqual(len(page.select('header.fc-estate-shell')),1)
        self.assertEqual(len(page.select('header.catalog-heading')),1)
        self.assertEqual(len(page.select('nav[aria-label="Fountain Coach publication estate"]')),1)
        # Public Solstice uses footer.solstice-footer#footer, not .footer.
        solstice=legacy('site-header').replace('class="footer" id="footer"',
                                                'class="solstice-footer" id="footer"')
        html,receipt=project_public(solstice,'solstice',M)
        page=BeautifulSoup(html,'html.parser')
        self.assertEqual(len(page.select('footer#footer')),1)
        self.assertTrue(receipt['legacyImprintRetained'])
        self.assertIn('Original rights, author and credits',
                      page.select_one('details.fc-owner-imprint').get_text(' ',strip=True))

    def test_duplicate_publisher_nav_is_refused(self):
        src=legacy('topbar').replace('</header>',
           '<nav aria-label="Fountain Coach publication estate"></nav></header>',1)
        with self.assertRaisesRegex(ValueError,'duplicated publisher navigation'):
            project_public(src,'governance',M)

    def test_nine_identities_satzfunk_inert_info_and_status_footer(self):
        html,r=project_public(legacy(),'governance',M)
        p=BeautifulSoup(html,'html.parser')
        n=p.select_one('nav.fc-shell-reel')
        self.assertEqual(tuple(x['data-estate-id'] for x in n.select('[data-estate-id]')),ALL_IDS)
        self.assertEqual(len(n.select('a[data-estate-id]')),8)
        s=n.select_one('[data-estate-id="satzfunk"]')
        self.assertEqual(s.name,'span')
        self.assertEqual(s['aria-disabled'],'true')
        self.assertIsNone(s.get('href'))
        self.assertFalse(n.select('[data-estate-id="status"]'))
        self.assertEqual(len(n.select('a.estate-info[href="#footer"]')),1)
        self.assertTrue(p.select_one('footer a[href="https://status.fountain.coach/"]'))
        self.assertTrue(p.select_one('footer a[href="https://governance.fountain.coach/compliance/"]'))
        self.assertFalse(p.select('meta[name="robots"][content*="noindex"]'))

    def test_noindex_and_duplicate_shell_fail(self):
        s=legacy().replace('</head>','<meta name="robots" content="noindex,nofollow"></head>')
        with self.assertRaisesRegex(ValueError,'noindex'):project_public(s,'governance',M)
        html,_=project_public(legacy(),'governance',M)
        with self.assertRaisesRegex(ValueError,'already versioned'):project_public(html,'governance',M)

    def test_preview_still_private(self):
        html,_=project(legacy('site-header'),'governance',M)
        self.assertEqual(BeautifulSoup(html,'html.parser').select_one('meta[name="robots"]')['content'],
                         'noindex,nofollow')

    def eight(self,chapter_count=2):
        pages={}
        for ident in PUBLIC_OWNERS:
            home=self.root/ident;home.mkdir()
            page,_=project_public(legacy(),ident,M)
            (home/'index.html').write_text(page)
            pages[ident]=str(home/'index.html')
        gov=self.root/'governance'
        routes=[{'publicPaths':['/index.html']}]
        for i in range(chapter_count):
            sub=gov/'chapters'/str(i);sub.mkdir(parents=True)
            (sub/'index.html').write_text((gov/'index.html').read_text())
            routes.append({'publicPaths':[f'/chapters/{i}/index.html']})
        route=self.root/'routes.json'
        route.write_text(json.dumps({'host':'governance.fountain.coach','routes':routes}))
        css=self.root/'shell.css';css.write_text('shared CSS')
        mark=self.root/'logo.png';mark.write_bytes(b'logo')
        return pages,{x:str(css) for x in PUBLIC_OWNERS},{x:str(mark) for x in PUBLIC_OWNERS},gov,route

    def test_all_eight_plus_160_chapters(self):
        result=check_candidate(M,*self.eight(160))
        self.assertTrue(result['passed'],str(result['failures'][:1]))
        self.assertEqual(result['routesTested'],168)
        self.assertFalse(result['publicReleased'])
        self.assertFalse(result['nativeSafariAccepted'])

    def test_missing_owner_rejected(self):
        pages,css,logos,root,route=self.eight()
        pages.pop('book')
        with self.assertRaisesRegex(ValueError,'eight public'):
            check_candidate(M,pages,css,logos,root,route)

    def test_mismatched_shared_css_rejected(self):
        pages,css,logos,root,route=self.eight()
        bad=self.root/'bad.css';bad.write_text('wrong');css['teatro']=str(bad)
        self.assertFalse(check_candidate(M,pages,css,logos,root,route)['passed'])

    def test_broken_satzfunk_link_rejected(self):
        pages,css,logos,root,route=self.eight()
        p=Path(pages['governance'])
        p.write_text(p.read_text().replace('data-estate-id="satzfunk"',
                       'href="https://satzfunk.fountain.coach/" data-estate-id="satzfunk"'))
        self.assertFalse(check_candidate(M,pages,css,logos,root,route)['passed'])

    def test_missing_governance_chapter_rejected(self):
        pages,css,logos,root,route=self.eight()
        (root/'chapters'/'1'/'index.html').unlink()
        with self.assertRaisesRegex(ValueError,'missing declared'):
            check_candidate(M,pages,css,logos,root,route)

    def owned_site(self):
        site=self.root/'owner';site.mkdir()
        (site/'index.html').write_text(legacy())
        (site/'chapters'/'158').mkdir(parents=True)
        (site/'chapters'/'158'/'index.html').write_text(legacy('site-header'))
        (site/'assets').mkdir()
        (site/'assets'/'work.css').write_text('original editorial styles')
        sha=self.root/'publication-files.sha256'
        sha.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+
                      p.relative_to(site).as_posix()+'\n'
                      for p in sorted(site.rglob('*')) if p.is_file()))
        routes=self.root/'owner-routes.json'
        routes.write_text(json.dumps({'host':'governance.fountain.coach','routes':[
            {'publicPaths':['/index.html']},{'publicPaths':['/chapters/158/index.html']}]}))
        shell=self.root/'shell-source';shell.mkdir();(shell/'assets').mkdir()
        (shell/'estate-shell.css').write_text('shared CSS')
        (shell/'estate-shell-state.js').write_text('state')
        (shell/'assets'/'estate-shell-logo.png').write_bytes(b'logo')
        return site,sha,routes,shell

    def test_build_source_locked_candidate_without_publication(self):
        site,sha,routes,shell=self.owned_site()
        out=self.root/'candidate';receipt=self.root/'receipt.json'
        r=prepare(site,sha,'governance',M,'a'*40,out,receipt,shell,routes)
        self.assertEqual(r['projectedHTMLCount'],2)
        self.assertEqual(r['sourceFileCount'],3)
        self.assertFalse(r['publicReleased'])
        self.assertEqual((out/'assets'/'work.css').read_text(),'original editorial styles')
        self.assertFalse((out/'receipt.json').exists())
        with self.assertRaisesRegex(ValueError,'already exists'):
            prepare(site,sha,'governance',M,'a'*40,out,receipt,shell,routes)

    def test_tampered_source_refuses_without_output(self):
        site,sha,routes,shell=self.owned_site()
        (site/'index.html').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'inventory differs'):
            prepare(site,sha,'governance',M,'a'*40,self.root/'candidate',
                    self.root/'receipt.json',shell,routes)
        self.assertFalse((self.root/'candidate').exists())

if __name__=='__main__':unittest.main()
