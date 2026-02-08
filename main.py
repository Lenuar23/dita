"""
Steam Dota 2 Market Parser — головний скрипт.
Моніторить Steam Market на наявність кур'єрів з певними стилями
та надсилає сповіщення через Telegram.
"""

import sys
import time
import logging
from datetime import datetime

import config
from steam_parser import SteamMarketParser
from telegram_bot import TelegramNotifier


def setup_logging():
    """Налаштовує логування у файл та консоль."""
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
    ]

    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
    )


def validate_config():
    """Перевіряє що конфіг заповнений правильно."""
    errors = []

    if config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        errors.append("❌ Не вказано TELEGRAM_BOT_TOKEN в config.py")

    if config.TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        errors.append("❌ Не вказано TELEGRAM_CHAT_ID в config.py")

    if not config.ITEM_NAME:
        errors.append("❌ Не вказано ITEM_NAME в config.py")

    if config.CHECK_INTERVAL_SECONDS < 30:
        errors.append("⚠️ CHECK_INTERVAL_SECONDS занадто малий (мінімум 30)")

    return errors


def print_banner():
    """Виводить стартовий банер."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║           🎮 Steam Dota 2 Market Parser 🎮              ║
║          Моніторинг предметів на маркеті                ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Головна функція — запускає цикл моніторингу."""

    setup_logging()
    logger = logging.getLogger("main")

    print_banner()

    # Валідація конфігу
    errors = validate_config()
    if errors:
        for err in errors:
            print(err)
        print("\n📝 Відредагуй файл config.py і спробуй знову.")
        sys.exit(1)

    # Ініціалізація модулів
    notifier = TelegramNotifier(
        bot_token=config.TELEGRAM_BOT_TOKEN,
        chat_id=config.TELEGRAM_CHAT_ID,
        proxy=config.PROXY,
    )

    parser = SteamMarketParser(
        app_id=config.DOTA2_APP_ID,
        proxy=config.PROXY,
    )

    # Перевірка з'єднання з Telegram ботом
    print("🔌 Перевірка з'єднання з Telegram ботом...")
    if not notifier.test_connection():
        print("❌ Не вдалося підключитися до Telegram бота!")
        print("   Перевір TELEGRAM_BOT_TOKEN в config.py")
        sys.exit(1)

    # Формуємо тексти для фільтрів
    styles_filter = ', '.join(str(s) for s in config.DESIRED_STYLES) if config.DESIRED_STYLES else 'Всі'
    gems_filter = ', '.join(config.DESIRED_GEMS) if config.DESIRED_GEMS else 'Всі'
    price_filter = f'${config.MAX_PRICE_USD}' if config.MAX_PRICE_USD > 0 else 'Без обмеження'

    # Надсилаємо стартове повідомлення
    start_msg = (
        "🚀 <b>Steam Market Parser запущений!</b>\n\n"
        f"🔍 <b>Шукаю:</b> {config.ITEM_NAME}\n"
        f"🎨 <b>Фільтр стилів:</b> {styles_filter}\n"
        f"💎 <b>Фільтр гемів:</b> {gems_filter}\n"
        f"💰 <b>Макс. ціна:</b> {price_filter}\n"
        f"⏰ <b>Інтервал:</b> кожні {config.CHECK_INTERVAL_SECONDS} сек.\n"
    )
    notifier.send_message(start_msg)

    print(f"\n🔍 Шукаю: {config.ITEM_NAME}")
    print(f"🎨 Фільтр стилів: {styles_filter}")
    print(f"💎 Фільтр гемів: {gems_filter}")
    print(f"💰 Макс. ціна: {price_filter}")
    print(f"⏰ Інтервал перевірки: {config.CHECK_INTERVAL_SECONDS} секунд")
    print(f"\n{'='*55}")
    print("🟢 Парсер працює... (Ctrl+C для зупинки)\n")

    check_count = 0

    try:
        while True:
            check_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            logger.info(f"🔄 Перевірка #{check_count} о {now}")

            # Парсимо лістинги
            found_items = parser.parse_listings(
                item_name=config.ITEM_NAME,
                desired_gems=config.DESIRED_GEMS if config.DESIRED_GEMS else None,
                desired_styles=config.DESIRED_STYLES if config.DESIRED_STYLES else None,
                max_price=config.MAX_PRICE_USD,
            )

            if found_items:
                logger.info(f"🎉 Знайдено {len(found_items)} предмет(ів)!")

                # Обмеження: максимум 5 сповіщень за раз щоб не спамити
                items_to_notify = found_items[:5]
                if len(found_items) > 5:
                    logger.info(f"📬 Надсилаю перші 5 з {len(found_items)}, решта — наступного разу")

                for item in items_to_notify:
                    # Форматуємо та відправляємо повідомлення
                    message = notifier.format_item_message(item)
                    success = notifier.send_message(message)

                    if success:
                        parser.mark_as_notified(item["listing_id"])
                        logger.info(
                            f"📨 Сповіщення відправлено: {item['name']} — {item['price']}"
                        )
                    else:
                        logger.warning(
                            f"⚠️ Не вдалося відправити сповіщення для: {item['name']}"
                        )

                    # Невелика пауза між повідомленнями
                    time.sleep(1)
            else:
                logger.info("😴 Нічого не знайдено, чекаємо...")

            # Чекаємо перед наступною перевіркою
            logger.info(
                f"⏳ Наступна перевірка через {config.CHECK_INTERVAL_SECONDS} сек."
            )
            time.sleep(config.CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n\n🛑 Парсер зупинений користувачем.")
        logger.info("Парсер зупинений (KeyboardInterrupt)")

        # Надсилаємо повідомлення про зупинку
        notifier.send_message("🛑 <b>Steam Market Parser зупинений.</b>")

    except Exception as e:
        logger.critical(f"💥 Критична помилка: {e}", exc_info=True)
        notifier.send_message(f"💥 <b>Parser впав з помилкою:</b>\n<code>{e}</code>")
        raise


if __name__ == "__main__":
    main()
