#!/usr/bin/env bash
# Atomic activation of the exact Client-Centered v177 onto existing WLAN 8200.
# Keeps the v176 drop-in and release for immediate rollback.
set -euo pipefail
base=/home/benedikt/estate-shell-acceptance-staging
service=fountain-shell-acceptance-preview.service
prev=shared-shell-20261109-v176-four-domain-c265c57
next=shared-shell-20261110-v177-client-centered-bd8f6d9
before="$base/releases/$prev"
after="$base/releases/$next"
wrapper="$base/candidates/serve_client_centered_v177.py"
unit="$HOME/.config/systemd/user/$service.d"
override="$unit/91-client-centered-v177.conf"
receipt="$base/candidates/client-centered-v177-bd8f6d9-activation.txt"
status=not-activated
armed=0
rollback(){
  if [[ "$status" == activated || "$armed" != 1 ]];then return;fi
  echo "ROLLBACK_TO_V176" | tee -a "$receipt"
  ln -s "$before" "$base/current.rollback.tmp"
  mv -Tf "$base/current.rollback.tmp" "$base/current"
  rm -f "$override"
  systemctl --user daemon-reload
  systemctl --user restart "$service"
}
trap rollback EXIT

[[ "$(readlink -f "$base/current")" == "$before" ]] || { echo PREDECESSOR_DRIFT; exit 1; }
[[ "$(sha256sum "$before/source-lock.json" | cut -d ' ' -f 1)" == 8029b4c0c2ebe21ae608f42ad51bacdd779124e72a74dcc22b1ca7ba57cd5a2b ]] || exit 1
[[ "$(sha256sum "$after/source-lock.json" | cut -d ' ' -f 1)" == f67e3dd27d08d73e96f04e6c67a08983bb6c87145126f45c62f924a3fea4c688 ]] || exit 1
[[ "$(sha256sum "$wrapper" | cut -d ' ' -f 1)" == 48ef30117aaa4ea0c5c3fd4bed23dd7f96ebcb62caee0d417a79cb12d768cec0 ]] || exit 1
[[ -f "$unit/90-four-domain-v176.conf" ]] || { echo PARENT_STAGE_OVERRIDE_MISSING; exit 1; }
[[ ! -e "$override" ]] || { echo UNEXPECTED_V177_OVERRIDE; exit 1; }
systemctl --user is-active --quiet "$service"
mkdir -p "$unit"
armed=1
printf '%s\n' "[Service]" "ExecStart=" "ExecStart=/usr/bin/python3 $wrapper --root $base/current --bind 192.168.8.50 --port 8200" > "$unit/.client-centered-v177.new"
mv -T "$unit/.client-centered-v177.new" "$override"
ln -s "$after" "$base/current.v177.next"
mv -Tf "$base/current.v177.next" "$base/current"
systemctl --user daemon-reload
systemctl --user restart "$service"
ready=0
for attempt in $(seq 1 165);do
  if curl -fsS --max-time 3 -o /dev/null 'http://192.168.8.50:8200/estate/read/essay--client-centered/' 2>/dev/null;then
    ready=1;break
  fi
  if ! systemctl --user is-active --quiet "$service";then
    echo "STAGING_SERVICE_EXIT" | tee -a "$receipt";break
  fi
  sleep 1
done
[[ "$ready" == 1 ]] || { echo STAGE_URL_TIMEOUT | tee -a "$receipt";exit 1; }
for route in \
  /estate/ /status/ /governance/ /teatro/ \
  /review-20261109/access/ /review-20261109/status/ /review-20261109/fcis/ \
  /estate/read/essay--client-centered/ \
  /estate/read/essay--client-centered/assets/images/client-centered-positions.svg \
  /estate/read/essay--client-centered/assets/images/client-centered-open-method.svg \
  /estate/read/essay--client-centered/edition-manifest.json;do
  curl -fsS --max-time 15 -o /dev/null "http://192.168.8.50:8200$route"
  printf 'ACCEPTED %s\n' "$route" | tee -a "$receipt"
done
[[ "$(readlink -f "$base/current")" == "$after" ]] || exit 1
systemctl --user is-active --quiet "$service"
systemctl --user show -p ExecStart "$service" | grep -q 'serve_client_centered_v177.py'
manifestsha=$(curl -fsS --max-time 12 http://192.168.8.50:8200/estate/read/essay--client-centered/edition-manifest.json | sha256sum | cut -d ' ' -f 1)
[[ "$manifestsha" == "$(sha256sum "$after/estate/read/essay--client-centered/edition-manifest.json" | cut -d ' ' -f 1)" ]] || exit 1
code=$(curl -sS --max-time 8 --path-as-is -o /dev/null -w '%{http_code}' 'http://192.168.8.50:8200/estate/read/essay--client-centered/../source-lock.json')
[[ "$code" == 403 ]] || { echo TRAVERSAL_REFUSAL_MISSING;exit 1; }
code=$(curl -sS --max-time 8 -o /dev/null -w '%{http_code}' 'http://192.168.8.50:8200/source-lock.json')
[[ "$code" == 404 ]] || { echo SOURCE_LOCK_LEAK;exit 1; }
status=activated
echo 'V177_CLIENT_CENTERED_CANONICAL_WLAN_ACCEPTED' | tee -a "$receipt"
trap - EXIT
