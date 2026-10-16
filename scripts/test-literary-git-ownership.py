#!/usr/bin/env python3
"""Negative tests for Git-owned literary identity and recovery admission."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("literary_git",
    ROOT/"scripts/verify-literary-git-ownership.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class OwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid=json.loads(module.MANIFEST.read_text())

    def test_real_registry_is_consistent(self):
        self.assertEqual(len(module.validate(copy.deepcopy(self.valid))["records"]),8)
        self.assertEqual(sum(r["sourceState"]=="GIT_OBJECT_VERIFIED_LOCAL"
                             for r in self.valid["records"]),6)

    def test_duplicate_source_identity_rejected(self):
        data=copy.deepcopy(self.valid)
        data["records"].append(copy.deepcopy(data["records"][0]))
        with self.assertRaises(module.Refusal):module.validate(data)

    def test_forged_source_hash_and_ref_rejected(self):
        for attribute,value in (
            ("ownerCommit","HEAD"),
            ("sourceSHA256","NOT_HASH"),
            ("gitBlob","00"),
            ("sourcePath","../../private-source"),
            ("sourcePath","/Users/person"),
            ("ownerRepository","unowned/repository")
        ):
            data=copy.deepcopy(self.valid)
            data["records"][0][attribute]=value
            with self.subTest(field=attribute):
                with self.assertRaises(module.Refusal):module.validate(data)

    def test_runtime_claim_cannot_be_promoted_by_git_metadata(self):
        for flag in ("completeLibraryInventory","anyFountainStoreRestored",
                     "independentCompleteStoreBackupVerified"):
            data=copy.deepcopy(self.valid)
            data[flag]=True
            with self.assertRaises(module.Refusal):module.validate(data)
        for key,value in (("publicationAdmission","PUBLISHED"),
                          ("storeRecoveryState","RESTORED")):
            data=copy.deepcopy(self.valid);data["records"][0][key]=value
            with self.assertRaises(module.Refusal):module.validate(data)

    def test_unmirrored_store_cannot_claim_git(self):
        data=copy.deepcopy(self.valid)
        data["records"][-1]["ownerRepository"]="Fountain-Coach/guessed"
        with self.assertRaises(module.Refusal):module.validate(data)

    def test_remote_recovery_refuses_unverified_corpus(self):
        with self.assertRaises(module.Refusal):
            module.github_recovery(self.valid,"reframe-ulysses","/tmp/never-write")
        with self.assertRaises(module.Refusal):
            module.github_recovery(self.valid,"unlisted-fixture","/tmp/never-write")

    def test_local_git_provenance_is_exact(self):
        self.assertEqual(module.local_verify(self.valid),6)
        data=copy.deepcopy(self.valid);data["records"][0]["sourceSHA256"]="0"*64
        with self.assertRaises(module.Refusal):module.local_verify(data)

if __name__=="__main__":unittest.main()
