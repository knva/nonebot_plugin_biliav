from time import strftime, localtime

import httpx
import json
import re
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment

url: str = "https://api.bilibili.com/x/web-interface/view/detail"

global_config = nonebot.get_driver().config
config = global_config.dict()
b_comments = config.get('b_comments', False)
b_b23tv = config.get('b_b23tv', True)

if type(b_comments) != bool and b_comments == "True":
    b_comments = True
else:
    b_comments = False

if type(b_b23tv) != bool and b_b23tv == "False":
    b_b23tv = False
else:
    b_b23tv = True

import math


async def b23tv2bv(b23tv: str) -> str:
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = await client.get(b23tv, headers=headers)
    return re.findall("[Bb][Vv]1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2}", str(r.next_request.url))[0]


async def bv2av(Bv: str) -> int:
    # 1.去除Bv号前的"Bv"字符
    BvNo1: str = Bv[2:]
    keys: dict[str:str] = {
        '1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
        'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38', 'K': '51',
        'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50', 'U': '10', 'V': '44',
        'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
        'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41',
        'k': '16', 'm': '11', 'n': '37', 'o': '2',
        'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14',
        'z': '19'

    }
    # 2. 将key对应的value存入一个列表
    BvNo2: list[int] = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))

    # 3. 对列表中不同位置的数进行*58的x次方的操作

    BvNo2[0]: int = int(BvNo2[0] * math.pow(58, 6))
    BvNo2[1]: int = int(BvNo2[1] * math.pow(58, 2))
    BvNo2[2]: int = int(BvNo2[2] * math.pow(58, 4))
    BvNo2[3]: int = int(BvNo2[3] * math.pow(58, 8))
    BvNo2[4]: int = int(BvNo2[4] * math.pow(58, 5))
    BvNo2[5]: int = int(BvNo2[5] * math.pow(58, 9))
    BvNo2[6]: int = int(BvNo2[6] * math.pow(58, 3))
    BvNo2[7]: int = int(BvNo2[7] * math.pow(58, 7))
    BvNo2[8]: int = int(BvNo2[8] * math.pow(58, 1))
    BvNo2[9]: int = int(BvNo2[9] * math.pow(58, 0))

    # 4.求出这10个数的合
    sum: int = 0
    for i in BvNo2:
        sum += i
    # 5. 将和减去100618342136696320
    sum -= 100618342136696320
    # 6. 将sum 与177451812进行异或
    temp: int = 177451812

    return sum ^ temp


async def get_top_comments(av: str) -> str:
    av: str = str(av)
    if av[0:2] == "BV":
        avcode = bv2av(av)
    else:
        avcode = av.replace("av", "")
    async with httpx.AsyncClient() as client:
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        r = await client.get(url=f'https://api.bilibili.com/x/v2/reply/main?next=0&type=1&oid={avcode}',
                             headers=headers)
    rd: dict[str:str, int, dict] = json.loads(r.text)
    if rd['code'] == "0":
        if not rd["data"]:
            return None
    hot_comments: dict[str:str, int, dict] = rd['data']['replies'][:3]
    msg: str = "\n-----------------\n--前三热评如下--\n-----------------\n"
    for c in hot_comments:
        name = c['member']['uname']
        txt = c['content']['message']
        msg += f'{name}: {txt}\n\n'
    return msg


async def get_av_data(av_list: list[str]) -> list[str]:
    msg_list: list[str] = []
    for avcode in av_list:
        msg: str = ""
        if avcode[0:2].upper() == "BV":
            avcode = bv2av(avcode)
        elif avcode[0:2].lower() == "av":
            avcode = avcode.replace("av", "")
        elif avcode[0:7].lower() == "b23.tv/":
            if b_b23tv:
                msg += avcode + ", "
                avcode = await b23tv2bv(avcode)
                avcode = await bv2av(avcode)
            else:
                continue
        else:
            continue
        new_url: str = url + f"?aid={avcode}"
        async with httpx.AsyncClient() as client:
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            r = await client.get(new_url, headers=headers)
        try:
            video_info: dict = json.loads(r.text)
            if video_info["code"] == 0:
                if not video_info["data"]:
                    continue
            else:
                continue

            # 视频所有信息
            view: dict = video_info["data"]["View"]

            # 分p数
            videos: int = view["videos"]

            # 分区id
            # tid: str = view["tid"]

            # 子分区名称
            tname: str = view["tname"]

            # 版权, 1为原创, 2为转载, 无法辨别当为原创时是否允许转载
            the_copyright: int | str = view["copyright"]
            if the_copyright == 1:
                the_copyright = "原创"
            elif the_copyright == 2:
                the_copyright = "转载"
            else:
                the_copyright = ""

            # 封面url
            pic_url: str = view["pic"]

            # 标题
            title: str = view["title"]

            # 发布时间
            # 详情参考: https://github.com/SocialSisterYi/bilibili-API-collect/issues/306
            # 其实data里还有一个ctime键, 为创建时间, 秒级时间戳, pubdate为发布时间
            # 但是实际上两者是反过来的, 也就是真正的发布时间应为ctime键的值(ctime >= pubdate)
            # 但是据上述issue所说, 老视频的ctime可能会被重置为2017年的某个时间
            # 所以个人感觉最好是使用pubdate, 秒级时间戳
            pubdate: int = view["pubdate"]
            # ctime: int = view["ctime"]

            pubdate: str = strftime("%Y-%m-%d %H:%M:%S", localtime(pubdate))

            # 视频描述v1版本
            desc_v1: str = view["desc"]
            # 视频描述v2版本, 主要区别是返回了被at的人的mid
            # desc_v2:dict = view["desc_v2"]

            # 视频总时长, 所有分p, 单位为秒
            duration: int = view["duration"]

            # 先组合duration相关string
            duration_m: int
            duration_s: int
            duration_m, duration_s = divmod(int(duration), 60)
            duration_h: int
            duration_h, duration_m = divmod(duration_m, 60)
            duration_str: str = f"{duration_h:02d}:{duration_m:02d}:{duration_s:02d}"

            # up主信息与合作成员列表, 非合作视频不存在此项, 需先判断
            # 合作成员列表中存在up主信息

            # 先组合author信息相关string
            author_message: str = ""

            if "staff" in view:
                # 合作成员列表
                staff_list: list = view["staff"]

                staff: dict
                for staff in staff_list:
                    # 成员名称
                    cache_title: str = staff["title"]

                    # 成员昵称
                    cache_name: str = staff["name"]

                    # 成员头像url
                    # cache_face_url: str = staff["face"]

                    # 成员粉丝数
                    cache_follower: int = staff["follower"]

                    author_message += f"{cache_title}: {cache_name}-{cache_follower}粉丝 " + " "
                    # author_message += f"{cache_title}: {cache_name}-{cache_follower}粉丝 " + MessageSegment.image(
                    #     cache_face_url) + " "

            else:
                # up主信息
                card: dict = video_info["data"]["Card"]

                # up主昵称
                card_name: str = card["card"]["name"]

                # up主粉丝数
                card_follower: int = card["follower"]

                # up主头像url
                # card_face_url: str = card["card"]["face"]

                author_message += f"昵称: {card_name}-粉丝数: {card_follower}"
                # author_message += f"昵称: {card_name}-粉丝数: {card_follower}" + MessageSegment.image(card_face_url)

            # 视频曾获荣誉, 如果没有则不存在该键
            # 先组合honor相关string
            honor_message: str = ""
            if "honor" in view["honor_reply"]:
                honor_message += "视频曾获荣誉: "

                honor_list: list = view["honor_reply"]["honor"]
                honor: dict
                for honor in honor_list:
                    # 荣誉描述
                    cache_tag_name: str = honor["desc"]
                    honor_message += f"{cache_tag_name} "

                honor_message += " "

            # 视频状态信息
            view_stat: dict = view["stat"]

            # 播放数
            stat_view: int = view_stat["view"]

            # 弹幕数
            stat_danmaku: int = view_stat["danmaku"]

            # 评论数
            stat_reply: int = view_stat["reply"]

            # 收藏数
            stat_fav: int = view_stat["favorite"]

            # 投币数
            stat_coin: int = view_stat["coin"]

            # 分享数
            stat_share: int = view_stat["share"]

            # 获赞数
            stat_like: int = view_stat["like"]

            # tags
            tag_list: list = video_info["data"]["Tags"]

            # 先组合tags相关string
            tag_message: str = ""

            tag: dict
            for tag in tag_list:
                # tag名称
                cache_tag_name = tag["tag_name"]
                tag_message += f"{cache_tag_name} "

            link: str = f"https://www.bilibili.com/video/{avcode}"

            msg += \
                f"av{avcode}" + ": " + "标题: " + title + "\n" + MessageSegment.image(pic_url) \
                + "\n" + f"发布时间: {pubdate} 分p数: {videos} 分区: {tname} 视频总时长: {duration_str} " \
                + f"版权信息: {the_copyright}" \
                + "\n" + f"播放: {stat_view} 弹幕: {stat_danmaku} 评论: {stat_reply} 收藏: {stat_fav} " \
                + f"硬币: {stat_coin} 分享: {stat_share} 点赞: {stat_like}\n" \
                + honor_message + "tag: " + tag_message \
                + f"\n点击链接进入: {link}\n简介: {desc_v1}\nup主信息: " + author_message

            print(msg)
            if b_comments:
                msg += await get_top_comments(avcode)

        except:
            msg += "错误!!! 没有此av或BV号。"

        msg_list.append(msg)
    return msg_list
