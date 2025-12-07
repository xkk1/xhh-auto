from typing import Any

from . import __author__, __version__
from . import __package__ as 模块名


名称: str = "小红狐截图"  # 脚本名称，默认：__package__
简介: str = "提供页面截图，以及本地保存"  # 脚本简介，默认：__doc__
作者: list[str] = [__author__]  # 脚本作者，默认：__author__
版本: str = __version__  # 脚本版本，默认：[__version__]
调试: bool = False  # 仅开启调试模式时启用脚本。默认：False

from .页面操作 import 页面截图
from .页面操作 import 简单远程控制
页面操作: dict[str, dict[str, Any]] = {
    "页面截图": {  # 页面操作脚本名，唯一
        "入口函数": 页面截图.入口函数,  # 入口函数 (页面名: str)
        "关闭函数": 页面截图.关闭函数,  # 关闭函数 (页面名: str | None) 页面名=None->关闭全部
        "脚本状态": 页面截图.脚本状态,  # 脚本开启状态函数 (页面名: str | None) -> bool
        "配置页面": 页面截图.配置页面,  # 配置页面函数 (页面名: str) -> dict[str, str]
        "名称": "小红狐页面截图",  # 脚本名称 str
        "简介": "提供页面截图，以及本地保存",  # 脚本简介 str
        "调试": False,  # 仅开启调试模式时启用脚本 bool 默认：False
    },
    "简单远程控制": {  # 页面操作脚本名，唯一
        "入口函数": 简单远程控制.入口函数,  # 入口函数 (页面名: str)
        "关闭函数": 简单远程控制.关闭函数,  # 关闭函数 (页面名: str | None) 页面名=None->关闭全部
        "脚本状态": 简单远程控制.脚本状态,  # 脚本开启状态函数 (页面名: str | None) -> bool
        "配置页面": 简单远程控制.配置页面,  # 配置页面函数 (页面名: str) -> dict[str, str]
        "名称": "小红狐简单远程控制",  # 脚本名称 str
        "简介": "基于页面截图的简单远程控制",  # 脚本简介 str
        "调试": False,  # 仅开启调试模式时启用脚本 bool 默认：False
    },
}

def flask路由(子路径: str):
    import flask
    请求方法 = flask.request.method  # HTTP 请求方法
    if 子路径 == "/api/页面操作/页面截图" and 请求方法 == "GET":
        from .页面操作 import 页面截图
        return 页面截图.路由()
    简单远程控制url = "/api/页面操作/简单远程控制" 
    if 子路径.startswith(简单远程控制url) and 请求方法 == "GET":
        from .页面操作 import 简单远程控制
        return 简单远程控制.路由(子路径.removeprefix(简单远程控制url))
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

