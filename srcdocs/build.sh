#!/usr/bin/env bash
# this_file: srcdocs/build.sh
# Build the adjacent site; remaining arguments are forwarded to the renderer.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export PYTHONPATH="$PWD/..:$PWD${PYTHONPATH:+:$PYTHONPATH}"

if [[ "${1:-}" == build ]]; then shift; fi
exec uvx --python 3.12 --from mkdocs==1.6.1 \
  --with mkdocs-material \
  --with pymdown-extensions \
  --with 'vexy-python-markdown-steroids @ git+https://github.com/vexyart/vexy-python-markdown-steroids@v0.4.13' \
  mkdocs build --config-file markdown-steroids.yml "$@"
