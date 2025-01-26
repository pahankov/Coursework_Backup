import os
import requests
from tqdm import tqdm
import logging
from vk_api import VKAPI
from yandex_disk import YandexDisk
from file_handler import FileHandler

class PhotoBackup:
    def __init__(self, vk_token, yandex_token):
        self.vk_api = VKAPI(vk_token)
        self.yandex_disk = YandexDisk(yandex_token)
        self.logger = logging.getLogger('PhotoBackup')
        self.file_handler = FileHandler()

    def backup_photos(self, vk_user_id, photos_count):
        user_info = self.vk_api.get_user_info(vk_user_id)
        if isinstance(user_info, list) and user_info and user_info[0].get('is_closed'):
            error_message = "Профиль пользователя закрыт."
            self.logger.error(error_message)
            print(f"Ошибка: {error_message}")
            return

        photos = self.vk_api.get_photos(vk_user_id, count=photos_count)
        if photos is None or 'error' in photos:
            error_message = "Не удалось получить фотографии. Пожалуйста, проверьте, что вы ввели правильный ID пользователя."
            self.logger.error(error_message)
            print(f"Ошибка: {error_message}")
            return
        if 'items' in photos and len(photos['items']) == 0:
            error_message = "У пользователя нет фотографий."
            self.logger.error(error_message)
            print(f"Ошибка: {error_message}")
            return

        # Проверяем наличие папки на Яндекс.Диске
        if self.yandex_disk.file_exists("VK_Photos"):
            self.logger.info("Папка 'VK_Photos' уже существует.")
            print("Папка 'VK_Photos' уже существует.")
        else:
            self.yandex_disk.create_folder("VK_Photos")
            self.logger.info("Папка 'VK_Photos' была создана.")
            print("Папка 'VK_Photos' была создана.")

        photos_info = []
        for index, photo in enumerate(tqdm(photos['items'], desc='Сохранение фотографий')):
            max_size_photo = max(photo['sizes'], key=lambda size: size['width'] * size['height'])
            likes_count = photo.get('likes', {}).get('count', 'unknown')
            unique_file_name = f"{likes_count}.jpg" if likes_count != 'unknown' else f"photo_{photo['date']}.jpg"

            # Выводим отладочную информацию
            self.logger.debug(f"Обработка фотографии {index + 1}/{photos_count}: {max_size_photo['url']}")

            try:
                # Загружаем фото напрямую на Яндекс.Диск
                self.yandex_disk.upload_external_resource(max_size_photo['url'], f"VK_Photos/{unique_file_name}")
                self.logger.info(f"Фотография успешно загружена на Яндекс.Диск: {unique_file_name}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Ошибка при загрузке фотографии на Яндекс.Диск: {e}")
                continue

            photos_info.append({
                'file_name': unique_file_name,
                'url': max_size_photo['url'],
                'width': max_size_photo['width'],
                'height': max_size_photo['height'],
                'type': max_size_photo['type']
            })

        self.file_handler.save_photos_info(photos_info, 'photos_info.json')
        self.logger.info('Резервное копирование завершено. Информация о фотографиях сохранена в photos_info.json.')

        print("Фотографии успешно сохранены на Яндекс.Диск.")
        self.logger.info("Фотографии успешно сохранены на Яндекс.Диск.")

