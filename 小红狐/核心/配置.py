import os
import pathlib

from ..工具.目录工具 import 数据目录
from ..工具.数据工具 import 获取本地数据


默认配置 = {
    "环境变量": {
        "SCRIPT_PATH": "小红狐/脚本",
        "PLAYWRIGHT_BROWSERS_PATH": "浏览器",
        "PLAYWRIGHT_BROWSERS_TYPE": "chromium",
        "PORT": "44321",
        "DEBUG": "False"
    }
}

配置数据 = 获取本地数据(数据目录 / "元梦之星小红狐.json", 默认配置)


def 初始化环境变量():
    for 键, 值 in 配置数据["环境变量"].items():
        os.environ[键] = os.environ.get(键, 值)
    配置数据.保存()
    from ..工具 import 目录工具
    目录工具.脚本目录 = pathlib.Path(os.environ.get("SCRIPT_PATH", 配置数据["环境变量"]["SCRIPT_PATH"]))
