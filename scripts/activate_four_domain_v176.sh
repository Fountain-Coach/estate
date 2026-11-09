#!/usr/bin/env bash
# Source-bound v176 admission at the existing, registered WLAN service.
# Do not create a second environment, alter DNS/Caddy, or publish externally.
set -euo pipefail
base=/home/benedikt/estate-shell-acceptance-staging
service=fountain-shell-acceptance-preview.service
prev=shared-shell-20261108-v175-governance161-shell-1486f09
next=shared-shell-20261109-v176-four-domain-c265c57
current="$base/current"
before="$base/releases/$prev"
after="$base/releases/$next"
wrapper="$base/candidates/serve_four_domain_v176.py"
unit="$HOME/.config/systemd/user/$service.d"
dropin="$unit/90-four-domain-v176.conf"
receipt="$base/candidates/four-domain-v176-c265c57-activation.txt"
status=not-activated
armed=0
rollback() {
  if [[ "$status" == activated || "$armed" != 1 ]]; then return; fi
  echo "ROLLBACK_TO_V175" | tee -a "$receipt"
  ln -s "$before" "$base/current.rollback.tmp"
  mv -Tf "$base/current.rollback.tmp" "$current"
  rm -f "$dropin"
  systemctl --user daemon-reload
  systemctl --user restart "$service"
}
trap rollback EXIT

[[ "$(readlink -f "$current")" == "$before" ]] || { echo "PREDECESSOR_DRIFT"; exit 1; }
[[ "$(sha256sum "$before/source-lock.json" | cut -d ' ' -f 1)" == d546d92aab66ebdd2615d6e24660461ab759866d6f0f19de290c40f0559edf1a ]] || exit 1
[[ "$(sha256sum "$after/source-lock.json" | cut -d ' ' -f 1)" == 8029b4c0c2ebe21ae608f42ad51bacdd779124e72a74dcc22b1ca7ba57cd5a2b ]] || exit 1
[[ "$(sha256sum "$wrapper" | cut -d ' ' -f 1)" == a27ac8d6567d83eb6d3cc86dd844135d3c1726067fefa1596fb0dec3f2217913 ]] || exit 1
[[ ! -e "$dropin" ]] || { echo "UNEXPECTED_EXISTING_OVERRIDE"; exit 1; }
systemctl --user is-active --quiet "$service"
armed=1
mkdir -p "$unit"
printf '%s\n' "[Service]" "ExecStart=" "ExecStart=/usr/bin/python3 $wrapper --root $current --bind 192.168.8.50 --port 8200" > "$unit/.four-domain-v176.new"
mv -T "$unit/.four-domain-v176.new" "$dropin"
ln -s "$after" "$base/current.v176.next"
mv -Tf "$base/current.v176.next" "$current"
systemctl --user daemon-reload
systemctl --user restart "$service"

ready=0
for attempt in $(seq 1 160); do
  if curl -fsS --max-time 2 -o /dev/null "http://192.168.8.50:8200/review-20261109/domain-map.json" 2>/dev/null; then
    ready=1
    break
  fi
  if ! systemctl --user is-active --quiet "$service"; then
    echo "SERVICE_EXIT_BEFORE_ACCEPTANCE"
    break
  fi
  sleep 1
done
[[ "$ready" == 1 ]] || { echo "CANONICAL_STAGING_READBACK_TIMEOUT"; exit 1; }
for route in \
  /estate/ /status/ /governance/ /teatro/ \
  /review-20261109/access/ /review-20261109/status/ \
  /review-20261109/fcis/ /review-20261109/domain-map.json \
  /review-20261109/access/public-facts.json \
  /review-20261109/access/edition-manifest.json; do
  curl -fsS --max-time 10 -o /dev/null "http://192.168.8.50:8200$route" || exit 1
  printf 'ACCEPTED %s\n' "$route" | tee -a "$receipt"
done
[[ "$(readlink -f "$current")" == "$after" ]] || exit 1
systemctl --user is-active --quiet "$service"
if ! systemctl --user show -p ExecStart "$service" | grep -q "serve_four_domain_v176.py"; then
  echo "UNEXPECTED_PREVIEW_ENTRYPOINT"; exit 1
fi
actual=$(curl -fsS --max-time 10 "http://192.168.8.50:8200/review-20261109/domain-map.json" | sha256sum | cut -d ' ' -f 1)
[[ "$actual" == dd302ff4c5314078183d4e9c3e0a7f3949b9ce026591c0de4b0a7fb001d0d6ff ]] || exit 1
code=$(curl -sS --max-time 8 --path-as-is -o /dev/null -w "%{http_code}" "http://192.168.8.50:8200/review-20261109/../source-lock.json")
[[ "$code" == 403 ]] || { echo "TRAVERSAL_REFUSAL_MISSING"; exit 1; }
code=$(curl -sS --max-time 8 -o /dev/null -w "%{http_code}" "http://192.168.8.50:8200/source-lock.json")
[[ "$code" == 404 ]] || { echo "SOURCELOCK_DISCLOSURE"; exit 1; }
status=activated
echo "V176_CANONICAL_WLAN_ACTIVATION_ACCEPTED" | tee -a "$receipt"
trap - EXIT
