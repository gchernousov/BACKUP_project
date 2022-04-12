import requests
from datetime import datetime, date

#ПОМЕСТИТЕ в файл token_vk.txt токен от приложения vkontakte
with open('token_vk.txt') as file:
    token = file.read()

class Vkontakte:

    def __init__(self, id_user):
        self.id_user = id_user
        self.url = 'https://api.vk.com/method/'
        self.token = token
        self.version = '5.131'

    def get_user(self):
        """Получение базовой информации о пользователе.
        Проверка статуса профиля: открыт или закрыт"""
        new_url = self.url + 'users.get'
        params = {
            "user_ids": self.id_user,
            "access_token": self.token,
            "v": self.version
        }
        req = requests.get(new_url, params=params)
        close_status = req.json()['response'][0]['is_closed']
        return close_status

    def get_photos_info(self, album_type, default_count=1000):
        """Функция для получения информации об альбоме фотографий в вконтакте"""
        new_url = self.url + 'photos.get'
        params = {
            "owner_id": self.id_user,
            "album_id": album_type,
            "rev": 0,
            "extended": 1,
            "photo_sizes": 1,
            "count": default_count,
            "access_token": self.token,
            "v": self.version
        }
        req = requests.get(new_url, params=params)
        return req.json()['response']

    def get_albums_info(self):
        """Функция для формирования списка id личных альбомов пользователя"""
        new_url = self.url + 'photos.getAlbums'
        params = {
            "owner_id": self.id_user,
            "photo_sizes": 1,
            "access_token": self.token,
            "v": self.version
        }
        req = requests.get(new_url, params=params)
        albums_id_list = []
        for album_id in req.json()['response']['items']:
            albums_id_list.append(str(album_id['id']))
        return albums_id_list

    def get_json_file_photos(self, photos_album, how_many_photos):
        """Функция для формирования json словаря информации о фото"""
        dict_photos_info = {"photos": []}
        count = 0
        for photo_info in photos_album:
            count += 1
            id_photo = photo_info['id']
            max_size_photo = 0
            for photo in photo_info['sizes']:
                heightxwidth = photo['height'] * photo['width']
                # Фотографии, загруженные до 2012г., имеют значение height и width = 0
                if heightxwidth > 0:
                    if max_size_photo < heightxwidth:
                        max_size_photo = heightxwidth
                        photo_url = photo['url']
                        photo_size_type = photo['type']
                else:
                    if photo['type'] == 'w' or photo['type'] == 'z' or photo['type'] == 'y' or photo['type'] == 'x':
                        photo_url = photo['url']
                        photo_size_type = photo['type']
                    else:
                        photo_url = photo['url']
                        photo_size_type = photo['type']
            unix_date_photo = photo_info['date']
            date_photo = date.fromtimestamp(unix_date_photo) # получаем дату загрузки фотографии в альбом
            # Формируем название файла с фотографией
            photo_name = f'{str(count)}_vk_{photo_size_type}_{date_photo}_{str(photo_info["likes"]["count"])}.jpg'
            dict_photos_info["photos"].append(
                {"id_photo": id_photo, "file_name": photo_name,
                 "url_photo": photo_url, "size": photo_size_type}
            )
            if count == how_many_photos:
                break
        return dict_photos_info