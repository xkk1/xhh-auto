import os
from pathlib import Path

from flask import Flask
from waitress import serve

from .路由 import *


def 主函数():
    # 获取当前目录
    网站目录 = Path(os.environ.get("SCRIPT_DIR", (Path(".") / "脚本").resolve())) / "管理网站"
    print(网站目录)
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
    if 调试:
        网站.run(host="0.0.0.0", port=端口, debug=True)
    else:
        serve(网站, host="0.0.0.0", port=端口)
