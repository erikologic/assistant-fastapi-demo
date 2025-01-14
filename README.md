## Manually test the API
```bash
curl -i "http://127.0.0.1:8000/api/private" \
    -H "Authorization: Bearer $(./get_token.sh)"
```
