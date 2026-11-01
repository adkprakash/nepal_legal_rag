#!/usr/bin/env bash
# Runs ON THE SERVER via:  ssh target 'bash -s'
# The caller exports: APP_ENV IMAGE_TAG DEPLOY_PATH USE_GPU GHCR_PULL_USER GHCR_PULL_TOKEN
# All logic lives in main() so no command can swallow the rest of the script from stdin.

set -euo pipefail

read_env() {   # read_env <KEY> <default>  (reads env/<APP_ENV>/infra.env)
  local v
  v="$(awk -F= -v k="$1" '$1==k {sub(/^[^=]*=/, ""); print; exit}' "env/${APP_ENV}/infra.env" | tr -d '\r"')"
  echo "${v:-$2}"
}

deploy_tag() {
  echo "==> Deploying tag $1"
  IMAGE_TAG="$1" make deploy APP_ENV="$APP_ENV" USE_GPU="${USE_GPU:-true}"
}

wait_healthy() {   # wait_healthy <url> <name>   (up to 10 minutes)
  local url="$1" name="$2" i
  for i in $(seq 1 60); do
    if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
      echo "    $name is healthy"
      return 0
    fi
    sleep 10
  done
  echo "    $name did not become healthy within 10 minutes"
  return 1
}

main() {
  : "${APP_ENV:?}" "${IMAGE_TAG:?}" "${DEPLOY_PATH:?}" "${GHCR_PULL_USER:?}" "${GHCR_PULL_TOKEN:?}"
  local use_gpu="${USE_GPU:-true}"
  local tarball="/tmp/nlr-${APP_ENV}-${IMAGE_TAG}.tgz"
  local history=".deploy_history_${APP_ENV}"
  local f prev_tag=""

  cd "$DEPLOY_PATH"
  trap 'docker logout ghcr.io >/dev/null 2>&1 || true' EXIT

  echo "==> Unpacking release ${IMAGE_TAG}"
  tar xzf "$tarball"
  rm -f "$tarball"

  echo "==> Preflight"
  for f in infra admin user; do
    if [ ! -f "env/${APP_ENV}/${f}.env" ]; then
      echo "ERROR: env/${APP_ENV}/${f}.env is missing on this server."
      echo "Create env/${APP_ENV}/${f}.env on this server, fill in every value, then re-run."
      exit 1
    fi
  done

  if [ -f "$history" ]; then
    prev_tag="$(tail -n 1 "$history")"
  fi

  echo "==> Registry login"
  printf '%s' "$GHCR_PULL_TOKEN" | docker login ghcr.io -u "$GHCR_PULL_USER" --password-stdin >/dev/null

  # Output is discarded on purpose: the resolved config contains secrets
  echo "==> Validating compose configuration"
  IMAGE_TAG="$IMAGE_TAG" make config APP_ENV="$APP_ENV" USE_GPU="$use_gpu" >/dev/null

  local admin_url user_url
  admin_url="http://127.0.0.1:$(read_env ADMIN_API_HOST_PORT 8001)/health"
  user_url="http://127.0.0.1:$(read_env USER_API_HOST_PORT 8002)/health"

  if deploy_tag "$IMAGE_TAG" \
     && wait_healthy "$admin_url" admin_api \
     && wait_healthy "$user_url" user_api; then
    echo "$IMAGE_TAG" >> "$history"
    tail -n 20 "$history" > "${history}.tmp" && mv "${history}.tmp" "$history"
    make ps APP_ENV="$APP_ENV" USE_GPU="$use_gpu" || true
    docker image prune -f >/dev/null
    echo "==> Deploy OK"
    return 0
  fi

  echo "==> Deploy FAILED. Recent logs:"
  make logs-tail APP_ENV="$APP_ENV" USE_GPU="$use_gpu" SERVICE="admin_api worker user_api" || true

  if [ -n "$prev_tag" ] && [ "$prev_tag" != "$IMAGE_TAG" ]; then
    echo "==> Rolling back to $prev_tag"
    deploy_tag "$prev_tag" || true
    wait_healthy "$admin_url" admin_api || true
    wait_healthy "$user_url" user_api || true
  else
    echo "No earlier release recorded, nothing to roll back to."
  fi
  return 1
}

main