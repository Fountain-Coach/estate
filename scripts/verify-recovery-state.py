#!/usr/bin/env python3
"""Offline Fountain Coach state-recovery manifest and fail-closed DoD contract.

No private data, live Store, SecretStore, SSH, network or registrar access.
"""
import copy, hashlib, json, re, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"recovery/state/state-manifest.json"
READINESS=ROOT/"recovery/state/readiness.json"
REPORT=ROOT/"recovery/state/README.md"
EXPECTED={
"public-estate-static-artifacts","estate-owned-source-and-manifests",
"fountainstore-durable-institutional-records","store-publication-and-scenario-receipts",
"store-unpublished-personal-context","unpublished-manuscripts-and-editorial-drafts",
"media-attachment-payloads-and-digests","owner-signing-root-and-golden-key",
"host-and-device-enrollment-authority","secretstore-backend-protected-values",
"fountainauthkit-domain-grants-and-state","oauth-signing-keys-and-external-tokens",
"registrar-dns-and-provider-account-control","github-organization-owner-and-release-custody",
"successor-transfer-and-legal-owner-intent","operational-client-runtime-and-integrations"}
FIELDS={"id","classification","authority","ownerRepo","backupPolicy","discoveryState",
"restoreMethod","distribution","readiness","risk","evidenceRefs","requiredFor",
"liveInstanceReceipt","independentBackupReceipt","cleanRoomRestoreReceipt"}
CLASS={"institutional-knowledge","personal-context","authority-capability"}
POLICY={"public-digest-pinned","git-history-and-pinned-release","typed-private-snapshot-offsite",
"purpose-limited-encrypted-offsite-or-omit","rights-classified-private-asset-backup",
"never-open-native-custody","encrypted-partitioned-state-backup","restricted-succession-record-offsite",
"per-service-classification-needed"}
DISTRIBUTION={"public","protected","custodial","mixed","undetermined"}
STATUS={"UNVERIFIED","STATIC_600_BYTES_VERIFIED","BLOCKED_NO_ACCEPTED_LOST_ROOT_PROTOCOL"}
MUST_REMAIN_FALSE=("operationalInstancesFullyInventoried","privateStoresInspected",
"privateBackupsVerified","goldenKeyLostRootRecoveryAccepted",
"cleanRoomPrivateRestoreAccepted","productionPromotionAuthorized","credentialsIncluded")
RECEIPTS=("liveInstanceReceipt","independentBackupReceipt","cleanRoomRestoreReceipt")
FORBIDDEN_KEYS={"privateKey","privateKeyBytes","secretValue","accessToken","refreshToken",
"password","sshPrivateKey","rawStoreRecord","personalPayload","recoveryToken","credentialValue","apiKeyValue"}
FORBIDDEN_VALUES=[
r"-----BEGIN\s+[A-Z ]*PRIVATE KEY-----",
r"\bgh[pousr]_[a-zA-Z0-9]{20,}\b",r"\bgithub_pat_[a-zA-Z0-9_]{20,}\b",
r"\bsk-[a-zA-Z0-9]{20,}\b",r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
r"\b(?:CF_API_TOKEN|HETZNER_API_TOKEN|SECRETSTORE_PASSWORD)\s*=\s*[^\s\"']+"]
class ContractError(ValueError): pass
def refuse(message): raise ContractError(message)
def sha(data): return hashlib.sha256(data).hexdigest()
def load(): return json.loads(MANIFEST.read_bytes())
def validate(data):
    if not isinstance(data,dict) or data.get("schema")!="fountain.estate.recovery-state-manifest.v1":
        refuse("Invalid recovery state manifest schema")
    if data.get("authority")!="Fountain-Coach/estate" or data.get("ownerDecision")!="docs/decisions/003-owner-continuity-golden-key-recovery.md":
        refuse("Missing owner decision/manifest authority")
    if any(data.get(field) is not False for field in MUST_REMAIN_FALSE):
        refuse("Metadata cannot claim production, private recovery or owner trust")
    proof=data.get("publicStaticEvidence")
    if not isinstance(proof,dict) or proof.get("publicGETResponsesVerified")!=600 or proof.get("publicHostnames")!=9 or proof.get("scope")!="bounded public static published files only":
        refuse("Static public evidence incorrect or broadened")
    rows=data.get("entries")
    if not isinstance(rows,list) or any(not isinstance(x,dict) for x in rows):
        refuse("Recovery classes missing")
    identities=[x.get("id") for x in rows]
    if len(rows)!=len(EXPECTED) or set(identities)!=EXPECTED:
        refuse("Missing or duplicate required class")
    for r in rows:
        ident=r["id"]
        if set(r)!=FIELDS:refuse(ident+": class fields changed")
        for field in ("authority","ownerRepo","backupPolicy","discoveryState","restoreMethod","risk","requiredFor"):
            if not isinstance(r.get(field),str) or not r[field].strip():
                refuse(ident+": missing "+field)
        if r["classification"] not in CLASS or r["backupPolicy"] not in POLICY or r["distribution"] not in DISTRIBUTION or r["readiness"] not in STATUS:
            refuse(ident+": unknown classification/policy/status")
        if not r["ownerRepo"].startswith("Fountain-Coach/"):refuse("Owner component missing "+ident)
        if not isinstance(r["evidenceRefs"],list) or not r["evidenceRefs"] or not all(isinstance(x,str) and x.strip() for x in r["evidenceRefs"]):
            refuse(ident+": evidence references missing")
        if any(r[key] is not None for key in RECEIPTS):
            refuse(ident+": unreviewed private receipt in open manifest")
        if r["classification"]=="authority-capability" and (r["backupPolicy"]!="never-open-native-custody" or r["distribution"]!="custodial"):
            refuse(ident+": forbidden open authority-capability export")
        if r["classification"]=="personal-context" and (r["distribution"]=="public" or r["backupPolicy"] not in {"purpose-limited-encrypted-offsite-or-omit","encrypted-partitioned-state-backup"}):
            refuse(ident+": invalid personal-context eligibility")
        if r["readiness"]=="STATIC_600_BYTES_VERIFIED" and ident!="public-estate-static-artifacts":
            refuse(ident+": cannot inherit static proof")
        if r["readiness"]=="BLOCKED_NO_ACCEPTED_LOST_ROOT_PROTOCOL" and ident!="owner-signing-root-and-golden-key":
            refuse(ident+": invalid lost-root claim")
        if any(key in r for key in FORBIDDEN_KEYS):refuse(ident+": secret payload key")
    index={r["id"]:r for r in rows}
    if index["owner-signing-root-and-golden-key"]["readiness"]!="BLOCKED_NO_ACCEPTED_LOST_ROOT_PROTOCOL":
        refuse("Lost owner root has no accepted recovery")
    if index["public-estate-static-artifacts"]["readiness"]!="STATIC_600_BYTES_VERIFIED":
        refuse("Previously verified bounded static proof missing")
    if any(key in data for key in FORBIDDEN_KEYS):refuse("Top-level credential material key")
    serialized=json.dumps(data,sort_keys=True)
    if any(re.search(p,serialized) for p in FORBIDDEN_VALUES):
        refuse("Secret-shaped material in public manifest")
    return data
def derive(data,manifest_sha):
    validate(data)
    gates=[
      ("complete-operational-state-inventory","No independent inventory of all actual production instances"),
      ("independent-private-backup-custody","No verified encrypted off-host backup, retrieval and integrity receipt"),
      ("golden-key-and-successor-authority","FCIS 139 lacks accepted lost-root recovery; successor authority unproved"),
      ("clean-room-private-store-restoration","No authenticated restore of actual protected Store state and media"),
      ("authorized-publication-continuity","No authorized new publication from restored private authority with independent readback"),
      ("repeatable-timed-owner-accepted-proof","No two accepted cold drills, measured RTO/RPO, rollback and owner receipt")
    ]
    return {"schema":"fountain.estate.recovery-continuity-readiness.v1",
       "manifestSHA256":manifest_sha,
       "stage":"STATE_MANIFEST_METADATA_ONLY",
       "overall":"NOT_READY_FOR_PRIVATE_OWNER_CONTINUITY",
       "publicObservedStaticByteRecovery":"PASS_BOUNDED",
       "privateStoreRecoveryAccepted":False,"lostOwnerKeyRecoveryAccepted":False,
       "successorAuthorityAccepted":False,"productionPromotionAuthorized":False,
       "stateClassCount":len(data["entries"]),
       "classes":dict(sorted(Counter(x["classification"] for x in data["entries"]).items())),
       "evidenceStates":dict(sorted(Counter(x["readiness"] for x in data["entries"]).items())),
       "operationalInstanceReceiptCount":0,"independentPrivateBackupReceiptCount":0,
       "cleanRoomPrivateRestoreReceiptCount":0,
       "acceptance":[{"id":key,"state":"BLOCKED","reason":reason} for key,reason in gates]}
def human(data,readiness):
    lines=["# Recovery State Manifest — Fountain Coach","",
      "**Private owner continuity: NOT READY.** The existing 600/600 public static recovery proof remains valid but does not attest any private recovery.","",
      "This manifest catalogs 16 types of state, NOT an authenticated inventory of installed production instances. It contains no private Store record, password, key, user information, or secret. The evidence references point to owner components and governance, not live backup receipts.","",
      "| State class | FCIS 118 classification | Authority / owner component | Recovery assessment |",
      "|---|---|---|---|"]
    for row in data["entries"]:
        lines.append("| "+row["id"]+" | "+row["classification"]+" | "+row["ownerRepo"]+" | "+row["readiness"]+" |")
    lines+=["","## Programme Definition of Done gates","",
            "| Acceptance gate | State | Required evidence |","|---|---|---|"]
    for gate in readiness["acceptance"]:
        lines.append("| "+gate["id"]+" | "+gate["state"]+" | "+gate["reason"]+" |")
    lines+=["","## Next governed action","",
       "Obtain an authorized **read-only**, redacted inventory of actual live Store instance identities, sources of truth, protected attachment classes, and eligibility/omission policy. Do not read credentials, export raw Store files, or infer production state from development fixtures. Each operational dependency must be traced to its own custody authority.",
       "",
       "A later governed adapter may write a private typed backup receipt outside this public repository. This Stage 1 verifier intentionally refuses even plausible-looking receipts in its open manifest.",
       "",
       "Chapter 139 has no accepted lost-root owner-recovery operation. Replacing a key or using host root is NOT a valid Golden Key restore. Chapter 143 requires one bounded owner bootstrap/session rather than repeated credential prompts.",
       "",
       "## Checks","",
       "Run npm run recovery:state:verify to prove the snapshot and derived readiness are unchanged; npm run recovery:state:test to run synthetic denial tests. Neither command contacts a live host or reads secret material.",
       ""]
    return "\n".join(lines)
def execute(mode):
    blob=MANIFEST.read_bytes()
    data=validate(json.loads(blob))
    result=derive(data,sha(blob))
    serialized=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    doc=human(data,result)
    if mode=="build":
        READINESS.write_text(serialized)
        REPORT.write_text(doc)
    elif READINESS.read_text()!=serialized or REPORT.read_text()!=doc:
        refuse("Recovery metadata or evidence report stale")
    print("RECOVERY_STATE_"+mode.upper(),len(data["entries"]),"classes",
      len(result["acceptance"]),"BLOCKED gates",result["overall"])
if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in {"build","verify"}:
        raise SystemExit("usage: verify-recovery-state.py build|verify")
    execute(sys.argv[1])
