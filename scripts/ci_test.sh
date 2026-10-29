#!/bin/sh
# CI checks used before publishing: unit tests, bank validation, and the phone build in iPhone and Android viewports.
set -eu
cd "$(dirname "$0")/.."
npm test
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_bank.py --published > /dev/null
if [ -z "${PLAYWRIGHT_MODULE:-}" ]; then
  npm install --no-save --no-audit --no-fund playwright@1 > /dev/null
  npx playwright install --with-deps chromium > /dev/null
fi
sh scripts/build_static.sh ci
node tests/phone.browser.mjs
if [ -d _site/cid ]; then node tests/cid.browser.mjs; fi
