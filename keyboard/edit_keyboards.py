from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def delete_button(keyboard: InlineKeyboardMarkup, el_del):
    '''Не понятно в какой момент он добавляет доп услуги в счет и удаляет кнопки доп.услуг'''
    keyboard_new = []
    
    for keys in keyboard.inline_keyboard:
        time_key = []
        
        for key in keys:
            if el_del not in key.callback_data:
                if 'Спасибо, не надо' in key.text:
                    key.text = 'Пожалуй хватит'
                time_key.append(key)
            
        keyboard_new.append(time_key)
        
    keyboards = InlineKeyboardMarkup(inline_keyboard=keyboard_new)
    
    if len(keyboards.inline_keyboard[0]) >= 1:
        return keyboards
    else:
        return await buy_button()
        

async def buy_button():
    keyboards = InlineKeyboardBuilder()
    keyboards.add(
        InlineKeyboardButton(
            text='Оформить заявку',
            callback_data='application'
        ),
        InlineKeyboardButton(
            text='Перейти к оплате',
            callback_data='order'
        ),
        InlineKeyboardButton(
            text='Очистить корзину',
            callback_data='clean_card'
            )
    
    )
    
    return keyboards.adjust(2).as_markup()
    