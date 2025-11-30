from typing import Any

from . import __author__, __version__
from . import __package__ as 模块名


名称: str = "小红狐脚本开发"  # 脚本名称，默认：__package__
简介: str = "小红狐脚本开发"  # 脚本简介，默认：__doc__
作者: list[str] = [__author__]  # 脚本作者，默认：__author__
版本: str = __version__  # 脚本版本，默认：[__version__]
调试: bool = True  # 仅开启调试模式时启用脚本。默认：False
总控页面: dict[str, str] = {  # 总控页面 {URL: 标题}
    f"/api/脚本/路由/{模块名}/文档/主页.html": "小红狐脚本开发文档",
}

页面操作: dict[str, dict[str, Any]] = {
    "开发者工具": {  # 页面操作脚本名，唯一
        "入口函数": None,  # 入口函数 (页面名: str)
        "关闭函数": None,  # 关闭函数 (页面名: str | None) 页面名=None->关闭全部
        "脚本状态": None,  # 脚本开启状态函数 (页面名: str | None) -> bool
        "配置页面": None,  # 配置页面函数 (页面名: str) -> dict[str, str]
        "名称": "小红狐脚本开发者工具",  # 脚本名称 str
        "简介": "小红狐脚本开发者工具",  # 脚本简介 str
        "调试": True,  # 仅开启调试模式时启用脚本 bool 默认：False
    },
}

def flask路由(子路径: str):
    import flask
    请求方法 = flask.request.method  # HTTP 请求方法
    # 文档
    if 请求方法 == "GET" and 子路径.startswith("/文档"):
        from .文档 import 文档
        return 文档.路由(子路径[3:])
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
