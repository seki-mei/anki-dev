#!/bin/bash
BASE="$HOME/software/anki-dev"
NAME="$1"
[ -z "$1" ] && { echo "Usage: $0 <addon-name>" >&2; exit 1; }
cd "$BASE/$NAME" || exit 1
rm -rf "__pycache__"
zip -r "../$NAME.ankiaddon" *
