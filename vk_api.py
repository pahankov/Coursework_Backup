import requests
import logging

class VKAPI:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': f'OAuth {self.token}'}

    @staticmethod
    def create_url(endpoint):
        return f'https://api.vk.com/method/{endpoint}'

    def get_user_info(self, user_id):
        try:
            url = self.create_url('users.get')
            params = {
                'user_ids': user_id,
                'access_token': self.token,
                'v': '5.131',
                'fields': 'is_closed'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            if 'response' in result and result['response']:
                user_info = result['response'][0]
                if user_info.get('is_closed'):
                    logging.error("Профиль пользователя закрыт.")
                    return {'error': 'Профиль пользователя закрыт.'}
                return user_info
            else:
                error_code = result.get('error', {}).get('error_code', 'Unknown')
                error_msg = result.get('error', {}).get('error_msg', 'Unknown error')
                if error_code == 'Unknown':
                    error_msg = 'Пользователь не найден или произошла неизвестная ошибка.'
                logging.error(f"Ошибка в ответе: код ошибки {error_code}, сообщение: {error_msg}")
                return {'error': f"Ошибка в ответе: код ошибки {error_code}, сообщение: {error_msg}"}
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе информации о пользователе: {e}")
            return {'error': f"Ошибка при запросе информации о пользователе: {e}"}

    def get_photos(self, user_id, count=5):
        try:
            url = self.create_url('photos.get')
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
                if len(result['response']['items']) == 0:
                    logging.error("У пользователя нет фотографий.")
                    return {'error': 'У пользователя нет фотографий.'}
                return result['response']['items']
            else:
                error_code = result.get('error', {}).get('error_code', 'Unknown')
                error_msg = result.get('error', {}).get('error_msg', 'Unknown error')
                logging.error(f"Ошибка в ответе: код ошибки {error_code}, сообщение: {error_msg}")
                if error_code == 5:
                    logging.error("Ошибка авторизации VK: неверный токен доступа.")
                elif error_code == 113:
                    logging.error("ID пользователя VK не существует.")
                return None
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе фотографий: {e}")
            return None
