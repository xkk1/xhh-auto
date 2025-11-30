import os
import pathlib

from ..import __package__ as 模块名
from ..核心.配置 import 获取配置数据


默认配置 = {
    "环境变量": {
        "SCRIPT_PATH": "脚本",
        "PLAYWRIGHT_BROWSERS_PATH": "浏览器",
        "PLAYWRIGHT_BROWSERS_TYPE": "chromium",
        "PLAYWRIGHT_BROWSERS_LAUNCH_MODE": "launch",
        "PLAYWRIGHT_BROWSERS_CDP_ENDPOINT_URL": "http://127.0.0.1:9222",
        "MANAGE_SITE_PORT": "44321",
        "MANAGE_SITE_AUTO_OPEN_BROWSER": "True",
        "MANAGE_SITE_AUTO_OPEN_DELAY": "1.0",
        "MANAGE_SITE_ROOT_REDIRECT_URL": "/小红狐.html",
        "DEBUG": "False"
    }
}
配置数据 = 获取配置数据(脚本模块名=模块名, 默认值=默认配置)


def 初始化小红狐配置():
    for 键, 值 in 配置数据["环境变量"].items():
        os.environ[键] = os.environ.get(键, 值)
    配置数据.保存()
    from ..工具 import 目录工具
    os.environ["小红狐"] = str(目录工具.小红狐目录)
    目录工具.脚本目录 = pathlib.Path(os.environ.get("SCRIPT_PATH", 配置数据["环境变量"]["SCRIPT_PATH"])).resolve()

def 判断开关(值: str) -> bool:
    # 判断是否为 true 1 yes on... 首字母
    if len(值) >= 1 and 值.lower()[0] in "t1yo是开真":
        return True
    else:
        return False

def 获取调试() -> bool:
    return 判断开关(os.environ.get("DEBUG", 配置数据["环境变量"]["DEBUG"]))

def 获取浏览器路径() -> pathlib.Path:
    return pathlib.Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", 配置数据["环境变量"]["PLAYWRIGHT_BROWSERS_PATH"]))

def 获取浏览器类型() -> str:
    return os.environ.get("PLAYWRIGHT_BROWSERS_TYPE", 配置数据["环境变量"]["PLAYWRIGHT_BROWSERS_TYPE"])

def 获取浏览器启动方式() -> str:
    return os.environ.get("PLAYWRIGHT_BROWSERS_LAUNCH_MODE", 配置数据["环境变量"]["PLAYWRIGHT_BROWSERS_LAUNCH_MODE"])

def 获取浏览器CDP端点URL() -> str:
    return os.environ.get("PLAYWRIGHT_BROWSERS_CDP_ENDPOINT_URL", 配置数据["环境变量"]["PLAYWRIGHT_BROWSERS_CDP_ENDPOINT_URL"])

def 获取管理网站端口() -> int:
    try:
        return int(os.environ.get("MANAGE_SITE_PORT", 配置数据["环境变量"]["MANAGE_SITE_PORT"]))
    except ValueError:
        return 44321
def 获取自动打开管理网站() -> bool:
    return 判断开关(os.environ.get("MANAGE_SITE_AUTO_OPEN_BROWSER", 配置数据["环境变量"]["MANAGE_SITE_AUTO_OPEN_BROWSER"]))

def 获取管理网站打开延迟() -> float:
    try:
        return float(os.environ.get("MANAGE_SITE_AUTO_OPEN_DELAY", 配置数据["环境变量"]["MANAGE_SITE_AUTO_OPEN_DELAY"]))
    except ValueError:
        return 1.0
