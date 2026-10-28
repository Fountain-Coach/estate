#!/usr/bin/env python3
"""Bounded author-led editorial stage delta over an immutable v56 predecessor.

Run against a disposable *copy*, never active current. No public deployment.
Preserves all existing v56 bytes except declared HTML/chrome routes and adds
independent authentic edition assets from the pinned Git source.
"""
from __future__ import annotations
import hashlib, json, re, shutil, sys
from pathlib import Path
from urllib.parse import urlsplit

base, owner = (Path(sys.argv[1]), Path(sys.argv[2]))
assert (base/"estate/index.html").is_file() and (base/"source-lock.json").is_file()
assert (owner/"site/index.html").is_file() and (owner/"site/assets/author-landing.css").is_file()
source = (owner/"site/index.html").read_text()
target = base/"estate/index.html"
prior = target.read_text()
main_rx = re.compile(r'<main\b[\s\S]*?</main>', re.I)
assert len(main_rx.findall(source))==len(main_rx.findall(prior))==1
original_main = main_rx.search(source).group()
assert original_main.count('class="essay-gallery-card"') == 4
assert '<h1 id="landing-heading">' in original_main
assert 'href="/essays/"' in original_main
# Stage-only routing. Canonical/source payload is untouched.
new_main = re.sub(r'((?:href|src)=")/(?=(?:essays|assets|editions|collections)/)',r'\1/estate/',original_main)
new_main = new_main.replace('href="https://works.benedikt-eickhoff.de/"',
                            'href="/works/" data-canonical-href="https://works.benedikt-eickhoff.de/"')
rendered = main_rx.sub(lambda _:new_main,prior,count=1)
assert 'class="fc-estate-shell"' in rendered or 'class="fc-estate-shell"' in prior
assert rendered.count('data-estate-id="satzfunk"')==1
assert rendered.count('data-estate-id="works"')==1
assert rendered.count('class="essay-gallery-card"')==4
rendered,n = re.subn(r'<title>[\s\S]*?</title>',
                     '<title>Fountain Coach — Writing, software and performance by Benedikt Eickhoff</title>',
                     rendered,count=1)
assert n==1
# The shell belongs to the registered active stage. Replace only the editorial
# head metadata, not the existing CSS/JS shell, origin bindings or legal footer.
head,sep,tail = rendered.partition('</head>')
assert sep
def set_meta(body, discriminator, new):
    pattern = r'<meta\b(?=[^>]*'+discriminator+r')[^>]*>'
    changed,count = re.subn(pattern,lambda _:new,body,count=1,flags=re.I)
    assert count==1,(discriminator,"metadata not found")
    return changed
head=set_meta(head,r'name="description"',
    '<meta name="description" content="An independent development and publishing practice by Benedikt Eickhoff. Read essays and inspect Reframe, Teatro, MIDI 2.0 and their evidence.">')
head=set_meta(head,r'name="fountain:publication-role"',
    '<meta name="fountain:publication-role" content="author-led estate identity">')
head=set_meta(head,r'property="og:title"',
    '<meta property="og:title" content="Fountain Coach — Writing, software and performance">')
head=set_meta(head,r'property="og:description"',
    '<meta property="og:description" content="Writing, software and performance by Benedikt Eickhoff.">')
head=set_meta(head,r'property="og:image"',
    '<meta property="og:image" content="https://fountain.coach/essays/the-door-is-a-score/assets/teatro-door-score-social-v2.jpg">')
head=set_meta(head,r'name="twitter:title"',
    '<meta name="twitter:title" content="Fountain Coach — Writing, software and performance">')
head=set_meta(head,r'name="twitter:description"',
    '<meta name="twitter:description" content="An independent development and publishing practice by Benedikt Eickhoff.">')
head=set_meta(head,r'name="twitter:image"',
    '<meta name="twitter:image" content="https://fountain.coach/essays/the-door-is-a-score/assets/teatro-door-score-social-v2.jpg">')
if 'assets/author-landing.css' not in head:
    head += '<link href="/estate/assets/author-landing.css" rel="stylesheet">\n'
rendered=head+sep+tail
rendered=rendered.replace('<small>Publication estate</small></span>','<small>Independent practice · Benedikt Eickhoff</small></span>',1)
assert 'Author the conditions for what comes next.' not in rendered
assert rendered.count('data-estate-shell-version="')==2
assert 'data-footer-contract="fountain.estate.canonical-footer.v1"' in rendered
target.write_text(rendered)
(base/"estate/assets").mkdir(parents=True,exist_ok=True)
shutil.copy2(owner/"site/assets/author-landing.css",base/"estate/assets/author-landing.css")

# Complete authentic source-owned editions remain available next door.
# This adds no fabricated publication or rewrites to existing v56 essays.
for name in ("editions","collections/first-readings"):
    src=owner/"site"/name
    dst=base/"estate"/name
    assert src.is_dir()
    shutil.copytree(src,dst,dirs_exist_ok=True)
for name in ("assets/linotype","assets/estate-bookshelf"):
    src=owner/"site"/name
    dst=base/"estate"/name
    assert src.is_dir()
    shutil.copytree(src,dst,dirs_exist_ok=True)
for name in ("assets/essay-pathways.css","assets/editions.css"):
    src=owner/"site"/name
    dst=base/"estate"/name
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)

def remap_html(html:str):
    # All root-relative navigational assets resolve on the *private* stage host.
    html=re.sub(r'((?:href|src)=")/(?=(?:essays|assets|editions|collections)/)',
                r'\1/estate/',html)
    html=html.replace('href="/"','href="/estate/"')
    # Semantic canonical/OG metadata remains on the real source host. Only
    # interactive anchors to an existing Fountain Coach route remap to WLAN.
    html=re.sub(r'href="https://fountain\.coach/((?:essays|editions|collections)/[^"]*)"',
                lambda m:'href="/estate/'+m.group(1)+'" data-canonical-href="https://fountain.coach/'+m.group(1)+'"',html)
    return html
changed=[]
for name in ("editions","collections/first-readings"):
    for f in sorted((base/"estate"/name).rglob("*.html")):
        f.write_text(remap_html(f.read_text()))
        changed.append(f.relative_to(base).as_posix())
for f in (base/"estate/assets/linotype/essays.css",):
    t=f.read_text()
    f.write_text(t.replace("url('/essays/","url('/estate/essays/"))

# Source-lock is private, and its predecessor is retained. No file marked as
# public ever claims EstatePublisher production approval.
lock=base/"source-lock.json"
m=json.loads(lock.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m["authorLedEditorialStage"]={
 "schema":"fountain.estate.author-led-staging-delta.v1",
 "sourceOwner":"Fountain-Coach/fountain.coach",
 "sourceSHA":"aa38389ba2ef9070d91a36c169e74902ed3b096b",
 "estateOwner":"Fountain-Coach/estate",
 "estateSourceSHA":"81cdf15ee26e37fd8d0008ab624e41f3e966c421",
 "predecessor":"shared-shell-20261028-v56-modell-wirklichkeit-e3753d7",
 "stageRole":"one-person editorial identity + original four essay plates",
 "homepageSHA256":sha(target),
 "homepageCSSSHA256":sha(base/"estate/assets/author-landing.css"),
 "addedEditionHTMLRoutes":len(changed),
 "preserveAllOldStageRoutes":True,
 "publicReleased":False,
 "browserAcceptancePending":True
}
m["authorPublished"]=False
lock.write_text(json.dumps(m,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
print(json.dumps({"stageCandidate":"composed","root":str(base),
 "homeSHA256":sha(target),"CSS_SHA256":sha(base/"estate/assets/author-landing.css"),
 "editionRoutes":changed,
 "priorEssayDoorSHA256":sha(base/"estate/essays/the-door-is-a-score/index.html"),
 "priorEssayComposableSHA256":sha(base/"estate/essays/the-composable-book/index.html")
 },indent=2))
