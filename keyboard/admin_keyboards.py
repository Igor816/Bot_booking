from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup#KeyboardButton, # ReplyKeyboardMarkup

# async def admin_button(date, time, user_id):
#     keybord = InlineKeyboardBuilder()
    
#     keybord.add(InlineKeyboardButton(
#                     text='Подтвердить',
#                     callback_data=f'confirmreserve={date}|{time}|{user_id}'
#     ),
#                 InlineKeyboardButton(
#                     text='Отклонить',
#                     callback_data=f'canselreserve={date}|{time}|{user_id}'
#                 )) 
#     return keybord


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

# async def admin_button(date, time, user_id):
#     kb = [
#         KeyboardButton(
#             text='Подтвердить',
#             callback_data=f'confirmreserve={date}|{time}|{user_id}'
#         ),
#         KeyboardButton(
#             text='Отклонить',
#             callback_data=f'canselreserve={date}|{time}|{user_id}'
#         )
#     ]
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder='Выбор за вами, хехе'
#     )
#     return keyboard  