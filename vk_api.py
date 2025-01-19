import requests
import logging

class VKAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.vk.com/method/'
        self.version = '5.131'

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params.update({'access_token': self.token, 'v': self.version})
        url = f'{self.base_url}{endpoint}'
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            if 'error' in result:
                error_code = result['error'].get('error_code', 'Unknown')
                error_msg = result['error'].get('error_msg', 'Unknown error')
                logging.error(f"Ошибка в ответе: код ошибки {error_code}, сообщение: {error_msg}")
                if error_code == 5:
                    return {'error': 'Неверный токен ВКонтакте. Пожалуйста, проверьте ваш токен.'}
                return None
            return result.get('response')
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе: {e}")
            return None

    def get_user_info(self, user_id):
        params = {
            'user_ids': user_id,
            'fields': 'is_closed'
        }
        user_info = self._make_request('users.get', params)
        if user_info and 'error' in user_info:
            return user_info
        if user_info and user_info[0].get('is_closed'):
            logging.error("Профиль пользователя закрыт.")
            return {'error': 'Профиль пользователя закрыт.'}
        return user_info[0] if user_info else None

    def get_photos(self, user_id, count=5):
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': count
        }
        photos = self._make_request('photos.get', params)
        if photos and 'error' in photos:
            return photos
        if photos and len(photos['items']) == 0:
            logging.error("У пользователя нет фотографий.")
            return {'error': 'У пользователя нет фотографий.'}
        return photos['items'] if photos else None

