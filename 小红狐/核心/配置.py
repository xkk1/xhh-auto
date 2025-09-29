import os

from ..工具.目录工具 import 数据目录
from ..工具.数据工具 import 获取本地数据


默认配置 = {
    "环境变量": {
        "PLAYWRIGHT_BROWSERS_PATH": "浏览器",
        "PLAYWRIGHT_BROWSERS_TYPE": "webkit",
        "PORT": "44321",
        "DEBUG": "False"
    }
}

配置数据 = 获取本地数据(数据目录 / "元梦之星小红狐.json", 默认配置)

def 初始化环境():
    for 键, 值 in 配置数据["环境变量"].items():
        os.environ[键] = os.environ.get(键, 值)
    配置数据.保存()
