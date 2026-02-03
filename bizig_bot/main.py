import asyncio
import os
from pathlib import Path

from aiogram import F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import create_bot, create_dispatcher


WORKSPACE_ROOT = Path("/root/.openclaw/workspace")
CURSOR_TEMP = WORKSPACE_ROOT / "cursor_temp"
BIZIG2DEV = CURSOR_TEMP / "Bizig2Dev.md"
BIZIK_RULES = CURSOR_TEMP / "BIZIK_RULES.md"


class ProjectState(StatesGroup):
    active_project = State()


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Главное меню")],
            [KeyboardButton(text="📂 Проекты"), KeyboardButton(text="🤖 Агенты")],
            [KeyboardButton(text="📊 Статус"), KeyboardButton(text="📜 Правила")],
            [KeyboardButton(text="📌 Next steps")],
        ],
        resize_keyboard=True,
    )


async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет, я Bizig‑бот (CloudBot мультиагент).\n"
        "Выбери действие:",
        reply_markup=main_menu_kb()
    )


async def handle_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🏠 Главное меню", reply_markup=main_menu_kb())


def _read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Файл {path.name} не найден."
    except Exception as e:  # noqa: BLE001
        return f"Не удалось прочитать {path.name}: {e}"


async def handle_status(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project = data.get("active_project", "Bizig (default)")
    
    text = _read_file_safe(BIZIG2DEV)
    todo = text.count("[TODO]")
    wip = text.count("[WIP]")
    done = text.count("[DONE]")
    blocked = text.count("[BLOCKED]")
    
    await message.answer(
        f"📊 Статус: {project}\n\n"
        f"TODO: {todo}\n"
        f"WIP: {wip}\n"
        f"DONE: {done}\n"
        f"BLOCKED: {blocked}"
    )


async def handle_rules(message: Message) -> None:
    raw = _read_file_safe(BIZIK_RULES)
    lines = raw.splitlines()
    head = "\n".join(lines[:80])
    if len(lines) > 80:
        head += "\n\n… (смотри полный файл BIZIK_RULES.md в репозитории)"
    await message.answer(f"📜 Правила Bizig\n\n{head}")


async def handle_next_steps(message: Message) -> None:
    text = _read_file_safe(BIZIG2DEV)
    lines = text.splitlines()
    tasks: list[str] = []
    for line in lines:
        line = line.strip()
        if line.startswith("### [") and "T20" in line:
            tasks.append(line.lstrip("# "))
        if len(tasks) >= 5:
            break
    if not tasks:
        await message.answer("📌 Next steps\n\nПока нет активных задач T20x в Bizig2Dev.md")
        return
    joined = "\n".join(f"- {t}" for t in tasks)
    await message.answer(f"📌 Next steps\n\n{joined}")


async def handle_projects(message: Message, state: FSMContext) -> None:
    # Список проектов (пока хардкод, потом можно читать из Task2Dev.md)
    projects = [
        "Bizig (default)",
        "PingiVPN",
        "My Jarvis",
        "HIGISFIELD",
        "WriteTapping",
    ]
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=p)] for p in projects
        ] + [[KeyboardButton(text="🏠 Главное меню")]],
        resize_keyboard=True,
    )
    
    data = await state.get_data()
    current = data.get("active_project", "Bizig (default)")
    
    await message.answer(
        f"📂 Проекты\n\nТекущий: {current}\n\nВыбери проект:",
        reply_markup=kb
    )


async def handle_project_select(message: Message, state: FSMContext) -> None:
    project_name = message.text
    await state.update_data(active_project=project_name)
    await message.answer(
        f"✅ Переключился на проект: {project_name}",
        reply_markup=main_menu_kb()
    )


async def handle_agents(message: Message) -> None:
    # Заглушка для агентов (пока список хардкод)
    agents = [
        "Cursor-1 (Architect)",
        "Cursor-2 (Developer)",
        "ClawBot (Autonomous)",
        "Bizig-Bot (Telegram)",
    ]
    
    text = "🤖 Агенты\n\n" + "\n".join(f"- {a}" for a in agents)
    text += "\n\n(Функция переключения агентов в разработке)"
    
    await message.answer(text)


async def main() -> None:
    token = os.environ.get("BIZIG_BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задан BIZIG_BOT_TOKEN в переменных окружения")

    bot = create_bot(token)
    dp = create_dispatcher()

    # Главное меню
    dp.message.register(cmd_start, F.text == "/start")
    dp.message.register(handle_main_menu, F.text == "🏠 Главное меню")
    
    # Основные кнопки
    dp.message.register(handle_status, F.text == "📊 Статус")
    dp.message.register(handle_rules, F.text == "📜 Правила")
    dp.message.register(handle_next_steps, F.text == "📌 Next steps")
    
    # Проекты и агенты
    dp.message.register(handle_projects, F.text == "📂 Проекты")
    dp.message.register(handle_agents, F.text == "🤖 Агенты")
    
    # Выбор проекта (любой текст, который совпадает с названием проекта)
    project_names = ["Bizig (default)", "PingiVPN", "My Jarvis", "HIGISFIELD", "WriteTapping"]
    for pname in project_names:
        dp.message.register(handle_project_select, F.text == pname)

    await dp.start_polling(bot)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
