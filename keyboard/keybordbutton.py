from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from others.requests import Requests


async def get_button_name(name):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                text=name
            )
                ]
        ], 
        resize_keyboard=True,
        one_time_keyboard=True
    )



# async def get_number():
#     return ReplyKeyboardMarkup(keyboard=[
#         [
#             KeyboardButton( 
#                 text='Отправить номер телефона', 
#                 request_contact=True)
#          ]
#         ],
#             resize_keyboard=True, 
#             input_field_placeholder='Нажмите на кнопку'
#         )
    
    

async def kb_get_date(requests: Requests):
    list_date = await requests.db_get_date()
    date_list = InlineKeyboardBuilder()
    
    for el_date in list_date:
        date_list.add(InlineKeyboardButton(
            text=el_date,
            callback_data=f'reserver_date={el_date}'
        ))
    return date_list.adjust(2).as_markup()



async def get_kb_time(requests: Requests, data_needed):
    list_time = await requests.db_get_time(data_needed)
    time_list = InlineKeyboardBuilder()

    for el_date in list_time:
        time_list.add(InlineKeyboardButton(
            text=el_date,
            callback_data=f'reserver_time={el_date}'
            ))
    return time_list.adjust(3).as_markup()


    
     