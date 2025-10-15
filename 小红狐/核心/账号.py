import pathlib
import shutil
from typing import Any, Dict, Optional

from 小红狐.工具.数据工具 import 数据类, 获取本地数据
from ..工具.目录工具 import 账号目录

浏览器存储状态文件名 = "浏览器存储状态.json"
默认浏览器存储状态文件 = pathlib.Path(__file__).parent / "默认浏览器存储状态.json"
账号目录.mkdir(parents=True, exist_ok=True)


def 获取账号目录(账号名: Optional[str]=None):
    if 账号名:
        return 账号目录 / 账号名
    else:
        return 账号目录

def 获取全部账号名():
    return [账号名.name for 账号名 in 获取账号目录().iterdir()]

def 新建账号(账号名: str) -> pathlib.Path:
    if 账号名 in 获取全部账号名():
        raise FileExistsError(f"账号 {账号名} 已经存在")
    新建账号目录 = 获取账号目录(账号名)
    新建账号目录.mkdir()
    # 复制默认浏览器存储状态文件
    shutil.copy(默认浏览器存储状态文件, 新建账号目录 / 浏览器存储状态文件名)
    return 新建账号目录

def 删除账号(账号名: str):
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    shutil.rmtree(获取账号目录(账号名))

def 修改账号名(账号名: str, 新账号名: str):
    if 新账号名 in 获取全部账号名():
        raise FileExistsError(f"账号 {新账号名} 已经存在")
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    shutil.move(获取账号目录(账号名), 获取账号目录(新账号名))

def 复制账号(账号名: str, 新账号名: str):
    if 新账号名 in 获取全部账号名():
        raise FileExistsError(f"账号 {新账号名} 已经存在")
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    shutil.copytree(获取账号目录(账号名), 获取账号目录(新账号名))

def 获取账号数据(账号名: Optional[str]=None, 默认值: Optional[Dict[str, Any]] = None) -> 数据类:
    return 获取本地数据(获取账号目录(账号名) / "数据.json", 默认值=默认值)

def 获取账号浏览器存储状态文件(账号名: str) -> pathlib.Path:
    if 账号名 not in 获取全部账号名():
        raise FileNotFoundError(f"账号 {账号名} 不存在")
    return 获取账号目录(账号名) / 浏览器存储状态文件名
