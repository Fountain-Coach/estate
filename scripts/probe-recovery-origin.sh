#!/bin/sh
# Read-only recovery-origin readiness probe. Prints no credentials and mutates
# no DNS, SSH configuration, publication content, container or application.
set -u
command_exists() { command -v "$1" >/dev/null 2>&1; }
yesno() { if command_exists "$1"; then printf yes; else printf no; fi; }
printf 'schema=fountain.estate.origin-prerequisite-witness.v1\n'
printf 'operating_system='
if [ -f /etc/os-release ]; then . /etc/os-release; printf '%s-%s\n' "$ID" "$VERSION_ID"; else uname -s; fi
printf 'git_available='; yesno git; printf '\n'
printf 'docker_available='; yesno docker; printf '\n'
printf 'caddy_available='; yesno caddy; printf '\n'
printf 'cloudflared_available='; yesno cloudflared; printf '\n'
if command_exists docker; then
    if docker image inspect caddy:latest >/dev/null 2>&1; then
        printf 'cached_caddy_image=yes\n'
    else
        printf 'cached_caddy_image=no-or-daemon-unavailable\n'
    fi
fi
if command_exists git; then
    count=$(git config --global --get-regexp '^url\..*\.insteadof$' 2>/dev/null | wc -l | tr -d ' ' || :)
    printf 'git_global_url_rewrite_count=%s\n' "$count"
    if GIT_TERMINAL_PROMPT=0 timeout 12 git ls-remote -q https://github.com/Fountain-Coach/estate.git HEAD >/dev/null 2>&1; then
        printf 'default_git_https_estate=usable\n'
    else
        printf 'default_git_https_estate=unusable\n'
    fi
    if GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0 timeout 12 git ls-remote -q https://github.com/Fountain-Coach/estate.git HEAD >/dev/null 2>&1; then
        printf 'isolated_git_https_estate=usable\n'
    else
        printf 'isolated_git_https_estate=unusable\n'
    fi
    if GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0 timeout 12 git ls-remote -q https://github.com/Fountain-Coach/midi2-gpu-fabric.git HEAD >/dev/null 2>&1; then
        printf 'isolated_git_https_private_archive=usable\n'
    else
        printf 'isolated_git_https_private_archive=not_accessible_without_auth\n'
    fi
fi
if command_exists ssh; then
    greeting=$(timeout 12 ssh -o BatchMode=yes -o ConnectTimeout=7 -o StrictHostKeyChecking=yes -T git@github.com </dev/null 2>&1 || :)
    case "$greeting" in
      *'successfully authenticated'*) printf 'github_ssh_private_archive=key_accepted\n' ;;
      *) printf 'github_ssh_private_archive=not_verified\n' ;;
    esac
fi
printf 'mutations_performed=no\n'
