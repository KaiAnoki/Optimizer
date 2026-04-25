#!/usr/bin/env bash
set -euo pipefail
python run_cli.py "Explain the ARES optimizer architecture" >/tmp/ares_optimizer_smoke.json
pytest -q
