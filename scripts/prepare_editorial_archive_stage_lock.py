#!/usr/bin/env python3
"""Pin exact v152 current-works/archive staging delta to v151 Reader source."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

PREDECESSOR="shared-shell-20261105-v151-semantic-spread-17e32af"
RELEASE="shared-shell-20261105-v152-editorial-archive-1609cb9"
OWNER="Fountain-Coach/fountain.coach"
SOURCE_COMMIT="1609cb909ae2f89b4b28223fe70c482638d6b854"
OLD_LOCK="ad15c096e83c4695c1b0feb1ec85a3f5f354498baf3a3ffc42d05cff1cad97b9"
KEY="machineReadingEditorialArchiveAdmission"
FILES={
    "estate/index.html":"77f90b8db05a42700f727b4558f7e91a6406e2ae6bf25d59d953fa5ddae7b3d9",
    "estate/assets/linotype/reading-first-app.js":"9fa017c008cebad8586a49a03741aae398a36a0fc61e935364f45b6e913b6345",
    "estate/essays/index.html":"a72cf4bcd1cffebb94585ee20ccb7c4eb2dab4652a85c7d9555cac2b62014e08",
    "estate/assets/essay-share/manifest.json":"21326154d893de327ca889596b4bd8da074d984c16d476a3f1afc0f8abfeefa3"
}
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def admission()->dict:
    return {
      "schema":"fountain.press.publication-editorial-archive.v1",
      "sourceOwner":OWNER,"sourceCommit":SOURCE_COMMIT,
      "sourcePaths":[
         "scenarios/reading-first-20261101/index.html",
         "scenarios/reading-first-20261101/reading-first-app.js",
         "scenarios/reading-first-20261101/essay-share-manifest.json",
         "site/essays/index.html",
         "scenarios/reading-first-20261101/editorial-archive-decision.json"
      ],
      "predecessor":PREDECESSOR,"release":RELEASE,
      "writerDecisionDate":"2026-11-05",
      "archivedWork":"essay--to-read-is-not-to-remember",
      "archivedWorkTitle":"Did the Machine Actually Read the Book?",
      "originalSourceHTMLSHA256":"553b26f69963d0787c416b64b56591d3ccb46b01541d57debf1f79dc5d6a1714",
      "originalPrivateStageRouteSHA256":"2eb20df27e4b1a85c2c531f061a712f2aaf66f792df5cda518bb14b62d0822b3",
      "currentEssayCount":5,"unchangedFirstReadingsCount":30,
      "archiveRoutePreserved":True,"originalWriterProseUnchanged":True,
      "ReaderShellUnchanged":True,"PressCompositorUnchanged":True,
      "privateMediaUnchanged":True,"stageOnly":True,
      "publicReleased":False,"fountainStoreAdmitted":False,
      "changedFileSHA256":FILES
    }
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--predecessor-lock",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    opts=a.parse_args()
    original=opts.predecessor_lock.read_bytes()
    if sha(original)!=OLD_LOCK:raise ValueError("Unknown v151 Reader ancestor lock")
    contents=json.loads(original)
    if KEY in contents or "modernPageSemanticSpreadAdmission" not in contents:
        raise ValueError("Unadmitted original source")
    contents[KEY]=admission()
    blob=(json.dumps(contents,ensure_ascii=False,indent=2)+"\n").encode()
    if opts.out.exists():raise ValueError("Refuse candidate lock overwrite")
    opts.out.parent.mkdir(parents=True,exist_ok=True)
    opts.out.write_bytes(blob)
    print(json.dumps({"release":RELEASE,"predecessor":PREDECESSOR,
      "sourceCommit":SOURCE_COMMIT,"lockSHA256":sha(blob),"files":FILES},indent=2))
if __name__=="__main__":main()
