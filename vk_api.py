import requests

class VKAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://api.vk.com/method"

    def get_user_info(self, user_id):
        url = f"{self.api_url}/users.get"
        params = {
            "user_ids": user_id,
            "access_token": self.access_token,
            "v": "5.131"
        }
        response = requests.get(url, params=params)
        result = response.json()
        if 'error' in result:
            return {'error': result['error']}
        return result.get('response', [])

    def get_photos(self, user_id, count=5):
        url = f"{self.api_url}/photos.get"
        params = {
            "owner_id": user_id,
            "album_id": "profile",
            "rev": 1,
            "count": count,
            "photo_sizes": 1,  # Включает размеры фотографий в ответ
            "access_token": self.access_token,
            "v": "5.131"
        }
        response = requests.get(url, params=params)
        result = response.json()
        if 'error' in result:
            return {'error': result['error']}
        return result.get('response', {})
