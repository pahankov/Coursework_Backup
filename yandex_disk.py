import requests

class YandexDisk:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://cloud-api.yandex.net/v1/disk"

    def file_exists(self, path):
        url = f"{self.api_url}/resources"
        headers = {
            "Authorization": f"OAuth {self.access_token}"
        }
        params = {
            "path": path
        }
        response = requests.get(url, headers=headers, params=params)
        return response.status_code == 200

    def create_folder(self, path):
        url = f"{self.api_url}/resources"
        headers = {
            "Authorization": f"OAuth {self.access_token}"
        }
        params = {
            "path": path
        }
        response = requests.put(url, headers=headers, params=params)
        response.raise_for_status()

    def upload_external_resource(self, url, path):
        upload_url = f"{self.api_url}/resources/upload"
        headers = {
            "Authorization": f"OAuth {self.access_token}"
        }
        params = {
            "path": path,
            "url": url
        }
        response = requests.post(upload_url, headers=headers, params=params)
        response.raise_for_status()
