import sqlite3

from config_data.config import Config


def connect_db():
    # Создаем экземпляр класса Config для получения конфигурационных данных
    config = Config()
    # Получаем путь к базе данных из конфигурационного объекта
    path = config.DATABASE_PATH

    # Устанавливаем соединение с базой данных по указанному пути
    conn = sqlite3.connect(path)
    # Возвращаем объект соединения с базой данных
    return conn
