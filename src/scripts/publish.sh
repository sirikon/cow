#!/usr/bin/env bash
set -euo pipefail

function main {
  version="$(sed 's/[ \n]//g' <VERSION)"
  commit="$(git rev-parse --verify HEAD)"

  log "Publishing Cow" \
    "  version: ${version}" \
    "   commit: ${commit}"
}

function log { (
  printf "\e[2m▓▒░ %s\e[m\n" "$@"
); }

main
