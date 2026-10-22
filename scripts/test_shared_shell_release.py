#!/usr/bin/env python3
"""Negative and positive gates for shared shell, including publication split."""
import sys,unittest,tempfile,json,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from estate_shell import project,manifest,VERSION
from check_shared_shell_release import acceptance

ROOT=Path(__file__).resolve().parent.parent
MANIFEST=manifest(ROOT/'navigation/canonical-reel.v1.json')
SAMPLE="""<!doctype html><html><head><title>Original editorial work</title></head><body>
<main><article><h1>Original authored source</h1><p>Unaltered writer text.</p></article></main></body></html>"""
class CrossDomainShell(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='fc-shell-test-')
  self.root=Path(self.temp.name);self.sites={};self.css={};self.logo={}
  for ident in ('estate','teatro','solstice'):
   html,receipt=project(SAMPLE,ident,MANIFEST)
   path=self.root/(ident+'.html');path.write_text(html)
   self.sites[ident]=str(path)
   css=self.root/(ident+'.css');css.write_bytes((ROOT/'shell/estate-shell.css').read_bytes())
   mark=self.root/(ident+'.png');mark.write_bytes((ROOT/'shell/assets/estate-shell-logo.png').read_bytes())
   self.css[ident]=str(css);self.logo[ident]=str(mark)
   self.assertFalse(receipt['publicReleased'])
   self.assertIn('Original authored source',html)
 def tearDown(self):self.temp.cleanup()
 def check(self,mode='structural',**kwargs):
  return acceptance(MANIFEST,self.sites,self.css,self.logo,mode,**kwargs)
 def mutate(self,ident,old,new):
  p=Path(self.sites[ident]);s=p.read_text()
  self.assertIn(old,s)
  p.write_text(s.replace(old,new,1))
 def test_three_owner_positive(self):
  result=self.check();self.assertTrue(result['passed'],result)
 def test_book_source_preserved(self):
  for p in self.sites.values():self.assertIn('Unaltered writer text',Path(p).read_text())
 def test_rename_link_fails(self):
  self.mutate('estate','data-estate-id="teatro"','data-estate-id="forged"')
  self.assertFalse(self.check()['passed'])
 def test_reorder_fails(self):
  self.mutate('teatro','data-estate-id="estate"','data-estate-id="teatro"')
  self.assertFalse(self.check()['passed'])
 def test_incorrect_current_fails(self):
  self.mutate('solstice',' aria-current="page"','')
  self.assertFalse(self.check()['passed'])
 def test_footer_provenance_missing_fails(self):
  self.mutate('estate','data-footer-slot="provenance"','data-footer-slot="wrong"')
  self.assertFalse(self.check()['passed'])
 def test_status_in_reel_fails(self):
  self.mutate('estate','data-estate-id="estate"','data-estate-id="status"')
  self.assertFalse(self.check()['passed'])
 def test_footer_status_missing_fails(self):
  self.mutate('teatro','href="https://status.fountain.coach/"','href="/wrong"')
  self.assertFalse(self.check()['passed'])
 def test_shell_revision_drift_fails(self):
  self.mutate('estate',VERSION,'wrong',)
  self.assertFalse(self.check()['passed'])
 def test_css_owner_drift_fails(self):
  Path(self.css['solstice']).write_text('body{color:magenta}')
  self.assertFalse(self.check()['passed'])
 def test_mark_owner_drift_fails(self):
  Path(self.logo['teatro']).write_bytes(b'forged')
  self.assertFalse(self.check()['passed'])
 def test_bookshelf_is_not_domain_release(self):
  self.assertFalse(self.check('publication')['passed'])
 def test_unauthorized_receipt_placeholder_never_sufficient(self):
  # Even apparent evidence must be validated by the native Publisher.
  a=self.root/'fake-ipad.json';a.write_text(json.dumps({
   'nativeSafariIPad':True,'headerFooterTransitionReport':'unverified',
   'screenshotHashes':{'fake':'deadbeef'},'sourceRevisions':['fake']}))
  b=self.root/'fake-publisher.json';b.write_text(json.dumps({
   'estatePublisherTerminalReceipt':'unverified',
   'publicHTTPSReadbacks':['fake'],'rollbackRelease':'fake'}))
  # This assertion presently exposes the admission gap: the checker must
  # never accept a self-declared file as real native/authorized evidence.
  self.assertFalse(self.check('publication',webkit=a,publisher=b)['passed'])
if __name__=='__main__':unittest.main()
