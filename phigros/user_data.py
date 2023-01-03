from typing import Union, Dict, Literal, Tuple

from .database import (
    get_data,
    getsongrks
)
from .config import data_path


def get_userdata(qq: int) -> Union[Dict[str, Dict[str, str]], None]:
    '''
    通过qq号获取对应的数据所有数据
    qq:qq号
    return:{曲名:{难度:acc}}
           None(找不到)(数据错误)
    '''
    rt_dic: Dict[str, Dict[str, str]] = {}
    try:
        with open(data_path/f'{qq}.csv', 'r', encoding='utf-8') as f:
            data = f.read().lower()
        each: list[str] = data.split('\n')
        for i in each:
            lis = i.split(',')
            if lis == ['']:
                pass
            else:
                if rt_dic.get(lis[0], None) == None:
                    rt_dic[lis[0]] = {}
                rt_dic[lis[0]][lis[1]] = lis[2]
        return rt_dic
    except (FileNotFoundError, IndexError):
        return None


def changdata(qq: int, song: str, lv: str, acc: str) -> Union[Literal[True], Literal[False]]:
    '''
    修改qq号对应的数据
    qq:qq号
    song:曲名
    lv:难度
    acc:acc
    return:True(成功)
           False(错误(找不到歌曲或没有数据))
    '''
    data: Dict[str, Dict[str, str]] = get_userdata(qq)
    if data == None:
        return False
    elif data.get(song, None) == None:
        return False
    elif data[song].get(lv) == None:
        return False
    data[song][lv] = acc
    savedata(data, qq)
    return True


def savedata(data: Dict[str, Dict[str, str]], qq: int) -> None:
    '''
    保存对应qq的数据
    data:get_userdata的返回值({曲名:{难度:acc}})
    qq:qq号
    return:None
    '''
    wd = ''
    for song in data.keys():
        for lv in data[song].keys():
            acc = data[song][lv]
            wd += f'{song},{lv},{acc}\n'
    with open(data_path/f'{qq}.csv', 'w', encoding='utf-8') as f:
        f.write(wd)


def get_acc(qq: int, song: str, lv: str) -> Union[str, None]:
    '''
    获取用户某一首歌的acc
    qq:qq号
    song:歌名
    lv:难度
    return:acc
           None(找不到歌曲/找不到用户数据)
    '''
    data: Dict[str, Dict[str, str]] = get_userdata(qq)
    if data == None:
        return None
    elif data.get(song, None) == None:
        return None
    elif data[song].get(lv) == None:
        return None
    return data[song][lv]


def get_user_songrks(qq: int, song: str, lv: str) -> Union[int, None]:
    '''
    获取用户的单曲rks
    return:int(rks)
           None(找不到数据)
    '''
    acc: str = get_acc(qq, song, lv)
    songrks: str = getsongrks(song, lv)
    if acc == None or songrks == None:
        return None
    acc = float(acc)
    songrks = float(songrks)
    if acc < 70:
        return 0
    else:
        acc = acc/100
        return ((acc*100-55)/45)**2*songrks


def getb19(qq: int) -> Tuple[Dict[str, float], Dict[str, float]]:
    '''
    根据用户数据获取b19
    qq:qq号
    return:phi1,b19
    '''
    rkslist: Dict[str:int] = {}
    b19: Dict[str, float] = {}
    phi1 = 0.0
    db: Dict[str, dict[str:list[str]]] = get_data()
    for song in db.keys():
        for lv in db[song].keys():
            songrks: int = get_user_songrks(qq, song, lv)
            if songrks == None:
                pass
            else:
                rkslist[song+':'+lv] = songrks
    rkslist = {i[0]: i[1] for i in sorted(
        rkslist.items(),  key=lambda d: d[1], reverse=True)}
    j: int = 0
    for i in rkslist.keys():
        j += 1
        b19[i] = rkslist[i]
        if j >= 19:
            break
    ds_: float = 0.0
    for i in rkslist.keys():
        if get_acc(qq, i[:-3], i[-2:]) == '100':
            ds: float = float(getsongrks(i[:-3], i[-2:]))
            if ds >= ds_:
                ds_ = ds
                phi1: Dict[str, float] = {i: float(getsongrks(i[:-3], i[-2:]))}
    return phi1, b19


def getrks(qq: int) -> float:
    '''
    获取用户的rks
    qq:qq号
    return:rks
    '''
    data: Tuple[Dict[str, float], Dict[str, float]] = getb19(qq)
    phi1: Dict[str, float] = data[0]
    b19: Dict[str, float] = data[1]
    rks: float = 0.0
    for i in phi1.keys():
        rks += phi1[i]
    for i in b19.keys():
        rks += b19[i]
    rks /= 20
    return rks


def get_info(qq: int, lv: str) -> Union[Dict[str, int], None]:
    '''
    获取用户信息
    qq:qq号
    lv:等级(EZ,HD,IN,AT,ALL)
    retrun:{总共(ALL),打过(clear),AP(AP)}
           None(找不到数据)
    '''
    data: Dict[str, Dict[str, str]] = get_userdata(qq)
    if data == None:
        return None
    lv: str = lv.lower()
    all: int = 0
    clear: int = 0
    ap: int = 0
    if lv == 'all':
        for song in data.keys():
            for lvs in data[song].keys():
                all += 1
                if float(data[song][lvs]) > 0:
                    clear += 1
                if float(data[song][lvs]) == 100:
                    ap += 1
        return {'ALL': all, 'clear': clear, 'AP': ap}
    for song in data.keys():
        for lvs in data[song].keys():
            if lvs == lv:
                all += 1
                if float(data[song][lvs]) > 0:
                    clear += 1
                if float(data[song][lvs]) == 100:
                    ap += 1
    return {'ALL': all, 'clear': clear, 'AP': ap}
