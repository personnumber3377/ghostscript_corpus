#!/usr/bin/env bash
set -euo pipefail

indir="../ps_corpus"     # change if needed
outdir="./first40_from_header"             # where snippets go
mkdir -p "$outdir"

# Grab .ps and .eps files (recursively), robust to spaces in names.
find "$indir" -type f \( -iname '*.ps' -o -iname '*.eps' \) -print0 |
while IFS= read -r -d '' f; do
  # First line number that starts with %!PS-Adobe...
  start=$(grep -a -n -m1 '^%[!]PS-Adobe' "$f" | cut -d: -f1) || true
  [[ -n "${start:-}" ]] || { echo "skip (no PS-Adobe header): $f"; continue; }

  base=$(basename "$f")
  out="$outdir/${base%.*}_first40.ps"

  # Print header line + next 39 lines (or fewer if file is shorter)
  tail -n +"$start" "$f" | head -n 40 > "$out"
done
