import os
from pathlib import Path

from flask import Flask
from waitress import serve

from ..工具.日志工具 import 获取日志记录器
from ..核心.小红狐配置 import 获取调试, 获取端口
from .路由 import *


日志 = 获取日志记录器(__name__)
网站目录 = Path(__file__).parent.resolve()
调试 = 获取调试()
端口 = 获取端口()


def 主函数():
    日志.调试(f"🌈元梦之星小红狐管理网站启动中，网站目录：{str(网站目录)}")
    网站 = Flask(
        __name__,
        static_folder=网站目录/"静态文件",
        static_url_path="",
        template_folder=网站目录/"模板"
        )

    # 注册蓝图
    网站.register_blueprint(主页蓝图)
    
    日志.信息(f"🔨管理网站启动中，端口：{端口}，调试：{调试}")
    if 调试:
        网站.run(host="0.0.0.0", port=端口, debug=True)
    else:
        serve(网站, host="0.0.0.0", port=端口)

