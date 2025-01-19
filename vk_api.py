import requests
import logging

class VKAPI:
    def __init__(self):
        self.token = "vk1.a.qaBLM8IVuTQJxmYSjqK_PF0-6U_MUqygqPLSFIZ6F0GYrkybRFiHkbEmGJeLzORCPQD2_5Qt_qLTDqZWsNhmMpFPL6jqIJIWGuUpQR4pyHGd2RO2Tf3UHEzgQhaFYZ6OimnjpM6sTnl0ACoiDbg2IYm-aEvCzx0W-SG-c6LgY13D9dDiQwr1x2i_jmbMFldA"

    def get_headers(self):
        return {'Authorization': f'OAuth {self.token}'}

    def create_url(self, endpoint):
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
                    logging.error("ID пользователя VK не существует или у пользователя нет фотографий.")
                    return None
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

