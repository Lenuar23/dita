# ============================================================
# Конфігурація Steam Dota 2 Market Parser
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram Bot ---
# Токен та Chat ID зберігаються у файлі .env (не пушиться в git)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- Steam Market ---
# Назва предмета яку шукаємо (точна назва як на маркеті)
# Приклади:
#   "Unusual Baby Roshan"
#   "Unusual Stumpy - Nature's Attendant"
#   "Unusual Skip the Delivery Frog"
#   "Unusual Cluckles the Brave"
ITEM_NAME = "Onibi"

# ID гри Dota 2 в Steam
DOTA2_APP_ID = 570

# --- Фільтр стилів (Onibi та подібні кур'єри) ---
# Вкажи номери стилів які тебе цікавлять
# Onibi має стилі від 1 до 21 (відкриваються грою)
# Якщо список порожній — покаже всі знайдені предмети
DESIRED_STYLES = [20, 21]

# --- Фільтр гемів / Ethereal & Prismatic Gems ---
# Для Unusual кур'єрів — вкажи назви гемів які тебе цікавлять
# Для Onibi це не потрібно — залиш порожнім
DESIRED_GEMS = []

# Максимальна ціна в USD (0 = без обмеження)
MAX_PRICE_USD = 15

# --- Інтервал перевірки ---
# Час між перевірками в секундах (не рекомендується менше 60 — Steam може заблокувати)
CHECK_INTERVAL_SECONDS = 120

# --- Логування ---
LOG_FILE = "parser.log"
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR

# Кількість результатів з маркету за один запит (макс 100)
RESULTS_COUNT = 100

# --- Проксі (опціонально) ---
# Якщо Steam блокує запити, можна використовувати проксі
# Формат: "http://user:pass@host:port" або "socks5://user:pass@host:port"
PROXY = os.getenv("PROXY", None)
