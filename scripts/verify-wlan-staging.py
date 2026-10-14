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
       ROOTS["teatro"]]
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
 for host in ("solstice","teatro"):
  body=fetch(ROOTS[host])[0].decode()
  check_rail(body,host,NAV)
  assert 'data-legal-role="company-status"' in body
  print("PASS",host,"front-door rail and footer")
 first=fetch(ROOTS["solstice"]+"editions/first-reading/")[0]
 assert b'id="book-viewport"' in first and b'id="book-next"' in first
 assets={
  "fountain":["assets/editions.css","assets/linotype/book.css",
              "assets/linotype/book.js","assets/linotype/linotype-engine.js",
              "assets/linotype/mobile-page-navigation.js","assets/linotype/essays.css"],
  "solstice":["assets/book.css","assets/book.js","assets/linotype-engine.js",
              "assets/mobile-page-navigation.js","assets/mobile-page-navigation.css"],
  "teatro":["assets/estate-core.css","assets/estate-core.js","assets/index-CY5_5ULO.js"]
 }
 for host,files in assets.items():
  for path in files:
   body,_=fetch(ROOTS[host]+path)
   assert len(body)>0,(host,path)
  print("PASS",host,len(files),"real assets")
 print("WLAN_EDITION_HIERARCHY_ACCEPTED",HREFS)

if __name__=="__main__":test()
