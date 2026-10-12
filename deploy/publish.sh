#!/bin/sh
# Upload only runtime files to the configured host.
set -eu

repo_directory=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
private_settings="$repo_directory/.private-deployment/publish.env"
if [ -f "$private_settings" ]; then
  . "$private_settings"
fi
: "${SOFEIJOADA_SSH_HOST:?Set the deployment SSH host privately}"
: "${SOFEIJOADA_DEPLOY_SCRIPT:?Set the deployment script path privately}"
[ -f "$SOFEIJOADA_DEPLOY_SCRIPT" ] || {
  echo "The configured deployment script is unavailable." >&2
  exit 1
}

ssh -o BatchMode=yes "$SOFEIJOADA_SSH_HOST" 'test -d /srv/sofeijoada/app && sudo -n systemctl is-active --quiet sofeijoada.service'

stage_directory=$(mktemp -d "${TMPDIR:-/tmp}/sofeijoada-publish.XXXXXX")
trap 'rm -rf -- "$stage_directory"' EXIT HUP INT TERM

for runtime_file in app.py locales.py requirements.txt; do
  cp "$repo_directory/$runtime_file" "$stage_directory/"
done
cp -R "$repo_directory/templates" "$repo_directory/static" "$stage_directory/"

cd "$stage_directory"
sh "$SOFEIJOADA_DEPLOY_SCRIPT" sofeijoada
