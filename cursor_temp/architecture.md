# 🏗️ АРХИТЕКТУРА BIZIG / OPENCLAW WORKSPACE

## 📁 Структура workspace

```
/root/.openclaw/workspace
├── AGENTS.md
├── HEARTBEAT.md              # задачи автопилота Bizig
├── cursor_temp/              # глобальные правила и состояние Bizig
│   ├── BIZIK_RULES.md
│   ├── Bizig2Dev.md
│   ├── architecture.md
│   └── DEVELOPMENT_HISTORY.md
├── projects/                 # проекты (боты/сервисы/скрипты)
│   └── ...
├── repositories/             # клоны git‑репозиториев
│   └── ...
└── skills/, test/, ...
```

## 🧠 Компоненты

- **Bizig Core (OpenClaw агент)** — читает/пишет файлы в `cursor_temp/`, управляет задачами и архитектурой.
- **Git/GitHub слой** — локальный git в `/root/.openclaw/workspace` с remote `Rules.git`.
- **Projects** — отдельные подпроекты в `projects/` с собственным кодом и планами.
- **Telegram Bot (Bizig Bot)** — отдельный сервис на Python + aiogram, работает с теми же файлами.

## 📲 Bizig Telegram Bot (проект)

Стек: Python 3 + aiogram v3.

Локально код будет жить в:
- `repositories/bizig-telegram-bot/`

Основные функции бота:
- Показать статус проектов и задач (чтение `Bizig2Dev.md`).
- Показать правила, архитектуру, историю.
- Работать с reply‑клавиатурой + inline‑кнопками.
- Принимать голосовые сообщения (OGG) и передавать их в голосовой пайплайн.

## 🎙 Голосовой пайплайн (OGG → задачи)

Высокоуровневая схема:
1. Пользователь отправляет голосовое (OGG) в Telegram‑бот.
2. Бот транскрибирует речь (через Whisper / внешний транскрипт‑бот).
3. Bizig получает текст и по маркеру распределяет его в:
   - `Bizig2Dev.md` — новые задачи,
   - `architecture.md` — изменения архитектуры,
   - `BIZIK_RULES.md` — обновление правил.
4. Обновления логируются в `DEVELOPMENT_HISTORY.md`.

Эта архитектура будет уточняться по мере разработки бота.
