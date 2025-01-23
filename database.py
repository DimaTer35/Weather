import sqlite3

# Функция для подключения к базе данных
def connect_db():
    conn = sqlite3.connect("weather_history.db")  # Имя файла базы данных
    return conn

# Создание таблицы, если её нет
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            weather TEXT,
            datetime TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления записи
def save_weather(city, temperature, weather, datetime):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather (city, temperature, weather, datetime)
        VALUES (?, ?, ?, ?)
    ''', (city, temperature, weather, datetime))
    conn.commit()
    conn.close()

# Функция для получения всех записей
def get_history():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather ORDER BY datetime DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Функция для очистки истории
def clear_history():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM weather')
    conn.commit()
    conn.close()
