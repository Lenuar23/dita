# 🚀 Деплойменту на Wispbyte БЕЗ GitHub (тільки файли)

## Крок 1: Підготуйте ZIP архів

### 1.1 Зіпуйте проект (Windows)

```bash
cd "d:\Dota tool box"
# Натисніть ПКМ на папці Onibi → Send to → Compressed folder
# Або використайте PowerShell:
Compress-Archive -Path "Onibi" -DestinationPath "onibi-parser.zip"
```

### 1.2 Вибрані файли для архіву:

✅ **Включіть ці файли:**
```
onibi-parser.zip
├── config.py              ✅
├── main.py                ✅
├── steam_parser.py        ✅
├── telegram_bot.py        ✅
├── requirements.txt       ✅
├── Dockerfile             ✅ (опціонально)
└── parser.log             ❌ (створиться автоматично)
```

❌ **НЕ включайте:**
```
├── .venv/                 ❌ (вільно перевстановлюється)
├── __pycache__/           ❌ (ненотрібне)
├── .env                   ❌ (встановлюється через панель)
└── .git/                  ❌ (GitHub дані)
```

---

## Крок 2: Завантаження на Wispbyte

### 2.1 Увійдіть на Wispbyte

1. Перейдіть на [wispbyte.com](https://wispbyte.com)
2. Логіньтеся
3. **Створіть новий сервер** або перейдіть до існуючого

### 2.2 Налаштування сервера (базові параметри)

- **Server Name**: `onibi-parser`
- **Docker Image**: `python:3.12-slim` або вибіріте **Python**
- **Ram**: 512 MB - 1 GB (достатньо)
- **Disk**: 5 GB

### 2.3 Завантажуйте файли через панель

1. На панелі Wispbyte перейдіть до **Files**
2. Натисніть **Upload Files** (як видно на твому скріншоті)
3. Виберіть `onibi-parser.zip`
4. Натисніть **Upload**

### 2.4 Розархівуйте файли

1. Клікніть на `onibi-parser.zip`
2. Натисніть **Extract** (якщо є опція)
3. Або використайте **Console** командою:

```bash
cd /home/container
unzip onibi-parser.zip
```

---

## Крок 3: Встановлення залежностей

### 3.1 Через Console на панелі Wispbyte

1. Перейдіть на **Console**
2. Виконайте команду:

```bash
pip install -r requirements.txt
```

3. Дочекайтеся завершення установки

### 3.2 Перевіряємо установку

```bash
python -m pip list | grep -E "requests|python-dotenv"
```

---

## Крок 4: Встановлення Environment Variables

### 4.1 На панелі Wispbyte перейдіть до **Settings** або **Startup**

1. Знайдіть розділ **Environment Variables** або **Variables**
2. Додайте:

```
TELEGRAM_BOT_TOKEN=8347544771:AAETta3bs5UTQrdtajKu8ICsdFs2V84gnPk
TELEGRAM_CHAT_ID=888387442
PROXY=  # залиште порожнім якщо не потрібен
```

### 4.2 Збережіть параметри

Натисніть **Save** або **Apply**

---

## Крок 5: Налаштування Startup Command

### 5.1 На панелі перейдіть до **Startup Settings**

1. Встановіть **Startup Command**:

```bash
python main.py
```

2. Встановіть **Install Command** (якщо запитує):

```bash
pip install -r requirements.txt
```

3. Натисніть **Save**

---

## Крок 6: Запуск сервера

### 6.1 Натисніть **Start Server**

1. Статус повинен змінитись на **Online**
2. Перейдіть на **Console** щоб бачити логи

### 6.2 Перевіряємо чи запустився парсер

У консолі повинні з'явитися повідомлення:

```
🔌 Перевірка з'єднання з Telegram ботом...
✅ Бот підключений: @OnibiParsers_bot
🚀 Steam Market Parser запущений!
```

---

## Крок 7: Тестування

### 7.1 Дивіться логи в Console

```
🔄 Перевірка #1 о 12:09:57
📋 Всього лістингів на маркеті: 1133
📄 Сторінка 1: обробляю 100 лістингів (з 0)
```

### 7.2 Перевіряєте Telegram

Повинно прийти повідомлення:
```
🚀 Steam Market Parser запущений!
```

---

## 🔄 Оновлення парсера (без GitHub)

Коли захочете оновити код:

### Спосіб 1: Через Console

```bash
# Зупиніть парсер
kill $(pgrep -f "python main.py")

# Видаліть старі файли
rm *.py

# Завантажте нові файли через Files → Upload
# або вкопіюйте через Console
```

### Спосіб 2: Через re-Upload ZIP

1. Видаліть старий ZIP
2. Завантажте нову версію
3. Розархівуйте
4. Перезавантажте сервер

---

## ⚠️ Обмеження без GitHub

| Параметр | GitHub | Прямі файли |
|----------|--------|-----------|
| Версіонування | ✅ Так | ❌ Вручну |
| История змін | ✅ Та | ❌ Нема |
| Автооновлення | ✅ Можливо | ❌ Нема |
| Простота | ❌ Складніше | ✅ Простіше |
| Безпека | ✅ Приватний repo | ⚠️ На сервері |

---

## 🛠️ Команди для Console (Wispbyte)

```bash
# Перевіряємо Python версію
python --version

# Встановлюємо залежності
pip install -r requirements.txt

# Запускаємо парсерручне
python main.py

# Перевіряємо процеси Python
ps aux | grep python

# Зупиняємо парсер
kill <PID>

# Переглядаємо логи
cat parser.log

# Перезавантажуємо файли
cd /home/container && ls -la
```

---

## 📊 Структура файлів на сервері

Після розархівування повинна бути така структура:

```
/home/container/
├── config.py
├── main.py
├── steam_parser.py
├── telegram_bot.py
├── requirements.txt
├── Dockerfile
├── README.md
├── DEPLOYMENT.md
├── test_deployment.py
└── parser.log  (створиться при запуску)
```

---

## ✅ Чек-лист перед запуском

- [ ] ZIP розархівовано
- [ ] requirements.txt встановлено (`pip install -r requirements.txt`)
- [ ] TELEGRAM_BOT_TOKEN встановлено (Environment Variables)
- [ ] TELEGRAM_CHAT_ID встановлено (Environment Variables)
- [ ] Startup Command: `python main.py`
- [ ] Статус сервера: **Online**
- [ ] У Console видно логи парсера

---

## 🎉 Готово!

Коли все налаштовано правильно:
✅ Парсер буде працювати 24/7  
✅ Буде надсилати повідомлення в Telegram  
✅ Автоматично перезавантажуватися при помилках  

**Успіху! 🚀**
