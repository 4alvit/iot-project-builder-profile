#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "${1:-}" == security || "${1:-}" == bandit ]]; then
  uvx --from bandit==1.8.6 bandit -r . -lll -x .git,.venv,.venv-ci,tests,scripts/release.py,scripts/release_control.py
  if [[ "${1:-}" == security ]]; then
    command -v trivy >/dev/null || { echo 'Trivy is required for the complete local security gate.' >&2; exit 1; }
    trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 --skip-dirs .git,.venv,.venv-ci,release-dist,dist,build .
  fi
  exit 0
fi
mode="${1:-all}"
[[ "$mode" =~ ^(all|lint|test)$ ]] || { echo 'Usage: ci.sh [lint|test|security]' >&2; exit 2; }
uv sync --locked --all-extras
if [[ "$mode" != test ]]; then
  uv run --locked ruff check .
  uv run --locked ruff format --check .
  uv run --locked mypy .
fi
if [[ "$mode" != lint ]]; then
  uv run --locked python scripts/check_test_readiness.py
fi
