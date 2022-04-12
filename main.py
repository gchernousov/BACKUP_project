from vkontakte import Vkontakte
from odnoklassniki import Odnoklassniki
from ydisk import YandexDisk
from gdrive import GoogleDrive

import json


def get_user_info():
    """Стартовое меню: запрашиваем соц.сеть (вконтакте или одноклассники) +
    id профиля и хранилище (yandex или google)
    """
    print('Из какой соц.сети будем выгружать фото?')
    get_info = False
    while get_info == False:
        soc_network = input('Введите vk (vkontakte) или ok (Одноклассники): ').lower()
        if soc_network == 'vk' or soc_network == 'ok':
            id_user = str(input(f'\nОтлично! Введите ID своего профиля: '))
            print('В какое хранилище загрузить фото?')
            while get_info == False:
                user_storage = input('Введите "yandex" (Яндекс.Диск) или "google" (Google.Drive): ').lower()
                if user_storage == 'yandex' or user_storage == 'google':
                    get_info = True
                else:
                    print('(!) Ошибка. Попробуйте еще раз\n')
        else:
            print('(!) Ошибка. Попробуйте еще раз\n')
    return id_user, soc_network, user_storage

def do_vkontakte():
    """Формирование json файла с фотографиями из профиля vkontakte, которые нужно выгрузить"""
    closed_status = vk.get_user()

    if closed_status == True:
        print('\n(!) Извините, но профиль закрыт')
        print('Выгрузить фотографии не получиться\n')
    else:
        print('Откуда загрузить фотографии?')
        get_answer = False
        while get_answer == False:
            album_type_answer = input('Введите 0 (из профиля), 1 (из альбомов) или 2 (со стены): ')
            if album_type_answer == '0':
                album_type = "profile"
                photo_album_user = vk.get_photos_info(album_type)
                number_of_photos = photo_album_user['count']

                print(f'\nУ вас {number_of_photos} фотографий')
                print('Сколько фотографий загрузить?')
                how_many_photos = int(input('> '))

                json_file_photos = vk.get_json_file_photos(photo_album_user['items'], how_many_photos)
                return json_file_photos
                get_answer = True
            elif album_type_answer == '1':
                album_id_list = vk.get_albums_info()
                photo_items_list = {'items': []}
                for album_type in album_id_list:
                    photo_album_user = vk.get_photos_info(album_type)
                    for photo_item in photo_album_user['items']:
                        photo_items_list['items'].append(photo_item)

                number_of_photos = len(photo_items_list['items'])
                if number_of_photos != 0:
                    print(f'\nУ вас {number_of_photos} фотографий')
                    print('Сколько фотографий загрузить?')
                    how_many_photos = int(input('> '))

                    json_file_photos = vk.get_json_file_photos(photo_items_list['items'], how_many_photos)
                    return json_file_photos
                    get_answer = True
                else:
                    print('\nВ ваших альбомах нет фотографий')
                    print('Но возможно они есть в профиле или на стене\n')
            elif album_type_answer == '2':
                album_type = "wall"
                photo_album_user = vk.get_photos_info(album_type)
                number_of_photos = photo_album_user['count']
                if number_of_photos != 0:
                    print(f'\nУ вас {number_of_photos} фотографий')
                    print('Сколько фотографий загрузить?')
                    how_many_photos = int(input('> '))

                    json_file_photos = vk.get_json_file_photos(photo_album_user['items'], how_many_photos)
                    return json_file_photos
                    get_answer = True
                else:
                    print('\nНа вашей стене нет фотографий')
                    print('Но возможно они есть в профиле или в альбомах\n')
            else:
                print('\n(!) Неверный ввод. Попробуйте еще раз')

def do_odnoklassniki():
    """Формирование json файла с фотографиями из профиля Одноклассников, которые нужно выгрузить"""
    photos_list = []
    user_photos = ok.get_user_photos()

    for photo in user_photos['photos']:
        photos_list.append(photo)

    id_albums = ok.get_albums_info()
    album_photos = ok.get_albums_photos(id_albums)
    photos_list.extend(album_photos)

    number_of_photos = len(photos_list)
    print(f'\nУ вас {number_of_photos} фотографий')
    print('Сколько фотографий загрузить?')
    how_many_photos = int(input('> '))

    json_file_photos = ok.get_json_file_photos(photos_list, how_many_photos)
    return json_file_photos

def do_yandex_disk(photos_list, social_network):
    """Передача списка фотографий для загрузки на Яндекс.Диск"""
    folder_name = ydisk.create_folder(social_network)
    ydisk.upload_file(photos_list, folder_name)

def do_google_drive(photos_list, social_network):
    """ередача списка фотографий для загрузки на Google.Drive"""
    credentials = gdrive.get_credentials()
    id_folder = gdrive.create_folder(credentials, social_network)
    gdrive.upload_files(credentials, photos_list, id_folder)

def create_upload_file_data(json_file_photos):
    """Формирование списка фотографий из имени и ссылки для дальнейшей загрузки"""
    file_name_list = []
    url_list = []

    for file in json_file_photos['photos']:
        file_name_list.append(file['file_name'])
        url_list.append(file['url_photo'])
    photos_list_to_upload = list(zip(file_name_list, url_list))
    return photos_list_to_upload

def save_json_file_photo(result_data):
    """Сохранение информации о фото в json файл"""
    with open('photos_info_log.json', 'w') as file:
        json.dump(result_data, file, ensure_ascii=False, indent=3)
        print('\nИнформация о фото сохранена в json файл photos_info_log.json')


if __name__ == '__main__':

    result_user_info = get_user_info()

    id_user = result_user_info[0] # ID профиля vk или ok
    user_snetwork = result_user_info[1] # соц.сеть (vk или ok)
    user_storage = result_user_info[2] # хранилище (yandex.disk или google.drive)

    vk = Vkontakte(id_user)
    ok = Odnoklassniki(id_user)
    ydisk = YandexDisk()
    gdrive = GoogleDrive()

    if user_snetwork == 'vk':
        json_file_photos = do_vkontakte()
    elif user_snetwork == 'ok':
        json_file_photos = do_odnoklassniki()

    photos_list_to_upload = create_upload_file_data(json_file_photos)

    if user_storage == 'yandex':
        do_yandex_disk(photos_list_to_upload, user_snetwork)
    elif user_storage == 'google':
        do_google_drive(photos_list_to_upload, user_snetwork)

    print('\n...............')

    save_json_file_photo(json_file_photos)