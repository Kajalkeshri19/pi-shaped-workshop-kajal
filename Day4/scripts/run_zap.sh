#!/usr/bin/env bash
set -euo pipefail

TARGET_URL=${TARGET_URL:-http://127.0.0.1:5000}
REPORT_PATH=${REPORT_PATH:-zap-report.html}

docker run --rm --network host owasp/zap2docker-stable zap-baseline.py -t "$TARGET_URL" -r "$REPORT_PATH"
