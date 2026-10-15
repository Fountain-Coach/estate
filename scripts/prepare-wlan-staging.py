#!/usr/bin/env python3
"""Prepare disposable HTML navigation for three-front, three-port WLAN stage.

Run only on an Ubuntu staging *release* copy, not in GitHub source or the
estate publisher. All non-rail content and book typography remain unchanged.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NAV = re.compile(
    r'(<nav\b[^>]*class="[^"]*\bestate-nav\b[^"]*"[^>]*>)(.*?)(</nav>)',
    re.S,
)
LINK = re.compile(
    r'(<a\b[^>]*data-estate-id="(?P<id>estate|first-reading|teatro)"[^>]*>.*?</a>)',
    re.S,
)
IP = "192.168.8.249"
DEST = {
    "estate": f"http://{IP}:8180/editions/essays/",
    "first-reading": f"http://{IP}:8181/editions/first-reading/",
    "teatro": f"http://{IP}:8182/editions/first-hearing/",
}

def rewrite(content: str):
    def update_nav(match):
        body = match.group(2)
        ids = LINK.findall(body)
        count = 0
        def update_link(link):
            nonlocal count
            fragment = link.group(1)
            identity = link.group("id")
            if identity not in DEST:
                return fragment
            transformed, replaced = re.subn(
                r'href="[^"]+"',
                'href="' + DEST[identity] + '"',
                fragment, count=1
            )
            if replaced != 1:
                raise ValueError("Missing href in navigation identity " + identity)
            count += 1
            return transformed
        new = LINK.sub(update_link, body)
        if count != 3:
            raise ValueError(f"Expected three editorial front doors; found {count}")
        return match.group(1) + new + match.group(3)
    updated, count = NAV.subn(update_nav, content)
    # The primary Fountain Coach entrance is now a real Linotype volume,
    # not an estate header rail. Its cover links to the other two editorial
    # fronts; stage them alongside the reader without changing Git source.
    cover = re.compile(r'(<section\b[^>]*class="[^"]*book-cover[^"]*"[^>]*>)(.*?)(</section>)',re.S)
    def update_cover(match):
        section = match.group(2)
        # First Reading and other independent books can also have a cover;
        # their original text is not the Fountain Coach editorial rail.
        if not LINK.search(section):
            return match.group()
        seen = set()
        def replace_link(m):
            identity = m.group("id")
            seen.add(identity)
            value = m.group(1)
            value, n = re.subn(r'href="[^"]+"', 'href="' + DEST[identity] + '"', value, count=1)
            if n != 1:raise ValueError("Essay cover navigation missing href: "+identity)
            return value
        rebuilt = LINK.sub(replace_link, section)
        if seen != {"first-reading", "teatro"}:
            raise ValueError("Expected First Reading + Teatro on essay cover: "+str(seen))
        return match.group(1)+rebuilt+match.group(3)
    updated, cover_count = cover.subn(update_cover, updated)
    # Nested Linotype essay readers use a deliberately restrained edition rail.
    # Its addresses are staged independently of the published Git source.
    edition_nav = re.compile(r'(<nav\b[^>]*class="[^"]*\bedition-rail\b[^"]*"[^>]*>)(.*?)(</nav>)',re.S)
    def update_edition_rail(match):
        seen=set()
        def replace_link(link):
            identity=link.group("id")
            seen.add(identity)
            fragment=link.group(1)
            fragment,n=re.subn(r'href="[^"]+"','href="'+DEST[identity]+'"',fragment,count=1)
            if n!=1:raise ValueError("Edition rail missing href: "+identity)
            return fragment
        new=LINK.sub(replace_link,match.group(2))
        if seen!={"estate","first-reading","teatro"}:
            raise ValueError("Incomplete edition rail: "+str(seen))
        return match.group(1)+new+match.group(3)
    updated, edition_count=edition_nav.subn(update_edition_rail,updated)
    # Edition grid uses real thumbnails, not the previous descriptive rail.
    # Only the three authoritative book links are substituted in disposable
    # WLAN proof releases; GitHub source keeps canonical HTTPS identities.
    if 'class="shelf-grid"' in updated:
        expected={
            '/editions/essays/':DEST['estate'],
            'https://works.benedikt-eickhoff.de/solstice/editions/first-reading/':DEST['first-reading'],
            'https://teatro.fountain.coach/':DEST['teatro'],
        }
        assert updated.count('class="shelf-entry"')==3
        for old,new in expected.items():
            pattern='href="'+old+'"'
            if updated.count(pattern)!=1:raise ValueError('Invalid edition grid destination '+old)
            updated=updated.replace(pattern,'href="'+new+'"',1)
        count+=3
    # Source owners retain canonical HTTPS reader URLs. The disposable WLAN
    # release translates only admitted bookshelf links (identified by
    # data-preview-host) into the three neighboring staging origins. It
    # never rewrites text, plates, the book renderer, or arbitrary anchors.
    if 'data-linotype-state="bookshelf"' in updated:
        shelf_link=re.compile(
            r'(<a class="shelf-book" href=")(?P<href>[^"]+)'
            r'(" data-preview-host="(?P<host>fountain|solstice|teatro)")')
        def staging_reader(match):
            href=match.group("href")
            host=match.group("host")
            if host=="fountain":
                prefix="https://fountain.coach/"
                if href==DEST["estate"]:
                    stage_href=href  # idempotent already-projected staging release
                else:
                    if not href.startswith(prefix+"editions/"):raise ValueError("Unapproved Fountain book URL "+href)
                    stage_href=f"http://{IP}:8180/"+href[len(prefix):]
            elif host=="solstice":
                prefix="https://works.benedikt-eickhoff.de/solstice/"
                if href==DEST["first-reading"]:
                    stage_href=href  # idempotent already-projected staging release
                else:
                    if not href.startswith(prefix+"editions/first-reading/"):raise ValueError("Unapproved First Reading URL "+href)
                    stage_href=f"http://{IP}:8181/"+href[len(prefix):]
            else:
                if href!="/editions/first-hearing/":raise ValueError("Unapproved Teatro URL "+href)
                stage_href=href
            return match.group(1)+stage_href+match.group(3)
        updated, shelf_count=shelf_link.subn(staging_reader,updated)
        count_expected=int(re.search(r'data-book-count="([0-9]+)"',updated).group(1))
        if shelf_count!=count_expected:raise ValueError("Incomplete source-backed bookshelf navigation")
    else:
        shelf_count=0
    return updated, count+cover_count+edition_count+shelf_count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", required=True, type=Path)
    args = parser.parse_args()
    release = args.release.resolve()
    if not (release.parent.name == "releases"
            and release.parent.parent.name == "estate-three-front-staging"):
        raise SystemExit("Refusing non-staging release: " + str(release))
    source_lock = release / "source-lock.json"
    if not source_lock.exists():
        raise SystemExit("Missing pinned GitHub source-lock.json")
    metadata = json.loads(source_lock.read_text())
    if set(metadata.get("sites", {})) != {"fountain", "solstice", "teatro"}:
        raise SystemExit("Incomplete release sources")
    stats = {}
    for site in ("fountain", "solstice", "teatro"):
        changed = counted = 0
        for page in sorted((release / site).rglob("index.html")):
            source = page.read_text(encoding="utf-8")
            projected, navs = rewrite(source)
            counted += navs
            if projected != source:
                page.write_text(projected, encoding="utf-8")
                changed += 1
        stats[site] = dict(navPages=counted, changed=changed)
    metadata["stageOnlyTransform"] = "governed estate links and exact source-admitted bookshelf reader hrefs to adjacent WLAN ports"
    metadata["navigationProjection"] = stats
    source_lock.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({"release": str(release), "projection": stats}, indent=2))

if __name__ == "__main__":
    main()
