from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build

import os
import io
import requests
from tqdm import tqdm

SCOPES = ['https://www.googleapis.com/auth/drive']

# !!!
# Для корректной работы нужно создать ключи доступа OAuth 2.0 в приложении в Google Cloud Platform
# Сохранить json файл с реквизитами, переименовать его в google_client_secret.json и поместить в корень проекта

class GoogleDrive:

    def __init__(self):
        self.scopes = SCOPES

    def get_credentials(self):
        """Получаем реквизиты из google_client_secret.json
        и формируем token.json для дальнейшего доступа к Google.Drive"""
        creds = None
        if os.path.exists('google_token.json'):
            creds = Credentials.from_authorized_user_file('google_token.json', self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_client_secret.json', self.scopes)
                creds = flow.run_local_server(port=8080)
            with open('google_token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def create_folder(self, credentials, social_network):
        """Создаем папку в Google.Drive"""
        service = build('drive', 'v3', credentials=credentials)

        if social_network == 'vk':
            folder_name = 'VK_Photos'
        elif social_network == 'ok':
            folder_name = 'OK_Photos'

        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        result = service.files().create(body=file_metadata, fields="id").execute()
        return result['id']

    def upload_files(self, credentials, photo_list, id_folder):
        """Загружаем файлы в Google.Drive"""
        service = build('drive', 'v3', credentials=credentials)
        for photo in tqdm(photo_list):
            file_name = photo[0]
            url = photo[1]
            url_file = io.BytesIO(requests.get(url).content)
            file_metadata = {
                "name": file_name,
                "parents": [id_folder]
            }
            media = MediaIoBaseUpload(url_file, mimetype="image/jpg", resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print('\nВсе фото успешно загружены!')