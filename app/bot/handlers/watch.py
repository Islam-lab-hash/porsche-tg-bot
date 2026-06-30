from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("watch"))
async def watch_command(message: Message) -> None:
    await message.answer(
        "Мониторинг включён для MVP-сценария. "
        "В Docker он запускается через APScheduler-заготовку; полноценная запись настройки в БД уже подготовлена."
    )


@router.message(Command("stop"))
async def stop_command(message: Message) -> None:
    await message.answer("Мониторинг отключён.")
