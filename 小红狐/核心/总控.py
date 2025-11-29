from .. import __package__ as 小红狐模块名
from .脚本 import 小红狐脚本信息, 获取导入脚本信息, 获取脚本
from .小红狐配置 import 配置数据

def 获取标签页URL排序() -> list[str]:
    配置数据.添加默认值({"标签页URL排序": list(获取脚本(模块名=小红狐模块名)["总控页面"].keys())})
    return 配置数据["标签页URL排序"]

def 修改标签页URL排序(标签页URL排序: list[str] = []):
    配置数据["标签页URL排序"] = 标签页URL排序
    配置数据.保存()

def 获取配置页面() -> dict[str, str]:
    导入脚本信息: dict[str, 小红狐脚本信息] = 获取导入脚本信息()
    配置页面: dict[str, str] = {}
    for 脚本模块名, 脚本信息 in 导入脚本信息.items():
        配置页面.update(脚本信息.获取总控页面配置页面())
    return 配置页面

def 获取标签页列表() -> list[dict[str, str]]:
    配置页面: dict[str, str] = 获取配置页面()
    标签页URL排序: list[str] = 获取标签页URL排序()
    标签页列表: list[dict[str, str]] = []
    for 标签页URL in 标签页URL排序:
        if 标签页URL in 配置页面:
            标签页列表.append({
                "url": 标签页URL,
                "标题": 配置页面[标签页URL],
            })
            配置页面.pop(标签页URL)
    for 标签页URL, 标签页标题 in 配置页面.items():
        标签页列表.append({
            "url": 标签页URL,
            "标题": 标签页标题,
        })
    return 标签页列表
