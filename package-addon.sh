#!/bin/bash
BASE="$HOME/software/anki-dev"

show_help() {
    cat << EOF
Usage: $0 [OPTIONS] <addon-name>

Package an Anki addon into .ankiaddon format.

Options:
    -o, --open      Open the packaged file with xdg-open after creation
    -h, --help      Show this help message

Arguments:
    <addon-name>    Name of the addon directory to package
EOF
}

OPEN=false
NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--open)
            OPEN=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Unknown option: $1" >&2
            show_help >&2
            exit 1
            ;;
        *)
            NAME="$1"
            shift
            ;;
    esac
done

[ -z "$NAME" ] && { echo "Error: addon-name required" >&2; show_help >&2; exit 1; }

cd "$BASE/$NAME" || exit 1
rm -rf "__pycache__"
zip -r "../$NAME.ankiaddon" . -x "meta.json"

if [ "$OPEN" = true ]; then
    xdg-open "../$NAME.ankiaddon"
fi
