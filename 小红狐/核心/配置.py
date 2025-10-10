import pathlib
import shutil
from typing import Any, Dict, Optional

from 小红狐.工具.数据工具 import 数据类, 获取本地数据
from ..工具.目录工具 import 配置目录, 全局配置目录


配置目录.mkdir(parents=True, exist_ok=True)
全局配置目录.mkdir(parents=True, exist_ok=True)


def 获取配置目录(配置名: Optional[str]=None):
    if 配置名:
        return 配置目录 / 配置名
    else:
        return 配置目录

def 获取脚本配置目录(配置名: str, 脚本模块名: Optional[str]=None):
    if 脚本模块名:
        return 配置目录 / 配置名 / 脚本模块名
    else:
        return 配置目录 / 配置名

def 获取全局配置目录(脚本模块名: Optional[str]=None):
    if 脚本模块名:
        return 全局配置目录 / 脚本模块名
    else:
        return 全局配置目录

def 获取全部配置名():
    return [配置名.name for 配置名 in 获取配置目录().iterdir()]

def 新建配置(配置名: str) -> pathlib.Path:
    if 配置名 in 获取全部配置名():
        raise FileExistsError(f"配置 {配置名} 已经存在")
    新建配置目录 = 获取配置目录(配置名)
    新建配置目录.mkdir()

def 删除配置(配置名: str):
    if 配置名 not in 获取全部配置名():
        raise FileNotFoundError(f"配置 {配置名} 不存在")
    shutil.rmtree(获取配置目录(配置名))

def 修改配置名(配置名: str, 新配置名: str):
    if 新配置名 in 获取全部配置名():
        raise FileExistsError(f"配置 {新配置名} 已经存在")
    if 配置名 not in 获取全部配置名():
        raise FileNotFoundError(f"配置 {配置名} 不存在")
    shutil.move(获取配置目录(配置名), 获取配置目录(新配置名))

def 复制配置(配置名: str, 新配置名: str):
    if 新配置名 in 获取全部配置名():
        raise FileExistsError(f"配置 {新配置名} 已经存在")
    if 配置名 not in 获取全部配置名():
        raise FileNotFoundError(f"配置 {配置名} 不存在")
    shutil.copytree(获取配置目录(配置名), 获取配置目录(新配置名))

def 获取配置数据(配置名: Optional[str]=None, 默认值: Optional[Dict[str, Any]] = None) -> 数据类:
    return 获取本地数据(获取配置目录(配置名) / "数据.json", 默认值=默认值)
