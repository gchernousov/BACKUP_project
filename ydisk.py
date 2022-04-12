import requests
from tqdm import tqdm

#ПОМЕСТИТЕ в файл token_yandex.txt токен от Яндекс.Диска
with open('token_yandex.txt') as file:
    token = file.read()

class YandexDisk:

    def __init__(self):
        self.token = token
        self.upload_link = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, social_network):
        """Функция для создания папки на Яндекс.Диске"""
        if social_network == 'vk':
            folder_name = 'vk_photos'
        elif social_network == 'ok':
            folder_name = 'ok_photos'
        params = {'path': folder_name}
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        requests.put(self.upload_link, params=params, headers=headers)
        return folder_name

    def get_upload_link(self, file_name, folder_name):
        """Функция для получения ссылки для загрузки файла"""
        path_to_save = f'{folder_name}/{file_name}'
        params = {'path': path_to_save, 'overwrite': 'true'}
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        req = requests.get(self.upload_link + '/upload', params=params, headers=headers)
        return req.json()

    def upload_file(self, photos_list, folder_name):
        """Функция для загрузки файлов"""
        for file in tqdm(photos_list):
            link_for_upload = self.get_upload_link(file[0], folder_name)['href']
            img = requests.get(file[1]).content
            req = requests.put(link_for_upload, img)
            req.raise_for_status()
        print('\nВсе фото успешно загружены!')