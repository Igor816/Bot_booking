from aiogram import Router, F,  Bot
from aiogram.types import CallbackQuery

from others.requests import Requests

rou = Router()


@rou.callback_query(F.data.startswith('confirmreserve') | F.data.startswith('canselreserve'))
async def answer_reserve(call: CallbackQuery, requests: Requests, bot: Bot):
    type_answer = call.data.split('=')[0]
    date_answer = call.data.split('=')[1].split('|')[0]
    time_answer = call.data.split('=')[1].split('|')[1]
    id_user_answer = call.data.split('=')[1].split('|')[2]
    
    text = call.message.text.replace('Требуется подтверждение', '')
    
    if 'confirmreserve' in type_answer:
        await requests.db_change_statuse('buse', date_answer, time_answer)
        msg_user = f'ВАШ ЗАКАЗ ПОДТВЕРЖДЕН\r\n\r\n{text}\nМенеджер вам перезвонит!' 
        msg_admin = f'ЗАКАЗ ПОДТВЕРЖДЕН\r\n\r\n{text}' 
        await call.message.edit_text(msg_admin, reply_markup=None)
        await bot.send_message(id_user_answer, msg_user)
    else:
        msg_user = f'ВАШ ЗАКАЗ ОТКЛОНЕН\r\n\r\n{text}'
        msg_admin = f'ЗАКАЗ ОТКЛОНЕН\r\n\r\n{text}'
        await bot.send_message(id_user_answer, msg_user)
        await call.message.edit_text(msg_admin, reply_markup=None)
        
        
    # await call.message.edit_text(msg_admin, reply_markup=None)
    