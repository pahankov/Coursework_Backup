import json
import os
import requests
import logging
from tqdm import tqdm
from vk_api import VKAPI
from yandex_disk import YandexDisk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_photos_info(photos_info, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(photos_info, file, ensure_ascii=False, indent=4)
        logging.info(f"Информация о фотографиях успешно сохранена в {file_path}")
    except IOError as e:
        logging.error(f"Ошибка при сохранении информации в файл {file_path}: {e}")

def main():
    vk_user_id = input('Введите ID пользователя VK: ')
    yandex_token = input('Введите токен Яндекс.Диска: ')
    photos_count = int(input('Введите количество фотографий для резервного копирования (по умолчанию 5): ') or 5)

    vk_api = VKAPI()
    yandex_disk = YandexDisk(yandex_token)

    # Создаем папку для сохранения фотографий
    if not os.path.exists('photos'):
        os.makedirs('photos')

    # Создаем папку на Яндекс.Диске
    yandex_disk.create_folder("VK_Photos")

    photos = vk_api.get_photos(vk_user_id, count=photos_count)
    if photos is None:
        logging.error("Не удалось получить фотографии. Пожалуйста, проверьте, что вы ввели правильный токен и ID пользователя.")
        return

    photos_info = []

    for photo in tqdm(photos, desc='Сохранение фотографий'):
        max_size_photo = max(photo['sizes'], key=lambda size: size['width'] * size['height'])
        file_name = f"{photo['likes']['count']}.jpg"
        if any(p['file_name'] == file_name for p in photos_info):
            file_name = f"{photo['likes']['count']}_{photo['date']}.jpg"
        file_path = os.path.join('photos', file_name)

        # Сохраняем фотографию на диск
        try:
            with open(file_path, 'wb') as file:
                file.write(requests.get(max_size_photo['url']).content)
            logging.info(f"Фотография успешно сохранена на диск: {file_path}")
        except IOError as e:
            logging.error(f"Ошибка при сохранении фотографии на диск {file_path}: {e}")
            continue

        # Проверяем наличие файла на Яндекс.Диске и добавляем уникальный суффикс, если файл существует
        unique_file_name = file_name
        suffix = 1
        while yandex_disk.file_exists(f"VK_Photos/{unique_file_name}"):
            unique_file_name = f"{file_name.split('.')[0]}_{suffix}.jpg"
            suffix += 1

        # Загружаем фотографию на Яндекс.Диск
        try:
            yandex_disk.upload_file(file_path, f"VK_Photos/{unique_file_name}")
        except Exception as e:
            logging.error(f"Ошибка при загрузке фотографии {file_path} на Яндекс.Диск: {e}")
            continue

        photos_info.append({
            'file_name': unique_file_name,
            'size': max_size_photo['type']
        })

    # Сохраняем информацию о фотографиях в JSON-файл
    save_photos_info(photos_info, 'photos_info.json')

    logging.info('Резервное копирование завершено. Информация о фотографиях сохранена в photos_info.json.')

if __name__ == '__main__':
    main()
