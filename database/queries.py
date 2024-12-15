import sqlite3
from database.connect import connect_db


# Функция для регистрации пользователя в таблице users
def register(user_id: int):
    """
    Регистрирует нового пользователя. Если пользователь уже зарегистрирован,
    запись игнорируется (INSERT OR IGNORE).
    """
    conn = connect_db()  # Подключение к базе данных
    cursor = conn.cursor()
    # Если пользователь не существует, добавить запись с нулевым балансом и статусом 'user'
    cursor.execute("INSERT OR IGNORE INTO users (user_id, role, balance) VALUES (?, ?, 0)", (user_id, 'user'))
    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем подключение


# Функция для записи статистики использования ботом
def record_stat(user_id: int):
    """
    Записывает в таблицу stats информацию о том, что пользователь 
    воспользовался ботом. Сохраняются user_id и текущая дата.
    """
    conn = connect_db()  # Подключение к базе данных
    cursor = conn.cursor()
    # Вставка записи в таблицу stats с текущей датой (DATE('now'))
    cursor.execute("INSERT INTO stats (user_id, date) VALUES (?, DATE('now'))", (user_id,))
    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем подключение


# Функция для получения общей статистики использования бота
def get_stats() -> str:
    """
    Генерирует текстовый отчет со статистикой использования бота:
    - общее число пользователей,
    - количество пользователей за сегодня,
    - общее число запросов,
    - количество запросов за сегодня.
    """
    conn = connect_db()  # Подключение к базе данных
    cursor = conn.cursor()

    # Считаем общее количество уникальных пользователей
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM stats")
    total_users = cursor.fetchone()[0]

    # Считаем уникальных пользователей за сегодня
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM stats WHERE date = DATE('now')")
    today_users = cursor.fetchone()[0]

    # Общее количество запросов
    cursor.execute("SELECT COUNT(*) FROM stats")
    total_requests = cursor.fetchone()[0]

    # Количество запросов за сегодня
    cursor.execute("SELECT COUNT(*) FROM stats WHERE date = DATE('now')")
    today_requests = cursor.fetchone()[0]

    conn.close()  # Закрываем подключение

    # Формируем строку со статистикой
    return (f"📊 Статистика использования бота:\n"
            f" ├ Всего пользователей: {total_users}\n"
            f" ├ Пользователей сегодня: {today_users}\n"
            f" ├ Всего запросов: {total_requests}\n"
            f" └ Запросов сегодня: {today_requests}")


# Функция для обновления баланса пользователя
def update_balance(user_id: int, amount: float):
    """
    Обновляет баланс пользователя. К текущему балансу 
    добавляется указанная сумма.
    
    :param user_id: Идентификатор пользователя
    :param amount: Сумма для добавления к текущему балансу
    """
    conn = connect_db()  # Подключение к базе данных
    cursor = conn.cursor()
    # Обновляем баланс пользователя на указанную сумму
    cursor.execute("UPDATE users SET balance = balance + ? WHERE users.user_id = ?", (amount, user_id))
    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем подключение


# Функция для получения текущего баланса пользователя
def get_balance(user_id: int):
    """
    Возвращает текущий баланс пользователя.

    :param user_id: Идентификатор пользователя
    :return: Текущий баланс пользователя
    """
    conn = connect_db()  # Подключение к базе данных
    cursor = conn.cursor()
    # Получаем баланс пользователя из таблицы users
    cursor.execute("SELECT users.balance FROM users WHERE users.user_id = ?", (user_id,))
    total_amount = cursor.fetchone()[0]
    conn.close()  # Закрываем подключение

    return total_amount