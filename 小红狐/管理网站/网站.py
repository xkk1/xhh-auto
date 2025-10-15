import asyncio
import os
from pathlib import Path
import socket
import webbrowser

from flask import Flask
from waitress import serve

from ..工具.日志工具 import 获取日志记录器
from ..工具.任务管理器工具 import 异步任务管理器
from ..核心.小红狐配置 import 获取调试, 获取管理网站端口, 获取自动打开管理网站
from . import 网站目录, 静态文件目录, 模板目录
from .路由 import *


日志 = 获取日志记录器(__name__)
调试 = 获取调试()
端口 = 获取管理网站端口()
自动打开管理网站 = 获取自动打开管理网站()


def 检测端口占用(端口: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", 端口))  # 或者使用 "127.0.0.1" 仅本地
            return False
        except OSError:
            return True  # 端口已被占用

async def 浏览器打开管理网站():
    from ..核心.小红狐配置 import 获取管理网站打开延迟
    管理网站打开延迟 = 获取管理网站打开延迟()
    日志.信息(f"🚀管理网站已启动，请等待 {管理网站打开延迟} 秒后自动打开浏览器")
    await asyncio.sleep(管理网站打开延迟)
    webbrowser.open(f"http://localhost:{端口}")

def 主函数():
    日志.调试(f"🌈元梦之星小红狐管理网站启动中，网站目录：{str(网站目录)}")
    网站 = Flask(
        __name__,
        static_folder=静态文件目录,
        static_url_path="",
        template_folder=模板目录
        )

    # 注册蓝图
    网站.register_blueprint(主页蓝图)
    
    if 检测端口占用(端口):
        日志.严重(f"❌端口 {端口} 已被占用，请选择其他端口")
        raise Exception(f"端口 {端口} 已被占用")
    日志.信息(f"🔨管理网站启动中，端口：{端口}，调试：{调试}")
    if 自动打开管理网站:
        异步任务管理器.启动任务("浏览器打开管理网站", 浏览器打开管理网站)
    if 调试:
        # 不启用 debug=True ，启用会导致浏览器重开多开
        网站.run(host="0.0.0.0", port=端口)
    else:
        serve(网站, host="0.0.0.0", port=端口)
