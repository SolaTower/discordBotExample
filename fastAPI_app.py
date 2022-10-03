import asyncio
from typing import Union

from discord import Message
from discord.ext.commands import Context
from discord.ui import View
from fastapi import FastAPI
from pydantic import BaseModel

import env
from DiscordBots.clean_example import bot

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def connect_bot():
    await bot.start(env.DISCORD_TOKEN)
    return {"status": "bot connected"}


@app.get("/interactions")
def read_root():
    from DiscordBots.clean_example import bot, join
    message = Message()
    bot.get_context()
    ctx = Context(message=message, bot=bot, view=None)
    join(ctx)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
