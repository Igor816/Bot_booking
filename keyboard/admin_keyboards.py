from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup



async def admin_button(date, time, user_id):
    keyboards =  InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
            text='Подтвердить',
            callback_data=f'confirmreserve={date}|{time}|{user_id}'
        ),
            InlineKeyboardButton(
                    text='Отклонить',
                    callback_data=f'canselreserve={date}|{time}|{user_id}'
                )
        ]
    ])
    return keyboards
