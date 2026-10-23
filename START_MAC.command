#!/bin/zsh
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo "Install Python 3.13 or 3.14 from python.org first."
  read "?Press Enter to close."
  exit 1
fi
if [ ! -f .venv/bin/python ]; then
  python3 -m venv .venv || exit 1
fi
.venv/bin/python -c 'import flask, sklearn, waitress' 2>/dev/null || .venv/bin/python -m pip install -r requirements.txt || exit 1
.venv/bin/python launch.py
