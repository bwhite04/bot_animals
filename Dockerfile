# Використовуємо офіційний Python runtime як базовий образ
FROM python:3.9-slim

# Встановлюємо робочий каталог у контейнері
WORKDIR /app

# Копіюємо вміст поточного каталогу у контейнер в /app
COPY . /app

# Встановлюємо всі необхідні пакунки, які зазначені у requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Робимо порт 5000 доступним для зовнішнього світу з цього контейнера
EXPOSE 6000

# Визначаємо змінну середовища
ENV NAME World

# Запускаємо bot.py при старті контейнера
CMD ["python", "bot.py"]
