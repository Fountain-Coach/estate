#!/usr/bin/env python3
"""Source-preserving, versioned EstateShell projection. Preview only.

Requires BeautifulSoup4; never mutates source owner, rights or public domain.
Reframe admission and Fountain Press Linotype remain independent.
"""
import argparse, hashlib, json
from pathlib import Path
from bs4 import BeautifulSoup

VERSION="fountain.estate.shell.v1-candidate-20261022"
REEL="fountain.estate.canonical-reel.v1"
FOOTER="fountain.estate.canonical-footer.v1"
LEGAL=(("Legal notices","https://governance.fountain.coach/legal/"),
       ("Privacy","https://governance.fountain.coach/privacy/"),
       ("Accessibility","https://governance.fountain.coach/accessibility/"),
       ("Copyright","https://governance.fountain.coach/copyright/"),
       ("Status","https://status.fountain.coach/"))
IDS=("estate","book","governance","midi2","instruments","teatro","satzfunk","pointer","solstice")

def manifest(path):
    d=json.loads(Path(path).read_text())
    if d["schema"]!=REEL or tuple(v["id"] for v in d["entries"])!=IDS:
        raise ValueError("canonical reel mismatch")
    if any(not v["url"].startswith("https://") for v in d["entries"]):
        raise ValueError("non-HTTPS destination")
    return d

def contract(d):
    return {"schema":"fountain.estate.shell-acceptance.v1","reelVersion":REEL,
        "footerVersion":FOOTER,
        "entries":[{k:e[k] for k in ("id","label","url")} for e in d["entries"]],
        "supportingDestinations":[{"id":"legal","url":LEGAL[0][1]},
                                  {"id":"status","url":LEGAL[-1][1]}],
        "primaryEditorialEntrances":["estate","solstice","teatro"],
        "publicationLanes":{"reframeBookshelf":{"releasesPublicWebsite":False,
            "createsEstateReelEntry":False},"estatePublisher":{
            "requiresSeparateRightsAndRoute":True,"independentHTTPSReadback":True}}}

def work_digest(soup):
    main=soup.find("main")
    if not main:return None
    clone=BeautifulSoup(str(main),"html.parser")
    for foot in clone.select("footer.footer#footer,footer.estate-footer#footer"):
        foot.decompose()
    return hashlib.sha256(str(clone.find("main")).encode()).hexdigest()

def fragment(d,ident,logo):
    from html import escape as h
    if ident not in IDS and ident!="status":raise ValueError("unknown identity")
    links=[]
    for e in d["entries"]:
        active=' aria-current="page"' if ident==e["id"] else ""
        links.append('<a class="fc-reel-link" data-estate-id="'+e["id"]+
           '" data-icon-id="'+e["id"]+'" aria-label="'+h(e["label"])+
           '" href="'+h(e["url"],quote=True)+'"'+active+
           '><svg viewBox="0 0 24 24" aria-hidden="true"><path d="'+
           h(e["path"],quote=True)+'"/></svg><span>'+h(e["label"])+'</span></a>')
    links.append('<a class="fc-reel-link estate-info" href="#footer" aria-label="Info">'
         '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<path d="M12 11v6m0-10v.1"/></svg><span>Info</span></a>')
    header='<header class="fc-estate-shell" data-estate-shell-version="'+VERSION+\
       '" data-estate-slot="masthead"><div class="fc-shell-row">'+\
       '<a class="fc-publisher" href="https://fountain.coach/"><img class="estate-logo" '+\
       'alt="Fountain Coach" src="'+h(logo,quote=True)+'"/>'+\
       '<span class="fc-publisher-name">Fountain Coach<small>Publication estate</small></span></a>'+\
       '<span class="fc-site-identity">'+h(ident.upper())+'</span></div>'+\
       '<nav class="estate-nav site-nav fc-shell-reel" id="site-nav" data-site-nav="" data-reel-contract="'+REEL+\
       '" aria-label="Fountain Coach publication estate">'+''.join(links)+'</nav></header>'
    legal=' · '.join('<a href="'+h(url,quote=True)+'">'+h(label)+'</a>' for label,url in LEGAL)
    footer='<footer class="estate-footer fc-estate-shell" id="footer" role="contentinfo" '+\
       'data-estate-shell-version="'+VERSION+'" data-footer-contract="'+FOOTER+'">'+\
       '<div class="fc-footer-grid"><section data-footer-slot="imprint"><h2>Fountain Coach</h2>'+\
       '<p>Founded by Benedikt Eickhoff · Berlin</p></section>'+\
       '<section data-footer-slot="provenance"><h2>Source &amp; edition</h2>'+\
       '<p>Independent editorial owner: '+h(ident)+'</p></section>'+\
       '<section data-footer-slot="legal"><h2>Legal &amp; access</h2><p>'+legal+'</p></section>'+\
       '<section data-footer-slot="release-state"><h2>Publication state</h2>'+\
       '<p>Private template preview; no public release authorized.</p></section></div></footer>'
    return header,footer

def project(source,identity,d,logo="/assets/estate-shell-logo.png"):
    soup=BeautifulSoup(source,"html.parser")
    if not soup.head or not soup.body:raise ValueError("not a complete HTML document")
    if soup.select_one("[data-estate-shell-version]"):raise ValueError("duplicate shell")
    original=work_digest(soup)
    controls=[tag.get("id") for tag in soup.select(".book-toolbar button[id],.book-pagination button[id]")]
    header,footer=fragment(d,identity,logo)
    old_header=soup.select_one("header.site-header")
    if old_header:old_header.replace_with(BeautifulSoup(header,"html.parser").header)
    else:soup.body.insert(0,BeautifulSoup(header,"html.parser").header)
    old_footer=soup.select_one("footer.footer#footer")
    if old_footer:old_footer.replace_with(BeautifulSoup(footer,"html.parser").footer)
    else:soup.body.append(BeautifulSoup(footer,"html.parser").footer)
    css=soup.new_tag("link",rel="stylesheet",href="/assets/estate-shell.css")
    soup.head.append(css)
    robots=soup.new_tag("meta");robots["name"]="robots";robots["content"]="noindex,nofollow"
    soup.head.append(robots)
    if original!=work_digest(soup):raise AssertionError("authored work content mutated")
    if any(not soup.select_one('[id="'+c+'"]') for c in controls):
        raise AssertionError("book control changed")
    out=str(soup)
    return out,{"identity":identity,"sourceSHA256":hashlib.sha256(source.encode()).hexdigest(),
                "projectionSHA256":hashlib.sha256(out.encode()).hexdigest(),
                "sourceWorkSHA256":original,"retainedReaderControls":controls,
                "shellVersion":VERSION,"publicReleased":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True,type=Path)
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--identity",required=True)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--logo",default="/assets/estate-shell-logo.png")
    x=p.parse_args()
    out,receipt=project(x.source.read_text(),x.identity,manifest(x.manifest),x.logo)
    if x.output.exists():raise SystemExit("refuse overwrite")
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(out)
    print(json.dumps(receipt,indent=2))

if __name__=="__main__":main()
