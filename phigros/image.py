import os
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
from PIL.Image import Image as Img
from PIL.ImageFont import FreeTypeFont
from typing import (
    Union,
    Dict,
    Tuple,
    List
)
from pathlib import Path

from .database import getsongrks
from .config import (
    temp_path,
    img_path,
    bg_path,
    font_path
)
from .user_data import (
    getb19,
    getrks,
    get_user_songrks,
    get_acc,
    get_userdata,
    get_info
)


def addimage(up: Union[str, Path], down: Union[str, Path], x: int, y: int, out: Union[str, Path], r: bool = False) -> None:
    '''
    在图片上覆盖另一张图片
    up:上面的图片的路径
    down:下面的图片路径
    x,y:上面图片的坐标
    out:输出图片的路径
    r:透明覆盖
    return:None
    '''
    img1: Image = Image.open(up)
    img2: Image = Image.open(down)
    if r:
        data: Tuple[Img] = img1.split()
        a: Image = data[-1]
        img2.paste(img1, (x, y), mask=a)
    else:
        img2.paste(img1, (x, y))
    img2.save(out)


def addtext(img: Union[str, Path], text: str, x: int, y: int, size: int, color: str, out: Union[str, Path]) -> None:
    '''
    在图片上覆盖文字
    img:下面的图片的路径
    text:文字
    x,y:上面图片的坐标
    size:
    color:颜色
    out:输出图片的路径
    return:None
    '''
    img1: Image = Image.open(img)
    draw: ImageDraw = ImageDraw.Draw(img1)
    ft: FreeTypeFont = ImageFont.truetype(str(font_path/'simyou.ttf'), size)
    draw.text((x, y), text, font=ft, fill=color)
    img1.save(out)


def resetsize(img: Union[str, Path], x: int, y: int, out: Union[str, Path]) -> None:
    '''
    重新设置图片的大小
    img:原图路径
    x,y:新的大小
    out:输出图片的路径
    return:None
    '''
    try:
        img1: Image = Image.open(img)
        img1 = img1.resize((x, y), Image.Resampling.LANCZOS)
    except FileNotFoundError:
        img1: Image = Image.open(img_path/'NotFound.png')
    img1.save(out)


def get_b19image(qq: int, name: str) -> str:
    '''
    获取b19图片
    qq:qq号
    name:用户名
    return:结果,正常为OK
    '''
    data: Tuple[Dict[str, float], Dict[str, float]] = getb19(qq)
    if data == None:
        return '找不到数据'
    phi1: Dict[str, float] = data[0]
    b19: Dict[str, float] = data[1]
    names: list[str] = [i for i in phi1.keys()] + [i for i in b19.keys()]
    rks: float = getrks(qq)
    addtext(img_path/'bg.png', f'{rks:.3f}', 550, 128,
            20, (99, 101, 109), temp_path/f'{qq}_bg_rks.png')  # 背景+rks
    addtext(temp_path/f'{qq}_bg_rks.png', name, 420, 60,
            40, 'white', temp_path/f'{qq}_bg_rks_song_0.png')  # 背景+名称
    j: int = 0
    l: List[Tuple[int, int]] = [(0, i) for i in range(198, 1599, 140)]
    r: List[Tuple[int, int]] = [(330, i) for i in range(220, 1621, 140)]
    for i in names:
        if j % 2 == 0:
            ls: List[Tuple[int, int]] = l
        else:
            ls: List[Tuple[int, int]] = r
        xy: Tuple[int, int] = ls[j//2]
        song: str = i[:-3]
        lv: str = i[-2:]
        lvpt: Path = img_path / (lv.upper()+'.png')
        addtext(lvpt, getsongrks(song, lv), 19, 0, 12,
                'white', temp_path/f'{qq}_{lv}_{song}_rks.png')  # 等级+定数
        rks = get_user_songrks(qq, song, lv)
        addtext(temp_path/f'{qq}_{lv}_{song}_rks.png', f'{rks:.3f}',
                1, 11, 9, 'white', temp_path/f'{qq}_{lv}_{j}.png')  # 等级+单曲rks
        addimage(temp_path/f'{qq}_{lv}_{j}.png', img_path /
                 'song.png', 225, 22, temp_path/f'{qq}_{lv}_{j}_song.png')  # 歌曲+等级
        resetsize(bg_path/f'{song}.png', 190, 100,
                  temp_path/f'{qq}_{song}_reset.png')  # 重新设置曲绘
        addimage(temp_path/f'{qq}_{song}_reset.png', temp_path / f'{qq}_{lv}_{j}_song.png',
                 15, 21, temp_path/f'{qq}_{lv}_{j}_song_pic.png')  # 歌曲+曲绘
        addtext(temp_path/f'{qq}_{lv}_{j}_song_pic.png', str(j), 29,
                4, 13, 'black', temp_path/f'{qq}_{lv}_{j}_song_pic_id.png')  # 歌曲+编号
        addtext(temp_path/f'{qq}_{lv}_{j}_song_pic_id.png', song, 82,
                4, 13, 'white', temp_path/f'{qq}_{lv}_{j}_song_pic_name.png')  # 歌曲+曲名
        addtext(temp_path/f'{qq}_{lv}_{j}_song_pic_name.png', get_acc(qq, song, lv)+'%',
                227, 80, 15, 'white', temp_path/f'{qq}_{lv}_{j}_song_finish.png')  # 歌曲+acc
        addimage(temp_path/f'{qq}_{lv}_{j}_song_finish.png', temp_path / f'{qq}_bg_rks_song_{j}.png',
                 xy[0], xy[1], temp_path/f'{qq}_bg_rks_song_{j+1}.png', r=True)  # 背景+歌曲
        j += 1
    oldname: Path = temp_path/f'{qq}_bg_rks_song_20.png'
    newname: Path = temp_path/f'{qq}_b19.png'
    os.system(f'copy {oldname} {newname}')
    return 'OK'


'''
素材图片信息

单独
pic
190*100
左15,21
id
左29,上4,size13
info
60*20
左225,上22
acc
左227,上80,size15
name
左82,上4,size13

lv
定数 左19,上0,size12
单曲rks 左1,上11,size9

总
name 左420,上60,size40
左1 左0,上198
右1 左330,上220
每个 330*140
rks 左550,上128,size20,rgb(99, 101, 109)
'''


def getinfo(qq: int, name: str) -> str:
    '''
    获取用户的信息
    qq:qq号
    name:用户名
    return:结果,正常为OK
    '''
    if get_userdata(qq) == None:
        return '找不到数据'
    addtext(img_path/'info.png', name, 264, 85, 40, 'white',
            temp_path/f'{qq}_info_username.png')  # 个人信息+名称
    rks: float = getrks(qq)
    addtext(temp_path/f'{qq}_info_username.png', f'{rks:.2f}', 201, 130,
            30, (180, 181, 182), temp_path/f'{qq}_info_rks.png')  # 个人信息+rks
    ez: Dict[str, int] = get_info(qq, 'ez')
    hd: Dict[str, int] = get_info(qq, 'hd')
    in_: Dict[str, int] = get_info(qq, 'in')
    at: Dict[str, int] = get_info(qq, 'at')
    all_: Dict[str, int] = get_info(qq, 'all')
    ez_text: str = f"clear:{ez['clear']}/{ez['ALL']} ap:{ez['AP']}/{ez['ALL']}"
    hd_text: str = f"clear:{hd['clear']}/{hd['ALL']} ap:{hd['AP']}/{hd['ALL']}"
    in_text: str = f"clear:{in_['clear']}/{in_['ALL']} ap:{in_['AP']}/{in_['ALL']}"
    at_text: str = f"clear:{at['clear']}/{at['ALL']} ap:{at['AP']}/{at['ALL']}"
    all_text: str = f"clear:{all_['clear']}/{all_['ALL']} ap:{all_['AP']}/{all_['ALL']}"
    addtext(temp_path/f'{qq}_info_rks.png', ez_text, 615,
            88, 30, 'white', temp_path/f'{qq}_info_ez.png')
    addtext(temp_path/f'{qq}_info_ez.png', hd_text, 615,
            195, 30, 'white', temp_path/f'{qq}_info_hd.png')
    addtext(temp_path/f'{qq}_info_hd.png', in_text, 615,
            290, 30, 'white', temp_path/f'{qq}_info_in.png')
    addtext(temp_path/f'{qq}_info_in.png', at_text, 615,
            395, 30, 'white', temp_path/f'{qq}_info_at.png')
    addtext(temp_path/f'{qq}_info_at.png', all_text, 130,
            395, 30, 'white', temp_path/f'{qq}_info.png')
    return 'OK'


'''
素材图片信息

用户名 左264,上85,size40
rks 左201,上135

左615,size30
EZ 上88
HD 上195
IN 上290
AT 上395

All 左130,上395,size30
'''
