from typing import Any

from . import __author__, __version__
from . import __package__ as 模块名


名称: str = "小红狐自动化"  # 脚本名称，默认：__package__
简介: str = "小红狐自动化管理脚本"  # 脚本简介，默认：__doc__
作者: list[str] = [__author__]  # 脚本作者，默认：__author__
版本: str = __version__  # 脚本版本，默认：[__version__]
调试: bool = False  # 仅开启调试模式时启用脚本。默认：False
总控页面: dict[str, str] = {  # 总控页面 {URL: 标题}
    "/api/目录/小红狐/内置脚本/网站/总控.html": "小红狐总控",
}

from .内置脚本.页面生成 import 新建页面

# 页面生成脚本
页面生成: dict[str, dict[str, Any]] = {
    "新建页面": {  # 页面生成脚本名，唯一
        "新建页面": 新建页面.新建页面,  # 新建页面函数 (页面名: str) -> playwright.async_api.Page
        "关闭页面": 新建页面.关闭页面,  # 关闭页面函数 (页面名: str | None) 页面名=None->关闭全部
        "获取页面": 新建页面.获取页面,  # 获取页面函数 (页面名: str) -> playwright.async_api.Page | None
        "配置页面": 新建页面.配置页面,  # 配置页面函数 (页面名: str) -> dict[str, str]
        "名称": 新建页面.名称,  # 脚本名称 str
        "简介": "小红狐页面生成",  # 脚本简介 str
        "调试": False,  # 仅开启调试模式时启用脚本 bool 默认：False
    },
}

默认启用页面生成脚本名: str = "新建页面"

from .内置脚本.页面操作 import 页面管理

页面操作: dict[str, dict[str, Any]] = {
    "页面管理": {  # 页面操作脚本名，唯一
        "入口函数": 页面管理.入口函数,  # 入口函数 (页面名: str)
        "关闭函数": 页面管理.关闭函数,  # 关闭函数 (页面名: str | None) 页面名=None->关闭全部
        "脚本状态": 页面管理.脚本状态,  # 脚本开启状态函数 (页面名: str | None) -> bool
        "配置页面": 页面管理.配置页面,  # 配置页面函数 (页面名: str) -> dict[str, str]
        "名称": 页面管理.名称,  # 脚本名称 str
        "简介": "管理页面、脚本，选中自动开启时将保持开启状态",  # 脚本简介 str
        "调试": False,  # 仅开启调试模式时启用脚本 bool 默认：False
    },
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

默认启用页面操作脚本名元组: tuple[str, ...] = ("页面管理",)

def flask_route(子路径: str):
    import flask
    # 获取请求方法
    method = flask.request.method

    # 获取各种参数
    args = flask.request.args  # GET 参数
    form = flask.request.form  # POST 表单参数
    json_data = flask.request.get_json(silent=True)  # JSON 请求体，silent=True 避免解析失败报错

    所有数据 = {
        "子路径": 子路径,
        "method": method,
        "args": args,
        "form": form,
        "json_data": json_data
    }
    return flask.jsonify(所有数据), 200
