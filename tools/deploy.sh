#!/bin/sh
# Upload the committed sources to MyDevil and rebuild the live site.
# The daily cron on the server reruns the build to publish scheduled posts.
set -e
HOST=pawelsome@s64.mydevil.net
REMOTE=empire-site
cd "$(dirname "$0")/.."
git archive --format=tar HEAD | ssh "$HOST" "
  set -e
  rm -rf $REMOTE/src.new && mkdir -p $REMOTE/src.new
  tar -xf - -C $REMOTE/src.new
  rm -rf $REMOTE/src && mv $REMOTE/src.new $REMOTE/src
  python3 $REMOTE/src/tools/build_site.py --out domains/empirecorporation.eu/public_html --state $REMOTE/state.json --ping
"
