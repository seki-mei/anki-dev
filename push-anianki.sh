#!/bin/bash
SRC="$HOME/software/anki-dev/anianki/"
DEST="$HOME/.var/app/net.ankiweb.Anki/data/Anki2/addons21/anianki/"

rsync -av --delete --exclude '/user_files/images/' --exclude '/__pycache__/' --exclude '/meta.json' "$SRC" "$DEST"
