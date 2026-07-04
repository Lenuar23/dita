# 🎮 Steam Dota 2 Market Parser

Моніторинг Steam Community Market для пошуку кур'єрів Dota 2 з певними стилями (гемами).
При знаходженні — надсилає сповіщення в Telegram з ціною та посиланням.

## 📋 Можливості

- ✅ Моніторинг Steam Market в реальному часі
- ✅ Фільтр за Ethereal / Prismatic гемами (стилями)
- ✅ Фільтр за максимальною ціною
- ✅ Сповіщення в Telegram з ціною та посиланням
- ✅ Захист від дублювання сповіщень
- ✅ Логування у файл та консоль
- ✅ Підтримка проксі

## 🚀 Швидкий старт

### 1. Створи віртуальне середовище та встанови залежності

```bash
python -m venv venv
.\venv\bin\Activate.ps1
pip install -r requirements.txt
```

> ⚠️ Якщо PowerShell не дозволяє запускати скрипти, виконай спершу:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force`

### 2. Створи Telegram бота

1. Відкрий Telegram і знайди бота **@BotFather**
2. Напиши `/newbot`
3. Дай боту ім'я та username
4. Скопіюй **токен** який дасть BotFather
5. Знайди бота **@userinfobot** або **@RawDataBot** — напиши йому щоб дізнатися свій **Chat ID**
6. **Важливо:** напиши своєму новому боту `/start` щоб він міг тобі писати

### 3. Налаштуй config.py

Відкрий `config.py` і заповни:

```python
# Токен бота від BotFather
TELEGRAM_BOT_TOKEN = "1234567890:ABCDefghIJKLmnopQRSTuvwxyz"

# Твій Chat ID
TELEGRAM_CHAT_ID = "123456789"

# Назва предмета (точна назва з маркету!)
ITEM_NAME = "Unusual Baby Roshan"

# Фільтр гемів (стилів) — залиш порожнім щоб бачити все
DESIRED_GEMS = [
    "Ethereal Flame",
    "Creator's Light",
]

# Максимальна ціна (0 = без обмеження)
MAX_PRICE_USD = 500

# Інтервал перевірки (секунди)
CHECK_INTERVAL_SECONDS = 120
```

### 4. Запусти парсер

```bash
python main.py
```

## 📦 Як знайти точну назву предмета

1. Відкрий [Steam Community Market](https://steamcommunity.com/market/)
2. Знайди потрібний кур'єр
3. Скопіюй **точну назву** з заголовка сторінки

Приклади назв:
- `Unusual Baby Roshan`
- `Unusual Stumpy - Nature's Attendant`  
- `Unusual Skip the Delivery Frog`
- `Unusual Cluckles the Brave`
- `Unusual Kupu the Metamorpher`
- `Unusual War Dog`

> ⚠️ Для Unusual (з гемами) кур'єрів назва завжди починається з **"Unusual"**

## 💎 Назви гемів (стилів)

### Ethereal Gems (ефекти)
- Ethereal Flame
- Searing Essence  
- Piercing Beams
- Felicity's Blessing
- Resonant Energy
- Luminous Gaze
- Affliction of Vermin
- Divine Essence
- та інші...

### Prismatic Gems (кольори)
- Red, Blue, Green, Gold, Purple
- Creator's Light
- Legacy (унікальний колір)
- Brusque Britches Beige
- Verdant Green
- та інші...

## ⚙️ Додаткові налаштування

### Проксі
Якщо Steam блокує запити, додай проксі в `config.py`:
```python
PROXY = "http://user:pass@host:port"
# або
PROXY = "socks5://user:pass@host:port"
```

### Інтервал перевірки
Не ставте менше 60 секунд — Steam може тимчасово заблокувати IP:
```python
CHECK_INTERVAL_SECONDS = 120  # рекомендовано
```

## 📁 Структура проекту

```
steam-dota2-parser/
├── config.py          # Конфігурація (токени, назва предмета, фільтри)
├── main.py            # Головний скрипт запуску
├── steam_parser.py    # Парсер Steam Market API  
├── telegram_bot.py    # Модуль Telegram сповіщень
├── requirements.txt   # Залежності Python
├── parser.log         # Лог-файл (створюється автоматично)
└── README.md          # Цей файл
```

## ⚠️ Обмеження

- Steam Market API публічне і не потребує авторизації, але має rate-limiting
- Парсер автоматично чекає при отриманні HTTP 429 (Too Many Requests)
- Деякі предмети можуть не мати детальної інформації про геми через API
- Для надійної роботи рекомендується інтервал від 2 хвилин

## 🌐 Деплойменту на Wispbyte (24/7 хостинг)

### Швидкий старт деплойменту

1. **Прочитайте** детальну інструкцію в [DEPLOYMENT.md](DEPLOYMENT.md)
2. **Підготуйте** свої credentials:
   - GitHub акаунт (для хранення коду)
   - Wispbyte акаунт
   - Telegram Bot Token + Chat ID

### Основні кроки:

```bash
# 1. Ініціалізуйте Git
git init
git add .
git commit -m "Initial commit: Onibi Parser"

# 2. Створіть репозиторій на GitHub
# https://github.com/new

# 3. Додайте remote та запушіть
git remote add origin https://github.com/YOUR_USERNAME/onibi-parser.git
git push -u origin main
```

3. На **Wispbyte панелі**:
   - Натисніть **Create Server**
   - Виберіть **Python** або **Docker**
   - Встановіть Git URL: `https://github.com/YOUR_USERNAME/onibi-parser.git`
   - Додайте **Environment Variables**: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
   - Встановіть **Startup Command**: `python main.py`
   - Натисніть **Deploy**

### Переваги деплойменту на Wispbyte:
✅ Парсер працює 24/7 без зупинок  
✅ Автоматичне перезавантаження при помилках  
✅ Дешево (від $1/месяц за базову версію)  
✅ Простий інтерфейс управління  
✅ Зустрічена підтримка comunity  

## 🐳 Docker (локальне використання)

Якщо ви хочете запустити парсер у контейнері локально:

```bash
# Побудуйте образ
docker build -t onibi-parser .

# Запустіть контейнер
docker run -e TELEGRAM_BOT_TOKEN="YOUR_TOKEN" \
           -e TELEGRAM_CHAT_ID="YOUR_ID" \
           --name onibi-parser \
           onibi-parser

# Перевірте логи
docker logs -f onibi-parser

# Зупиніть контейнер
docker stop onibi-parser
```

## 📊 Моніторинг та налаштування

### Переглядання логів локально
```bash
tail -f parser.log
```

### Переглядання логів на Wispbyte
- Перейдіть на **Server Console** у панелі
- Дивіться вивід в реальному часі

## 🤝 Підтримка

Якщо у вас виникли проблеми:
1. Перевірте `/parser.log` файл на помилки
2. Переконайтеся що `config.py` налаштований правильно
3. Перевірте чи Telegram бот має дозвіл писати в ваш чат
4. Спробуйте запустити локально перед деплойментом на сервер
