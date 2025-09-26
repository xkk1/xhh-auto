import os
import pathlib

from . import 主函数 as 元梦之星小红狐主函数


def 主函数():
    # 当前目录
    小红狐脚本目录 = pathlib.Path(__file__).parent.resolve()
    启动器目录 = 小红狐脚本目录.parent
    # 设置一个临时环境变量指定浏览器存放目录
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", (启动器目录 / "浏览器").as_posix())
    # 设置数据目录
    os.environ["DATA_DIR"] = os.environ.get("DATA_DIR", (启动器目录 / "数据").as_posix())
    # 设置脚本目录
    os.environ["SCRIPT_DIR"] = os.environ.get("SCRIPT_DIR", 启动器目录.as_posix())
    # 运行脚本
    元梦之星小红狐主函数()


if __name__ == "__main__":
    主函数()
