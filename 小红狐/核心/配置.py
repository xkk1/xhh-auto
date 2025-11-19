import pathlib
import shutil
from typing import Any

from .. import __package__ as 小红狐模块名
from ..工具.日志工具 import 获取日志记录器
from ..工具.数据工具 import 数据类, 获取本地数据
from ..工具.目录工具 import 配置目录, 全局配置目录
from ..小红狐脚本 import 默认启用页面生成脚本名, 默认启用页面操作脚本名元组


日志 = 获取日志记录器(__name__)
配置目录.mkdir(parents=True, exist_ok=True)
全局配置目录.mkdir(parents=True, exist_ok=True)


def 获取配置目录(配置名: str | None = None, 脚本模块名: str | None = None):
    if 配置名 and 脚本模块名:
        return 配置目录 / 配置名 / 脚本模块名
    elif 配置名 and not 脚本模块名:
        return 配置目录 / 配置名
    elif not 配置名 and 脚本模块名:
        return  全局配置目录 / 脚本模块名
    else:
        return 配置目录

def 获取配置数据(配置名: str | None = None, 脚本模块名: str | None = None, 默认值: dict[str, Any] | None = None) -> 数据类:
    return 获取本地数据(获取配置目录(配置名=配置名, 脚本模块名=脚本模块名) / "数据.json", 默认值=默认值)

def 获取全部配置名():
    return [配置名.name for 配置名 in 获取配置目录().iterdir()]

def 新建配置(配置名: str) -> pathlib.Path:
    if 配置名 in 获取全部配置名():
        raise FileExistsError(f"配置 {配置名} 已经存在")
    新建配置目录 = 获取配置目录(配置名=配置名)
    新建配置目录.mkdir()

def 删除配置(配置名: str):
    if 配置名 not in 获取全部配置名():
        raise FileNotFoundError(f"配置 {配置名} 不存在")
    shutil.rmtree(获取配置目录(配置名=配置名))

def 修改配置名(配置名: str, 新配置名: str):
    if 新配置名 in 获取全部配置名():
        raise FileExistsError(f"配置 {新配置名} 已经存在")
    if 配置名 not in 获取全部配置名():
        raise FileNotFoundError(f"配置 {配置名} 不存在")
    shutil.move(获取配置目录(配置名=配置名), 获取配置目录(配置名=新配置名))

def 复制配置(配置名: str, 新配置名: str):
    if 新配置名 in 获取全部配置名():
        raise FileExistsError(f"配置 {新配置名} 已经存在")
    if 配置名 not in 获取全部配置名():
        raise FileNotFoundError(f"配置 {配置名} 不存在")
    shutil.copytree(获取配置目录(配置名), 获取配置目录(新配置名))

def 获取页面生成脚本(配置名: str = "默认") -> dict[str, str]:
    配置数据: 数据类 = 获取配置数据(
        配置名=配置名, 脚本模块名=小红狐模块名,
        默认值={"页面生成脚本": {"脚本模块名": 小红狐模块名, "页面生成脚本名": 默认启用页面生成脚本名}}
    )
    页面生成脚本: dict[str, str] = 配置数据["页面生成脚本"]
    try:
        from ..核心.脚本 import 小红狐脚本信息, 获取脚本
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
        assert not 脚本模块["页面生成"][页面生成脚本["页面生成脚本名"]]["入口函数"], "页面生成脚本入口函数不能为空"
    except:
        # 改为默认页面生成脚本
        修改页面生成脚本(配置名=配置名, 脚本模块名=小红狐模块名, 页面生成脚本名=默认启用页面生成脚本名)
        日志.警告(f"配置“{配置名}”改为使用默认页面生成脚本")
        配置数据["页面生成脚本"] = {"脚本模块名": 小红狐模块名, "页面生成脚本名": 默认启用页面生成脚本名}
        配置数据.保存()
        页面生成脚本 = 配置数据["页面生成脚本"]
    return 页面生成脚本

def 修改页面生成脚本(配置名: str = "默认", 脚本模块名: str | None = None, 页面生成脚本名: str | None = None) -> None:
    if 脚本模块名 is None or 页面生成脚本名 is None:
        raise ValueError("脚本模块名或脚本名不能为空")
    配置数据: 数据类 = 获取配置数据(配置名=配置名, 脚本模块名=小红狐模块名)
    配置数据["页面生成脚本"] = {"脚本模块名": 小红狐模块名, "页面生成脚本名": 页面生成脚本名}
    配置数据.保存()

def 获取页面操作自动开启脚本(配置名: str = "默认") -> dict[str, list[str]]:
    配置数据: 数据类 = 获取配置数据(
        配置名=配置名, 脚本模块名=小红狐模块名,
        默认值={"页面操作自动开启脚本": {小红狐模块名: list(默认启用页面操作脚本名元组)}}
    )
    return 配置数据["页面操作自动开启脚本"]

def 添加页面操作自动开启脚本(配置名: str = "默认", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None) -> None:
    if 脚本模块名 is None or 页面操作脚本名 is None:
        raise ValueError("脚本模块名或脚本名不能为空")
    配置数据: 数据类 = 获取配置数据(
        配置名=配置名, 脚本模块名=小红狐模块名,
        默认值={"页面操作自动开启脚本": {小红狐模块名: list(默认启用页面操作脚本名元组)}}
    )
    if 脚本模块名 not in 配置数据["页面操作自动开启脚本"]:
        配置数据["页面操作自动开启脚本"][脚本模块名] = []
    if 页面操作脚本名 not in 配置数据["页面操作自动开启脚本"][脚本模块名]:
        配置数据["页面操作自动开启脚本"][脚本模块名].append(页面操作脚本名)
    配置数据.保存()

def 删除页面操作自动开启脚本(配置名: str = "默认", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None) -> None:
    if 脚本模块名 is None or 页面操作脚本名 is None:
        raise ValueError("脚本模块名或脚本名不能为空")
    配置数据: 数据类 = 获取配置数据(
        配置名=配置名, 脚本模块名=小红狐模块名,
        默认值={"页面操作自动开启脚本": {小红狐模块名: list(默认启用页面操作脚本名元组)}}
    )
    if 脚本模块名 not in 配置数据["页面操作自动开启脚本"]:
        return
    if 页面操作脚本名 not in 配置数据["页面操作自动开启脚本"][脚本模块名]:
        return
    配置数据["页面操作自动开启脚本"][脚本模块名].remove(页面操作脚本名)
    if 配置数据["页面操作自动开启脚本"][脚本模块名] == []:
        del 配置数据["页面操作自动开启脚本"][脚本模块名]
    配置数据.保存()
