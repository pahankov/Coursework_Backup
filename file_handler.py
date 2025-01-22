import json
import logging

class FileHandler:
    def save_photos_info(self, photos_info, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(photos_info, f, ensure_ascii=False, indent=4)
            logging.info(f"Информация о фотографиях успешно сохранена в файл: {filename}")
        except Exception as e:
            logging.error(f"Ошибка при сохранении информации о фотографиях в файл {filename}: {e}")
