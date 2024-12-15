from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Callable, Awaitable


class StatsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict], Awaitable],
            event: Message,
            data: dict
    ):
        user_id = event.from_user.id
        print(f"User {user_id} triggered an event.")
        await handler(event, data)
