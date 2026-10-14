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
 assert 'class="edition-list"' in catalogue
 assert '<h1>Editions<span>.</span></h1>' in catalogue
 assert 'id="book-viewport"' not in catalogue
 check_rail(catalogue,"catalogue",NAV)
 assert 'data-legal-role="company-status"' in catalogue
 print("PASS","fountain","editions catalogue at root","three edition rail links")
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
 teatro=fetch(ROOTS["teatro"])[0].decode()
 assert teatro==fetch(ROOTS["teatro"]+"editions/first-hearing/")[0].decode()
 assert 'id="book-viewport"' in teatro and 'id="book-flow"' in teatro
 assert teatro.count('data-book-chapter=')==1
 assert teatro.count('src="/assets/edition/')==1
 assert 'id="book-media-toggle"' in teatro and 'id="book-ear-status"' in teatro
 assert 'class="book-ear-icon"' in teatro
 assert 'class="book-ear-meter"' not in teatro
 assert teatro.index('id="book-media-toggle"')<teatro.index('id="book-media-settings"')<teatro.index('class="book-ear-icon"')
 css=fetch(ROOTS["teatro"]+"assets/linotype/book.css")[0].decode()
 assert 'justify-content:space-between' in css
 assert '.book-reading-controls .book-media-control{margin-right:auto}' in css
 assert '.book-reading-controls #book-toc-button{margin-left:auto' in css
 control_css=fetch(ROOTS["teatro"]+"assets/linotype/book-player.css")[0].decode()
 assert '--ear-scale' in control_css and '.book-ear-meter' not in control_css
 assert 'left:0;right:auto' in control_css
 scene_script=fetch(ROOTS["teatro"]+"assets/linotype/teatro-stage-page.js")[0].decode()
 assert 'fountain:book:play-request' in scene_script and 'fountain:book:transport' in scene_script
 player_script=fetch(ROOTS["teatro"]+"assets/linotype/book-player.mjs")[0].decode()
 assert 'fountain:book:play-request' in player_script
 assert 'fountain:book:transport' in player_script
 assert "earIcon" in player_script and "source==='teatro-web-audio-preview'?0.30:0.025" in player_script
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
 print("PASS","teatro","standalone reader controls/side rail, MIDI2 Ear, old site header/footer absent; stage retained")
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
