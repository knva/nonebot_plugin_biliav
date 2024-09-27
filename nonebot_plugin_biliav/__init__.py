# import nonebot
import asyncio

from nonebot import get_driver, on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import T_State
from nonebot.plugin import PluginMetadata

global_config = get_driver().config
config = global_config.dict()
b_sleep_time = config.get('b_sleep_time', 2)
b_sleep_time = int(b_sleep_time)

from .data_source import get_av_data
import re

__plugin_meta__ = PluginMetadata(
    name="NoneBot biliav小程序 查看插件",
    description="NoneBot biliav小程序 查看插件",
    usage="发送av170001或者BV号即可查看。",
    type="application",
    extra={},
)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
biliav = on_regex(r"[Aa][Vv]\d{1,12}|[Bb][Vv]1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2}|[Bb]23\.[Tt][Vv]/[A-Za-z0-9]{7}")


@biliav.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    avcode_list: list[str] = re.compile(
        r"[Aa][Vv]\d{1,12}|[Bb][Vv]1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2}|[Bb]23\.[Tt][Vv]/[A-Za-z0-9]{7}").findall(
        str(event.get_message()))
    if not avcode_list:
        return
    rj_list: list[str] = await get_av_data(avcode_list)
    for rj in rj_list:
        await bot.send(event=event, message=rj)
        await asyncio.sleep(b_sleep_time)
