#! /bin/sh

## This script is used as an example to generate an authorised API request to the API

set -e

. .env

get_token() {
    curl --request POST \
    --url "https://${AUTH0_DOMAIN}/oauth/token" \
    --header 'content-type: application/x-www-form-urlencoded' \
    --data grant_type=client_credentials \
    --data audience="$AUTH0_API_AUDIENCE" \
    --data client_id="$TEST_CLIENT_ID" \
    --data client_secret="$TEST_CLIENT_SECRET"  | jq '.access_token' | xargs echo -n
   }

TOKEN=$(get_token)

curl -i -X POST "http://127.0.0.1:8000/assistance/" \
    -H "Content-Type: application/json" \
    -d '{"topic": "Sales", "description": "I need help so much!"}' \
    -H "Authorization: Bearer ${TOKEN}" 