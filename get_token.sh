#! /bin/bash

set -e

source .env

curl --request POST \
  --url "https://${AUTH0_DOMAIN}/oauth/token" \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=client_credentials \
   --data audience="$AUTH0_API_AUDIENCE" \
   --data client_id="$TEST_CLIENT_ID" \
   --data client_secret="$TEST_CLIENT_SECRET"  | jq '.access_token' | xargs echo -n