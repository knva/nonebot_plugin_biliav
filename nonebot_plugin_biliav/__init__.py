# import nonebot
from nonebot import get_driver, on_regex

from .config import Config
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, Message

global_config = get_driver().config
config = Config(**global_config.dict())

from .data_source import get_av_data
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
biliav = on_regex("^av*|^BV*")
@biliav.handle()
async def handle(bot:Bot,event:Event,state:T_State):
    rj = await get_av_data(event.get_message())
    await biliav.send(rj)
