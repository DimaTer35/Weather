import requests
from dotenv import load_dotenv
import os
from database import create_table, save_weather, get_history, clear_history
from datetime import datetime

# Загружаем API-ключ
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Функция получения погоды
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        }
    else:
        return {"error": f"Ошибка: {response.status_code}"}

# Основной код
create_table()  # Создаём таблицу, если её нет
while True:
    print("\n1. Получить погоду")
    print("2. Показать историю запросов")
    print("3. Очистить историю")
    print("4. Выйти")
    choice = input("Выберите действие: ")

    if choice == "1":
        city = input("Введите город: ")
        weather = get_weather(city)
        if "error" in weather:
            print(weather["error"])
        else:
            print(f"Город: {weather['city']}")
            print(f"Температура: {weather['temperature']}°C")
            print(f"Погода: {weather['weather']}")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_weather(weather["city"], weather["temperature"], weather["weather"], now)
    elif choice == "2":
        history = get_history()
        print("\nИстория запросов:")
        if history:
            for record in history:
                print(f"{record[4]} - {record[1]}: {record[2]}°C, {record[3]}")
        else:
            print("История пуста.")
    elif choice == "3":
        clear_history()
        print("История очищена.")
    elif choice == "4":
        print("Выход...")
        break
    else:
        print("Некорректный выбор, попробуйте ещё раз.")
