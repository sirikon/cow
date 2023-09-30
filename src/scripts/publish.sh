#!/usr/bin/env bash
set -euo pipefail
cd "$(realpath "$(dirname "${BASH_SOURCE[0]}")/../..")"

function main {
  version="$(sed 's/[ \n]//g' <VERSION)"
  commit="$(git rev-parse --verify HEAD)"

  cow_image_base="sirikon/cow"
  cow_image_version_and_commit="${cow_image_base}:${version}-${commit}"
  cow_image_version_only="${cow_image_base}:${version}"
  cow_image_latest="${cow_image_base}:latest"

  export COW_IMAGE="${cow_image_version_and_commit}"

  log "Publishing Cow" \
    "  version: ${version}" \
    "   commit: ${commit}" \
    "   images:" \
    "       ${cow_image_version_and_commit}" \
    "       ${cow_image_version_only}" \
    "       ${cow_image_latest}"

  log "Building"
  docker compose \
    -f ./docker-compose.yml \
    -f ./src/docker-environment/docker-compose.base.yml \
    -f ./src/docker-environment/docker-compose.build.yml \
    -f ./src/docker-environment/docker-compose.publish.yml \
    build

  if [ "${1:-}" = "confirm" ]; then
    log "Pushing"
    docker tag "${cow_image_version_and_commit}" "${cow_image_version_only}"
    docker tag "${cow_image_version_and_commit}" "${cow_image_latest}"
    docker push "${cow_image_version_and_commit}"
    docker push "${cow_image_version_only}"
    docker push "${cow_image_latest}"
  else
    echo "Run again the publish script with 'confirm' argument to finally push."
  fi
}

function log { (
  printf "\e[2m▓▒░ %s\e[m\n" "$@"
); }

main "$@"
