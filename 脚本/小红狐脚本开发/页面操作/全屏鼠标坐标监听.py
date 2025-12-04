from pathlib import Path
from 小红狐.核心.页面 import 获取页面状态, 获取页面
from 小红狐.工具.任务管理器工具 import 异步任务管理器

from .. import __package__ as 模块名


def 入口函数(页面名: str):
    页面状态 = 获取页面状态(页面名=页面名)
    if 页面状态 == None:
        raise Exception(f"页面“{页面名}”未创建")
    elif 页面状态 == False:
        raise Exception(f"页面“{页面名}”手动关闭")
    page = 获取页面(页面名=页面名)
    async def 异步函数():
        # 将本地 JS 文件作为脚本标签注入页面
        await page.add_script_tag(path=Path(__file__).parent / "全屏鼠标坐标监听.user.js")

    异步任务管理器.运行(异步函数())

def 关闭函数(页面名: str | None):
    页面状态 = 获取页面状态(页面名=页面名)
    if 页面状态 == None:
        raise Exception(f"页面“{页面名}”未创建")
    elif 页面状态 == False:
        raise Exception(f"页面“{页面名}”手动关闭")
    page = 获取页面(页面名=页面名)
    异步任务管理器.运行(page.evaluate("stopMouseDragClickListener()"))

def 脚本状态(页面名: str | None) -> bool:
    页面状态 = 获取页面状态(页面名=页面名)
    if not 页面状态:
        return False
    page = 获取页面(页面名=页面名)
    result = 异步任务管理器.运行(page.evaluate("typeof stopMouseDragClickListener !== 'undefined'"))
    return result
