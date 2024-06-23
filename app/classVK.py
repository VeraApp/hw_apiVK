"""Класс VK

Данный класс позволяет по токену и ид пользователя, скачать изображения из социальной сети VK.
"""

import requests
import log

class VK:
    API_BASE_URL = 'https://api.vk.com/method'
    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.user_id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def __build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.199'
        }

    def get_profile_photos(self):
         params = self.get_common_params()
         params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': '1'})
         try:
            response = requests.get(self.__build_url('photos.get'), params=params)
            log.logging.info("Downloading images")
         except:
             log.logging.error(f"Loading image to VK, status_code: {response.status_code}")

         return response.json()