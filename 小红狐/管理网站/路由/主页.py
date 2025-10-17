from flask import Blueprint, redirect

from ...工具.日志工具 import 获取日志记录器
from ...核心.小红狐配置 import 配置数据

日志 = 获取日志记录器(__name__)
主页蓝图 = Blueprint(
    "主页",
    __name__
)


@主页蓝图.route('/')
def 主页():
    日志.调试(f"访问主页 {配置数据["环境变量"]["MANAGE_SITE_ROOT_REDIRECT_URL"]}")
    return redirect(配置数据["环境变量"]["MANAGE_SITE_ROOT_REDIRECT_URL"])
