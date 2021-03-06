# import nonebot
from nonebot import get_driver, on_regex

from .config import Config
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, Message

global_config = get_driver().config
config = Config(**global_config.dict())

from .data_source import get_av_data
import re
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
biliav = on_regex("av(\d{1,12})|BV(1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2})")
@biliav.handle()
async def handle(bot:Bot,event:Event,state:T_State):
    avcode = re.search('av(\d{1,12})|BV(1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2})', str(event.get_message()))
    if avcode==None:
        return
    rj = await get_av_data(avcode[0])
    await biliav.send(rj)
