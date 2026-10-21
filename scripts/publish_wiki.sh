#!/usr/bin/env bash
# Publish wiki/ to this repository's actual GitHub Wiki.
#
# This is a manual/CI step, not part of controller.py's pipeline — GitHub has no
# REST/GraphQL API for wiki content, so the only way to update it is a git push
# to <repo>.wiki.git, the wiki's own (separate) git repository.
#
# One-time prerequisite: the wiki must be initialized once through the GitHub
# web UI (Settings → Features → Wikis → enabled, then the Wiki tab → "Create
# the first page" → save anything). Until that's done, <repo>.wiki.git does
# not exist and this script's clone step will fail with a 401.
#
# Usage:
#   GITHUB_REPO=owner/name ./scripts/publish_wiki.sh
# (requires git credentials for github.com with push access to the repo, e.g.
#  via `gh auth login` or a configured credential helper)

set -euo pipefail

REPO="${GITHUB_REPO:-JohnOnAvocados/PS5-Jailbreak-Research}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/wiki"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

echo "Cloning wiki repo for $REPO ..."
git clone "https://github.com/${REPO}.wiki.git" "$WORK_DIR/wiki_repo"

echo "Syncing wiki/ -> wiki repo (excluding this script's own docs) ..."
rsync -a --delete \
  --exclude ".git" \
  --exclude "README_PUBLISHING.md" \
  "$SRC_DIR/" "$WORK_DIR/wiki_repo/"

cd "$WORK_DIR/wiki_repo"
git add -A
if git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

git commit -m "Sync wiki content from main repo wiki/"
git push origin HEAD
echo "Wiki published."
