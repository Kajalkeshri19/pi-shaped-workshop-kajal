#!/usr/bin/env bash
set -euo pipefail

# Start flask app in background
cd app
python -m flask run --host=0.0.0.0 --port=5000 &
FLASK_PID=$!

for i in {1..15}; do
  if curl -sS http://127.0.0.1:5000/ >/dev/null; then
    echo "Flask up"
    break
  fi
  sleep 1
done

./run_zap.sh

wait $FLASK_PID
