"""
Модуль для відправки повідомлень через Telegram бота.
"""

import logging
import requests

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Відправляє сповіщення в Telegram."""

    BASE_URL = "https://api.telegram.org/bot{token}"

    def __init__(self, bot_token: str, chat_id: str, proxy: str = None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = self.BASE_URL.format(token=bot_token)
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Відправляє текстове повідомлення в Telegram чат.
        Повертає True якщо повідомлення відправлено успішно.
        """
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
        }

        try:
            response = self.session.post(url, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()

            if result.get("ok"):
                logger.info("✅ Повідомлення успішно відправлено в Telegram")
                return True
            else:
                logger.error(f"❌ Telegram API помилка: {result.get('description')}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Помилка відправки в Telegram: {e}")
            return False

    def test_connection(self) -> bool:
        """Перевіряє з'єднання з ботом."""
        url = f"{self.base_url}/getMe"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                bot_name = data["result"]["username"]
                logger.info(f"✅ Бот підключений: @{bot_name}")
                return True
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Не вдалося підключитися до бота: {e}")
            return False

    def format_item_message(self, item: dict) -> str:
        """
        Форматує повідомлення про знайдений предмет.

        Очікуваний формат item:
        {
            "name": str,
            "price": str,
            "listing_id": str,
            "link": str,
            "filtered_link": str,  - посилання з фільтром по стилю
            "gems": list[str],
            "styles": list[int],
            "image_url": str (optional),
        }
        """
        gems_text = ", ".join(item.get("gems", [])) or None
        styles = item.get("styles", [])
        styles_text = ", ".join(str(s) for s in styles) if styles else None

        msg = (
            "🎮 <b>ЗНАЙДЕНО ПРЕДМЕТ НА STEAM MARKET!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Назва:</b> {item['name']}\n"
        )

        if item.get("page"):
            msg += f"📄 <b>Сторінка:</b> {item['page']}\n"

        if styles_text:
            max_style = max(styles)
            msg += f"🎨 <b>Макс. відкритий стиль:</b> {max_style} (всього: {len(styles)})\n"

        if gems_text:
            msg += f"💎 <b>Геми:</b> {gems_text}\n"

        msg += (
            f"💰 <b>Ціна:</b> {item['price']}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 <a href=\"{item.get('filtered_link', item['link'])}\">Переглянути на Steam Market</a>"
        )

        if item.get("inspect_link"):
            msg += f"🔍 <a href=\"{item['inspect_link']}\">Inspect in Game</a>\n"

        msg += "\n⚡ Поспішай, поки не купили!"

        return msg
