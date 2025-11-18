import pathlib
import shutil
from typing import Any

from .. import __package__ as 小红狐模块名
from ..核心.脚本 import 获取脚本
from ..工具.数据工具 import 数据类, 获取本地数据
from ..工具.目录工具 import 页面目录
from .配置 import 获取全部配置名, 新建配置
from .配置 import 添加页面操作自动开启脚本 as 配置_添加页面操作自动开启脚本
from .配置 import 删除页面操作自动开启脚本 as 配置_删除页面操作自动开启脚本
from .配置 import 获取页面生成脚本 as 配置_获取页面生成脚本
from .配置 import 修改页面生成脚本 as 配置_修改页面生成脚本


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

def 获取全部页面名():
    return [页面名.name for 页面名 in 获取页面目录().iterdir()]

def 新建页面(页面名: str) -> pathlib.Path:
    if 页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {页面名} 已经存在")
    新建页面目录 = 获取页面目录(页面名=页面名)
    新建页面目录.mkdir()

def 删除页面(页面名: str) -> None:
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    shutil.rmtree(获取页面目录(页面名=页面名))

def 修改页面名(页面名: str, 新页面名: str) -> None:
    if 新页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {新页面名} 已经存在")
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
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
    页面数据 = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名, 默认值={"标签页URL排序": list(获取脚本(模块名=小红狐模块名).获取配置页面(页面名=页面名).keys())})
    return 页面数据["标签页URL排序"]

def 修改标签页URL排序(页面名: str = "默认页面六个字", 标签页URL排序: list[str] = []):
    页面数据 = 获取页面数据(页面名=页面名, 脚本模块名=小红狐模块名)
    页面数据["标签页URL排序"] = 标签页URL排序
    页面数据.保存()

def 获取页面生成脚本(页面名: str = "默认页面六个字") -> str:
    配置名: str = 获取页面配置名(页面名)
    return 配置_获取页面生成脚本(配置名=配置名)

def 修改页面生成脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面生成脚本名: str | None = None) -> None:
    配置名: str = 获取页面配置名(页面名)
    配置_修改页面生成脚本(配置名=配置名, 脚本模块名=脚本模块名, 页面生成脚本名=页面生成脚本名)

def 添加页面操作自动开启脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None):
    配置名: str = 获取页面配置名(页面名)
    配置_添加页面操作自动开启脚本(配置名=配置名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)

def 删除页面操作自动开启脚本(页面名: str = "默认页面六个字", 脚本模块名: str | None = None, 页面操作脚本名: str | None = None):
    配置名: str = 获取页面配置名(页面名)
    配置_删除页面操作自动开启脚本(配置名=配置名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)
