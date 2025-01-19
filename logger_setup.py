import logging

class LoggerSetup:
    def __init__(self, log_file='app.log'):
        self.logger = logging.getLogger('backup_logger')
        self.logger.setLevel(logging.INFO)

        # Проверяем и удаляем существующие обработчики
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Создаем обработчик для записи в файл с указанием кодировки UTF-8 и режимом дозаписи
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

