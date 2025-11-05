# Server Status Bot

Python-скрипт для мониторинга сервера и отправки статуса в Telegram через systemd user-таймер.

---

## Функционал

* Отслеживает:

  * загрузку CPU,
  * среднюю нагрузку системы (`load average`),
  * использование RAM.
* Отправляет информацию в Telegram чат.
* Автоматическая корректная работа с виртуальным окружением (`.venv`) и `.env` файлом.
* Работает через systemd user-таймер (`.service` + `.timer`).

---

## Структура проекта

```
server_status_bot/
├─ .gitignore
├─ README.md
├─ .env.example
├─ requirements.txt
├─ server_status_bot.py
├─ start_bot.sh
├─ server_status_bot.service
└─ server_status_bot.timer
```

---

## Установка и настройка

### 1. Клонируем репозиторий

```bash
git clone https://github.com/USERNAME/server_status_bot.git
cd server_status_bot
```

### 2. Создаем виртуальное окружение и устанавливаем зависимости

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка `.env`

* Создаём копию примера:

```bash
cp .env.example .env
```

* Открываем `.env` и подставляем свои значения:

```env
BOT_TOKEN=ваш_токен_бота
CHAT_ID=ваш_chat_id
HOSTNAME=имя_сервера_или_оставьте_пустым
TIMEOUT=10
```

> **HOSTNAME** используется в сообщениях, если не указан — берётся системное имя.
> **TIMEOUT** — таймаут для отправки сообщений в секундах.

---

### 4. Настройка systemd таймера

* Копируем `.service` и `.timer` в папку user systemd:

```bash
cp server_status_bot.service ~/.config/systemd/user/
cp server_status_bot.timer ~/.config/systemd/user/
```

* Перезагружаем демона и включаем таймер:

```bash
systemctl --user daemon-reload
systemctl --user enable server_status_bot.timer
systemctl --user start server_status_bot.timer
```

* Проверяем статус и логи:

```bash
systemctl --user status server_status_bot.timer
journalctl --user -u server_status_bot.service -f
```

> Скрипт `start_bot.sh` гарантирует, что таймер будет запускать скрипт с правильным Python из `.venv` и подгружать `.env`.

---

### 5. Проверка работы

* Первое сообщение в Telegram должно прийти в течение нескольких минут после запуска таймера.
* Логи можно смотреть через `journalctl`:

```bash
journalctl --user -u server_status_bot.service -f
```

---

### 6. Важные заметки

* **Никогда не пушьте `.env` с токенами в публичный репозиторий.**
* Системный таймер запускается **от имени пользователя**, который его создал. `%h` в `.service` = домашняя папка пользователя.
* Любой пользователь может клонировать репозиторий, создать `.venv` и `.env`, и таймер будет работать без ручной правки путей.
