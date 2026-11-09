from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def registration_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data="confirm_reg"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Начать заново",
                    callback_data="restart_reg"
                )
            ]
        ]
    )

    return keyboard