# yandex_disk.py
import requests
import time

class YandexDisk:
    def __init__(self, token):
        self.token = token

    def create_folder(self, folder_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': folder_name}
        response = requests.put(url, headers=headers, params=params)
        return response.status_code == 201

    def file_exists(self, file_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': file_name}
        response = requests.get(url, headers=headers, params=params)
        return response.status_code == 200

    def upload_file(self, file_path, file_name):
        try:
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {'Authorization': f'OAuth {self.token}'}
            params = {'path': file_name, 'overwrite': 'true'}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            upload_url = response.json()['href']

            with open(file_path, 'rb') as file:
                response = requests.put(upload_url, files={'file': file})
                response.raise_for_status()
            print(f"Фотография успешно загружена: {file_name}")
        except (requests.RequestException, IOError) as e:
            print(f"Ошибка при загрузке на Яндекс.Диск: {e}")
