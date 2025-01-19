import requests
import logging

class YandexDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': f'OAuth {self.token}'}

    def create_url(self, endpoint):
        return f'https://cloud-api.yandex.net/v1/disk/{endpoint}'

    def create_folder(self, folder_name):
        logging.info(f"Создание папки '{folder_name}' на Яндекс.Диске.")
        try:
            url = self.create_url('resources')
            headers = self.get_headers()
            params = {'path': folder_name}
            response = requests.put(url, headers=headers, params=params)
            if response.status_code == 201:
                logging.info(f"Папка '{folder_name}' успешно создана на Яндекс.Диске.")
            elif response.status_code == 409:
                logging.info(f"Папка '{folder_name}' уже существует на Яндекс.Диске.")
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Ошибка при создании папки на Яндекс.Диске: {e}")

    def file_exists(self, file_name):
        try:
            url = self.create_url('resources')
            headers = self.get_headers()
            params = {'path': file_name}
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Ошибка при проверке наличия файла на Яндекс.Диске: {e}")
            return False

    def upload_file(self, file_path, file_name):
        try:
            url = self.create_url('resources/upload')
            headers = self.get_headers()
            params = {'path': file_name, 'overwrite': 'true'}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            upload_url = response.json()['href']

            with open(file_path, 'rb') as file:
                response = requests.put(upload_url, files={'file': file})
                response.raise_for_status()
            logging.info(f"Фотография успешно загружена: {file_name}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при загрузке на Яндекс.Диск: {e}")
        except IOError as e:
            logging.error(f"Ошибка при открытии файла для загрузки на Яндекс.Диск: {e}")
