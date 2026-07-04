#!/usr/bin/env python
"""
Python скрипт для створення ZIP архіву для деплойменту на Wispbyte
Без GitHub - просто завантажуємо файли
"""

import os
import shutil
import zipfile
from pathlib import Path

# Налаштування
PROJECT_DIR = r"d:\Dota tool box\Onibi"
OUTPUT_ZIP = r"d:\Dota tool box\onibi-parser.zip"

# Файли які потрібно включити
INCLUDE_FILES = [
    "config.py",
    "main.py",
    "steam_parser.py",
    "telegram_bot.py",
    "requirements.txt",
    "Dockerfile",
    "README.md",
    "DEPLOYMENT.md",
    "DEPLOYMENT_NO_GITHUB.md",
    "test_deployment.py",
    ".env",
]

def create_deployment_zip():
    """Створює ZIP архів для деплойменту."""
    
    print("=" * 60)
    print("🔧 ПІДГОТОВКА ZIP АРХІВУ ДЛЯ WISPBYTE")
    print("=" * 60)
    
    # Видаляємо старий ZIP якщо існує
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)
        print("✅ Старий архів видалено")
    
    # Створимо ZIP архів
    print("\n📦 Додаю файли до архіву...")
    
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in INCLUDE_FILES:
            file_path = os.path.join(PROJECT_DIR, filename)
            
            # Перевіряємо чи файл існує
            if os.path.exists(file_path):
                # Додаємо файл до архіву
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname=arcname)
                print(f"  ✅ Додано: {filename}")
            else:
                print(f"  ⚠️  Не знайдено: {filename}")
    
    # Показуємо інформацію про архів
    file_size = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    
    print("\n" + "=" * 60)
    print("✅ АРХІВ ГОТОВИЙ!")
    print("=" * 60)
    print(f"Шлях: {OUTPUT_ZIP}")
    print(f"Розмір: {file_size:.2f} MB")
    
    print("\n📋 НАСТУПНІ КРОКИ:")
    print("1. Перейдіть на Wispbyte панель (wispbyte.com)")
    print("2. Перейдіть до Files → Upload Files")
    print("3. Виберіть цей архів: onibi-parser.zip")
    print("4. Розархівуйте на сервері:")
    print("   $ cd /home/container")
    print("   $ unzip onibi-parser.zip")
    print("5. Встановіть залежності:")
    print("   $ pip install -r requirements.txt")
    print("6. Встановіть Environment Variables:")
    print("   - TELEGRAM_BOT_TOKEN")
    print("   - TELEGRAM_CHAT_ID")
    print("7. Запустіть Startup Command:")
    print("   $ python main.py")
    print("=" * 60)
    
    return OUTPUT_ZIP

if __name__ == "__main__":
    try:
        create_deployment_zip()
        print("\n✨ Все готово для деплойменту!")
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        exit(1)
