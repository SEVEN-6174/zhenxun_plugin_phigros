from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
    Bot,
    MessageEvent
)
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.params import CommandArg
from random import randint
from typing import Dict, NoReturn, Tuple, List, Type
from base64 import b64decode
import os

from .database import (
    get_songdata,
    get_names,
)
from .user_data import (
    changdata,
    getb19,
    getrks,
    get_acc
)
from .config import (
    bg_path,
    data_path,
    temp_path
)
from .image import (
    get_b19image,
    getinfo
)

getsong: Type[Matcher] = on_command('查歌曲', priority=5, block=True)
getname: Type[Matcher] = on_command('查看所有歌曲', priority=5, block=True)
randsong: Type[Matcher] = on_command('随首歌', priority=5, block=True)
change: Type[Matcher] = on_command('修改数据', priority=5, block=True)
update: Type[Matcher] = on_command('更新数据', priority=5, block=True)
best19: Type[Matcher] = on_command('/b19', priority=5, block=True)
clear: Type[Matcher] = on_command('清理phi缓存', priority=5, block=True)
info: Type[Matcher] = on_command('phi-info', priority=5, block=True)

user_data: Dict[int, list[str, str, str, str]] = {}


@getsong.handle()
async def _(arg: Message = CommandArg()) -> NoReturn:
    if not arg:
        await getsong.finish('未输入参数')
    arg: str = arg.extract_plain_text().lower()
    name: str = arg[:-3]
    lv: str = arg[-2:]
    data: Dict[str, str] = get_songdata(song_name=name, lv=lv)
    if data == None:
        end: str = '找不到对象'
    else:
        end: str = f'''
歌名:{data['song']}
难度:{data['lv']}
物量:{data['notes']}
定数:{data['ds']}
        '''.strip()
        try:
            await getsong.send(MessageSegment.image(file=bg_path/(data['song'].replace(' ', '')+'.png')))
        except ActionFailed:
            await getsong.send('找不到图片，请联系管理员补充')
    await getsong.finish(end)


@getname.handle()
async def _() -> NoReturn:
    names: List[str] = get_names()
    await getname.finish('所有的歌曲名:\n'+'\n'.join(names) + '\n总曲目数目:' + str(len(names)))


@randsong.handle()
async def _() -> NoReturn:
    names: List[str] = get_names()
    name: str = names[randint(0, len(names)-1)]
    await randsong.finish(f'建议打:{name}')


@change.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()) -> NoReturn:
    global user_data
    qq: int = event.user_id
    if not arg:
        await change.finish('未输入参数')
    arg: List[str] = arg.extract_plain_text().split(' ')
    if arg[0] != '提交':
        if len(arg) != 2:
            await change.finish('输入有误')
        if user_data.get(qq, None) == None:
            user_data[qq] = ['', '', '', '']
        if arg[0] == '1' or arg[0] == '2' or arg[0] == '3' or arg[0] == '4':
            user_data[qq][int(arg[0])-1] = arg[1]
            print(arg[1])
        await change.finish('数据提交成功')
    else:
        if arg[0] == '提交':
            try:
                text: str = ''.join(user_data[qq])
                print(text)
                de: str = b64decode(text).decode('utf-8')
                with open(data_path/f'{qq}.csv', 'w', encoding='utf-8') as f:
                    f.write(de)
                del user_data[qq]
                re: str = '数据修改完成'
            except Exception as e:
                re: str = f'出错了\n{type(e)}:{e}'
            await change.finish(re)
        else:
            await change.finish('输入有误')


@update.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()) -> NoReturn:
    qq: int = event.user_id
    if not arg:
        await update.finish('未输入参数')
    arg: list[str] = arg.extract_plain_text().lower().split(' ')
    if len(arg) < 3:
        await update.finish('输入有误')
    if arg[-1] == '强制':
        t: bool = False
        arg = arg[:-1]
    else:
        t: bool = True
    song: str = ' '.join(arg[:-2])
    lv: str = arg[-2]
    acc: str = arg[-1]
    old: str = get_acc(qq, song, lv)
    if old == None:
        await update.finish('出错了,可能是没有数据或歌名错误或等级错误')
    if old >= acc and t:
        await update.finish('拒绝操作,旧数据大于等于新数据')
    if acc < 0 or acc > 100:
        await update.finish('acc在0到100之间')
    if not changdata(qq, song, lv, acc):
        await update.finish('出错了,可能是没有数据或歌名错误或等级错误')
    else:
        await update.finish('更新成功')


@best19.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()) -> NoReturn:
    qq: int = event.user_id
    if not arg:
        data: Tuple[Dict[str, float], Dict[str, float]] = getb19(qq)
        phi1: Dict[str, float] = data[0]
        b19: Dict[str, float] = data[1]
        names: list[str] = [i for i in phi1.keys()] + [i for i in b19.keys()]
        if len(names) < 20:
            await best19.finish('先打满至少20首歌吧')
        rt: str = get_b19image(qq, event.sender.nickname)
        if rt == 'OK':
            await best19.finish(MessageSegment.at(qq)+MessageSegment.image(temp_path/f'{qq}_b19.png'))
        else:
            await best19.finish(rt)
    else:
        if not (arg.extract_plain_text() == 'text'):
            await best19.finish('参数错误')
        else:
            data: Tuple[Dict[str, float], Dict[str, float]] = getb19(qq)
            if data == None:
                await best19.finish('找不到数据')
            phi1: Dict[str, float] = data[0]
            b19: Dict[str, float] = data[1]
            names: list[str] = [i for i in phi1.keys()] + \
                [i for i in b19.keys()]
            rks: float = getrks(qq)
            try:
                text: str = f'''
rks:{rks:.3f}
#0 {names[0]}
    rks:{phi1[names[0]]:.3f}
#1 {names[1]}
    rks:{b19[names[1]]:.3f}
#2 {names[2]}
    rks:{b19[names[2]]:.3f}
#3 {names[3]}
    rks:{b19[names[3]]:.3f}
#4 {names[4]}
    rks:{b19[names[4]]:.3f}
#5 {names[5]}
    rks:{b19[names[5]]:.3f}
#6 {names[6]}
    rks:{b19[names[6]]:.3f}
#7 {names[7]}
    rks:{b19[names[7]]:.3f}
#8 {names[8]}
    rks:{b19[names[8]]:.3f}
#9 {names[9]}
    rks:{b19[names[9]]:.3f}
#10 {names[10]}
    rks:{b19[names[10]]:.3f}
#11 {names[11]}
    rks:{b19[names[11]]:.3f}
#12 {names[12]}
    rks:{b19[names[12]]:.3f}
#13 {names[13]}
    rks:{b19[names[13]]:.3f}
#14 {names[14]}
    rks:{b19[names[14]]:.3f}
#15 {names[15]}
    rks:{b19[names[15]]:.3f}
#16 {names[16]}
    rks:{b19[names[16]]:.3f}
#17 {names[17]}
    rks:{b19[names[17]]:.3f}
#18 {names[18]}
    rks:{b19[names[18]]:.3f}
#19 {names[19]}
    rks:{b19[names[19]]:.3f}
'''.strip()
            except IndexError:
                await best19.finish('先打满至少20首歌吧')
            await best19.finish(MessageSegment.at(qq)+'\n'+text)


@clear.handle()
async def _() -> None:
    os.system(f'del /f /s /q {temp_path}\\*.*')
    await clear.finish('清理完毕')


@info.handle()
async def _(event: MessageEvent) -> None:
    qq: int = event.user_id
    name: str = event.sender.nickname
    rt: str = getinfo(qq, name)
    if rt == 'OK':
        await info.finish(MessageSegment.at(qq)+MessageSegment.image(temp_path/f'{qq}_info.png'))
    else:
        await info.finish(rt)