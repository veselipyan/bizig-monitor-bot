# 🤖 Мониторинг Бизиг Бот

Telegram-бот для мониторинга и управления мультиагентной системой (OpenClaw, Cursor-1, Cursor-2).

## 🎯 Функции (MVP)

- 🏠 **Главное меню** — центр управления
- 📂 **Проекты** — список проектов (Bizig, PingiVPN, My Jarvis, HIGISFIELD, WriteTapping) + выбор активного
- 🤖 **Агенты** — список агентов (OpenClaw, Cursor-1, Cursor-2, Bizig-Bot) + статус
- 📊 **Статус** — общая картина (TODO/WIP/DONE/BLOCKED)
- 📜 **Правила** — показывает BIZIK_RULES.md
- 📌 **Next steps** — ближайшие задачи из Task2Dev.md

## 🚀 Установка

### 1. Клонировать репозиторий
```bash
git clone git@github.com:veselipyan/bizig-monitor-bot.git
cd bizig-monitor-bot
```

### 2. Создать виртуальное окружение
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Создать бота через @BotFather
1. Открыть [@BotFather](https://t.me/BotFather) в Telegram
2. Отправить `/newbot`
3. Ввести имя и username
4. Получить токен

### 5. Запустить бота
```bash
export BIZIG_BOT_TOKEN=YOUR_TOKEN_HERE
python -m bizig_bot.main
```

## 🔧 Настройка systemd (автозапуск)

### 1. Создать systemd unit файл
```bash
sudo nano /etc/systemd/system/bizig-monitor-bot.service
```

### 2. Добавить содержимое
```ini
[Unit]
Description=Мониторинг Бизиг Бот (CloudBot MultiAgent Interface)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/bizig-monitor-bot
Environment=BIZIG_BOT_TOKEN=YOUR_TOKEN_HERE
ExecStart=/path/to/bizig-monitor-bot/.venv/bin/python -m bizig_bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Запустить и включить автозапуск
```bash
sudo systemctl daemon-reload
sudo systemctl enable bizig-monitor-bot.service
sudo systemctl start bizig-monitor-bot.service
sudo systemctl status bizig-monitor-bot.service
```

## 📝 Зависимости

- Python 3.10+
- aiogram 3.13.0+

## 🔐 Безопасность

- Whitelist пользователей (только указанные User ID могут использовать бота)
- Токен бота хранится в переменной окружения

## 🚧 Roadmap (Фаза 2)

- [ ] 🔔 Автоматические уведомления о завершении задач
- [ ] 📋 Список задач + фильтры
- [ ] ➕ Создание задач через бота
- [ ] 📜 Логи агентов (последние 20-50 строк)
- [ ] ⏸️ Команды агентам (пауза/стоп/рестарт)
- [ ] 🎤 Голосовые команды
- [ ] 📈 Статистика и графики

## 📚 Документация

- [Концепция бота](https://github.com/veselipyan/bizig-monitor-bot/blob/master/docs/CONCEPT.md) (TODO)
- [Инструкция для ClawBot](https://github.com/veselipyan/bizig-monitor-bot/blob/master/docs/CLAWBOT_MANUAL.md) (TODO)

## 📄 Лицензия

MIT

## 👤 Автор

[@veselipyan](https://github.com/veselipyan)
