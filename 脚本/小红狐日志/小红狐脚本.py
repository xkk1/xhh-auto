from typing import Any

from . import __author__, __version__
from . import __package__ as 模块名


名称: str = "小红狐日志"  # 脚本名称，默认：__package__
简介: str = "提供显示实时日志接口、页面"  # 脚本简介，默认：__doc__
作者: list[str] = [__author__]  # 脚本作者，默认：__author__
版本: str = __version__  # 脚本版本，默认：[__version__]
调试: bool = False  # 仅开启调试模式时启用脚本。默认：False
# 总控页面生成函数 () -> dict[str, str]  {URL: 标题}
def 总控页面() -> dict[str, str]:
    页面: dict[str, str] = {
        f"/api/目录/脚本/{模块名}/网页/总控.html": "小红狐日志",
    }
    return 页面

from . import 核心
def flask路由(子路径: str):
    import flask
    请求方法 = flask.request.method  # HTTP 请求方法
    if 子路径 == "/api/日志/服务器发送事件" and 请求方法 == "GET":
        return 核心.日志服务器发送事件路由()
    elif 子路径 == "/api/日志/渠道名" and 请求方法 == "GET":
        return 核心.获取渠道名列表路由()
    elif 子路径 == "/api/日志/最新" and 请求方法 == "GET":
        return 核心.获取最新日志路由()
    elif 子路径 == "/api/日志/历史" and 请求方法 == "GET":
        return 核心.获取历史日志路由()
    elif 子路径 == "/api/日志/新增" and 请求方法 == "GET":
        return 核心.新增日志路由()
    elif 子路径 == "/api/日志/新增" and 请求方法 == "POST":
        return 核心.新增日志路由()
    elif 子路径 == "/api/日志/内容上限" and 请求方法 == "GET":
        return 核心.获取内容上限路由()
    elif 子路径 == "/api/日志/内容上限" and 请求方法 == "POST":
        return 核心.设置内容上限路由()
    elif 子路径 == "/api/日志/设置内容上限" and 请求方法 == "GET":
        return 核心.设置内容上限路由()
    查询参数 = flask.request.args  # GET 参数
    表单数据 = flask.request.form  # POST 参数
    json请求体 = flask.request.get_json(silent=True)  # JSON 请求体，silent=True 避免解析失败报错

    所有数据 = {
        "子路径": 子路径,
        "请求方法": 请求方法,
        "查询参数": 查询参数,
        "表单数据": 表单数据,
        "JSON请求体": json请求体
    }
    return flask.jsonify(所有数据), 200

