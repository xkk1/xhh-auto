import pathlib
import shutil
from typing import Any


from .. import __package__ as 模块名
from ..工具.数据工具 import 关闭本地数据, 数据类, 获取本地数据
from ..工具.目录工具 import 账号目录
from ..工具.任务管理器工具 import 异步任务管理器

浏览器存储状态文件名 = "浏览器存储状态.json"
默认浏览器存储状态文件 = pathlib.Path(__file__).parent / "默认浏览器存储状态.json"
账号目录.mkdir(parents=True, exist_ok=True)


def 获取账号目录(账号名: str | None = None, 脚本模块名: str | None = None) -> pathlib.Path:
    if 账号名 and 脚本模块名:
        return 账号目录 / 账号名 / 脚本模块名
    elif 账号名 and not 脚本模块名:
        return 账号目录 / 账号名
    elif not 账号名 and 脚本模块名:
        raise ValueError("账号名不能为空")
    else:
        return 账号目录

def 获取账号数据(账号名: str | None = None, 脚本模块名: str | None = None, 默认值: dict[str, Any] | None = None) -> 数据类:
    return 获取本地数据(获取账号目录(账号名=账号名, 脚本模块名=脚本模块名) / "数据.json", 默认值=默认值)

def 关闭账号数据(账号名: str | None = None, 脚本模块名: str | None = None) -> bool:
    return 关闭本地数据(获取账号目录(账号名=账号名, 脚本模块名=脚本模块名) / "数据.json")

def 获取全部账号名():
    return [账号名.name for 账号名 in 获取账号目录().iterdir()]

def 新建账号(账号名: str):
    if 账号名 in 获取全部账号名():
        raise FileExistsError(f"账号 {账号名} 已经存在")
    新建账号目录 = 获取账号目录(账号名=账号名, 脚本模块名=模块名)
    新建账号目录.mkdir(parents=True, exist_ok=True)
    # 复制默认浏览器存储状态文件
    shutil.copy(默认浏览器存储状态文件, 新建账号目录 / 浏览器存储状态文件名)

def 删除账号(账号名: str):
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    关闭账号数据(账号名=账号名)
    shutil.rmtree(获取账号目录(账号名=账号名))

def 修改账号名(账号名: str, 新账号名: str):
    if 新账号名 in 获取全部账号名():
        raise FileExistsError(f"账号 {新账号名} 已经存在")
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    关闭账号数据(账号名=账号名)
    shutil.move(获取账号目录(账号名=账号名), 获取账号目录(账号名=新账号名))

def 复制账号(账号名: str, 新账号名: str):
    if 新账号名 in 获取全部账号名():
        raise FileExistsError(f"账号 {新账号名} 已经存在")
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    shutil.copytree(获取账号目录(账号名=账号名), 获取账号目录(账号名=新账号名))

def 获取账号浏览器存储状态文件(账号名: str) -> pathlib.Path:
    if 账号名 not in 获取全部账号名():
        新建账号(账号名=账号名)
    浏览器存储状态文件: pathlib.Path = 获取账号目录(账号名=账号名, 脚本模块名=模块名) / 浏览器存储状态文件名
    if not 浏览器存储状态文件.exists():
        shutil.copy(默认浏览器存储状态文件, 浏览器存储状态文件)
    return 浏览器存储状态文件

def 保存账号状态(账号名: str):
    from ..核心.浏览器 import 保存浏览器上下文账号
    异步任务管理器.运行(保存浏览器上下文账号(账号名=账号名))
