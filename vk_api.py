# vk_api.py
import requests

class VKAPI:
    def __init__(self, token):
        self.token = token

    def get_photos(self, user_id, count=5):
        try:
            url = 'https://api.vk.com/method/photos.get'
            params = {
                'owner_id': user_id,
                'album_id': 'profile',
                'access_token': self.token,
                'v': '5.131',
                'extended': 1,
                'photo_sizes': 1,
                'count': count
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            if 'response' in result:
                return result['response']['items']
            else:
                print(f"Ошибка в ответе: {result}")
                return None
        except requests.RequestException as e:
            print(f"Ошибка при запросе фотографий: {e}")
            return None
