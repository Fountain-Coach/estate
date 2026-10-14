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
    "estate": f"http://{IP}:8180/",
    "first-reading": f"http://{IP}:8181/editions/first-reading/",
    "teatro": f"http://{IP}:8182/",
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
    return updated, count

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
    metadata["stageOnlyTransform"] = "exactly three editorial navigation hrefs to adjacent WLAN ports"
    metadata["navigationProjection"] = stats
    source_lock.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({"release": str(release), "projection": stats}, indent=2))

if __name__ == "__main__":
    main()
