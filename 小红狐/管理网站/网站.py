import os
from pathlib import Path

from flask import Flask
from waitress import serve

from ..工具.日志工具 import 获取日志记录器
from .路由 import *


日志 = 获取日志记录器(__name__)
网站目录 = Path(__file__).parent.resolve()


def 主函数():
    日志.调试(f"🌈元梦之星小红狐网站初始化中，网站目录：{网站目录.as_posix()}")
    网站 = Flask(
        __name__,
        static_folder=(网站目录/"静态文件").as_posix(),
        static_url_path="",
        template_folder=(网站目录/"模板").as_posix()
        )

    # 注册蓝图
    网站.register_blueprint(主页蓝图)
    
    调试 = (os.environ.get("DEBUG", "False") == "True")  # 如果没设置，默认认为是生产环境
    端口 = int(os.environ.get("PORT", "44321"))  # 默认端口 44321
    日志.信息(f"🔨管理网站启动中，端口：{端口}，调试：{调试}")
    if 调试:
        网站.run(host="0.0.0.0", port=端口, debug=True)
    else:
        serve(网站, host="0.0.0.0", port=端口)
