import requests
import hashlib

#ПОМЕСТИТЕ в файл access_ok.txt ключи от приложения в Одноклассниках
with open('access_ok.txt') as file:
    PUBLIC_KEY = file.readline().strip()
    SESSION_KEY = file.readline().strip()
    SECRET_SESSION_KEY = file.readline().strip()

class Odnoklassniki:

    def __init__(self, id_user):
        self.id_user = id_user
        self.url = 'https://api.ok.ru/fb.do'
        self.public_key = PUBLIC_KEY
        self.session_key = SESSION_KEY
        self.secret_session_key = SECRET_SESSION_KEY

    def get_albums_info(self):
        """Получение информации об альбомах пользователя"""
        method = 'photos.getAlbums'
        sig_str = f"application_key={self.public_key}fid={self.id_user}format=jsonmethod={method}{self.secret_session_key}"
        sig = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
        params = {
            "application_key": self.public_key,
            "format": "json",
            "method": method,
            "fid": self.id_user,
            "sig": sig,
            "access_token": self.session_key
        }
        req = requests.get(self.url, params=params)
        albums = []
        for album in req.json()["albums"]:
            albums.append(album["aid"])
        return albums

    def get_user_photos(self):
        """Получение информации о фотографиях из ПРОФИЛЯ пользователя"""
        method = 'photos.getPhotos'
        sig_str = f"application_key={self.public_key}fid={self.id_user}format=jsonmethod={method}{self.secret_session_key}"
        sig = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
        params = {
            "application_key": self.public_key,
            "fid": self.id_user,
            "format": "json",
            "method": method,
            "sig": sig,
            "access_token": self.session_key
        }
        req = requests.get(self.url, params=params)
        return req.json()

    def get_albums_photos(self, id_albums):
        """Получение фотографий из АЛЬБОМОВ пользователя"""
        method = 'photos.getPhotos'
        photos_list = []
        for id_album in id_albums:
            sig_str = f"aid={id_album}application_key={self.public_key}format=jsonmethod={method}{self.secret_session_key}"
            sig = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
            params = {
                "aid": id_album,
                "application_key": self.public_key,
                "format": "json",
                "method": method,
                "sig": sig,
                "access_token": self.session_key
            }
            req = requests.get(self.url, params=params)
            for photo in req.json()['photos']:
                photos_list.append(photo)
        return photos_list

    def get_json_file_photos(self, photos_list, how_many_photos):
        """Функция для формирования json словаря информации о фото"""
        dict_photos_info = {"photos": []}
        count = 0

        for photo in photos_list:
            count += 1
            # Формируем название файла с фотографией
            photo_name = f'{str(count)}_ok_{photo["id"]}_{photo["mark_count"]}.jpg'
            dict_photos_info["photos"].append(
                {"id_photo": photo["id"],
                 "file_name": photo_name,
                 "url_photo": photo["pic640x480"],
                 "size": "640x480"}
            )
            if count == how_many_photos:
                break
        return dict_photos_info