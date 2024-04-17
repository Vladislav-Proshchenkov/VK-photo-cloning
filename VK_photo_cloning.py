import requests
import json
import pprint
import time

vk_token = ('vk1.a.Wq13QYbHJxLIVRYS-lkf4DUPVs7_iBFuGeOVYK21D5tPDZi1puOcmDbjkm5PTPOrxGEChI4DaohNSzap8B4YCEIuF90D815m'
            'e9JSkfDDjuZo7BRhQhPfQjsdhYQ5jaVDIAnLGfCM1G7ycogA0YsOFJtnvClnJO5-CXFy-ZFTgSfnaqMKcmHJLvZRtZlnhL0d')
URL_Yandex = "https://cloud-api.yandex.net/v1/disk/resources"
URL_Yandex_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload"

class VK_photo_cloning:
    URL = 'https://api.vk.com/method/'
    def __init__(self, vk_token, owner_id, album_id):
        self.vk_token = vk_token
        self.owner_id = owner_id
        self.album_id = album_id

    def get_photos(self):
        params = {
            'access_token': self.vk_token,
            'v': 5.199,
            'owner_id': self.owner_id,
            'album_id': self.album_id,
            'extended': 1
        }
        response = requests.get(self.URL + 'photos.get', params=params)
        #pprint.pprint(response.json())
        status_code = response.status_code
        if status_code != 200:
            print('Ошибка получения данных')
            exit()
        if response.json()['response']['count'] == 0:
            print('Нет фотографий')
        if album_id == 'wall':
            with open('wall.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=2, ensure_ascii=False)
        elif album_id == 'profile':
            with open('profile.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=2, ensure_ascii=False)
        return response.json()

    def create_folder(self):
        params = {
            'path': 'VK photos',
        }
        headers = {
            'Authorization': f'OAuth {yandex_token}'
        }
        response = requests.put(URL_Yandex, headers=headers, params=params)
        params = {
            'path': f'VK photos/{album}',
        }
        response = requests.put(URL_Yandex, headers=headers, params=params)
        #print(response.json())

    def clone_photos(self):
        photos = self.get_photos()
        self.create_folder()
        max_photos = {}
        new_names = {}
        count = 0
        for photo in photos['response']['items']:
            max_photo = max(photo['sizes'], key=lambda x: x['height'])
            date_photo = photo['date']
            max_photos[count] = {'url_photo': max_photo['url'],
                                 'likes_count': photo['likes']['count'],
                                 'date_photo': time.strftime('%Y.%m.%d %H-%M-%S', time.localtime(date_photo)),
                                 'name': photo['likes']['count']}
            count += 1
        for i, photo in max_photos.items():
            if str(photo['likes_count']) not in new_names.values():
                new_names[i] = str(photo['likes_count'])
            else:
                new_names[i] = f'{str(photo['likes_count'])} {photo['date_photo']}'
        for key, value in new_names.items():
            max_photos[key]['name'] = value
        #pprint.pprint(max_photos)
        for photo in max_photos.values():
            params = {
                'path': f'VK photos/{album}/{photo['name']}.jpg',
                'overwrite': 'true'
            }
            headers = {
                'Authorization': f'OAuth {yandex_token}'
            }
            response = requests.get(URL_Yandex_upload, headers=headers, params=params)
            #print(response.json())
            params = {
                'url': photo['url_photo'],
                'path': f'VK photos/{album}/{photo['name']}.jpg'
            }
            response = requests.post(URL_Yandex_upload, headers=headers, params=params)
            #print(response.json())

if __name__ == '__main__':

    print('1 - фотографии со стены\n'
          '2 - фотографии профиля\n')
    album_id = input('Введите альбом: ')
    if album_id == '1':
        album = 'wall'
    elif album_id == '2':
        album = 'profile'
    else:
        print('Неверный альбом')
        exit()
    #owner_id = input('Введите пользователя: ') # мой id 680361694
    owner_id = 680361694
    yandex_token = input('Введите токен Яндекс.Диска: ')
    user = VK_photo_cloning(vk_token, owner_id, album)
    user.clone_photos()