from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config.settings import get_settings
from app.db.repositories import get_or_create_user, set_user_budget
from app.db.session import SessionLocal
from app.utils.money import format_rub


router = Router()


@router.message(Command("settings"))
async def settings_command(message: Message) -> None:
    defaults = get_settings()
    budget = defaults.default_budget_rub
    try:
        async with SessionLocal() as session:
            user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
            budget = user.budget_rub
    except Exception:
        pass
    await message.answer(
        "Текущие настройки:\n"
        f"Бюджет: {format_rub(budget)}\n"
        "Модели: Porsche Panamera GTS 2019, Porsche 911 2019\n"
        "Источники: mock_ru, mock_foreign\n"
        "Зарубежные лоты: включены\n"
        "Утопленники: включены\n"
        "Минимальный score: 40\n\n"
        "Изменить бюджет: /budget 4000000"
    )


@router.message(Command("budget"))
async def budget_command(message: Message) -> None:
    parts = message.text.split(maxsplit=1) if message.text else []
    if len(parts) != 2 or not parts[1].replace(" ", "").isdigit():
        await message.answer("Напиши так: /budget 4000000")
        return
    budget = int(parts[1].replace(" ", ""))
    if budget < 500_000:
        await message.answer("Бюджет выглядит слишком маленьким. Укажи сумму от 500 000 ₽.")
        return
    try:
        async with SessionLocal() as session:
            await set_user_budget(session, message.from_user.id, budget)
    except Exception:
        await message.answer("Бюджет принят для текущего поиска, но БД сейчас недоступна.")
        return
    await message.answer(f"Бюджет сохранён: {format_rub(budget)}")


@router.message(Command("sources"))
async def sources_command(message: Message) -> None:
    await message.answer(
        "Доступные источники MVP:\n"
        "- mock_ru: российские тестовые объявления\n"
        "- mock_foreign: зарубежный тестовый salvage-аукцион\n\n"
        "Файлы-заготовки для Авито, Авто.ру, Дром, Copart и IAAI уже есть."
    )
