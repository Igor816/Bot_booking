from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile#InputMediaPhoto, Contact
from aiogram import Router, F, Bot
from aiogram.filters import Command
import re


from others.requests import Requests
from others.state_user import States
from others.data_user import get_data_state, get_data_for_admin, db_get_service_price

from keyboard.keybordbutton import get_button_name, kb_get_date, get_kb_time#, get_number
from keyboard.services_button import kb_get_services, kb_get_add_services
from keyboard.edit_keyboards import delete_button, buy_button
from keyboard.admin_keyboards import admin_button

from data.config import settin


rout = Router()


@rout.callback_query(F.data.startswith('add_service_cansel'))
async def add_service_cansel(call: CallbackQuery, state: FSMContext):
        await call.message.edit_text(await get_data_state(state), reply_markup=await buy_button())
        

    
@rout.callback_query(F.data.startswith('clean_card'))
async def clear_card(call: CallbackQuery, state: FSMContext):
        await state.clear()
        await call.message.edit_text('Корзина очищенна. Чтобы начать заново нажмите /start', reply_markup=None)
        await state.clear()
        

@rout.callback_query(F.data.startswith('application'))    
async def application(call: CallbackQuery, state: FSMContext):
    # await state.set_state(States.state_get_phone)
    await state.set_state(States.hand_enter_number)
    await call.message.answer('Оставьте ваш номер телефона :)')#await get_number()


@rout.callback_query(F.data.startswith('add_service'), States.state_add_service)
async def handler_add_servise(call: CallbackQuery, state: FSMContext):
    add = []
    
    data = await state.get_data()
    if 'state_add_service' in data:
        add = data['state_add_service']

    add_service = call.data.split('=')[1].split('|')[0]
    add_service_price = call.data.split('=')[1].split('|')[1]
    add.append({add_service: add_service_price})
    
    await state.update_data(state_add_service=add)
    keyboard = await delete_button(call.message.reply_markup, call.data)
    await call.message.edit_text(await get_data_state(state), reply_markup=keyboard)



@rout.callback_query(F.data.startswith('services'), States.state_service)
async def get_add_service(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data_needed = data['state_date'] 
    time_needed = data['state_time']
    service = call.data.split('=')[1].split('|')[0]
    price = call.data.split('|')[1].split('|')[0]
    
    await state.update_data(state_service=service, price=price)
    await state.set_state(States.state_add_service)
    await call.message.edit_text(f"Выбранная дата: {data_needed}\r\nВыбранное время:  {time_needed}\r\nВаша стрижка: {service} {price}\n"
                                f"Я могу предложить вам одну из наши соопуствующих услуг: ",
                                reply_markup= await kb_get_add_services())




@rout.callback_query(F.data.startswith('reserver_time='), States.state_time)
async def get_service(call: CallbackQuery, state: FSMContext, requests: Requests):
    data = await state.get_data()
    data_needed = data['state_date'] 
    time_needed = call.data.split('=')[1]
    
    await state.update_data(state_time=time_needed)
    await state.set_state(States.state_service)
    await call.message.edit_text(f'Выбранная дата: {data_needed}\r\n Выбранное время: {time_needed}\r\n'
                                 f'Теперь выберите стрижку', reply_markup= await kb_get_services())
    await requests.db_change_statuse('process', data_needed, time_needed)
    
    
    

@rout.callback_query(F.data.startswith('reserver_date='), States.state_date)
async def get_time(call: CallbackQuery, state: FSMContext, requests: Requests):
    data_needed = call.data.split('=')[1]
    
    await call.message.edit_text(f'Выбрана дата: {data_needed}\r\nТеперь выберите желаемое время:',
                                reply_markup=await get_kb_time(requests, data_needed))
    await state.set_state(States.state_time)
    await state.update_data(state_date=data_needed)



@rout.message(F.text == "/catalog")
async def get_photo_catalog(message: Message, bot: Bot):
    """"
    Создать кнопку для показа след. фото без цикла в хендерах. Там же можем использовать
    сетку для вывода красивого интерфейса фотографий(в виде сетки 3х3 или 3х4)
    """
    media = [
        FSInputFile("image/photo_2025-06-18_06-59-26.jpg"),
        FSInputFile("image/photo_2025-06-18_06-59-28.jpg"),
        FSInputFile("image/photo_2025-06-18_06-59-30.jpg"),
        FSInputFile("image/photo_2025-06-18_07-00-01.jpg"),
        FSInputFile("image/photo_2025-06-18_07-00-08.jpg"),
        FSInputFile("image/photo_2025-06-18_07-00-11.jpg"),
        FSInputFile("image/photo_2025-06-18_07-00-14.jpg")
    ]
    
    for i in media:
        await message.answer_photo(i)



@rout.message(States.state_name)
async def get_data(message: Message, state: FSMContext, requests: Requests): 
    await message.answer(f'Приятно познакомится {message.text}, выберите дату: ', 
                         reply_markup= await kb_get_date(requests))
    await state.update_data(state_name=message.text)
    await state.set_state(States.state_date)



@rout.message(Command(commands=['start']))
async def get_name(message: Message, state: FSMContext, requests: Requests):
    await message.answer('Привет! Я помощник салона красоты Мальвина. Как я могу к тебе обращаться?',
                         reply_markup= await get_button_name(message.from_user.first_name))
    await state.set_state(States.state_name)
    await requests.add_user(message.from_user.id, message.from_user.last_name,
                            message.from_user.first_name, message.from_user.username)
    
      
     

@rout.message(States.hand_enter_number)  
async def check_phone(message: Message, state: FSMContext, bot: Bot, requests: Requests):
    result = re.match(r'(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                      message.text)
    if not result:
        return await message.answer('Это не похоже на номер телефона, попробуйте еще раз!')
    await state.update_data(hand_enter_number= message.text)
    await message.answer('Спасибо за ваш заказ! Ваши данные переданы менеджеру, ожидайте звонка! ')
    
    data = await state.get_data()
    date_needed = data['state_date']
    time_needed = data['state_time']
    number = data["hand_enter_number"]
    
    await requests.db_get_phone(message.from_user.id, number)
    await bot.send_message(chat_id=settin.ID_admin, text=await get_data_for_admin(state),
                           reply_markup= await admin_button(date_needed, time_needed, 
                                                            message.from_user.id))
    await db_get_service_price(state, requests)

    
    
    