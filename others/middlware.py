import asyncio
from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from data.settings import async_sessionmaker, AsyncSession
from others.requests import Requests


class DbSession(BaseMiddleware):
    def __init__(self, session_poll: async_sessionmaker[AsyncSession]):
        self.session_poll = session_poll
    
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        async with self.session_poll.begin() as session:
            data['requests'] = Requests(session)
            return await handler(event, data)
        
        
######################################

# class SlowpokeMiddleware(BaseMiddleware):
#     def __init__(self, sleep_sec: int):
#         self.sleep_sec = sleep_sec
        
#     async def __call__(self, 
#                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
#                        event:TelegramObject, 
#                        data:Dict[str, Any],
#                        ) -> Any:
        
#         await asyncio.sleep(self.sleep_sec)
#         result = await handler(event, data)
#         print(f'Hanler was deplayed by {self.sleep_sec} seconds')
#         return result
#######################################

# class UserInternalIdMiddleware(BaseMiddleware):
#     def get_internal_id(self, user_id: int) -> int:
#         return randint(100_000_000, 900_000_000) + user_id
    
#     async def __call__(self, 
#                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
#                        event:TelegramObject, 
#                        data:Dict[str, Any],
#                        ) -> Any:
#         user = data['event_from_user']
#         data['internal_id'] = self.get_internal_id(user.id)
#         return await handler(event, data)
    
    
# class HappyMonthMiddleware(BaseMiddleware):
#     async def __call__(self, 
#                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
#                        event:TelegramObject, 
#                        data:Dict[str, Any],
#                        ) -> Any:
        
#         internal_id: int = data['internal_id']
#         current_month: int = datetime.now().month
#         is_happy_month: bool = (internal_id % 12) == current_month
#         data['is_happy_month'] = is_happy_month
#         return await handler(event, data)
    
