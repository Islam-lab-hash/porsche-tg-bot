from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.keyboards import main_keyboard
from app.bot.messages import HELP_TEXT, START_TEXT
from app.db.repositories import get_or_create_user
from app.db.session import SessionLocal


router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    try:
        async with SessionLocal() as session:
            await get_or_create_user(session, message.from_user.id, message.from_user.username)
    except Exception:
        pass
    await message.answer(START_TEXT, reply_markup=main_keyboard())


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(HELP_TEXT)
