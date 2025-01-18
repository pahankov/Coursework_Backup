import requests

class YandexDisk:
    def __init__(self, token):
        self.token = token

    def create_folder(self, folder_name):
        try:
            url = 'https://cloud-api.yandex.net/v1/disk/resources'
            headers = {'Authorization': f'OAuth {self.token}'}
            params = {'path': folder_name}
            response = requests.put(url, headers=headers, params=params)
            if response.status_code == 409:
                print(f"Папка '{folder_name}' уже существует на Яндекс.Диске.")
            else:
                response.raise_for_status()
                print(f"Папка '{folder_name}' успешно создана на Яндекс.Диске.")
        except requests.RequestException as e:
            if response.status_code == 401:
                print("Ошибка при создании папки на Яндекс.Диске: неверный токен доступа.")
            else:
                print(f"Ошибка при создании папки на Яндекс.Диске: {e}")

    def file_exists(self, file_name):
        try:
            url = 'https://cloud-api.yandex.net/v1/disk/resources'
            headers = {'Authorization': f'OAuth {self.token}'}
            params = {'path': file_name}
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 404:
                return False  # Файл не найден, это нормально
            response.raise_for_status()
            return response.status_code == 200
        except requests.RequestException as e:
            if response.status_code == 401:
                print("Ошибка при проверке наличия файла на Яндекс.Диске: неверный токен доступа.")
            else:
                print(f"Ошибка при проверке наличия файла на Яндекс.Диске: {e}")
            return False

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
        except requests.RequestException as e:
            if response.status_code == 401:
                print("Ошибка при загрузке на Яндекс.Диск: неверный токен доступа.")
            else:
                print(f"Ошибка при загрузке на Яндекс.Диск: {e}")
        except IOError as e:
            print(f"Ошибка при открытии файла для загрузки на Яндекс.Диск: {e}")
