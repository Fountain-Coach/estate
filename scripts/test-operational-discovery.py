#!/usr/bin/env python3
"""Synthetic refusal tests for read-only Stage 2 source discovery."""
import copy
import importlib.util
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("opdiscovery",ROOT/"scripts/verify-operational-discovery.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
class OperationalDiscoveryTests(unittest.TestCase):
    def setUp(self):
        import json
        self.obj=json.loads(module.SOURCE.read_text())
    def reject(self,change):
        data=copy.deepcopy(self.obj)
        change(data)
        with self.assertRaises(module.DiscoveryError):
            module.validate(data)
    def test_source_evidence_passes_without_claiming_live(self):
        module.validate(self.obj)
        report=module.readiness(self.obj)
        self.assertEqual(report["status"],"BLOCKED_NO_NATIVE_OWNER_AUTHORITY")
        self.assertEqual(report["sourceAPIsConfirmed"],2)
        self.assertEqual(report["candidateOperationalTargets"],7)
        self.assertFalse(report["productionDataInspected"])
    def test_fake_live_source_claim_denied(self):
        self.reject(lambda x:x.update(liveSourceAuthorityVerified=True))
    def test_fake_native_authorization_denied(self):
        self.reject(lambda x:x.update(discoveryAuthorityStatus="OWNER_APPROVED"))
    def test_fake_completed_stage2_denied(self):
        self.reject(lambda x:x.update(stage2Gate="ACCEPTED"))
    def test_fake_store_instance_count_denied(self):
        self.reject(lambda x:x.update(verifiedLiveInstanceCount=1))
    def test_fake_private_backup_count_denied(self):
        self.reject(lambda x:x.update(verifiedIndependentPrivateBackupCount=1))
    def test_fake_native_receipt_denied(self):
        self.reject(lambda x:x.update(nativeInventoryReceipt={"issuer":"LLM","approved":True}))
    def test_fake_candidate_receipt_denied(self):
        self.reject(lambda x:x["sourceCandidateClasses"][0].update(redactedReceipt="mock"))
    def test_live_candidate_accepted_denied(self):
        self.reject(lambda x:x["sourceCandidateClasses"][0].update(operationalDiscoveryStatus="VERIFIED"))
    def test_missing_target_denied(self):
        self.reject(lambda x:x["sourceCandidateClasses"].pop())
    def test_duplicate_target_denied(self):
        self.reject(lambda x:x["sourceCandidateClasses"].append(copy.deepcopy(x["sourceCandidateClasses"][0])))
    def test_private_records_read_denied(self):
        self.reject(lambda x:x.update(privateRecordsRead=True))
    def test_private_path_recorded_denied(self):
        self.reject(lambda x:x.update(privateFilePathsRecorded=True))
    def test_secretstore_read_denied(self):
        self.reject(lambda x:x.update(secretStoreAccessed=True))
    def test_forged_offhost_backup_in_source_denied(self):
        self.reject(lambda x:x["sourceInspection"]["declarations"][0].update(offHostBackupProven=True))
    def test_unpinned_git_source_denied(self):
        self.reject(lambda x:x["sourceInspection"].update(sourceRevision="0"*40))
    def test_dropped_restore_api_denied(self):
        self.reject(lambda x:x["sourceInspection"]["declarations"][0].update(symbols=["createBackup"]))
    def test_private_key_pem_denied(self):
        self.reject(lambda x:x.update(scope="-----BEGIN PRIVATE KEY----- anything"))
    def test_unapproved_extra_field_denied(self):
        self.reject(lambda x:x.update(rawStoreRecord="secret"))
    def test_unrecognized_component_denied(self):
        self.reject(lambda x:x["sourceCandidateClasses"][0].update(component="Unknown/Host"))
    def test_static_evidence_never_promotes_private_state(self):
        report=module.readiness(copy.deepcopy(self.obj))
        self.assertEqual(report["verifiedLiveStoreInstances"],0)
        self.assertEqual(report["verifiedIndependentPrivateBackups"],0)
        self.assertFalse(report["ownerTrustRecoveryAccepted"])
if __name__=="__main__":
    unittest.main()
