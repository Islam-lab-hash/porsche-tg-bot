from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message


router = Router()


@router.message(Command("favorites"))
@router.message(F.text == "⭐ Избранное")
async def favorites_command(message: Message) -> None:
    await message.answer("Избранное подготовлено в БД. В MVP кнопка сохраняет действие, полноценный список добавляется следующим шагом.")


@router.callback_query(F.data == "favorite")
async def favorite_callback(callback: CallbackQuery) -> None:
    await callback.answer("Добавлено в избранное для MVP-сценария")


@router.callback_query(F.data == "hide")
async def hide_callback(callback: CallbackQuery) -> None:
    await callback.answer("Скрыто для MVP-сценария")


@router.callback_query(F.data == "cost_details")
async def cost_callback(callback: CallbackQuery) -> None:
    await callback.answer("Подробный расчёт уже показан в карточке", show_alert=True)


@router.callback_query(F.data == "damage_details")
async def damage_callback(callback: CallbackQuery) -> None:
    await callback.answer("Повреждения уже показаны в карточке", show_alert=True)
