#!/usr/bin/env python3
"""Local EstateShell structural and negative acceptance fixtures.

Run: python3 scripts/test_shared_shell_acceptance.py
No DNS, production release, manuscript, Store or remote-host changes.
"""
from pathlib import Path
import json
import tempfile
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from estate_shell import manifest,contract,project,work_digest
from check_shared_shell_release import acceptance

ROOT=Path(__file__).resolve().parent.parent
M=manifest(ROOT/"navigation/canonical-reel.v1.json")
SOURCE='<!doctype html><html><head><title>Source edition</title></head><body><main id="main"><article id="work"><p>Authored original text.</p></article></main></body></html>'

class ShellAcceptance(unittest.TestCase):
    def setUp(self):
        self.d=tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        self.base=Path(self.d.name)
        self.sites={};self.css={};self.logo={}
        for ident in ("estate","solstice"):
            dest=self.base/ident
            dest.mkdir()
            html,receipt=project(SOURCE,ident,M)
            path=dest/"index.html";path.write_text(html)
            self.sites[ident]=str(path)
            css=dest/"shell.css";css.write_text("shared pinned css")
            logo=dest/"logo.svg";logo.write_text("<svg/>")
            self.css[ident]=str(css);self.logo[ident]=str(logo)
            self.assertFalse(receipt["publicReleased"])
        self.entry=Path(self.sites["estate"])
    def check(self,mode="structural"):
        return acceptance(M,self.sites,self.css,self.logo,mode)
    def corrupt(self,old,new):
        current=self.entry.read_text()
        self.assertIn(old,current)
        self.entry.write_text(current.replace(old,new,1))
    def assert_bad(self,needle):
        r=self.check()
        self.assertFalse(r["passed"])
        self.assertIn(needle,json.dumps(r))
    def test_positive_common_shell(self):
        self.assertTrue(self.check()["passed"])
    def test_unmodified_source_work(self):
        src=__import__("bs4").BeautifulSoup(SOURCE,"html.parser")
        out=__import__("bs4").BeautifulSoup(self.entry.read_text(),"html.parser")
        self.assertEqual(work_digest(src),work_digest(out))
    def test_one_version(self):
        self.assertIn("shellVersion",project(SOURCE,"estate",M)[1])
    def test_two_publication_lanes(self):
        c=contract(M)
        self.assertEqual(c["primaryEditorialEntrances"],["estate","solstice","teatro"])
        self.assertFalse(c["publicationLanes"]["reframeBookshelf"]["releasesPublicWebsite"])
        self.assertFalse(c["publicationLanes"]["reframeBookshelf"]["createsEstateReelEntry"])
    def test_duplicate_projection_refused(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            project(self.entry.read_text(),"estate",M)
    def test_unrecognized_owner_refused(self):
        with self.assertRaisesRegex(ValueError,"unknown"):
            project(SOURCE,"madeup",M)
    def test_reel_missing_item_refused(self):
        self.corrupt('data-estate-id="teatro"','data-estate-id="absent"')
        self.assert_bad("reel membership/order drift")
    def test_reel_extra_status_refused(self):
        self.corrupt('data-estate-id="estate"','data-estate-id="status"')
        self.assert_bad("reel membership/order drift")
    def test_wrong_active_refused(self):
        self.corrupt(' aria-current="page"','')
        self.assert_bad("active identity mismatch")
    def test_wrong_footer_role_refused(self):
        self.corrupt('data-footer-slot="provenance"','data-footer-slot="other"')
        self.assert_bad("footer slot order drift")
    def test_status_missing_footer_refused(self):
        self.corrupt('href="https://status.fountain.coach/"','href="/wrong"')
        self.assert_bad("Status must appear in legal footer")
    def test_footer_version_drift_refused(self):
        self.corrupt('data-footer-contract="fountain.estate.canonical-footer.v1"','data-footer-contract="v0"')
        self.assert_bad("footer contract mismatch")
    def test_css_drift_refused(self):
        Path(self.css["estate"]).write_text("changed css")
        self.assert_bad("CSS byte drift")
    def test_logo_drift_refused(self):
        Path(self.logo["solstice"]).write_text("changed mark")
        self.assert_bad("logo byte drift")
    def test_publication_no_receipt_refused(self):
        r=self.check(mode="publication")
        self.assertFalse(r["passed"])
        self.assertFalse(r["gates"]["nativeWebKit"])
        self.assertFalse(r["gates"]["authorizedPublication"])

if __name__=="__main__":
    unittest.main(verbosity=2)
