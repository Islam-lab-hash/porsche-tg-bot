from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Начать поиск")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="⭐ Избранное")],
        ],
        resize_keyboard=True,
    )


def listing_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Открыть объявление", url=url)],
            [
                InlineKeyboardButton(text="💰 Подробный расчёт", callback_data="cost_details"),
                InlineKeyboardButton(text="🧠 Повреждения", callback_data="damage_details"),
            ],
            [
                InlineKeyboardButton(text="⭐ В избранное", callback_data="favorite"),
                InlineKeyboardButton(text="❌ Скрыть", callback_data="hide"),
            ],
        ]
    )
