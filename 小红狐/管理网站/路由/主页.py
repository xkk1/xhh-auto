from flask import Blueprint, render_template

from ...工具.日志工具 import 获取日志记录器
from .. import 静态文件目录

日志 = 获取日志记录器(__name__)
主页蓝图 = Blueprint(
    "主页",
    __name__,
    static_folder=静态文件目录,
    static_url_path=""
)


@主页蓝图.route('/')
def 主页():
    日志.调试("访问主页")
    return 主页蓝图.send_static_file("index.html")
