import requests
import logging

class YandexDisk:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def _make_request(self, method, endpoint, **kwargs):
        url = f'{self.BASE_URL}{endpoint}'
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Ошибка при выполнении запроса: {e}")
            return None

    def create_folder(self, folder_name):
        logging.info(f"Создание папки '{folder_name}' на Яндекс.Диске.")
        response = self._make_request('PUT', 'resources', params={'path': folder_name})
        if response:
            if response.status_code == 201:
                logging.info(f"Папка '{folder_name}' успешно создана на Яндекс.Диске.")
            elif response.status_code == 409:
                logging.info(f"Папка '{folder_name}' уже существует на Яндекс.Диске.")

    def file_exists(self, file_name):
        response = self._make_request('GET', 'resources', params={'path': file_name})
        if response:
            return response.status_code == 200
        return False

    def upload_file(self, file_path, file_name):
        response = self._make_request('GET', 'resources/upload', params={'path': file_name, 'overwrite': 'true'})
        if response:
            upload_url = response.json()['href']
            try:
                with open(file_path, 'rb') as file:
                    upload_response = requests.put(upload_url, files={'file': file})
                    upload_response.raise_for_status()
                logging.info(f"Фотография успешно загружена: {file_name}")
            except IOError as e:
                logging.error(f"Ошибка при открытии файла для загрузки на Яндекс.Диск: {e}")

    def check_token(self):
        response = self._make_request('GET', '')
        return response is not None
