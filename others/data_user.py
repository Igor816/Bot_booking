from aiogram.fsm.context import FSMContext
from others.requests import Requests 

async def db_get_service_price(state: FSMContext, requests: Requests):
    data = await state.get_data()
    date_ = data['state_date']
    time_ = data['state_time']
    dict_data = data["state_add_service"]
    service = data['state_service']
    price = data['price']
    
    
    text_serv = [service]
    total_price = int(price) 
    
    for el_data in dict_data:
        for key, value in el_data.items():
            text_serv.append(key) 
            total_price += int(value)
        
    text_result= ", ".join(text_serv)
    
    await requests.db_paste_serv_price(text_result, total_price, date_, time_)


async def get_data_state(state: FSMContext):
    data = await state.get_data()
    data_needed = data['state_date']
    time_needed = data['state_time']
    service = data['state_service']
    price = data['price']
    
    text_user = f"Выбранная дата: {data_needed},\r\nВыбранное время: {time_needed},\
    \r\nВаша стрижка: {service} {price}\r\n"
    total_price = int(price) 
    
    if "state_add_service" in data:
        dict_data = data["state_add_service"]
        
        text_user += "\r\nСопутствуещие услуги: "            
    
        for el_data in dict_data:
            for key, value in el_data.items():
                text_user += f"\r\n{key} {value}$" 
                total_price += int(value)
        
        text_user += f"\r\n\r\nСумма к оплате: {total_price}$"
    
    return text_user



async def get_data_for_admin(state: FSMContext):
    data = await state.get_data()
    data_needed = data['state_date']
    time_needed = data['state_time']
    service = data['state_service']
    price = data['price']
    
    name = data['state_name']
    # phone = data['state_get_phone']
    phone2 = data['hand_enter_number']
    
    text_user = f"Требуется подтверждение.\n"\
                f"Имя: {name},\r\nТелефон: {phone2},\n"\
                f"Дата: {data_needed},\r\nВремя: {time_needed},\r\n"\
                f"Cтрижка: {service} {price}\r\n$"
    
    total_price = int(price) 
    
    if "state_add_service" in data:
        dict_data = data["state_add_service"]
        
        text_user += "\r\nСопутствуещие услуги: "            
    
        for el_data in dict_data:
            for key, value in el_data.items():
                text_user += f"\r\n{key} {value}$" 
                total_price += int(value)
        
        text_user += f"\r\n\r\nСумма к оплате: {total_price}$"
    
    return text_user