import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE=Path(__file__).with_name("serve_shared_shell_preview.py")
spec=importlib.util.spec_from_file_location("serve_shared_shell_preview",MODULE)
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)

class SharedShellPreviewMediaTests(unittest.TestCase):
    def make_root(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root=Path(temp.name)
        for rel in ("estate/index.html","teatro/index.html",
                    "solstice/editions/first-reading/index.html",
                    "assets/estate-shell.css","assets/estate-shell-logo.png",
                    "assets/estate-shell-state.js"):
            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b"fixture")
        lock={"status":"WLAN-PREVIEW-NOT-PUBLIC",
          "templateVersion":"fountain.estate.shell.v2-editorial-20261022",
          "archiveMediaCopied":False,"authorPublished":False,
          "releaseReceipt":None,"sites":{"estate":{},"teatro":{},"solstice":{}}}
        (root/"source-lock.json").write_text(json.dumps(lock))
        return root,lock

    def media(self,root,lock,authorized=True):
        data=b"released-public-mp4-fixture"
        path="teatro/media/bandcamp-20261024/shaders/40479.mp4"
        target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        lock["teatroSatzfunkPlayerScenarioStage"]={
          "scenarioID":"teatro.satzfunk-player-ear-wind.01",
          "scenarioRoute":"/teatro/scenarios/satzfunk-player/ear-wind/",
          "status":"WLAN-CANDIDATE-PLAYER-ROUTE-AND-BOOK-STAGED-LIVE-ACCEPTANCE-PENDING",
          "publicProductionAffected":False,"releasedMediaFiles":[{
            "path":path,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
            "publicReleaseAuthorized":authorized,
            "publicSource":"https://satzfunk.fountain.coach/media/bandcamp-20261024/shaders/40479.mp4",
            "sourceRepository":"Fountain-Coach/Satzfunk"}]}
        (root/"source-lock.json").write_text(json.dumps(lock))
        return path

    def test_accepts_only_exact_public_player_media_in_teatro_namespace(self):
        root,lock=self.make_root();path=self.media(root,lock)
        self.assertEqual(server.inspect(root)["teatroSatzfunkPlayerScenarioStage"]["releasedMediaFiles"][0]["path"],path)

    def test_rejects_media_without_source_lock_authorization(self):
        root,lock=self.make_root()
        p=root/"teatro/media/track.mp4";p.parent.mkdir(parents=True);p.write_bytes(b"unlisted")
        with self.assertRaisesRegex(RuntimeError,"Unexpected MP4"):
            server.inspect(root)

    def test_rejects_false_public_rights_and_invalid_path(self):
        root,lock=self.make_root();self.media(root,lock,authorized=False)
        with self.assertRaisesRegex(RuntimeError,"released-media entry"):
            server.inspect(root)
        root,lock=self.make_root();self.media(root,lock)
        lock["teatroSatzfunkPlayerScenarioStage"]["releasedMediaFiles"][0]["path"]="estate/track.mp4"
        (root/"source-lock.json").write_text(json.dumps(lock))
        with self.assertRaisesRegex(RuntimeError,"released-media entry"):
            server.inspect(root)

    def test_rejects_bytes_or_digest_drift(self):
        root,lock=self.make_root();self.media(root,lock)
        lock["teatroSatzfunkPlayerScenarioStage"]["releasedMediaFiles"][0]["bytes"]+=1
        (root/"source-lock.json").write_text(json.dumps(lock))
        with self.assertRaisesRegex(RuntimeError,"media bytes mismatch"):
            server.inspect(root)

if __name__=="__main__":unittest.main()
