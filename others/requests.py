from datetime import datetime
from sqlalchemy import text#insert, update, values


class Requests:
    def __init__(self, conn):
        self.conn = conn


    
    
    async def db_get_date(self):
        date_now = datetime.today().strftime("%d.%m.%Y %H:%M")
        date_raw = datetime.strptime(date_now, "%d.%m.%Y %H:%M")
        query = text("""SELECT DISTINCT b_date
                        FROM booking
                        WHERE b_status= 'free'
                        AND b_datetime > :date_now
                        ORDER BY b_date ASC LIMIT 3 
                     """)
        rows = await self.conn.execute(query, {'date_now':date_raw})
        results = rows.fetchall()
        
        list_date = [str(result[0].strftime('%d.%m.%Y')) for result in results]
        return list_date
    
    
    
    async def db_get_time(self, data_needed):
        data_now = datetime.today().strftime("%d.%m.%Y %H:%M")
        data_now1 = datetime.strptime(data_now, "%d.%m.%Y %H:%M")
        date_raw = datetime.strptime(data_needed, "%d.%m.%Y")
        
        query = text("""SELECT DISTINCT b_time 
                     FROM booking 
                     WHERE b_status = 'free' 
                     AND b_date = :data_needed 
                     AND b_datetime > :date_raw 
                     ORDER BY b_time ASC
                     """)
        rows = await self.conn.execute(query, {'data_needed':date_raw, 'date_raw':data_now1})
        results = rows.fetchall()
        
        list_time = [str(result[0].strftime("%H:%M")) for result in results]
        return list_time
    
    
    
    async def add_user(self, id_users, last_name, name_first, username):
        query = text(f"INSERT INTO users (telegram_id, first_name, last_name, username) " \
                f"VALUES (:id_users, :last_name, :name_first, :username)" \
                f"ON CONFLICT (telegram_id) " \
                f"DO UPDATE SET username=:username, last_name=:last_name, first_name=:name_first")
        await self.conn.execute(query, {'id_users':id_users, 'last_name':last_name, 
                                            'name_first':name_first, 'username':username})
    
    
    
    async def db_change_statuse(self, status, date, time):
        date_ = datetime.strptime(date, "%d.%m.%Y")
        time_ = datetime.strptime(time, "%H:%M")
        query = text("""
            UPDATE booking SET b_status=:status 
            WHERE b_date = :date
            AND b_time = :time
        """)
        
        
        await self.conn.execute(query, {"status": status, "date": date_, "time": time_})
        
    async def db_paste_serv_price(self, serv_, price_, date, time):
        date_ = datetime.strptime(date, "%d.%m.%Y")
        time_ = datetime.strptime(time, "%H:%M")
        query = text("""
                    UPDATE booking 
                    SET 
                        b_service=:serv,
                        b_price = :price 
                    WHERE b_date = :date
                    AND b_time = :time 
                     """)
        await self.conn.execute(query, {"serv": serv_, "price":price_, 
                                        "date":date_, "time": time_})