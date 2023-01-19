<!--
 * @Author         : anlen123
 * @Date           : 2021-03-01 00:00:00
 * @LastEditors    : anlen123
 * @LastEditTime   : 2021-03-01 00:00:00
 * @Description    : None
 * @GitHub         : https://github.com/anlen123/nonebot_plugin_abbrreply
-->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot_plugin_biliav


_✨ NoneBot biliav小程序 查看插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot_plugin_biliav">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_biliav.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">
</p>

## 使用方式
发送:
av170001

或者BV17x411w7KC

或者https://b23.tv/m9e5LbH (可以通过`b_b23tv`配置项开关是否解析b23.tv的链接)

或者av170001BV17x411w7KChttps://b23.tv/m9e5LbH ,会返回3条视频信息(即支持单条消息解析多条不同类型或同类型的视频号,可以通过`b_sleep_time`配置项配置返回的消息之间的延迟)

返回b站小程序对应的视频

## 配置
`b_comments`:

作用: 是否携带前三热评

可选项: [True, False]

默认值: False


`b_b23tv`:

作用: 是否解析b23.tv链接

可选项: [True, False]

默认值: True


`b_sleep_time`:

作用: 单条消息携带多个视频号时,返回的消息之间的延迟

可选项: [int]

默认值: 2

## 安装

- 通过pip:
- - 1. pip install nonebot_plugin_biliav
- - 2. 在bot.py中添加下面这行代码: `nonebot.load_plugin("nonebot_plugin_biliav")`

- 通过nb-cli:
- - 1. 将命令行的路径移动到bot.py所在目录下
- - 2. nb plugin install nonebot-plugin-biliav

- 通过源码:
- - 1. 将本项目,通过git clone或下载压缩包并解压的方式,放在bot_folder/src/plugins/下,即下载好文件后,目录应是bot_folder/src/plugins/nonebot_plugin_biliav/
- - 2. 正常运行bot即可

### 已适配nonebot beta版本 感谢@anlen123 [https://github.com/anlen123](https://github.com/anlen123)
### 功能更新 感谢  @RiotGamesU [https://github.com/RiotGamesU](https://github.com/RiotGamesU)
