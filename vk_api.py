import requests

class VKAPI:
    def __init__(self):
        self.token = "vk1.a.qaBLM8IVuTQJxmYSjqK_PF0-6U_MUqygqPLSFIZ6F0GYrkybRFiHkbEmGJeLzORCPQD2_5Qt_qLTDqZWsNhmMpFPL6jqIJIWGuUpQR4pyHGd2RO2Tf3UHEzgQhaFYZ6OimnjpM6sTnl0ACoiDbg2IYm-aEvCzx0W-SG-c6LgY13D9dDiQwr1x2i_jmbMFldA"

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
                error_code = result.get('error', {}).get('error_code', 'Unknown')
                error_msg = result.get('error', {}).get('error_msg', 'Unknown error')
                print(f"Ошибка в ответе: код ошибки {error_code}, сообщение: {error_msg}")
                if error_code == 5:
                    print("Ошибка авторизации VK: неверный токен доступа.")
                return None
        except requests.RequestException as e:
            print(f"Ошибка при запросе фотографий: {e}")
            return None
