#!/bin/bash

set -e

RUN_ID="$1"
SEED="${2:-12345}"

if [ -z "$RUN_ID" ]; then
  echo "Usage: ./scripts/run_evomaster.sh run_01 12345"
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo "TOKEN environment variable is not set."
  echo "Run: TOKEN='your_token_here'"
  exit 1
fi

mkdir -p "logs/evomaster"
mkdir -p "results/evomaster/$RUN_ID"

java -jar tools/evomaster/evomaster.jar \
  --blackBox true \
  --bbTargetUrl http://localhost:8888 \
  --bbSwaggerUrl configs/openapi/crapi-openapi-spec.json \
  --outputFolder "results/evomaster/$RUN_ID" \
  --maxTime 5m \
  --seed "$SEED" \
  --header0 "Authorization: Bearer $TOKEN" \
  2>&1 | tee "logs/evomaster/${RUN_ID}.log"