#!/usr/bin/env bash
set -euo pipefail
cd "$(realpath "$(dirname "${BASH_SOURCE[0]}")/../..")"

function main {
  COW_VERSION="$(sed 's/[ \n]//g' <VERSION)"
  COW_COMMIT="$(git rev-parse --verify HEAD)"
  export COW_VERSION
  export COW_COMMIT

  export COW_IMAGE="sirikon/cow:${COW_VERSION}-${COW_COMMIT}"

  log "Publishing Cow" \
    "  version: ${COW_VERSION}" \
    "   commit: ${COW_COMMIT}"

  log "Building"
  docker compose \
    -f ./docker-compose.yml \
    -f ./src/docker-environment/docker-compose.base.yml \
    -f ./src/docker-environment/docker-compose.build.yml \
    build
  
  log "Pushing"
  docker push "${COW_IMAGE}"
}

function log { (
  printf "\e[2m▓▒░ %s\e[m\n" "$@"
); }

main
