# 🚀 Як захостити Onibi Parser на Wispbyte

## Крок 1: Підготовка до деплойменту

### 1.1 Переконайтеся, що у вас є:
- ✅ GitHub акаунт (або GitLab/Gitea)
- ✅ Wispbyte акаунт (wispbyte.com)
- ✅ Telegram Bot Token та Chat ID

### 1.2 Підготуйте середовище змінних
Ваш `.env` файл повинен містити:
```
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
PROXY=  # опціонально, якщо потрібен проксі
```

---

## Крок 2: Git підготовка

### 2.1 Ініціалізуйте Git репозиторій (якщо ще не зроблено):
```bash
cd "d:\Dota tool box\Onibi"
git init
git add .
git commit -m "Initial commit: Onibi Parser"
```

### 2.2 Создайте репозиторій на GitHub:
1. Перейдіть на github.com
2. Натисніть **New Repository**
3. Назвіть його `onibi-parser`
4. Встановіть як **Private** (щоб приховати токени)
5. Скопіюйте URL репозиторію

### 2.3 Додайте remote та запушіть код:
```bash
git remote add origin https://github.com/YOUR_USERNAME/onibi-parser.git
git branch -M main
git push -u origin main
```

---

## Крок 3: Деплойменту на Wispbyte

### 3.1 Увійдіть на Wispbyte

1. Перейдіть на [wispbyte.com](https://wispbyte.com)
2. Логіньтеся або реєструйтеся
3. Перейдіть до **Create Server**

### 3.2 Налаштуйте сервер

**Основні параметри:**
- **Server Name**: `onibi-parser`
- **Programming Language**: Python
- **Docker Image**: `python:3.12-slim` або стандартна Python опція
- **Ram**: 512 MB - 1 GB (достатньо для парсера)
- **Disk**: 5-10 GB

### 3.3 Розгортання коду

У Wispbyte є кілька варіантів:

#### **Варіант А: Через Git (рекомендується)**
1. На панелі сервера перейдіть до **Startup Settings**
2. Виберіть **Git Repository**
3. Вставте URL вашого репозиторію: `https://github.com/YOUR_USERNAME/onibi-parser.git`
4. Встановіть Branch: `main`
5. Встановіть **Install Command**:
   ```
   pip install -r requirements.txt
   ```
6. Встановіть **Startup Command**:
   ```
   python main.py
   ```

#### **Варіант Б: Через Docker (найкраще)**
1. Перейдіть до **Docker Configuration**
2. Встановіть **Dockerfile**: відзначте опцію "Use Dockerfile from repo"
3. Eller завантажте Dockerfile вручну:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```
4. Натисніть **Deploy**

### 3.4 Налаштування змінних середовища

1. На панелі сервера перейдіть до **Enviroment Variables**
2. Додайте:
   ```
   TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
   TELEGRAM_CHAT_ID=YOUR_CHAT_ID
   PROXY=  # якщо потрібен
   ```
3. **НЕ** комітьте `.env` файл у Git!

### 3.5 Запуск сервера

1. Натисніть **Start Server**
2. Дочекайтеся, поки статус змінюється на **Online**
3. Перевірьте логи у **Console**

---

## Крок 4: Моніторинг та налаштування

### 4.1 Перевірка логів
- Перейдіть на **Server Console**
- Дивіться вивід парсера в реальному часі
- Переконайтеся, що немає помилок

### 4.2 Налаштування автозапуску
- На панелі Wispbyte встановіть опцію **Auto Restart on Server Start**
- Це забезпечить, що парсер запуститься після перезавантаження

### 4.3 Встановлення Keepalive
Якщо сервер має ризик "спатити", встановіть cron job:
```bash
* * * * * curl -s https://YOUR_SERVER_IP:PORT/health || /start-parser.sh
```

---

## Крок 5: Тестування

### 5.1 Перевірте чи працює парсер:
1. У **Console** побачите повідомлення що парсер запущений
2. Чекайте 1-2 хвилин
3. Повинні з'явитися повідомлення про перевірку маркету

### 5.2 Тестувальний сигнал у Telegram
Якщо ви бачите:
```
✅ Бот підключений: @OnibiParsers_bot
🚀 Steam Market Parser запущений!
```
- **Все працює!** ✅

---

## Крок 6: Навантажувальні тести

### 6.1 Перевірка стійкості
- Дозвольте парсеру працювати 24 години
- Монітор консолі на помилки
- Перевірте вживання ОЗУ та диску

### 6.2 Налаштування інтервалу перевірки
У `config.py`:
```python
CHECK_INTERVAL_SECONDS = 120  # Кожні 2 хвилини
# Або збільшіть якщо Steam блокує:
CHECK_INTERVAL_SECONDS = 300  # Кожні 5 хвилин
```

---

## Часті проблеми та рішення

### ❌ Проблема: "Не вдалося підключитися до Telegram"
**Рішення:**
- Переконайтеся що токен встановлений правильно
- Перевірте інтернет з'єднання
- Спробуйте встановити PROXY

### ❌ Проблема: "Steam rate limit"
**Рішення:**
- Збільшіть `CHECK_INTERVAL_SECONDS` у config.py
- Встановіть проксі у config.py
- Спробуйте IP проксі сервіс

### ❌ Проблема: "Сервер гасне після 30 хвилин"
**Рішення:**
- Переконайтеся що сервер має **24/7** режим
- Встановіть **Auto Restart**
- Спробуйте Docker контейнер

### ❌ Проблема: "Memory/Disk issues"
**Рішення:**
- Збільшіть ресурси сервера на панелі
- Очистіть логи: `rm parser.log`
- Перезавантажте сервер

---

## Дипломатичні команди для управління

```bash
# Перевірка логів парсера
tail -f /app/parser.log

# Перезапуск парсера
systemctl restart onibi-parser

# Зупинка парсера
systemctl stop onibi-parser

# Перевірка статусу
systemctl status onibi-parser
```

---

## Безпека

⚠️ **ВАЖЛИВО:**
- ✅ Встановіть репозиторій як **Private**
- ✅ **НЕ** комітьте `.env` файл
- ✅ Використовуйте **Secrets** у Wispbyte для токенів
- ✅ Регулярно оновлюйте залежності
- ✅ Вивчайте логи на помилки безпеки

---

## Успішний деплойменту! 🎉

Якщо всі кроки виконано правильно, твій парсер буде:
- ✅ Працювати 24/7
- ✅ Автоматично перезапускатися при помилках
- ✅ Надсилати Telegram повідомлення при знахідці Onibi
- ✅ Масштабуватися за потребою

**Удачі з пошуком Onibi! 🚀**
