#!/bin/bash

set -e

RUN_ID="$1"
SEED="${2:-12345}"

if [ -z "$RUN_ID" ]; then
  echo "Usage: ./scripts/run_vampi_evomaster.sh run_01 12345"
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo "TOKEN environment variable is not set."
  echo "Run: export TOKEN='your_token_here'"
  exit 1
fi

mkdir -p "logs/vampi/evomaster"
mkdir -p "results/vampi/evomaster/$RUN_ID"

java -jar tools/evomaster/evomaster.jar \
  --blackBox true \
  --bbTargetUrl http://localhost:5002 \
  --bbSwaggerUrl configs/openapi/vampi-openapi.json \
  --outputFolder "results/vampi/evomaster/$RUN_ID" \
  --maxTime 5m \
  --seed "$SEED" \
  --header0 "Authorization: Bearer $TOKEN" \
  2>&1 | tee "logs/vampi/evomaster/${RUN_ID}_seed_${SEED}.log"
