#!/usr/bin/env python3
"""Verify Stage 2 recovery source discovery without accessing runtime secrets.

'build' inspects a pinned local *source repository* commit (not live host data)
and writes a public read-only contract summary.
'verify' checks the frozen evidence offline without source/host access.
"""
from pathlib import Path
import hashlib, json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"recovery/state"
SOURCE=DIR/"operational-discovery.json"
STATE=DIR/"state-manifest.json"
RESULT=DIR/"operational-readiness.json"
REPORT=DIR/"OPERATIONAL-DISCOVERY.md"
REVISION="aed7843e4f7780074885eb4e496939428013cd17"
CANDIDATES={
"authoritative-fountainstore-instance","store-receipts-and-publication-state",
"private-media-and-attachment-custody","reframe-private-project-and-personal-state",
"owner-native-secret-custody","writing-domain-authorization-runtime",
"independent-backup-destination"}
FORBIDDEN_VALUES=[
r"-----BEGIN\s+[A-Z ]*PRIVATE KEY-----",
r"\bgh[pousr]_[a-zA-Z0-9]{20,}\b",r"\bgithub_pat_[a-zA-Z0-9_]{20,}\b",
r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
r"\b(?:CF_API_TOKEN|HETZNER_API_TOKEN|SECRETSTORE_PASSWORD)\s*=\s*[^\s\"']+"
]
PUBLIC_KEYS={"schema","observedAt","status","scope","ownerDecision","stateManifest",
"productionInstanceInventoryAccepted","liveSourceAuthorityVerified","secretStoreAccessed",
"privateRecordsRead","privateFilePathsRecorded","hostRuntimeProbeAdmitted",
"discoveryAuthorityStatus","sourceInspection","sourceCandidateClasses",
"nativeInventoryReceipt","verifiedLiveInstanceCount","verifiedIndependentPrivateBackupCount",
"stage2Gate","nextPermittedOperation","prohibitedActions"}
class DiscoveryError(ValueError):pass
def refuse(message):raise DiscoveryError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def validate(data):
    if not isinstance(data,dict) or set(data)!=PUBLIC_KEYS or data["schema"]!="fountain.estate.operational-discovery.v1":
        refuse("Unrecognized operational discovery record")
    if data["status"]!="DECLARED_SOURCE_CAPABILITIES_ONLY" or data["stage2Gate"]!="BLOCKED_NO_NATIVE_AUTHORITY_ATTESTATION":
        refuse("Public source inspection cannot establish live operational readiness")
    if data["discoveryAuthorityStatus"]!="NATIVE_OWNER_SESSION_NOT_ESTABLISHED":
        refuse("Invalid owner authority claim")
    if data["ownerDecision"]!="docs/decisions/003-owner-continuity-golden-key-recovery.md" or data["stateManifest"]!="recovery/state/state-manifest.json":
        refuse("Wrong source decision binding")
    false_flags=("productionInstanceInventoryAccepted","liveSourceAuthorityVerified",
       "secretStoreAccessed","privateRecordsRead","privateFilePathsRecorded","hostRuntimeProbeAdmitted")
    if any(data[x] is not False for x in false_flags):refuse("Unproved operational or private access claimed")
    if data["nativeInventoryReceipt"] is not None:refuse("Unsigned/unverified native inventory receipt")
    if data["verifiedLiveInstanceCount"]!=0 or data["verifiedIndependentPrivateBackupCount"]!=0:
        refuse("Unverified runtime or backup count")
    src=data["sourceInspection"]
    if not isinstance(src,dict) or set(src)!={"component","sourceRevision","revisionContext","declarations"}:
        refuse("Invalid source contract witness")
    if src["component"]!="Fountain-Coach/Fountain-Store" or src["sourceRevision"]!=REVISION:
        refuse("Unpinned/unknown source tree")
    declarations=src["declarations"]
    if not isinstance(declarations,list) or len(declarations)!=2:
        refuse("Incomplete Store source API evidence")
    expected={
      "store-backup-api":("Sources/FountainStore/Store.swift",{"createBackup","listBackups","restoreBackup"}),
      "recovery-projection-kernel":("Sources/FountainStoreRecoveryKit/FountainStoreRecoveryKit.swift",
       {"FountainStoreRecoveryProjector","RecoveryClassification","RecoveryManifest"})}
    if {x["kind"] for x in declarations}!=set(expected):refuse("Invalid declared source API set")
    for entry in declarations:
        if set(entry)!={"kind","relativePath","symbols","observedImplementation","offHostBackupProven"}:
            refuse("Unexpected source evidence field")
        path,symbols=expected[entry["kind"]]
        if entry["relativePath"]!=path or set(entry["symbols"])!=symbols or len(entry["symbols"])!=len(symbols):
            refuse("Source API contract mismatches")
        if entry["offHostBackupProven"] is not False:refuse("Local Store API is not off-site recovery")
    if len(data["sourceCandidateClasses"])!=len(CANDIDATES) or {c["id"] for c in data["sourceCandidateClasses"]}!=CANDIDATES:
        refuse("Missing or duplicate operational source candidate")
    for row in data["sourceCandidateClasses"]:
        if set(row)!={"id","component","requiredNativeCapability","operationalDiscoveryStatus","redactedReceipt"}:
            refuse("Unexpected source candidate fields")
        if row["operationalDiscoveryStatus"]!="NOT_OBSERVED" or row["redactedReceipt"] is not None:
            refuse("Source metadata cannot forge live inventory evidence")
        if not isinstance(row["component"],str) or not row["component"].startswith("Fountain-Coach/"):
            refuse("Unknown candidate component")
        if not isinstance(row["requiredNativeCapability"],str) or not row["requiredNativeCapability"].strip():
            refuse("Missing native inventory capability")
    if not isinstance(data["prohibitedActions"],list) or "read-secretstore-values" not in data["prohibitedActions"]:
        refuse("Required secret access guard missing")
    encoded=json.dumps(data,sort_keys=True)
    if any(re.search(pattern,encoded) for pattern in FORBIDDEN_VALUES):
        refuse("Secret-like material in public operational report")
    if any(k in encoded for k in ('"privateKey":','"accessToken":','"userData":','"hostPrivatePath":')):
        refuse("Protected payload embedded in source discovery")
    return data
def source_verify(data):
    # Inspect only committed source code. This is *not* host process enumeration.
    source=ROOT.parents[1]/"Fountain-Store-authority-fix"
    if not (source/".git").exists():refuse("Pinned source checkout unavailable for rebuild")
    for item in data["sourceInspection"]["declarations"]:
        out=subprocess.run(["git","show",REVISION+":"+item["relativePath"]],
             cwd=source,capture_output=True)
        if out.returncode:refuse("Pinned Git source path missing "+item["relativePath"])
        code=out.stdout.decode("utf8")
        if any(sym not in code for sym in item["symbols"]):
            refuse("Expected recovery interface absent at pinned source revision")
        if item["kind"]=="store-backup-api":
            if 'options.path.appendingPathComponent("backups")' not in code:
                refuse("Store backup storage failure-domain assumption stale")
        if item["kind"]=="recovery-projection-kernel":
            if "authorityCapability" not in code or "unknownClassification" not in code:
                refuse("Recovery classification exclusion contract missing")
    return True
def readiness(data):
    validate(data)
    state=json.loads(STATE.read_text())
    if len(state["entries"])!=16 or state["privateStoresInspected"] is not False:
        refuse("Stage 1 evidence untrusted")
    return dict(schema="fountain.estate.operational-readiness.v1",
        discoveredSourceContractSHA256=sha(SOURCE.read_bytes()),
        stateManifestSHA256=sha(STATE.read_bytes()),
        stage="SOURCE_API_DISCOVERY_ONLY",
        status="BLOCKED_NO_NATIVE_OWNER_AUTHORITY",
        sourceComponent=data["sourceInspection"]["component"],
        inspectedSourceRevision=data["sourceInspection"]["sourceRevision"],
        sourceAPIsConfirmed=len(data["sourceInspection"]["declarations"]),
        candidateOperationalTargets=len(data["sourceCandidateClasses"]),
        authenticatedNativeInventoryReceipts=0,verifiedLiveStoreInstances=0,
        verifiedIndependentPrivateBackups=0,
        ownerTrustRecoveryAccepted=False,
        productionDataInspected=False,secretStoreAccessed=False,
        unverifiedClaimsAreOperationalProof=False,
        nextBoundary="Owner-enrolled read-only native inventory with independently verifiable redacted terminal receipt")
def human(data,result):
    lines=["# Stage 2 — Operational state discovery boundary","",
      "**Status: BLOCKED — no established native owner authorization or actual production Store inventory.**","",
      "This is a safe, read-only inspection of *pinned source APIs*, not a privileged scan of current processes or the Store filesystem. A protected machine-level service inventory was not admitted. No service configuration, credential, private record, backup or signing key was read.","",
      "## Verified source contracts","",
      "| Source contract | Owning repository | Pinned source path | Finding |",
      "|---|---|---|---|"]
    for row in data["sourceInspection"]["declarations"]:
        lines.append("| "+row["kind"]+" | Fountain-Coach/Fountain-Store | "+row["relativePath"]+
          " | "+row["observedImplementation"]+" |")
    lines+=["","**Important:** The Store's createBackup method writes into a 'backups' child of its own Store directory. This is a local backup mechanism, not evidence of independent encrypted off-host custody. The RecoveryKit's projector is pure and requires an authority-supplied document set; it does not discover an operational Store.","",
      "## Still-unverified operational target classes","",
      "| Candidate | Component authority | Actual live instance |",
      "|---|---|---|"]
    for row in data["sourceCandidateClasses"]:
        lines.append("| "+row["id"]+" | "+row["component"]+" | "+row["operationalDiscoveryStatus"]+" |")
    lines+=["","## Mandatory next acceptance boundary","",
      "1. Identify one exact operational FountainStore source through a previously enrolled native host/service adapter with bounded owner authorization.",
      "2. Record metadata only: source authority class, schema/version, declared classification scope, source sequence, count of eligible and omitted categories, typed read-only result, opaque evidence digest and independent verification. The signed/protected full receipt stays with its legitimate authority; the Estate accepts only a redacted, authenticated summary.",
      "3. Fail closed if the authority is stale, target is unknown, records are unclassified, inventory is partial, or the signed receipt cannot be independently verified.",
      "4. The off-host encrypted backup, clean-room restoration, Golden Key lost-root recovery and actual authorized publication require **separate** evidence and approvals. None follows from this source API audit.",
      "",
      "## Verification","",
      "Run npm run recovery:operational:verify for offline evidence reconciliation; npm run recovery:operational:test for synthetic fail-closed tests. Source implementation checking is restricted to pinned local Git code during npm run recovery:operational:build. No live machine interaction, private Store scan or network request is part of either test.",
      ""]
    return "\n".join(lines)
def execute(action):
    obj=validate(json.loads(SOURCE.read_text()))
    if action=="build":source_verify(obj)
    output=readiness(obj)
    encoded=json.dumps(output,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    docs=human(obj,output)
    if action=="build":
        RESULT.write_text(encoded);REPORT.write_text(docs)
    else:
        if RESULT.read_text()!=encoded or REPORT.read_text()!=docs:
            refuse("Stale/tampered operational readiness evidence")
    print("OPERATIONAL_SOURCE_"+action.upper(),
      output["sourceAPIsConfirmed"],"source APIs;",
      output["candidateOperationalTargets"],"candidate classes;",
      output["verifiedLiveStoreInstances"],"live instances VERIFIED;",
      output["status"])
if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("build","verify"):
        raise SystemExit("usage: verify-operational-discovery.py build|verify")
    execute(sys.argv[1])
