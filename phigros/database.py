from typing import Union, Dict, List

from .config import res_path

data: Dict[str, dict[str:list[str]]] = {}
# {曲名:{难度:[定数,物量]}}


def data_init() -> None:
    '''
    初始化数据
    '''
    global data
    with open(res_path / 'data.csv', 'r', encoding='utf-8') as f:
        data_: str = f.read().lower()
    each: List[str] = data_.split('\n')
    for i in each:
        lis: List[str] = i.split(',')
        if lis == ['']:
            pass
        else:
            if data.get(lis[0], None) == None:
                data[lis[0]] = {}
            data[lis[0]][lis[1]] = lis[2:]


def get_songdata(song_name: str, lv: str) -> Union[Dict[str, str], None]:
    '''
    获取歌曲数据
    song_name:曲名
    lv:难度(EZ,HD,IN,AT,SP)
    retrun:{song(曲名),lv(难度),ds(定数),notes(物量)}
           None(找不到)
    '''
    try:
        data_: Dict[str, str] = {'song': song_name, 'lv': lv,
                                 'ds': data[song_name][lv][0], 'notes': data[song_name][lv][1]}
    except KeyError:
        data_ = None
    return data_


def get_names() -> List[str]:
    '''
    获取所有歌名
    retrun [歌名,歌名]
    '''
    return [i for i in data.keys()]


def get_data() -> Dict[str, dict[str:list[str]]]:
    '''
    获取整个数据库
    retrun:{曲名:{难度:[定数,物量]}}

    '''
    return data


def getsongrks(song, lv) -> Union[str, None]:
    '''
    获取歌曲rks
    song:歌名
    lv:难度
    retrun:rks
           None(找不到歌曲)
    '''
    if data.get(song, None) == None:
        return None
    elif data[song].get(lv) == None:
        return None
    return data[song][lv][0]


if __name__ == '__main__':
    data_init()
