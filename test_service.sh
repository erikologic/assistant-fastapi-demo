#! /bin/sh

## This script is used to generate authorised requests to the API
## Usage: 
##   ./test_service.sh -e assistance  # calls assistance endpoint (requires auth)
##   ./test_service.sh -e heartbeat   # calls heartbeat endpoint (no auth)

set -e
. .env

# Default values
ENDPOINT="heartbeat"

# Parse command line options
while getopts "e:" opt; do
    case $opt in
        e) ENDPOINT=$OPTARG ;;
        ?) echo "Usage: $0 [-e endpoint]" >&2; exit 1 ;;
    esac
done

get_token() {
    curl --request POST \
    --url "https://${AUTH0_DOMAIN}/oauth/token" \
    --header 'content-type: application/x-www-form-urlencoded' \
    --data grant_type=client_credentials \
    --data audience="$AUTH0_API_AUDIENCE" \
    --data client_id="$TEST_CLIENT_ID" \
    --data client_secret="$TEST_CLIENT_SECRET" | jq '.access_token' | xargs echo -n
}

case $ENDPOINT in
    "assistance")
        TOKEN=$(get_token)
        curl -i -X POST "http://127.0.0.1:8000/assistance/" \
            -H "Content-Type: application/json" \
            -d '{"topic": "Sales", "description": "I need help so much!"}' \
            -H "Authorization: Bearer ${TOKEN}"
        ;;
    "heartbeat")
        curl -i -X GET "http://127.0.0.1:8000/heartbeat" \
            -H "Content-Type: application/json"
        ;;
    *)
        echo "Unknown endpoint: $ENDPOINT"
        echo "Valid endpoints are: assistance, heartbeat"
        exit 1
        ;;
esac 

