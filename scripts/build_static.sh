#!/bin/sh
# Builds the static phone version into _site/ (only runtime files; no research data).
# Usage: sh scripts/build_static.sh [build-id]
set -eu
cd "$(dirname "$0")/.."
BUILD="${1:-$(git rev-parse --short HEAD 2>/dev/null || date +%s)}"
rm -rf _site
mkdir -p _site/src _site/data _site/icons
cp evidence.html manifest.webmanifest _site/
sed 's|<meta charset="utf-8">|<meta charset="utf-8"><meta name="fde-storage" content="device">|' index.html > _site/index.html
grep -q 'fde-storage' _site/index.html
cp src/*.js src/*.css _site/src/
cp data/questions.json data/manifest.json data/quality.json data/rounds.json _site/data/
cp icons/*.png _site/icons/
sed "s/__BUILD__/$BUILD/" sw.js > _site/sw.js
touch _site/.nojekyll
# AI FDE (腾讯云人工智能前沿部署工程师, type=CID) bank at cid/
if [ -f cid/data/questions.json ]; then
  mkdir -p _site/cid/src _site/cid/data _site/cid/icons
  cp cid/index.html cid/manifest.webmanifest _site/cid/
  cp cid/src/*.js cid/src/*.css _site/cid/src/
  cp cid/data/questions.json cid/data/manifest.json cid/data/notes.json _site/cid/data/
  cp cid/icons/*.png _site/cid/icons/
  sed "s/__BUILD__/$BUILD/" cid/sw.js > _site/cid/sw.js
fi
echo "Built _site (build $BUILD)"
