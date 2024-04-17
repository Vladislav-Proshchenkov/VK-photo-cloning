import requests

params = {
    'client_id': '51902640',
    'display': 'page',
    'redirect_uri': 'https://example.com/callback',
    'scope': 'friends,photos',
    'response_type': 'token',
    'v': '5.199',
    'state': '123456'
}

responce = requests.get('https://oauth.vk.com/authorize', params=params)
print(responce.url)