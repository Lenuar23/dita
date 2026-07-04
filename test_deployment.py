#!/usr/bin/env python
"""
Скрипт тестування парсера перед деплойментом на Wispbyte.
Перевіряє всі залежності та конфігурацію.
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Перевіряє версію Python."""
    logger.info("🐍 Перевірка версії Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        logger.error(f"❌ Python 3.9+ потрібен. Встановлено: {version.major}.{version.minor}")
        return False
    logger.info(f"✅ Python {version.major}.{version.minor} OK")
    return True

def check_dependencies():
    """Перевіряє встановлені залежності."""
    logger.info("📦 Перевірка залежностей...")
    required = ['requests', 'dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            logger.info(f"  ✅ {package}")
        except ImportError:
            logger.error(f"  ❌ {package} - встановіть: pip install -r requirements.txt")
            missing.append(package)
    
    return len(missing) == 0

def check_config():
    """Перевіряє конфігурацію config.py."""
    logger.info("⚙️  Перевірка конфігурації...")
    try:
        import config
        
        # Перевіряє токен
        if config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.warning("  ⚠️  TELEGRAM_BOT_TOKEN не встановлен - встановіть у config.py")
        elif not config.TELEGRAM_BOT_TOKEN:
            logger.error("  ❌ TELEGRAM_BOT_TOKEN пустий!")
            return False
        else:
            logger.info("  ✅ TELEGRAM_BOT_TOKEN встановлен")
        
        # Перевіряє Chat ID
        if config.TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
            logger.warning("  ⚠️  TELEGRAM_CHAT_ID не встановлен - встановіть у config.py")
        elif not config.TELEGRAM_CHAT_ID:
            logger.error("  ❌ TELEGRAM_CHAT_ID пустий!")
            return False
        else:
            logger.info("  ✅ TELEGRAM_CHAT_ID встановлен")
        
        # Перевіряє ITEM_NAME
        if not config.ITEM_NAME or config.ITEM_NAME == "YOUR_ITEM_NAME":
            logger.error("  ❌ ITEM_NAME не встановлен!")
            return False
        logger.info(f"  ✅ ITEM_NAME: {config.ITEM_NAME}")
        
        # Перевіряє ціну
        logger.info(f"  ✅ MAX_PRICE_USD: ${config.MAX_PRICE_USD}")
        
        # Перевіряє інтервал
        if config.CHECK_INTERVAL_SECONDS < 30:
            logger.warning(f"  ⚠️  CHECK_INTERVAL_SECONDS дуже малий ({config.CHECK_INTERVAL_SECONDS}с)")
        else:
            logger.info(f"  ✅ CHECK_INTERVAL_SECONDS: {config.CHECK_INTERVAL_SECONDS}с")
        
        return True
        
    except Exception as e:
        logger.error(f"  ❌ Помилка читання config.py: {e}")
        return False

def test_telegram_connection():
    """Тестує з'єднання з Telegram ботом."""
    logger.info("🔌 Тестування Telegram з'єднання...")
    try:
        from telegram_bot import TelegramNotifier
        import config
        
        notifier = TelegramNotifier(
            bot_token=config.TELEGRAM_BOT_TOKEN,
            chat_id=config.TELEGRAM_CHAT_ID,
            proxy=config.PROXY,
        )
        
        if notifier.test_connection():
            logger.info("  ✅ Telegram бот підключився успішно")
            return True
        else:
            logger.error("  ❌ Не вдалося підключитися до Telegram")
            return False
            
    except Exception as e:
        logger.error(f"  ❌ Помилка тестування Telegram: {e}")
        return False

def test_steam_parser():
    """Тестує парсер Steam Market."""
    logger.info("🎮 Тестування Steam Market парсера...")
    try:
        from steam_parser import SteamMarketParser
        import config
        
        parser = SteamMarketParser(app_id=config.DOTA2_APP_ID)
        
        # Спробуємо отримати одну сторінку лістингів
        data = parser.get_item_listings_page(config.ITEM_NAME, start=0, count=10)
        
        if data and data.get("success"):
            total = data.get("total_count", 0)
            logger.info(f"  ✅ Парсер успішний (знайдено {total} лістингів)")
            return True
        else:
            logger.error("  ❌ Парсер не спромігся отримати дані")
            return False
            
    except Exception as e:
        logger.error(f"  ❌ Помилка парсера: {e}")
        return False

def main():
    """Запускає всі перевірки."""
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТУВАННЯ ПАРСЕРА ПЕРЕД ДЕПЛОЙМЕНТОМ")
    logger.info("=" * 60)
    
    checks = [
        ("Python версія", check_python_version),
        ("Залежності", check_dependencies),
        ("Конфігурація", check_config),
        ("Telegram", test_telegram_connection),
        ("Steam Market", test_steam_parser),
    ]
    
    results = {}
    for name, check in checks:
        logger.info("")
        try:
            results[name] = check()
        except Exception as e:
            logger.error(f"Критична помилка: {e}")
            results[name] = False
    
    # Резюме
    logger.info("")
    logger.info("=" * 60)
    logger.info("📊 РЕЗУЛЬТАТИ ТЕСТУВАННЯ")
    logger.info("=" * 60)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    logger.info("=" * 60)
    
    if all_passed:
        logger.info("✅ ВСІ ТЕСТИ ПРОЙШЛИ! Парсер готовий до деплойменту на Wispbyte.")
        logger.info("Следующий кроков:")
        logger.info("1. git init && git add . && git commit -m 'Initial commit'")
        logger.info("2. Завантажте на GitHub")
        logger.info("3. Встановіть на Wispbyte через Git URL")
        return 0
    else:
        logger.error("❌ ТЕСТУВАННЯ НЕ ПРОЙШЛО. Виправте помилки перше ніж деплойтити.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
