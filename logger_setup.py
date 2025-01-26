import logging

class LoggerSetup:
    def __init__(self):
        self.logger = logging.getLogger('backup_logger')
        self.logger.setLevel(logging.DEBUG)  # Устанавливаем уровень отладки

        # Создаем обработчик для вывода логов в файл с кодировкой UTF-8
        file_handler = logging.FileHandler('app.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Устанавливаем уровень отладки для обработчика

        # Создаем форматтер и добавляем его в обработчик
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Добавляем обработчик в логгер
        self.logger.addHandler(file_handler)

        # Отключаем пропагирование сообщений на корневой логгер
        self.logger.propagate = False

    def get_logger(self):
        return self.logger

