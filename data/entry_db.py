# import datetime as DT
from datetime import datetime as dt, timedelta, time, date

import asyncpg
from asyncpg import Connection

# import psycopg
# from psycopg import Connection

from data.config import settin
from data.settings import async_engine


async def database_entry():
    pool = await asyncpg.create_pool(
            host='127.0.0.1', port='5432', user='postgres', password='89936684600Ant', 
            database='boking_bot', command_timeout=10
        ) 
    
    if await get_count_row(pool) < 1:
        query = await get_query(3, str(dt.today().date()))

    else:
        query = await get_query(1, str(dt.today().date()))
  
        
    await pool.execute(query)
    await pool.close()


async def get_count_row(conn: Connection):
    count = await conn.fetchrow("SELECT COUNT(*) FROM booking")
    return count[0]


async def get_query(count_days, target_day):  # forming request. In parameters accepts - day reception and want day
    query = 'INSERT INTO booking (b_date, b_time, b_status, b_datetime) VALUES'

    target = dt.strptime(target_day, '%Y-%m-%d').date() + timedelta(days=1)  # to current day add day

    for x in range(count_days):
        date_target = target + timedelta(days=x)  # Объявим переменую в которой поместим след день
        for i in range(0, 10 * 60, 60):
            
            time_delta = f'{dt.combine(date.today(), time(8, 0)) + timedelta(minutes=i)}'
            times = dt.strptime(time_delta, '%Y-%m-%d %H:%M:%S')
            end_time = times.strftime("%H:%M")
                                    
                                    
            full_date_time = f'{date_target} {end_time}'
            # Формируем строку для запроса
            line = f"\r\n('{date_target}', '{end_time}', 'free', '{full_date_time}'),"
            query += line

    query = f'{query.strip(query[-1])};'
    return query

