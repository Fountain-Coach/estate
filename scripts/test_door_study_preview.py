"""Synthetic policy fixtures only; acoustic and rights evidence is separate."""
import importlib.util,json,hashlib,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('preview',Path(__file__).with_name('serve_shared_shell_preview.py'))
preview=importlib.util.module_from_spec(spec);spec.loader.exec_module(preview)
class StudyAdmission(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  for rel in ['estate/index.html','teatro/index.html','solstice/editions/first-reading/index.html','assets/estate-shell.css','assets/estate-shell-logo.png','assets/estate-shell-state.js']:
   p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
  self.meta={'status':'WLAN-PREVIEW-NOT-PUBLIC','templateVersion':'fountain.estate.shell.v2-editorial-20261022','archiveMediaCopied':False,'authorPublished':False,'releaseReceipt':None,'sites':{'estate':{},'teatro':{},'solstice':{}}}
  self.save()
 def tearDown(self):self.tmp.cleanup()
 def save(self):(self.root/'source-lock.json').write_text(json.dumps(self.meta))
 def declared(self):
  p=self.root/'estate/essays/the-door-is-a-score/assets/present.wav';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'synthetic policy fixture')
  self.meta['doorScoreEssayStage']={'sourceOwner':'Fountain-Coach/fountain.coach','sourceCommit':'a'*40,'scope':'owner-WLAN-only','publicProductionAffected':False,'sourceLicense':'CC0-1.0','sourceURL':'https://opengameart.org/content/100-cc0-metal-and-wood-sfx','permittedWAVFiles':[{'path':p.relative_to(self.root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'sourceKind':'authored-sound-study'}]};self.save();return p
 def test_prior_media_free_contract(self):preview.inspect(self.root)
 def test_declared_study(self):self.declared();preview.inspect(self.root)
 def test_undeclared_wav(self):
  (self.root/'unlisted.wav').write_bytes(b'fixture')
  with self.assertRaises(RuntimeError):preview.inspect(self.root)
 def test_changed_bytes(self):
  self.declared().write_bytes(b'changed')
  with self.assertRaises(RuntimeError):preview.inspect(self.root)
 def test_foreign_owner(self):
  self.declared();self.meta['doorScoreEssayStage']['sourceOwner']='other/owner';self.save()
  with self.assertRaises(RuntimeError):preview.inspect(self.root)
 def test_outside_declared_route(self):
  self.declared();self.meta['doorScoreEssayStage']['permittedWAVFiles'][0]['path']='estate/elsewhere.wav';self.save()
  with self.assertRaises(RuntimeError):preview.inspect(self.root)
if __name__=='__main__':unittest.main()
