import asyncio
from typing import Union

from discord import Message
from discord.ext.commands import Context
from fastapi import FastAPI
from pydantic import BaseModel

import env

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.on_event("startup")
async def startup_event():
    # from DiscordBots.clean_example import bot
    # asyncio.create_task(bot.start(env.DISCORD_TOKEN))
    # bot.get_context()
    pass


@app.get("/")
async def connect_bot():
    await startup_event()
    return {"status": "bot connected"}


@app.get("/interactions")
def read_root():
    message = Message()
    # bot.get_context()
    # ctx = Context(message=message, bot=bot, view=None)
    # join(ctx)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
