"""Класс YandexDisk

Данный класс разработан для работы с Яндекс Диском.
В нем реализованы методы позволяющие создать папку на Яндекс Диске и загрузить в нее фотографии.
"""

import requests
import log

class YandexDisk:

    def __init__(self, access_token):
        self.token = access_token
        self.headers = {'Authorization': f'OAuth {access_token}'}

    def create_folder(self):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {
            'path': 'Image'
        }
        try:
            response = requests.put(url, params=params, headers=self.headers)
            if response.status_code >= 200 and response.status_code <= 200:
                log.logging.info("Folder created")
        except:
            log.logging.error(f"Creating folder on YandexDisk, status_code: {response.status_code}")
        return response.status_code

    def download_photos(self, name_file, url_file):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'Image/{name_file}',
            'url': url_file
        }
        try:
            response = requests.post(url, params=params, headers=self.headers)
        except:
            log.logging.error(f"Loading image to YandexDisk, status_code: {response.status_code}")
        return response.status_code

    def parse_photos(self, photo_info):
        for i, element in enumerate(photo_info):
            file_name = f'{element[0]}.jpg'
            url_photo = element[3]
            self.download_photos(file_name, url_photo)













