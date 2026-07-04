# Використовуємо офіційний Python image
FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements.txt
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проекту
COPY . .

# Встановлюємо права доступу
RUN chmod +x main.py

# Запускаємо парсер
CMD ["python", "main.py"]
