#!/bin/bash
TOKEN=$(curl -s -X POST http://localhost:5002/users/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"name1","password":"pass1"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["auth_token"])')

echo "Authorization: Bearer $TOKEN"
