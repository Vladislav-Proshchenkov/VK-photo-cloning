import requests
import pprint
import time

token = 'vk1.a.7FN83kF7v6JuyFlgQMoK2jcmS3RZHKzt0jBrwr4sR4U3stmUPlgsjhkPS5FlKNyE07VMzuuCNW_qOElSHvPwg1N3ZHc1Tpwb4EQ9tJBGGTFxTOv3fl4rMLcx4khzhvs3JWRYH3vA72BKySdI5xzD8eZ8C0s0Zixyivd7A5RRwEPmk74duicLby0SbtjJ89pW'
# https://<адрес-сервера>/method/<имя-API-метода>?<параметры>

class VK_photo_cloning:
    URL = 'https://api.vk.com/method/'
    def __init__(self, token, owner_id, album_id):
        self.token = token
        self.owner_id = owner_id
        self.album_id = album_id

    def get_photos(self):
        params = {
            'access_token': self.token,
            'v': 5.199,
            'owner_id': self.owner_id,
            'album_id': self.album_id,
            'extended': 1
        }
        response = requests.get(self.URL + 'photos.get', params=params)
        return response.json()

    def clone_photos(self):
        photos = self.get_photos()
        #pprint.pprint (photos)
        for photo in photos['response']['items']:
            max_photo = max(photo['sizes'], key=lambda x: x['height'])
            url_photo = max_photo['url']
            likes_count = photo['likes']['count']
            date_photo = photo['date']
            print(url_photo, likes_count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date_photo)))


if __name__ == '__main__':
    user = VK_photo_cloning(token, 680361694, 'profile')
    user.clone_photos()