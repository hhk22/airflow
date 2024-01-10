import requests

client_id = '4406e0807f02bdd8a61b4f61a991e8c3'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'H47SWuOt6hsbIecZjdWsgOJKG68wQZN1c7jawOb5kZoiKAfhayK5QtVLcooKKiWRAAABjO7vQoyUJG13ldIf8A'

token_url = 'https://kauth.kakao.com/oauth/token'
data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'code': authorize_code
}

response = requests.post(token_url, data=data)
tokens = response.json()
print(tokens)

