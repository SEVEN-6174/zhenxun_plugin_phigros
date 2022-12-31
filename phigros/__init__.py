from .database import data_init
from .main import *

__zx_plugin_name__: str = "Phigros查分器"
__plugin_usage__: str = """
usage:
    Phigros查分器
    关于：
        数据库版本:2.4.5
        作者:seven
    指令：
        查歌曲 [name] [level]
            说明:
                查询歌曲信息
            例子:
                查歌曲 996 IN
        查看所有歌曲
            说明:
                显示数据库内所有的歌曲
            例子:
                查看所有歌曲
        随首歌
            说明:
                随机抽一首歌
            例子:
                随首歌
        /b19:
            说明:
                绘制b19成绩图
            例子:
                /b19
        /b19 text
            说明:
                b19文字版
            例子:
                /b19 text
        phi-info:
            说明:
                查看个人账户信息
            例子:
                phi-info
        清理phi缓存:
            说明:
                清理缓存
            例子:
                清理phi缓存
    关于修改数据
        说明:
            第一次使用需要电脑(数据小的时候一个个传也可以)
            下载程序:(链接暂无)
            产生的四个文本
            可用使用修改数据指令发送(较长，可用发送后撤回)
            发送完毕之后务必发送'修改数据 完成'
            数据有误可以重新发送更新
            当只有几首时，可用用更新数据指令
        指令:
            修改数据 [1-4] [data]
            修改数据 提交
            更新数据 [name] [level] [acc] ?[强制]
        例子:
            修改数据 1 out1.txt的内容
            修改数据 2 out2.txt的内容
            修改数据 3 out3.txt的内容
            修改数据 4 out4.txt的内容
            修改数据 提交
            更新数据 db doll AT 100.00
            更新数据 Rrhar'il IN 98.27
            更新数据 Rrhar'il IN 50.00 强制
        注意:
            1.acc不用%
            2.修改数据会完全替换所有数据
            3.更新数据旧数据大于新数据时会拒绝，如果是自己手误可以加上强制参数
""".strip()
__plugin_des__: str = "Phigros 查分器"
__plugin_cmd__: List[str] = ['清理phi缓存', 'phi-info',
                             'phi-chap', '/b19', '更新数据', '修改数据', '随首歌', "查歌曲", "查看所有歌曲名称"]
__plugin_settings__: Dict[str, List[str]] = {
    "cmd": ['清理phi缓存', 'phi-info', 'phi-chap', '/b19', '更新数据', '修改数据', '随首歌', "查歌曲", "查看所有歌曲名称"],
}
__plugin_type__: Tuple[str, int] = ("一些工具", 1)
__plugin_version__: float = 0.1
__plugin_author__: str = "SEVEN"


def init() -> None:
    '''
    初始化项目 
    '''
    data_init()


init()
