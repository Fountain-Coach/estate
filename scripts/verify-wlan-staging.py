#!/usr/bin/env python3
"""Read-only WLAN proof of edition-catalogue and nested Linotype hierarchy."""
from urllib.request import Request,urlopen
import json,re

IP="192.168.8.249"
ROOTS={host:f"http://{IP}:{port}/" for host,port in
       (("fountain",8180),("solstice",8181),("teatro",8182))}
NAV=re.compile(r'<nav\b[^>]*class="[^"]*\bestate-nav\b[^"]*"[^>]*>.*?</nav>',re.S)
EDNAV=re.compile(r'<nav\b[^>]*class="[^"]*\bedition-rail\b[^"]*"[^>]*>.*?</nav>',re.S)
IDS=["estate","first-reading","teatro"]
HREFS=[ROOTS["fountain"]+"editions/essays/",
       ROOTS["solstice"]+"editions/first-reading/",
       ROOTS["teatro"]+"editions/first-hearing/"]
SLUGS=[
 ("teatro-an-unfinished-composition",1),
 ("semantic-compilation-the-archive-is-not-the-edition",1),
 ("reframe-and-the-business-value-of-the-estate",3)
]
def fetch(url):
 with urlopen(Request(url,headers={"Cache-Control":"no-cache"}),timeout=18) as response:
  body=response.read()
  assert response.status==200,(url,response.status)
  assert "noindex" in response.headers.get("X-Robots-Tag",""),url
  return body,response.headers
def check_rail(html,label,matcher):
 nav=matcher.search(html)
 assert nav is not None,(label,"missing edition rail")
 links=nav.group()
 assert re.findall(r'data-estate-id="([^"]+)"',links)==IDS,(label,"wrong rail entries")
 for identity,href in zip(IDS,HREFS):
  anchor=re.search(r'<a\b[^>]*data-estate-id="'+identity+r'"[^>]*>',links)
  assert anchor is not None and 'href="'+href+'"' in anchor.group(),(label,identity,href)
 assert 'data-estate-id="status"' not in links
 return True

def test():
 for host,root in ROOTS.items():
  health=json.loads(fetch(root+"__stage/health")[0])
  assert health["status"]=="ready"
  assert health["productionPublished"] is False
  assert set(health["sites"])==set(ROOTS)
  assert health["sites"][host]["repository"] == {
   "fountain":"Fountain-Coach/fountain.coach",
   "solstice":"Fountain-Coach/solstice.fountain.coach",
   "teatro":"Fountain-Coach/teatro.fountain.coach"}[host]
  assert re.fullmatch(r"[a-f0-9]{40}",health["sites"][host]["commit"])
 catalogue=fetch(ROOTS["fountain"])[0].decode()
 assert catalogue==fetch(ROOTS["fountain"]+"editions/")[0].decode()
 assert 'data-linotype-state="bookshelf"' in catalogue
 assert catalogue.count('class="shelf-book"')==3
 assert catalogue.count('class="shelf-item"')==3
 assert catalogue.count('class="bookshelf-brand fc-identity-circle"')==1
 assert catalogue.count('class="shelf-cover"')==3
 assert '<h1' not in catalogue and 'id="book-viewport"' not in catalogue
 assert 'instrument-slot' not in catalogue
 for href in HREFS:
  assert 'href="'+href+'"' in catalogue,href
 for asset in ('fountain-coach-edition.png','first-reading-ink.png',
               'teatro-score-memory-vector-human-condition.svg'):
  assert len(fetch(ROOTS['fountain']+'assets/estate-bookshelf/'+asset)[0])>1000
 press_css=fetch(ROOTS['fountain']+'assets/linotype/bookshelf.css')[0]
 teatro_css=fetch(ROOTS['teatro']+'assets/linotype/bookshelf.css')[0]
 assert press_css==teatro_css and b'background:transparent;box-shadow:none;' in press_css
 identity=fetch(ROOTS['fountain']+'assets/linotype/identity-circle.css')[0]
 assert identity==fetch(ROOTS['teatro']+'assets/linotype/identity-circle.css')[0]
 assert b'--fc-identity-circle-radius:50%' in identity and b'--fc-identity-circle-stroke:1px' in identity
 assert b'@import url("./identity-circle.css")' in press_css
 detailed=fetch(ROOTS['fountain']+'editions/catalogue/')[0].decode()
 assert 'class="edition-list"' in detailed
 assert 'data-legal-role="company-status"' in detailed
 check_rail(detailed,'preserved detailed catalogue',NAV)
 print("PASS","fountain","four occupied cells plus twenty visible vacant slots","three canonical cover routes and retained detailed catalogue")
 essay_book=fetch(ROOTS["fountain"]+"editions/essays/")[0].decode()
 assert 'id="book-viewport"' in essay_book
 assert essay_book.count('data-book-chapter=')==3
 assert essay_book.count('src="/essays/')==5
 assert essay_book.count('data-book-toc-target=')==4
 check_rail(essay_book,"essay-volume",EDNAV)
 assert 'data-legal-role="company-status"' in essay_book
 print("PASS","fountain","complete essay volume, 3 chapters, 5 originals")
 for slug,plates in SLUGS:
  html=fetch(ROOTS["fountain"]+"editions/essays/"+slug+"/")[0].decode()
  assert html.count('data-book-chapter=')==1,slug
  assert html.count('src="/essays/')==plates
  assert html.count('data-book-toc-target=')==2
  assert 'data-edition-id="essays-'+slug+'"' in html
  assert 'href="/editions/essays/"' in html
  check_rail(html,slug,EDNAV)
  assert 'data-legal-role="company-status"' in html
  print("PASS","nested Linotype sub-edition",slug,"plates",plates)
 source=fetch(ROOTS["fountain"]+"essays/")[0].decode()
 check_rail(source,"original essay directory",NAV)
 assert 'data-legal-role="company-status"' in source
 body=fetch(ROOTS["solstice"])[0].decode()
 check_rail(body,"solstice",NAV)
 assert 'data-legal-role="company-status"' in body
 print("PASS","solstice","First Reading edition rail and footer")
 shelf=fetch(ROOTS["teatro"])[0].decode()
 assert shelf==fetch(ROOTS["teatro"]+"editions/")[0].decode()
 assert 'data-linotype-state="bookshelf"' in shelf
 assert 'data-book-count="3"' in shelf
 assert shelf.count('class="shelf-book"')==3
 assert shelf.count('class="shelf-cover"')==3
 assert shelf.count('data-preview-host="fountain"')==1
 assert shelf.count('data-preview-host="solstice"')==1
 assert shelf.count('data-preview-host="teatro"')==1
 assert shelf.count('data-release-status="public-live"')==1
 assert shelf.count('data-release-status="wlan-proof"')==2
 assert 'class="shelf-miniature"' not in shelf
 assert 'class="shelf-cover-title"' not in shelf
 assert 'class="shelf-cover-kicker"' not in shelf
 assert 'class="shelf-cover-author"' not in shelf
 assert 'class="bookshelf-toolbar"' not in shelf
 assert 'class="bookshelf-pagination"' not in shelf
 assert 'class="bookshelf-paper-head"' not in shelf
 assert 'class="bookshelf-paper-foot"' not in shelf
 assert 'class="bookshelf-intro"' not in shelf
 assert '<h1' not in shelf
 assert shelf.count('class="bookshelf-brand fc-identity-circle"')==1
 assert shelf.count('class="bookshelf-wordmark"')==0  # authentic mark alone (R24)
 assert 'FOUNTAIN COACH</span>' not in shelf
 assert 'src="/assets/bookshelf/fountain-coach-logo-transparent.png"' in shelf
 logo=fetch(ROOTS["teatro"]+"assets/bookshelf/fountain-coach-logo-transparent.png")[0]
 import hashlib
 assert hashlib.sha256(logo).hexdigest()=="8c5fad1c3db56138d5959da75991dc8034a0be537ce46da6ffcc0d9655e7f729"
 assert 'href="'+ROOTS["fountain"]+'editions/essays/"' in shelf
 assert 'href="'+ROOTS["solstice"]+'editions/first-reading/"' in shelf
 assert 'href="/editions/first-hearing/"' in shelf
 for root, path in [(ROOTS["fountain"],"editions/essays/"), (ROOTS["solstice"],"editions/first-reading/")]:
  assert 'id="book-flow"' in fetch(root+path)[0].decode()
 for path in (
  "editions/essays/teatro-an-unfinished-composition/",
  "editions/essays/semantic-compilation-the-archive-is-not-the-edition/",
  "editions/essays/reframe-and-the-business-value-of-the-estate/"):
  assert 'id="book-flow"' in fetch(ROOTS["fountain"]+path)[0].decode()
 for image in (
  "/assets/bookshelf/fountain-coach-edition.png",
  "/assets/bookshelf/first-reading-ink.png",
  "/assets/edition/teatro-score-memory-vector-human-condition.svg"):
  assert len(fetch(ROOTS["teatro"]+image.lstrip("/"))[0])>1000,image
 assert 'rotate(-3deg)' not in fetch(ROOTS["teatro"]+"assets/linotype/bookshelf.css")[0].decode()
 shelf_css=fetch(ROOTS["teatro"]+"assets/linotype/bookshelf.css")[0].decode()
 assert 'background:transparent;' in shelf_css
 assert '.bookshelf-brand{aspect-ratio:1;display:grid;place-items:center;' in shelf_css
 assert shelf.count('class="bookshelf-empty" aria-hidden="true"')==20
 assert catalogue.count('class="bookshelf-empty" aria-hidden="true"')==20
 assert 'box-shadow:none;' in shelf_css
 assert 'background:var(--paper);box-shadow:' not in shelf_css
 assert 'id="book-flow"' not in shelf
 assert 'governance-constitution' not in shelf and 'book-of-reframe' not in shelf
 assert len(fetch(ROOTS["teatro"]+"assets/linotype/bookshelf.css")[0])>1500
 teatro=fetch(ROOTS["teatro"]+"editions/first-hearing/")[0].decode()
 assert shelf!=teatro
 assert 'id="book-viewport"' in teatro and 'id="book-flow"' in teatro
 assert teatro.count('data-book-chapter=')==1
 assert teatro.count('src="/assets/edition/')==1
 assert 'class="fc-identity-circle" id="book-media-toggle"' in teatro and 'id="book-ear-status"' in teatro
 assert 'class="book-ear-icon"' in teatro
 assert 'class="book-player-status book-ear-status" id="book-ear-status"' in teatro
 assert 'id="book-ear-reading"' in teatro
 assert teatro.index('id="book-media-details"')<teatro.index('class="book-ear-icon"')
 assert 'class="book-ear-meter"' not in teatro
 assert teatro.index('id="book-media-toggle"')<teatro.index('id="book-media-settings"')<teatro.index('class="book-ear-icon"')
 css=fetch(ROOTS["teatro"]+"assets/linotype/book.css")[0].decode()
 assert 'justify-content:space-between' in css
 assert '.book-reading-controls .book-media-control{margin-right:auto}' in css
 assert '.book-reading-controls #book-toc-button{margin-left:auto' in css
 control_css=fetch(ROOTS["teatro"]+"assets/linotype/book-player.css")[0].decode()
 assert '--play-fill' in control_css and '--play-halo' in control_css
 assert '@import url("./identity-circle.css")' in control_css
 assert '--fc-identity-circle-radius' in control_css and '--fc-identity-circle-stroke' in control_css
 assert 'prefers-reduced-motion:reduce' in control_css
 assert '.book-ear-status' in control_css and '.book-ear-meter' not in control_css
 assert 'left:0;right:auto' in control_css
 scene_script=fetch(ROOTS["teatro"]+"assets/linotype/teatro-stage-page.js")[0].decode()
 assert 'fountain:book:play-request' in scene_script and 'fountain:book:transport' in scene_script
 player_script=fetch(ROOTS["teatro"]+"assets/linotype/book-player.mjs")[0].decode()
 assert 'fountain:book:play-request' in player_script
 assert 'fountain:book:transport' in player_script
 assert "earIcon" in player_script and "source==='teatro-web-audio-preview'?0.60:0.025" in player_script
 assert "'--play-halo'" in player_script and "'--play-fill'" in player_script
 assert "resetTransportVisual()" in player_script
 assert 'id="book-media-settings"' in teatro
 assert teatro.count('data-book-sound-parameter=')==4
 assert 'id="satzfunk-hear"' not in teatro and 'id="satzfunk-hearing-rail"' not in teatro
 assert '>Scene ↓<' not in teatro
 assert 'src="/assets/linotype/book-player.mjs"' in teatro
 assert 'data-teatro-scene-play' in teatro
 assert 'src="/assets/teatro-play.svg"' in teatro
 assert 'src="/assets/teatro-stage-poster.svg"' not in teatro
 atlas_script=fetch(ROOTS["teatro"]+"assets/linotype/mobile-page-navigation.js")[0].decode()
 assert 'book-atlas-identity' in atlas_script
 assert 'book-atlas-title' not in atlas_script
 assert 'cloneNode(true)' not in atlas_script
 for asset in ('assets/linotype/book-player.mjs','assets/linotype/book-midi2.mjs',
               'assets/linotype/book-player.css','assets/book-csound-host.js'):
  payload=fetch(ROOTS["teatro"]+asset)[0]
  assert len(payload)>200,("Missing MIDI2 player asset",asset)
 # The book is a reading instrument, not another estate website.
 assert 'class="book-toolbar book-reading-controls"' in teatro
 assert 'class="book-pagination book-reading-pagination"' in teatro
 assert 'class="book-back"' not in teatro
 assert 'class="edition-rail"' not in teatro
 assert 'class="book-legal"' not in teatro
 assert 'data-legal-role="company-status"' not in teatro
 assert 'aria-haspopup="dialog">Contents</button>' not in teatro
 assert 'id="book-toc-button"' in teatro
 assert '<svg viewBox="0 0 24 24"' in teatro
 assert 'id="book-type-button"' not in teatro
 assert 'id="book-appearance"' not in teatro
 assert 'id="book-font-smaller"' not in teatro
 assert 'id="book-font-larger"' not in teatro
 assert 'src="/assets/teatro-play.svg"' in teatro
 assert '<a href="/editions/">' not in teatro
 assert 'PUBLISHED SOURCE · FOUNTAIN.COACH / TEATRO' in teatro
 book_js=fetch(ROOTS["teatro"]+"assets/linotype/book.js")[0].decode()
 assert 'book-reading-shell' in book_js and 'setContentsOpen(' in book_js
 assert 'engine.compose(1)' in book_js
 assert 'fontSize=clamp(' not in book_js

 stage=fetch(ROOTS["teatro"]+"editions/stage/")[0].decode()
 assert 'data-teatro-stage-return' in stage
 assert 'href="/editions/first-hearing/"' in stage
 assert 'src="/assets/index-CY5_5ULO.js"' in stage
 assert 'id="root"' in stage
 check_rail(stage,"teatro stage",NAV)
 assert 'data-legal-role="company-status"' in stage
 print("PASS","teatro","source-pinned Bookshelf landing plus independent v16 reader, MIDI2 Ear and Stage")
 status=__import__("urllib.error",fromlist=["HTTPError"])
 try:
  fetch(ROOTS["teatro"]+"editions/first-hearing/hearings.json")
 except status.HTTPError as e:
  assert e.code==404,("Undisclosed published hearing?",e.code)
 else:
  raise AssertionError("No released, author-approved narrated Teatro hearing is admitted")
 first=fetch(ROOTS["solstice"]+"editions/first-reading/")[0]
 assert b'id="book-viewport"' in first and b'id="book-next"' in first
 assets={
  "fountain":["assets/editions.css","assets/linotype/book.css",
              "assets/linotype/book.js","assets/linotype/linotype-engine.js",
              "assets/linotype/mobile-page-navigation.js","assets/linotype/essays.css"],
  "solstice":["assets/book.css","assets/book.js","assets/linotype-engine.js",
              "assets/mobile-page-navigation.js","assets/mobile-page-navigation.css"],
  "teatro":["assets/estate-core.css","assets/estate-core.js","assets/index-CY5_5ULO.js",
             "assets/linotype/book.css","assets/linotype/book.js",
             "assets/linotype/linotype-engine.js","assets/linotype/mobile-page-navigation.js",
             "assets/satzfunk/satzfunk-book.mjs","assets/edition/teatro-score-memory-vector-human-condition.svg"]
 }
 for host,files in assets.items():
  for path in files:
   body,_=fetch(ROOTS[host]+path)
   assert len(body)>0,(host,path)
  print("PASS",host,len(files),"real assets")
 print("WLAN_EDITION_HIERARCHY_ACCEPTED",HREFS)

if __name__=="__main__":test()
