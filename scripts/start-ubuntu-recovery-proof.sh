#!/bin/sh
# Execute ONLY on designated Ubuntu recovery host.
# Isolated proof on loopback port 18480; no production DNS/Caddy/service mutation.
set -eu
ROOT=/home/benedikt/fountain-recovery-cold-20261015
NAME=fountain-estate-restore-20261015
ARCHIVE=release.tar.gz
EXPECTED=20232def0be2be915d608c9ea491ffbd131edb5350e3721c3d081a7086d7b444
test -f "$ROOT/$ARCHIVE" || { echo MISSING_PUBLIC_GITHUB_ARCHIVE; exit 1; }
cd "$ROOT"
printf '%s  %s\n' "$EXPECTED" "$ARCHIVE" | sha256sum -c -
if test -e payload && ! test -d payload; then
    echo RECOVERY_PAYLOAD_PATH_NOT_DIRECTORY
    exit 1
fi
if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
    echo REFUSING_TO_OVERWRITE_EXISTING_RECOVERY_CONTAINER
    exit 1
fi
if ss -ltn | grep -Eq '(^|:)18480[[:space:]]'; then
    echo RECOVERY_PORT_18480_ALREADY_IN_USE
    exit 1
fi
if ! test -d payload; then
    mkdir payload
    tar -xzf release.tar.gz -C payload --no-same-owner
fi
python3 - <<'PY'
from pathlib import Path, PurePosixPath
import hashlib
import json
import tarfile
root=Path('/home/benedikt/fountain-recovery-cold-20261015')
target=root/'payload'
with tarfile.open(root/'release.tar.gz',mode='r:gz') as t:
    expected=set()
    for item in t:
        p=PurePosixPath(item.name)
        if item.name.startswith('/') or any(part in ('.','..') for part in p.parts):
            raise RuntimeError('Invalid archive path')
        if not item.isfile():
            raise RuntimeError('Only regular files admitted')
        expected.add(str(p))
    actual={str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()}
    if expected!=actual:
        raise RuntimeError('Extracted recovery tree differs from archive')
manifest=json.loads((target/'manifest.json').read_text())
if manifest['releaseAdmitted'] or manifest['authorizedForProduction']:
    raise RuntimeError('Snapshot falsely granted release authority')
if len(manifest['hostnames'])!=9 or len(manifest['records'])!=600:
    raise RuntimeError('Manifest missing published URLs')
count=0
for row in manifest['records']:
    path=target/row['bundlePath']
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=row['sha256'] or len(data)!=row['bytes']:
        raise RuntimeError('Published byte check failed '+row['url'])
    count+=1
print('RECOVERY_PAYLOAD_VALIDATED',count,'public HTTP 200 responses',
     manifest['uniqueFilesOnDisk'],'unique files',flush=True)
PY
docker run --rm --mount type=bind,source="$ROOT/payload",target=/srv/recovery,readonly \
    caddy:2.10.2 caddy validate --config /srv/recovery/Caddyfile --adapter caddyfile
docker run --detach --name "$NAME" --restart no \
    --publish 127.0.0.1:18480:18480 \
    --mount type=bind,source="$ROOT/payload",target=/srv/recovery,readonly \
    caddy:2.10.2 caddy run --config /srv/recovery/Caddyfile --adapter caddyfile
docker inspect --format '{{json .HostConfig.PortBindings}}' "$NAME"
printf 'ISOLATED_UBUNTU_RECOVERY_ORIGIN_STARTED\n'
