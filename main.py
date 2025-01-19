import os
import sys
import logging
import requests
from tqdm import tqdm
from vk_api import VKAPI
from yandex_disk import YandexDisk
from logger_setup import LoggerSetup
from file_handler import FileHandler

# Отключаем корневой логгер
logging.getLogger().setLevel(logging.CRITICAL)

class ExitProgramException(Exception):
    pass

# Настройка логирования
logger_setup = LoggerSetup()
logger = logger_setup.get_logger()
file_handler = FileHandler()

def main():
    vk_api = VKAPI("vk1.a.qaBLM8IVuTQJxmYSjqK_PF0-6U_MUqygqPLSFIZ6F0GYrkybRFiHkbEmGJeLzORCPQD2_5Qt_qLTDqZWsNhmMpFPL6jqIJIWGuUpQR4pyHGd2RO2Tf3UHEzgQhaFYZ6OimnjpM6sTnl0ACoiDbg2IYm-aEvCzx0W-SG-c6LgY13D9dDiQwr1x2i_jmbMFldA")
    try:
        while True:
            vk_user_id = input('Введите ID пользователя VK (или нажмите Escape для выхода): ')
            if vk_user_id.lower() == 'escape':
                print("Выход из программы.")
                raise ExitProgramException()

            user_info = vk_api.get_user_info(vk_user_id)
            if user_info is None:
                error_message = "Не удалось получить информацию о пользователе. Пожалуйста, проверьте, что вы ввели правильный ID пользователя."
                print(f"Ошибка: {error_message}")
                logger.error(error_message)
                continue

            if 'error' in user_info:
                error_message = user_info['error']
                print(f"Ошибка: {error_message}")
                logger.error(error_message)
                continue

            if user_info.get('is_closed'):
                error_message = "Профиль пользователя закрыт."
                print(f"Ошибка: {error_message}")
                logger.error(error_message)
                continue

            photos = vk_api.get_photos(vk_user_id, count=5)
            if photos is None or 'error' in photos:
                error_message = photos.get('error') if photos else "У пользователя нет фотографий. Пожалуйста, проверьте, что вы ввели правильный ID пользователя."
                print(f"Ошибка: {error_message}")
                logger.error(error_message)
                continue

            break

        while True:
            yandex_token = input('Введите токен Яндекс.Диска (или нажмите Escape для выхода): ')
            if yandex_token.lower() == 'escape':
                print("Выход из программы.")
                raise ExitProgramException()

            yandex_disk = YandexDisk(yandex_token)
            if not yandex_disk.check_token():
                error_message = "Некорректный токен Яндекс.Диска. Пожалуйста, введите правильный токен."
                print(f"Ошибка: {error_message}")
                logger.error(error_message)
                continue

            if yandex_disk.file_exists("VK_Photos"):
                print("Папка 'VK_Photos' уже существует.")
                logger.info("Папка 'VK_Photos' уже существует.")
            else:
                yandex_disk.create_folder("VK_Photos")
                print("Папка 'VK_Photos' была создана.")
                logger.info("Папка 'VK_Photos' была создана.")

            break

        photos_count_input = input('Введите количество фотографий для резервного копирования (по умолчанию 5): ')
        photos_count = int(photos_count_input) if photos_count_input else 5

        # Информируем пользователя о сохранении логов после ввода данных
        logger.info('Логи будут сохранены в файл app.log')

        # Создаем папку для сохранения фотографий
        if not os.path.exists('photos'):
            os.makedirs('photos')

        photos = vk_api.get_photos(vk_user_id, count=photos_count)
        if photos is None or 'error' in photos:
            error_message = photos.get('error') if photos else "Не удалось получить фотографии. Пожалуйста, проверьте, что вы ввели правильный токен и ID пользователя."
            print(f"Ошибка: {error_message}")
            logger.error(error_message)
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
                with open(file_path, 'wb') as file:  # Открываем файл в бинарном режиме
                    file.write(requests.get(max_size_photo['url']).content)
                logger.info(f"Фотография успешно сохранена на диск: {file_path}")
            except IOError as e:
                logger.error(f"Ошибка при сохранении фотографии на диск {file_path}: {e}")
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
                logger.error(f"Ошибка при загрузке фотографии {file_path} на Яндекс.Диск: {e}")
                continue

            photos_info.append({
                'file_name': unique_file_name,
                'size': max_size_photo['type']
            })

        # Сохраняем информацию о фотографиях в JSON-файл
        file_handler.save_photos_info(photos_info, 'photos_info.json')

        logger.info('Резервное копирование завершено. Информация о фотографиях сохранена в photos_info.json.')

        # Выводим сообщение об успешном сохранении фотографий
        print("Фотографии успешно сохранены на Яндекс.Диск.")
        logger.info("Фотографии успешно сохранены на Яндекс.Диск.")

    except ExitProgramException:
        sys.exit()

if __name__ == '__main__':
    main()











