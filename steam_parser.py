"""
Модуль парсингу Steam Community Market для пошуку предметів Dota 2.
Працює через публічне Steam Market API (без авторизації).
"""

import logging
import time
import re
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)


class SteamMarketParser:
    """Парсер Steam Community Market для предметів Dota 2."""

    # Steam Market API endpoints
    SEARCH_URL = "https://steamcommunity.com/market/search/render/"
    LISTINGS_URL = "https://steamcommunity.com/market/listings/{app_id}/{item_name}/render/"
    ITEM_PAGE_URL = "https://steamcommunity.com/market/listings/{app_id}/{item_name}"

    def __init__(self, app_id: int = 570, proxy: str = None):
        self.app_id = app_id
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://steamcommunity.com/market/",
        })
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

        # Множина ID лістингів, про які ми вже сповіщували
        self.notified_listings: set = set()

    def search_item(self, item_name: str, count: int = 100) -> dict | None:
        """
        Шукає предмет на маркеті за назвою.
        Повертає JSON-відповідь або None у разі помилки.
        """
        params = {
            "query": item_name,
            "start": 0,
            "count": count,
            "search_descriptions": 0,
            "sort_column": "price",
            "sort_dir": "asc",
            "appid": self.app_id,
            "norender": 1,
            "currency": 1,  # USD
        }

        try:
            response = self.session.get(
                self.SEARCH_URL, params=params, timeout=20
            )
            response.raise_for_status()

            # Перевіряємо rate-limiting
            if response.status_code == 429:
                logger.warning("⚠️ Steam rate limit! Чекаємо 60 секунд...")
                time.sleep(60)
                return None

            data = response.json()

            if not data.get("success"):
                logger.error("❌ Steam API повернув помилку")
                return None

            total = data.get("total_count", 0)
            logger.info(f"📊 Знайдено {total} результат(ів) для '{item_name}'")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Помилка запиту до Steam Market: {e}")
            return None
        except ValueError as e:
            logger.error(f"❌ Помилка парсингу JSON: {e}")
            return None

    def get_item_listings_page(self, item_name: str, start: int = 0, count: int = 100) -> dict | None:
        """
        Отримує одну сторінку лістингів конкретного предмета.
        start — зсув (0, 100, 200, ...)
        count — кількість на сторінку (макс 100)
        """
        encoded_name = quote(item_name)
        url = self.LISTINGS_URL.format(app_id=self.app_id, item_name=encoded_name)

        params = {
            "start": start,
            "count": count,
            "currency": 1,  # USD
            "language": "english",
            "format": "json",
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.debug(f"📡 Запит сторінки start={start}, спроба {attempt + 1}")
                response = self.session.get(url, params=params, timeout=20)

                if response.status_code == 429:
                    wait_time = 60 * (attempt + 1)
                    logger.warning(f"⚠️ Steam rate limit! Чекаємо {wait_time} секунд... (спроба {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()

                if not data.get("success"):
                    logger.error(f"❌ Steam API лістингів повернув помилку: {data}")
                    return None

                return data

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Помилка запиту лістингів (спроба {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                return None
            except ValueError as e:
                logger.error(f"❌ Помилка парсингу JSON лістингів: {e}")
                return None
        
        logger.error("❌ Всі спроби вичерпано")
        return None

    def extract_gems_from_descriptions(self, descriptions: list) -> list[str]:
        """
        Витягує назви гемів (Ethereal/Prismatic) з описів предмета.
        Steam повертає геми як частину descriptions масиву.
        """
        gems = []
        if not descriptions:
            return gems

        for desc in descriptions:
            value = desc.get("value", "")
            # Геми зазвичай містять "Gem" або мають спеціальний колір
            # Prismatic: Color name
            # Ethereal: Effect name
            if "Prismatic:" in value or "Ethereal:" in value:
                # Очищаємо від HTML тегів
                clean = re.sub(r'<[^>]+>', '', value).strip()
                if clean:
                    gems.append(clean)
            elif desc.get("type") == "html" and "color" in desc.get("value", ""):
                # Деякі геми мають кольоровий текст
                clean = re.sub(r'<[^>]+>', '', value).strip()
                if clean and ("Gem" in clean or "Prismatic" in clean or "Ethereal" in clean):
                    gems.append(clean)

        return gems

    def extract_socket_gems(self, descriptions: list) -> list[str]:
        """
        Альтернативний спосіб витягування гемів — шукаємо в секції сокетів.
        """
        gems = []
        if not descriptions:
            return gems

        in_socket_section = False
        for desc in descriptions:
            value = desc.get("value", "")
            if "Socket" in value or "Gem" in value:
                in_socket_section = True
            if in_socket_section:
                clean = re.sub(r'<[^>]+>', '', value).strip()
                if clean and clean not in ("", "Empty Socket"):
                    gems.append(clean)

        return gems

    def extract_unlocked_styles(self, descriptions: list) -> list[int]:
        """
        Витягує номери ВІДКРИТИХ стилів з описів предмета.
        Пропускає стилі з позначкою (Locked).

        Формати Steam API:
          EN: "Upgrade Style 6" (відкритий), "Upgrade Style 7 (Locked)" (заблокований)
          RU: "Стиль-улучшение 6" (відкритий), "Стиль-улучшение 7 (Заблокировано)"
        """
        styles = []
        if not descriptions:
            return styles

        for desc in descriptions:
            value = desc.get("value", "")
            # Очищаємо від HTML тегів
            clean = re.sub(r'<[^>]+>', '', value).strip()

            # Пропускаємо заблоковані стилі
            if re.search(r'[Ll]ocked|[Зз]аблокировано|[Зз]аблоковано', clean):
                continue

            # EN: "Upgrade Style 6" (без Locked)
            en_match = re.search(r'[Uu]pgrade\s+[Ss]tyle\s+(\d+)', clean)
            if en_match:
                style_num = int(en_match.group(1))
                if style_num not in styles:
                    styles.append(style_num)
                continue

            # EN alt: "Style 6" або "Style 6 Unlocked"
            en_alt_match = re.search(r'[Ss]tyle\s+(\d+)', clean)
            if en_alt_match:
                style_num = int(en_alt_match.group(1))
                if style_num not in styles:
                    styles.append(style_num)
                continue

            # RU: "Стиль-улучшение 6" (без Заблокировано)
            ru_match = re.search(r'[Сс]тиль[- ]улучшение\s+(\d+)', clean)
            if ru_match:
                style_num = int(ru_match.group(1))
                if style_num not in styles:
                    styles.append(style_num)
                continue

        return sorted(styles)

    def get_max_style_from_tags(self, tags: list) -> int | None:
        """
        Отримує максимальний відкритий стиль з тегів предмета.
        Steam часто включає стиль в tags.
        """
        if not tags:
            return None

        max_style = 0
        for tag in tags:
            name = tag.get("localized_tag_name", "") or tag.get("name", "")
            # EN: "Style 20", "Style Upgrade 20"
            match = re.search(r'[Ss]tyle(?:\s+[Uu]pgrade)?\s+(\d+)', name)
            if match:
                style_num = int(match.group(1))
                if style_num > max_style:
                    max_style = style_num
            # RU: "Стиль-улучшение 20"
            ru_match = re.search(r'[Сс]тиль[- ]улучшение\s+(\d+)', name)
            if ru_match:
                style_num = int(ru_match.group(1))
                if style_num > max_style:
                    max_style = style_num

        return max_style if max_style > 0 else None

    def parse_listings(self, item_name: str, desired_gems: list[str] = None,
                       desired_styles: list[int] = None,
                       max_price: float = 0) -> list[dict]:
        """
        Головний метод — парсить лістинги предмета та фільтрує за гемами/стилями/ціною.

        Повертає список знайдених предметів у форматі:
        [
            {
                "name": str,
                "price": str,
                "price_value": float,
                "listing_id": str,
                "link": str,
                "gems": list[str],
                "styles": list[int],
                "inspect_link": str | None,
                "image_url": str | None,
            }
        ]
        """
        PAGE_SIZE = 100
        found_items = []
        start = 0
        total_count = None

        while True:
            data = self.get_item_listings_page(item_name, start=start, count=PAGE_SIZE)
            if not data:
                if total_count is None:
                    logger.error("❌ Не вдалося отримати першу сторінку лістингів")
                else:
                    logger.warning(f"⚠️ Не вдалося отримати сторінку {start // PAGE_SIZE + 1}, пропускаю")
                break

            if total_count is None:
                total_count = data.get("total_count", 0)
                logger.info(f"📋 Всього лістингів на маркеті: {total_count}")
                if total_count == 0:
                    logger.warning("⚠️ Steam повернув 0 лістингів — можливо предмет не існує або проблема з API")
                    break

            listinginfo = data.get("listinginfo", {})
            assets = data.get("assets", {})

            if not listinginfo:
                logger.info(f"📄 Сторінка {start // PAGE_SIZE + 1}: порожня, завершуємо")
                break

            page_num = start // PAGE_SIZE + 1
            logger.info(f"📄 Сторінка {page_num}: обробляю {len(listinginfo)} лістингів (з {start})")

            page_found = self._process_page_listings(
                listinginfo, assets, item_name, desired_gems, desired_styles, max_price, page_num
            )
            found_items.extend(page_found)

            # Переходимо на наступну сторінку
            start += PAGE_SIZE

            # Зупиняємося якщо дійшли до кінця
            if start >= total_count:
                break

            # Пауза між сторінками щоб не словити rate limit
            time.sleep(3)

        logger.info(f"📊 Підсумок: переглянуто {start} лістингів, знайдено {len(found_items)} з потрібними стилями")
        return found_items

    def _process_page_listings(self, listinginfo: dict, assets: dict,
                                item_name: str, desired_gems: list[str] = None,
                                desired_styles: list[int] = None,
                                max_price: float = 0, page_num: int = 1) -> list[dict]:
        """Обробляє лістинги однієї сторінки."""
        found_items = []

        for listing_id, listing in listinginfo.items():
            # Пропускаємо вже сповіщені
            if listing_id in self.notified_listings:
                continue

            # Отримуємо ціну
            price_cents = listing.get("converted_price", 0) + listing.get("converted_fee", 0)
            price_usd = price_cents / 100.0
            price_str = f"${price_usd:.2f} USD"

            # Перевірка максимальної ціни
            if max_price > 0 and price_usd > max_price:
                continue

            # Отримуємо інформацію про ассет (предмет)
            asset_info = listing.get("asset", {})
            app_id = str(asset_info.get("appid", self.app_id))
            context_id = str(asset_info.get("contextid", "2"))
            asset_id = str(asset_info.get("id", ""))

            # Шукаємо опис предмета
            item_desc = None
            if app_id in assets:
                if context_id in assets[app_id]:
                    if asset_id in assets[app_id][context_id]:
                        item_desc = assets[app_id][context_id][asset_id]

            gems = []
            styles = []
            inspect_link = None
            image_url = None
            actual_name = item_name

            if item_desc:
                actual_name = item_desc.get("market_hash_name", item_name)
                descriptions = item_desc.get("descriptions", [])
                tags = item_desc.get("tags", [])

                # Витягуємо геми
                gems = self.extract_gems_from_descriptions(descriptions)
                if not gems:
                    gems = self.extract_socket_gems(descriptions)

                # Витягуємо відкриті стилі
                styles = self.extract_unlocked_styles(descriptions)

                # Якщо в описах не знайшли — дивимось теги
                if not styles:
                    max_style = self.get_max_style_from_tags(tags)
                    if max_style:
                        styles = list(range(1, max_style + 1))

                # Отримуємо inspect link (якщо є)
                actions = item_desc.get("actions", []) or item_desc.get("market_actions", [])
                for action in actions:
                    if "inspect" in action.get("name", "").lower():
                        link = action.get("link", "")
                        link = link.replace("%listingid%", listing_id)
                        link = link.replace("%assetid%", asset_id)
                        inspect_link = link
                        break

                # Зображення
                icon_url = item_desc.get("icon_url_large", item_desc.get("icon_url", ""))
                if icon_url:
                    image_url = f"https://community.akamai.steamstatic.com/economy/image/{icon_url}"

            # Фільтр за гемами
            if desired_gems:
                gems_lower = [g.lower() for g in gems]
                match = any(
                    desired.lower() in gem_text
                    for desired in desired_gems
                    for gem_text in gems_lower
                )
                if not match:
                    logger.debug(
                        f"⏩ Лістинг {listing_id}: геми {gems} не відповідають фільтру"
                    )
                    continue

            # Фільтр за стилями
            if desired_styles:
                has_desired_style = any(s in styles for s in desired_styles)
                if not has_desired_style:
                    logger.debug(
                        f"⏩ Лістинг {listing_id}: стилі {styles} не містять потрібних {desired_styles}"
                    )
                    continue

            item_link = self.ITEM_PAGE_URL.format(
                app_id=self.app_id,
                item_name=quote(item_name)
            )

            # Генеруємо фільтроване посилання залежно від найвищого стилю
            filtered_link = item_link
            if styles:
                max_style = max(styles)
                # Фільтр: шукаємо Onibi без заблокованої версії цього стилю
                # URL encoded: onibi NOT "20 locked" = onibi+NOT+%2220+locked%22
                filtered_link = f"https://steamcommunity.com/market/listings/570/Onibi?filter=onibi+NOT+%22{max_style}+locked%22"

            found_items.append({
                "name": actual_name,
                "price": price_str,
                "price_value": price_usd,
                "listing_id": listing_id,
                "link": item_link,
                "filtered_link": filtered_link,
                "gems": gems,
                "styles": styles,
                "inspect_link": inspect_link,
                "image_url": image_url,
                "page": page_num,
            })

            styles_str = ', '.join(str(s) for s in styles) if styles else 'N/A'
            logger.info(
                f"✅ Знайдено: {actual_name} | {price_str} | "
                f"Сторінка: {page_num} | "
                f"Стилі: {styles_str} | "
                f"Геми: {', '.join(gems) if gems else 'N/A'}"
            )

        return found_items

    def mark_as_notified(self, listing_id: str):
        """Позначає лістинг як сповіщений (щоб не дублювати)."""
        self.notified_listings.add(listing_id)

    def get_item_price_overview(self, item_name: str) -> dict | None:
        """
        Отримує загальний огляд цін на предмет (мін., макс., медіана).
        """
        url = "https://steamcommunity.com/market/priceoverview/"
        params = {
            "appid": self.app_id,
            "currency": 1,
            "market_hash_name": item_name,
        }

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                return {
                    "lowest_price": data.get("lowest_price", "N/A"),
                    "median_price": data.get("median_price", "N/A"),
                    "volume": data.get("volume", "N/A"),
                }
            return None

        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error(f"❌ Помилка отримання цін: {e}")
            return None
