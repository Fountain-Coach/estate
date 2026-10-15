#!/usr/bin/env python3
"""Synthetic acceptance checks for the public Recovery State Manifest schema.

Every positive check uses fictitious metadata. These tests do not open live
Store, SecretStore, SSH, credentials or the production estate.
"""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("recovery_state",ROOT/"scripts/verify-recovery-state.py")
recovery=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recovery)

class RecoveryStateSyntheticTests(unittest.TestCase):
    def setUp(self):
        self.obj=recovery.load()
    def reject(self,mutate):
        data=copy.deepcopy(self.obj)
        mutate(data)
        with self.assertRaises(recovery.ContractError):
            recovery.validate(data)
    def test_complete_safe_metadata_accepts(self):
        self.assertEqual(len(recovery.validate(copy.deepcopy(self.obj))["entries"]),16)
        report=recovery.derive(self.obj,"0"*64)
        self.assertEqual(report["overall"],"NOT_READY_FOR_PRIVATE_OWNER_CONTINUITY")
        self.assertEqual(len(report["acceptance"]),6)
        self.assertTrue(all(g["state"]=="BLOCKED" for g in report["acceptance"]))
        self.assertEqual(report["evidenceStates"]["STATIC_600_BYTES_VERIFIED"],1)
    def test_missing_state_class_fails(self):
        self.reject(lambda x:x["entries"].pop())
    def test_duplicate_state_class_fails(self):
        self.reject(lambda x:x["entries"].__setitem__(-1,copy.deepcopy(x["entries"][0])))
    def test_unknown_classification_fails(self):
        self.reject(lambda x:x["entries"][1].update(classification="unreviewed"))
    def test_public_personal_context_fails(self):
        self.reject(lambda x:next(y for y in x["entries"] if y["id"]=="store-unpublished-personal-context").update(distribution="public"))
    def test_private_authority_must_not_use_public_backup(self):
        self.reject(lambda x:next(y for y in x["entries"] if y["id"]=="owner-signing-root-and-golden-key").update(backupPolicy="public-digest-pinned"))
    def test_fake_lost_root_success_rejected(self):
        self.reject(lambda x:next(y for y in x["entries"] if y["id"]=="owner-signing-root-and-golden-key").update(readiness="STATIC_600_BYTES_VERIFIED"))
    def test_fake_private_store_static_pass_rejected(self):
        self.reject(lambda x:next(y for y in x["entries"] if y["id"]=="fountainstore-durable-institutional-records").update(readiness="STATIC_600_BYTES_VERIFIED"))
    def test_forged_backup_receipt_rejected(self):
        self.reject(lambda x:x["entries"][2].update(independentBackupReceipt="receipt:all-good"))
    def test_fake_production_authorization_rejected(self):
        self.reject(lambda x:x.update(productionPromotionAuthorized=True))
    def test_fake_inspected_secretstore_rejected(self):
        self.reject(lambda x:x.update(privateStoresInspected=True))
    def test_injected_key_bytes_rejected(self):
        self.reject(lambda x:x["entries"][7].update(privateKey="not-for-public-git"))
    def test_injected_pem_rejected(self):
        self.reject(lambda x:x["entries"][7].update(risk="-----BEGIN PRIVATE KEY----- DO NOT STORE"))
    def test_unverified_source_no_longer_static_proof(self):
        self.reject(lambda x:x["publicStaticEvidence"].update(scope="complete private and public recovery"))
    def test_missing_governance_owner_decision_fails(self):
        self.reject(lambda x:x.update(ownerDecision="unbound"))
    def test_fake_succession_acceptance_fails(self):
        self.reject(lambda x:x.update(goldenKeyLostRootRecoveryAccepted=True))
    def test_invalid_receipt_properties_not_extra_public_fields(self):
        self.reject(lambda x:x["entries"][0].update(recoveredToken="example"))
    def test_metadata_does_not_imply_clean_room_restore(self):
        result=recovery.derive(copy.deepcopy(self.obj),"f"*64)
        self.assertFalse(result["privateStoreRecoveryAccepted"])
        self.assertFalse(result["lostOwnerKeyRecoveryAccepted"])
        self.assertFalse(result["successorAuthorityAccepted"])
        self.assertFalse(result["productionPromotionAuthorized"])
        self.assertEqual(result["cleanRoomPrivateRestoreReceiptCount"],0)

if __name__=="__main__":
    unittest.main()
