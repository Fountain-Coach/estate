#!/usr/bin/env python3
"""Auxiliary static HTML contract comparison (not an FCIS/Kit/release gate).

Use only a source-admitted contract revision for real route diagnosis. The bundled
contract.example.json is a synthetic fixture; it requires --fixture to run.

  python3 check_shell_snapshot.py --contract /accepted/contract.json \
    --site estate=/path/to/estate/index.html --site teatro=/path/to/teatro/index.html

This proves only comparison against the declared static schema. It does not
observe live WebKit, CSS geometry, audio, rights, Store, or production state.
"""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

DEFAULT_FOOTER = ('imprint', 'provenance', 'legal', 'release-state')


class Site(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.nav_depth = 0
        self.footer_depth = 0
        self.nav_count = 0
        self.footer_count = 0
        self.nav_attrs = {}
        self.footer_attrs = {}
        self.nav_links = []
        self.info_count = 0
        self.footer_slots = []
        self.footer_links = []
        self.logo_count = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set(a.get('class', '').split())
        if tag == 'nav' and 'estate-nav' in classes:
            self.nav_depth += 1
            self.nav_count += 1
            self.nav_attrs = a
        elif self.nav_depth and tag == 'nav':
            self.nav_depth += 1
        if tag == 'footer' and 'estate-footer' in classes:
            self.footer_depth += 1
            self.footer_count += 1
            self.footer_attrs = a
        elif self.footer_depth and tag == 'footer':
            self.footer_depth += 1
        if self.nav_depth:
            if tag == 'a' and 'data-estate-id' in a:
                self.nav_links.append(a)
            if tag in ('a', 'button') and 'estate-info' in classes:
                self.info_count += 1
                if tag == 'a' and a.get('href') != '#footer':
                    raise ValueError('Fixture Info link must target #footer')
                # For a button, this static parser cannot validate its actual
                # JS scroll target or browser interaction.
        if self.footer_depth:
            if 'data-footer-slot' in a:
                self.footer_slots.append(a['data-footer-slot'])
            if tag == 'a':
                self.footer_links.append(a.get('href', ''))
        if tag == 'img' and 'estate-logo' in classes:
            self.logo_count += 1

    def handle_endtag(self, tag):
        if tag == 'nav' and self.nav_depth:
            self.nav_depth -= 1
        if tag == 'footer' and self.footer_depth:
            self.footer_depth -= 1


def validate(contract, sites, fixture_mode=False):
    if contract.get('fixtureOnly') and not fixture_mode:
        raise ValueError('Bundled example is a synthetic fixture, not an accepted live manifest; use a source-admitted contract, or --fixture for fixture tests only')
    entries = contract['entries']
    ids = [e['id'] for e in entries]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Contract editorial IDs must be present and unique')
    required_footer = tuple(contract.get('footerSlots', DEFAULT_FOOTER))
    if not required_footer or len(set(required_footer)) != len(required_footer):
        raise ValueError('Contract footer slots must be present and unique')
    if not sites:
        raise ValueError('At least one declared HTML site is needed')
    digest = hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    checks = []
    for ident, path in sites:
        if ident not in ids and ident != 'status':
            raise ValueError('Unknown site identity ' + ident)
        page = Site(Path(path).read_text(encoding='utf-8'))
        problems = []
        if page.nav_count != 1:
            problems.append('Expected exactly one declared estate navigation')
        if page.footer_count != 1:
            problems.append('Expected exactly one declared estate footer')
        if page.nav_attrs.get('data-reel-contract') != contract['reelVersion']:
            problems.append('Reel contract version mismatch')
        if page.footer_attrs.get('data-footer-contract') != contract['footerVersion']:
            problems.append('Footer contract version mismatch')
        if page.footer_attrs.get('id') != 'footer':
            problems.append('Footer #footer identity missing')
        if page.logo_count != 1:
            problems.append('Declared publisher masthead needs one estate-logo')
        if page.info_count != 1:
            problems.append('Info affordance missing/duplicated')
        if [a.get('data-estate-id') for a in page.nav_links] != ids:
            problems.append('Declared editorial reel membership/order mismatch')
        for a, e in zip(page.nav_links, entries):
            if a.get('href') != e['url']:
                problems.append('Wrong ' + e['id'] + ' href')
            if a.get('aria-label') != e['label']:
                problems.append('Wrong ' + e['id'] + ' label')
            if a.get('data-icon-id') != e['id']:
                problems.append('Wrong ' + e['id'] + ' icon identity')
        active = [a.get('data-estate-id') for a in page.nav_links if a.get('aria-current') == 'page']
        if active != ([ident] if ident != 'status' else []):
            problems.append('Wrong active-page indication')
        if page.footer_slots != list(required_footer):
            problems.append('Footer slots/order mismatch')
        for target in contract['supportingDestinations']:
            if target['url'] not in page.footer_links:
                problems.append('Missing supporting footer link ' + target['id'])
        if any(a.get('data-estate-id') == 'status' for a in page.nav_links):
            problems.append('Status inserted in editorial reel')
        checks.append({'site': ident, 'path': str(path), 'pass': not problems, 'errors': problems})
    return {
        'passed': all(x['pass'] for x in checks),
        'checks': checks,
        'fixture_only': bool(contract.get('fixtureOnly')),
        'contract_digest': digest,
        'boundary': 'auxiliary static schema comparison only; not FCIS or visual/WebKit/rights/publication evidence',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', required=True)
    parser.add_argument('--site', action='append', required=True, help='id=/path/index.html')
    parser.add_argument('--fixture', action='store_true', help='explicit synthetic fixture diagnosis, never live acceptance')
    opts = parser.parse_args()
    sites = []
    for item in opts.site:
        if '=' not in item:
            parser.error('--site must be id=path')
        sites.append(item.split('=', 1))
    try:
        result = validate(json.loads(Path(opts.contract).read_text(encoding='utf-8')), sites, fixture_mode=opts.fixture)
    except (ValueError, AssertionError, OSError, KeyError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
