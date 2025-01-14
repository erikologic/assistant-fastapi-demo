#! /bin/sh
set -e

TOKEN=$(./get_token.sh)

curl -i -X POST "http://127.0.0.1:8000/assistance/" \
    -H "Content-Type: application/json" \
    -d '{"topic": "Sales", "description": "I need help so much!"}' \
    -H "Authorization: Bearer ${TOKEN}" 