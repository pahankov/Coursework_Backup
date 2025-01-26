import configparser
from photo_backup import PhotoBackup
from logger_setup import LoggerSetup

# Настройка логирования
logger_setup = LoggerSetup()
logger = logger_setup.get_logger()

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('config.ini')

VK_ACCESS_TOKEN = config.get('VK', 'ACCESS_TOKEN')
YANDEX_ACCESS_TOKEN = config.get('YANDEX', 'ACCESS_TOKEN')

def main():
    photo_backup = PhotoBackup(VK_ACCESS_TOKEN, YANDEX_ACCESS_TOKEN)

    while True:
        vk_user_id = input('Введите ID пользователя VK: ')
        user_info = photo_backup.vk_api.get_user_info(vk_user_id)
        if not user_info:
            error_message = "Не удалось получить информацию о пользователе. Пожалуйста, проверьте, что вы ввели правильный ID пользователя."
            print(f"Ошибка: {error_message}")
            logger.error(error_message)
            continue
        if 'error' in user_info:
            error_message = user_info['error']['error_msg'] if 'error_msg' in user_info['error'] else "Произошла ошибка при получении информации о пользователе."
            print(f"Ошибка: {error_message}")
            logger.error(error_message)
            continue
        if isinstance(user_info, list) and user_info and user_info[0].get('is_closed'):
            error_message = "Профиль пользователя закрыт."
            print(f"Ошибка: {error_message}")
            logger.error(error_message)
            continue
        if isinstance(user_info, list) and len(user_info) == 0:
            error_message = "Пользователь с указанным ID не найден."
            print(f"Ошибка: {error_message}")
            logger.error(error_message)
            continue

        # Проверка наличия фотографий у пользователя
        photos = photo_backup.vk_api.get_photos(vk_user_id, count=1)
        if not photos or 'error' in photos or ('items' in photos and len(photos['items']) == 0):
            error_message = "У пользователя нет фотографий. Пожалуйста, введите другой ID пользователя."
            print(f"Ошибка: {error_message}")
            logger.error(error_message)
            continue
        break

    photos_count_input = input('Введите количество фотографий для резервного копирования (по умолчанию 5): ')
    photos_count = int(photos_count_input) if photos_count_input else 5

    photo_backup.backup_photos(vk_user_id, photos_count)

if __name__ == '__main__':
    main()
