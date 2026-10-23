import hashlib,json,tempfile,unittest
from pathlib import Path
from complete_first_reading_stage import verify
class ReadingDependencies(unittest.TestCase):
    def test_declared_missing_and_changed_book_resources_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); asset=root/'solstice/assets/book.css'
            asset.parent.mkdir(parents=True);asset.write_bytes(b'original')
            item={'path':'solstice/assets/book.css','candidateSHA256':hashlib.sha256(b'original').hexdigest()}
            (root/'source-lock.json').write_text(json.dumps({'firstReadingDependencyWitness':{'files':[item]}}))
            self.assertEqual(verify(root),1)
            asset.unlink()
            with self.assertRaisesRegex(ValueError,'missing or changed'):verify(root)
            asset.write_bytes(b'wrong')
            with self.assertRaisesRegex(ValueError,'missing or changed'):verify(root)
if __name__=='__main__':unittest.main()
