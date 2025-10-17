import pathlib
import shutil
from typing import Any

from 小红狐.工具.数据工具 import 数据类, 获取本地数据
from ..工具.目录工具 import 页面目录


页面目录.mkdir(parents=True, exist_ok=True)

def 获取页面目录(页面名: str | None = None) -> pathlib.Path:
    if 页面名:
        return 页面目录 / 页面名
    else:
        return 页面目录

def 获取全部页面名():
    return [页面名.name for 页面名 in 获取页面目录().iterdir()]

def 新建页面(页面名: str) -> pathlib.Path:
    if 页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {页面名} 已经存在")
    新建页面目录 = 获取页面目录(页面名)
    新建页面目录.mkdir()

def 删除页面(页面名: str) -> None:
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    shutil.rmtree(获取页面目录(页面名))

def 修改页面名(页面名: str, 新页面名: str) -> None:
    if 新页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {新页面名} 已经存在")
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    shutil.move(获取页面目录(页面名), 获取页面目录(新页面名))

def 复制页面(页面名: str, 新页面名: str) -> None:
    if 新页面名 in 获取全部页面名():
        raise FileExistsError(f"页面 {新页面名} 已经存在")
    if 页面名 not in 获取全部页面名():
        raise FileNotFoundError(f"页面 {页面名} 不存在")
    shutil.copytree(获取页面目录(页面名), 获取页面目录(新页面名))

def 获取页面数据(页面名: str | None = None, 默认值: dict[str, Any] | None = None) -> 数据类:
    return 获取本地数据(获取页面目录(页面名) / "数据.json", 默认值=默认值)
