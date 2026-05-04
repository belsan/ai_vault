#!/usr/bin/env bash
# Build script for the manuscript.
#
# Usage:
#   ./build.sh        # build main.pdf in build/
#   ./build.sh clean  # remove build artifacts

set -euo pipefail

cd "$(dirname "$0")"

if [[ "${1:-}" == "clean" ]]; then
  rm -rf build
  exit 0
fi

mkdir -p build

# --- Regenerate dot-based figures when their .dot source is newer than
# --- the rendered .pdf. Skipped silently if `dot` is not on PATH so
# --- the build still works on a machine without Graphviz installed.
if command -v dot >/dev/null 2>&1; then
  for src in figures/*.dot; do
    [ -e "$src" ] || continue
    out="${src%.dot}.pdf"
    if [ ! -e "$out" ] || [ "$src" -nt "$out" ]; then
      echo "  dot  $src -> $out"
      dot -Tpdf "$src" -o "$out"
    fi
  done
else
  echo "  (graphviz not installed; using cached figures/*.pdf)"
fi

# Two passes + bibtex + two more passes is the safe pattern with natbib.
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex >/dev/null
( cd build && BIBINPUTS=..: bibtex main >/dev/null ) || true
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex >/dev/null

echo "Built build/main.pdf"
