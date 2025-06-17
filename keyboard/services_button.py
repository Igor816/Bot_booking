from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



        
async def kb_get_add_services():
    dict_services = {"Маникюр": 1200 ,"Педикюр": 500, "Реснички": 800}
    date_list = InlineKeyboardBuilder()
    
    for k, v in dict_services.items():
        date_list.add(InlineKeyboardButton(
            text=f'{k}: {v}$',
            callback_data=f'add_service={k}|{v}'
        ))
    
    date_list.add(InlineKeyboardButton(
        text='Спасибо, не надо',
        callback_data='add_service_cansel'
    ))
    
    return date_list.adjust(3).as_markup()


async def kb_get_services():
    dict_services = {"Пикси": 100, "Боб": 200, "Милитари": 120, "Гарсон": 180, 
                     "Гранж": 220, "Аврора": 250, "Голливуд": 300, "Итальянка": 270,
                     "Асиметрия": 260, "Лесенка": 240, "Шегги": 315, "Волчица":330}
    date_list = InlineKeyboardBuilder()
    
    for k, v in dict_services.items():
        date_list.add(InlineKeyboardButton(
            text=f'{k}: {v}$',
            callback_data=f'services={k}|{v}'
        )) 
    
    return date_list.adjust(3).as_markup()
