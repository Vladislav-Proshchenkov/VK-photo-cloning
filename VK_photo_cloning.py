import requests
import json
import pprint
import time

vk_token = ('vk1.a.CwnNZGlT2x3rYVvl0DROSYwsWxbYSNi4I_rMkgu4MtwoJpFWi0ev1ua4X2SrrakK-QjyjoHjAldZhVXkxQPidNWEK5CMxAcg'
            'HrCtuHLD_ilI_aHVC88c9tHuI0JBq2v3bK7fzGiHH3vWcEI8H0JYY3rivbcgLPH_XD2cj_7XL7S8fby1z4uCATTYBgjq9Bhu')
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

    def max_photo_in_album(self):
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
        return max_photos

    def clone_photos(self):
        max_photos = self.max_photo_in_album()
        print('Количество фотографий: ', len(max_photos))
        quantity = int(input('Введите количество фотографий для копирования: '))
        if quantity == 0:
            print('Не выбрано ни одной фотографии')
            exit()
        elif quantity < 0:
            print('Неверное значение')
            exit()
        elif quantity > len(max_photos):
            print('Неверное значение')
            exit()
        open("download.json", "w").close()
        for i in range(quantity):
            with open('download.json', 'a', encoding='utf-8') as file:
                json.dump(max_photos[i], file, indent=2, ensure_ascii=False)
            params = {
                'path': f'VK photos/{album}/{max_photos[i]['name']}.jpg',
                'overwrite': 'true'
            }
            headers = {
                'Authorization': f'OAuth {yandex_token}'
            }
            response = requests.get(URL_Yandex_upload, headers=headers, params=params)
            #print(response.json())
            params = {
                'url': max_photos[i]['url_photo'],
                'path': f'VK photos/{album}/{max_photos[i]['name']}.jpg',
                'overwrite': 'true'
            }
            response = requests.post(URL_Yandex_upload, headers=headers, params=params)
            # print(response.json())



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