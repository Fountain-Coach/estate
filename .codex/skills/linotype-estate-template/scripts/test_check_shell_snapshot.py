import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

base = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('checker', base/'check_shell_snapshot.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
contract = json.loads((base.parent/'references/contract.example.json').read_text())


def page(ident, sample=contract, missing_footer_status=False, reorder=False, info_button=False):
    entries = sample['entries'][::-1] if reorder else sample['entries']
    links = ''.join('<a data-estate-id="'+e['id']+'" data-icon-id="'+e['id']+'" href="'+e['url']+'" aria-label="'+e['label']+'"'+(' aria-current="page"' if e['id']==ident else '')+'></a>' for e in entries)
    footer_links = ''.join('<a href="'+e['url']+'">'+e['id']+'</a>' for e in sample['supportingDestinations'] if not (missing_footer_status and e['id']=='status'))
    slots = ''.join('<section data-footer-slot="'+s+'">'+(footer_links if s=='legal' else 'source credited')+'</section>' for s in sample['footerSlots'])
    info = '<button class="estate-info" type="button">Info</button>' if info_button else '<a class="estate-info" href="#footer">Info</a>'
    return ('<header><img class="estate-logo" alt="Publisher" src="logo.svg"/></header>'
            '<nav class="estate-nav" data-reel-contract="'+sample['reelVersion']+'">'+links+info+'</nav>'
            '<main>Authored domain body remains independent</main>'
            '<footer id="footer" class="estate-footer" data-footer-contract="'+sample['footerVersion']+'">'+slots+'</footer>')


class Test(unittest.TestCase):
    def run_case(self, html, ident='estate', sample=contract, fixture_mode=True):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)/'index.html'
            p.write_text(html)
            return checker.validate(sample, [(ident, p)], fixture_mode=fixture_mode)

    def test_valid_fixture(self):
        result = self.run_case(page('teatro'), 'teatro')
        self.assertTrue(result['passed'])
        self.assertTrue(result['fixture_only'])
        self.assertIn('not FCIS', result['boundary'])

    def test_reject_footer_drift(self):
        self.assertFalse(self.run_case(page('teatro', missing_footer_status=True), 'teatro')['passed'])

    def test_reject_reordered_reel(self):
        self.assertFalse(self.run_case(page('teatro', reorder=True), 'teatro')['passed'])

    def test_reject_incorrect_active(self):
        self.assertFalse(self.run_case(page('estate'), 'solstice')['passed'])

    def test_supporting_status_has_no_active(self):
        self.assertTrue(self.run_case(page('unknown'), 'status')['passed'])

    def test_example_requires_explicit_fixture(self):
        with self.assertRaisesRegex(ValueError, 'synthetic fixture'):
            self.run_case(page('estate'), 'estate', fixture_mode=False)

    def test_registry_size_is_data_driven(self):
        c = dict(contract)
        c['entries'] = contract['entries'][:-1]
        self.assertTrue(self.run_case(page('estate', sample=c), 'estate', sample=c)['passed'])

    def test_duplicate_registry_ids_rejected(self):
        c = dict(contract)
        c['entries'] = contract['entries'] + [contract['entries'][0]]
        with self.assertRaisesRegex(ValueError, 'unique'):
            self.run_case(page('estate', sample=c), 'estate', sample=c)

    def test_info_button_is_structural_not_proof_of_click(self):
        self.assertTrue(self.run_case(page('estate', info_button=True))['passed'])


if __name__ == '__main__':
    unittest.main()
