#!/usr/bin/env python3
"""R28 v65: source-bound First Readings teal containing-space projection."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

PREVIOUS="shared-shell-20261029-v64-reframe-app-ef6e193"
COLLECTION_SHA="8cbaa8cf73400602d0d61520f18d3b8f2e7885e2570981e941a6184b29d91314"
INPUTS={
 "estate/index.html":"c9d8fb59fcd4fc9079124bc2a04c9b58b6c5a5d4cda534b173be3b0a535f386d",
 "estate/collections/first-readings/index.html":"dc0540087350f1a26b58519b2bcbaa176d553b037268482f2796396fb4a3df84",
 "estate/editions/essays/teatro-an-unfinished-composition/index.html":"b3704d0bf5cfd9da4063abd3d4baa937030752eb18f4e6853aad81ca8cca964c",
 "estate/collections/first-readings/collection.json":COLLECTION_SHA,
 "estate/assets/linotype/bookshelf.css":"abf39bf95ff3057bd627fe5427131235964bf17896f02ae166cb36f7c17539fd",
 "estate/assets/linotype/book.css":"56e6780326e06fe63b48f8bfa2f46076c814bbc25b807d9bcb5237748c319693"
}
OUTPUTS={
 "estate/collections/first-readings/index.html",
 "estate/editions/essays/teatro-an-unfinished-composition/index.html",
 "estate/assets/linotype/bookshelf.css",
 "estate/assets/linotype/book.css"
}
SOURCE_CSS={
 "estate/assets/linotype/bookshelf.css":"f6a93b5b5e78697d5b92fdf862d9640b7e81923b2564a32667f9fe66215c792c",
 "estate/assets/linotype/book.css":"108693986bfe47966351cf6f4e73d022d471420a7d764cf0bc9be561c86913f4"
}
ATTRS=(' data-containing-space-id="first-readings"'
       ' data-containing-space-tone="teal"'
       ' data-containing-source-sha256="'+COLLECTION_SHA+'"')

def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
 return h.hexdigest()

def only(text,old,new):
 if text.count(old)!=1:raise ValueError("Unexpected source shape: "+old)
 return text.replace(old,new,1)

def paths(args):
 root=Path(args.root).resolve(strict=True)
 active=(root/"current").resolve(strict=True)
 if active.name!=PREVIOUS or active.parent!=root/"releases":raise RuntimeError("Wrong active predecessor")
 if not re.fullmatch(r"shared-shell-20261029-v65-reframe-color-[a-z0-9]{7}",args.release):raise ValueError("Release name invalid")
 target=root/"releases"/args.release
 return root,active,target

def build(args):
 root,active,target=paths(args)
 if target.exists():raise FileExistsError(target)
 for name,expected in INPUTS.items():
  if sha(active/name)!=expected:raise RuntimeError("Changed predecessor "+name)
 collection=json.loads((active/"estate/collections/first-readings/collection.json").read_text())
 if collection["identity"]!="first-readings" or [x["workId"] for x in collection["works"]]!=["teatro-an-unfinished-composition"]:
  raise RuntimeError("No verified source collection membership")
 sources={}
 for name,expected in SOURCE_CSS.items():
  original=Path(args.css_dir)/Path(name).name
  if sha(original)!=expected:raise RuntimeError("Press CSS source mismatch "+str(original))
  sources[name]=original
 sheet=(active/"estate/collections/first-readings/index.html").read_text()
 sheet=only(sheet,'class="book-app bookshelf-state collection-state app-surface"',
                 'class="book-app bookshelf-state collection-state app-surface containing-context"')
 sheet=only(sheet,'data-collection-id="first-readings"', 'data-collection-id="first-readings"'+ATTRS)
 sheet=only(sheet,'aria-label="First Readings editions"', 'aria-label="First Readings containing space"')
 if sheet.count('data-book-id="teatro-an-unfinished-composition"')!=1 or sheet.count('class="bookshelf-empty"')!=20:
  raise ValueError("Source collection altered")
 book=(active/"estate/editions/essays/teatro-an-unfinished-composition/index.html").read_text()
 book=only(book,'data-edition-id="essays-teatro-an-unfinished-composition"',
                'data-edition-id="essays-teatro-an-unfinished-composition"'+ATTRS)
 if 'id="book-viewport"' not in book or 'data-edition-entry-anchor="book-cover"' not in book:
  raise ValueError("Book source reader altered")
 try:
  shutil.copytree(active,target,symlinks=True)
  (target/"estate/collections/first-readings/index.html").write_text(sheet)
  (target/"estate/editions/essays/teatro-an-unfinished-composition/index.html").write_text(book)
  for name,source in sources.items():shutil.copyfile(source,target/name)
  if sha(target/"estate/index.html")!=INPUTS["estate/index.html"]:
   raise RuntimeError("Neutral root has changed")
  outputs={name:sha(target/name) for name in sorted(OUTPUTS)}
  lock=json.loads((target/"source-lock.json").read_text())
  record={"schema":"fountain.reframe.r28.semantic-color.v1",
    "state":"private-WLAN-candidate-only","release":target.name,
    "predecessor":PREVIOUS,"sourceCollectionSHA256":COLLECTION_SHA,
    "sourceMembership":["teatro-an-unfinished-composition"],
    "presentation":"teal field and circular context on containing collection; slim teal toolbar rail on member reader",
    "rootNeutral":True,"coverArtworkUnchanged":True,
    "sourceCSSSHA256":SOURCE_CSS,"originalSHA256":INPUTS,
    "outputSHA256":outputs,"published":False,
    "browserAcceptance":"pending"}
  lock["reframeSemanticColorV65"]=record
  (target/"source-lock.json").write_text(json.dumps(lock,indent=2,ensure_ascii=False)+"\n")
  return record
 except Exception:
  shutil.rmtree(target,ignore_errors=True)
  raise

def activate(args):
 root,active,target=paths(args)
 record=json.loads((target/"source-lock.json").read_text())["reframeSemanticColorV65"]
 if record["predecessor"]!=active.name:raise RuntimeError("Predecessor mismatch")
 for name,digest in record["outputSHA256"].items():
  if sha(target/name)!=digest:raise RuntimeError("Unreviewed artifact drift "+name)
 tmp=root/"current.reframe-color-next"
 if tmp.exists() or tmp.is_symlink():raise FileExistsError(tmp)
 tmp.symlink_to(Path("releases")/target.name)
 os.replace(tmp,root/"current")
 return {"active":target.name,"previous":active.name,"readbackRequired":True}

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--root",required=True)
 p.add_argument("--release",required=True)
 p.add_argument("--css-dir",default="/home/benedikt/r28-color-source")
 p.add_argument("--activate",action="store_true")
 args=p.parse_args()
 print(json.dumps(activate(args) if args.activate else build(args),indent=2))
