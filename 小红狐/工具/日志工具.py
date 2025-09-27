import logging
import os
from logging.handlers import RotatingFileHandler

from .目录工具 import 日志目录


class 日志级别:
    严重 = logging.CRITICAL
    致命 = 严重
    错误 = logging.ERROR
    警告 = logging.WARNING
    信息 = logging.INFO
    调试 = logging.DEBUG
    未设置 = logging.NOTSET
    自动级别 = 调试 if os.environ.get("DEBUG", "False") == "True" else 信息

class 日志类(logging.Logger):
    def __init__(self, name, 级别=日志级别.未设置):
        # 必须调用父类 Logger 的 __init__，传入 name 和 level
        super().__init__(name, 级别)
        self.调试 = super().debug
        self.信息 = super().info
        self.警告 = super().warning
        self.错误 = super().error
        self.严重 = super().critical
        self.致命 = super().fatal
        self.日志 = super().log


def 获取日志记录器(
    名称="元梦之星小红狐",
    日志文件=日志目录/"元梦之星小红狐.log",
    日志级别=日志级别.自动级别,
    控制台级别=日志级别.自动级别,
    文件级别=日志级别.自动级别,
    最大字节数=1 * 1024 * 1024,  # 1 MB
    备份文件数量=1,
    日志格式="%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s %(pathname)s:%(lineno)d %(funcName)s %(message)s",
    日期格式="%Y-%m-%d %H:%M:%S",
    控制台日志格式="%(asctime)s.%(msecs)d %(levelname)s %(name)s %(funcName)s %(message)s",
    控制台日期格式="%H:%M:%S",
    文件编码="utf-8"
) -> 日志类:
    logging.setLoggerClass(日志类)
    日志记录器 = logging.getLogger(名称)
    日志记录器.setLevel(日志级别)

    if 日志记录器.handlers:
        return 日志记录器  # 避免重复添加处理器

    日志目录 = os.path.dirname(os.path.abspath(日志文件))
    if 日志目录 and not os.path.exists(日志目录):
        os.makedirs(日志目录)

    格式化器 = logging.Formatter(fmt=日志格式, datefmt=日期格式)

    # 文件日志 —— 按大小切割
    文件处理器 = RotatingFileHandler(
        filename=日志文件,
        maxBytes=最大字节数,
        backupCount=备份文件数量,
        encoding=文件编码
    )
    文件处理器.setLevel(文件级别)
    文件处理器.setFormatter(格式化器)

    # 控制台日志
    控制台格式化器 = logging.Formatter(fmt=控制台日志格式, datefmt=控制台日期格式)
    控制台处理器 = logging.StreamHandler()
    控制台处理器.setLevel(控制台级别)
    控制台处理器.setFormatter(控制台格式化器)

    日志记录器.addHandler(文件处理器)
    日志记录器.addHandler(控制台处理器)

    return 日志记录器

def 获取异步日志记录器(*args, **kwargs):
    # 日志格式添加任务名称 %(taskName)s
    kwargs["日志格式"] = kwargs.get("日志格式", "%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s %(pathname)s:%(lineno)d %(funcName)s %(taskName)s %(message)s")
    kwargs["控制台日志格式"] = kwargs.get("控制台日志格式", "%(asctime)s.%(msecs)d %(levelname)s %(name)s %(funcName)s %(taskName)s %(message)s")
    return 获取日志记录器(*args, **kwargs)
