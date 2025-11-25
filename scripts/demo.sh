#!/bin/bash

set -e

API_URL="http://localhost:8000"

echo "=================================="
echo "SEO Agent Demo Script"
echo "=================================="
echo ""

echo "1. Health Check..."
curl -s "$API_URL/health" | jq .
echo ""

echo "2. Creating article generation job..."
RESPONSE=$(curl -s -X POST "$API_URL/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "best productivity tools for remote teams",
    "target_word_count": 800,
    "language": "en"
  }')

echo "$RESPONSE" | jq .
JOB_ID=$(echo "$RESPONSE" | jq -r .job_id)
echo ""

echo "Job ID: $JOB_ID"
echo ""

echo "3. Polling job status..."
for i in {1..30}; do
  echo "  Attempt $i/30..."
  STATUS=$(curl -s "$API_URL/api/v1/jobs/$JOB_ID" | jq -r .status)
  echo "  Status: $STATUS"
  
  if [ "$STATUS" == "completed" ] || [ "$STATUS" == "failed" ]; then
    break
  fi
  
  sleep 2
done
echo ""

echo "4. Fetching final result..."
curl -s "$API_URL/api/v1/jobs/$JOB_ID" | jq .
echo ""

echo "=================================="
echo "Demo Complete!"
echo "=================================="

