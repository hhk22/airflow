import requests

client_id = '4406e0807f02bdd8a61b4f61a991e8c3'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'msH94WmCfloFUQY9q_r_l-UadMR7W3yN5tyvtoangIp_IuDOl6iY9UzCpWkKPXUbAAABjO6kC07mTYKY7N6ACw'

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

