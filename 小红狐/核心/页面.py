import pathlib
import shutil
from typing import Any, Callable

from playwright.async_api import  Page

from .. import __package__ as 小红狐模块名
from ..工具.日志工具 import 获取日志记录器
from ..核心.脚本 import 小红狐脚本信息, 获取导入脚本信息字典, 获取脚本
from ..工具.数据工具 import 关闭路径下的所有本地数据, 数据类, 获取本地数据
from ..工具.目录工具 import 页面目录
from .配置 import 获取全部配置名, 新建配置
from .配置 import 获取页面操作自动开启脚本 as 配置_获取页面操作自动开启脚本
from .配置 import 添加页面操作自动开启脚本 as 配置_添加页面操作自动开启脚本
from .配置 import 删除页面操作自动开启脚本 as 配置_删除页面操作自动开启脚本
from .配置 import 获取页面生成脚本 as 配置_获取页面生成脚本
from .配置 import 修改页面生成脚本 as 配置_修改页面生成脚本
from ..小红狐脚本 import 默认启用页面操作脚本名元组


日志 = 获取日志记录器(__name__)
页面目录.mkdir(parents=True, exist_ok=True)

def 获取页面目录(页面名: str | None = None, 脚本模块名: str | None = None) -> pathlib.Path:
    if 页面名 and 脚本模块名:
        return 页面目录 / 页面名 / 脚本模块名
    elif 页面名 and not 脚本模块名:
        return 页面目录 / 页面名
    elif not 页面名 and 脚本模块名:
        raise ValueError("页面名不能为空")
    else:
        return 页面目录

def 获取页面数据(页面名: str | None = None, 脚本模块名: str = 小红狐模块名, 默认值: dict[str, Any] | None = None) -> 数据类:
    return 获取本地数据(获取页面目录(页面名=页面名, 脚本模块名=脚本模块名) / "数据.json", 默认值=默认值)

def 关闭页面数据(页面名: str | None = None, 脚本模块名: str = 小红狐模块名) -> None:
    return 关闭路径下的所有本地数据(获取页面目录(页面名=页面名, 脚本模块名=脚本模块名))

def 获取全部页面名():
    return [页面名.name for 页面名 in 获取页面目录().iterdir()]

def 新增页面(页面名: str) -> pathlib.Path:
    if 页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {页面名} 已经存在")
    新建页面目录 = 获取页面目录(页面名=页面名)
    新建页面目录.mkdir()

def 删除页面(页面名: str) -> None:
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    关闭页面数据(页面名=页面名)
    shutil.rmtree(获取页面目录(页面名=页面名))

def 修改页面名(页面名: str, 新页面名: str) -> None:
    if 新页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {新页面名} 已经存在")
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    关闭页面数据(页面名=页面名)
    shutil.move(获取页面目录(页面名=页面名), 获取页面目录(页面名=新页面名))

def 复制页面(页面名: str, 新页面名: str) -> None:
    if 新页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {新页面名} 已经存在")
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    shutil.copytree(获取页面目录(页面名=页面名), 获取页面目录(页面名=新页面名))

def 获取页面配置名(页面名: str = "默认页面六个字") -> str:
    配置名: str = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名, 默认值={"配置名": 页面名})["配置名"]
    if 配置名 not in 获取全部配置名():
        新建配置(配置名)
    return 配置名

def 修改页面配置名(页面名: str = "默认页面六个字", 配置名: str = "默认") -> None:
    页面数据 = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名)
    页面数据["配置名"] = 配置名
    页面数据.保存()

def 获取标签页URL排序(页面名: str = "默认页面六个字") -> list[str]:
    页面数据 = 获取页面数据(
        页面名=页面名, 脚本模块名=小红狐模块名,
        默认值={"标签页URL排序": list(获取脚本(模块名=小红狐模块名).获取页面操作配置页面(页面操作脚本名=默认启用页面操作脚本名元组[0], 页面名=页面名).keys())}
    )
    return 页面数据["标签页URL排序"]

def 修改标签页URL排序(页面名: str = "默认页面六个字", 标签页URL排序: list[str] = []):
    页面数据 = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名)
    页面数据["标签页URL排序"] = 标签页URL排序
    页面数据.保存()

def 获取页面生成脚本(页面名: str = "默认页面六个字") -> dict[str, str]:
    配置名: str = 获取页面配置名(页面名)
    return 配置_获取页面生成脚本(配置名=配置名)

def 修改页面生成脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面生成脚本名: str | None = None) -> None:
    配置名: str = 获取页面配置名(页面名)
    配置_修改页面生成脚本(配置名=配置名, 脚本模块名=脚本模块名, 页面生成脚本名=页面生成脚本名)

def 获取页面操作自动开启脚本(页面名: str = "默认页面六个字") -> dict[str, list[str]]:
    配置名: str = 获取页面配置名(页面名)
    return 配置_获取页面操作自动开启脚本(配置名=配置名)

def 添加页面操作自动开启脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None):
    配置名: str = 获取页面配置名(页面名)
    配置_添加页面操作自动开启脚本(配置名=配置名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)

def 删除页面操作自动开启脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None):
    配置名: str = 获取页面配置名(页面名)
    配置_删除页面操作自动开启脚本(配置名=配置名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)

def 获取页面操作开启脚本(页面名: str = "默认页面六个字") -> dict[str, list[str]]:
    页面操作开启脚本: dict[str, list[str]] = {}
    导入脚本信息字典: dict[str, 小红狐脚本信息] = 获取导入脚本信息字典()
    for 脚本模块名, 脚本信息 in 导入脚本信息字典.items():
        页面操作: dict[str, dict[str, Any]] = 脚本信息["页面操作"]
        if not isinstance(页面操作, dict):
            continue
        for 页面操作脚本名, 页面操作信息 in 页面操作.items():
            脚本状态函数: Callable[[str], bool] = 页面操作信息.get("脚本状态", None)
            if not isinstance(脚本状态函数, Callable):
                continue
            try:
                脚本状态: bool = 脚本状态函数(页面名=页面名)
                if 脚本状态:
                    页面操作开启脚本[脚本模块名] = 页面操作开启脚本.get(脚本模块名, []) + [页面操作脚本名]
            except Exception as e:
                日志.警告(f"获取页面操作开启脚本“{脚本模块名}”“{页面操作脚本名}”页面“{页面名}”失败: {e}")
    return 页面操作开启脚本

def 开启页面操作脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None) -> None:
    if 脚本模块名 is None or 页面操作脚本名 is None:
        raise ValueError("脚本模块名或脚本名不能为空")
    脚本模块: 小红狐脚本信息 = 获取脚本(模块名=脚本模块名)
    return 脚本模块["页面操作"][页面操作脚本名]["入口函数"](页面名=页面名)

def 开启页面操作自动开启脚本(页面名: str = "默认页面六个字"):
    页面操作自动开启脚本: dict[str, list[str]] = 获取页面操作自动开启脚本(页面名=页面名)
    导入脚本信息字典: dict[str, dict[str, Any]] = 获取导入脚本信息字典()
    开启失败记录: str = ""
    for 脚本模块名, 脚本列表 in 页面操作自动开启脚本.items():
        for 脚本名 in 脚本列表:
            if 脚本名 not in 导入脚本信息字典[脚本模块名]["页面操作"]:
                continue
            try:
                开启页面操作脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面操作脚本名=脚本名)
            except Exception as e:
                开启失败记录 += f"{脚本模块名}/{脚本名}：{e}\n"
    if 开启失败记录 != "":
        raise ValueError(开启失败记录)

def 关闭页面操作脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None) -> None:
    if 脚本模块名 is None or 页面操作脚本名 is None:
        raise ValueError("脚本模块名或脚本名不能为空")
    脚本模块: 小红狐脚本信息 = 获取脚本(模块名=脚本模块名)
    return 脚本模块["页面操作"][页面操作脚本名]["关闭函数"](页面名=页面名)

def 关闭页面操作自动开启脚本(页面名: str = "默认页面六个字"):
    页面操作自动开启脚本: dict[str, list[str]] = 获取页面操作自动开启脚本(页面名=页面名)
    导入脚本信息字典: dict[str, dict[str, Any]] = 获取导入脚本信息字典()
    关闭失败记录: str = ""
    for 脚本模块名, 脚本列表 in 页面操作自动开启脚本.items():
        for 脚本名 in 脚本列表:
            if 脚本名 not in 导入脚本信息字典[脚本模块名]["页面操作"]:
                continue
            try:
                关闭页面操作脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面操作脚本名=脚本名)
            except Exception as e:
                关闭失败记录 += f"{脚本模块名}/{脚本名}：{e}\n"
    if 关闭失败记录 != "":
        raise ValueError(关闭失败记录)

def 获取页面账号名(页面名: str = "默认页面六个字"):
    return 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名, 默认值={"账号": "默认"})["账号"]

def 修改页面账号名(页面名: str = "默认页面六个字", 账号名: str = "默认"):
    页面数据 = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名)
    页面数据["账号"] = 账号名
    页面数据.保存()

def 新建页面(页面名: str = "默认页面六个字"):
    页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
    脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
    脚本模块["页面生成"][页面生成脚本["页面生成脚本名"]]["新建页面"](页面名=页面名)

def 关闭页面(页面名: str = "默认页面六个字"):
    页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
    脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
    脚本模块["页面生成"][页面生成脚本["页面生成脚本名"]]["关闭页面"](页面名=页面名)

def 获取页面(页面名: str = "默认页面六个字") -> Page | None:
    页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
    脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
    页面: Page | None = 脚本模块["页面生成"][页面生成脚本["页面生成脚本名"]]["获取页面"](页面名=页面名)
    return 页面

def 获取页面状态(页面名: str = "默认页面六个字") -> bool | None:
    页面: Page | None = 获取页面(页面名=页面名)
    if not 页面:
        return None
    return not 页面.is_closed()

def 获取页面初始URL(页面名: str = "默认页面六个字") -> str | None:
    return 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名, 默认值={"初始URL": ""})["初始URL"]

def 修改页面初始URL(页面名: str = "默认页面六个字", 初始URL: str = ""):
    页面数据 = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名)
    页面数据["初始URL"] = 初始URL
    页面数据.保存()
