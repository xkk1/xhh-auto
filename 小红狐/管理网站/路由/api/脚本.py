from pathlib import Path
from types import NoneType
from typing import Any
from flask import Blueprint, jsonify

from ....工具.日志工具 import 获取日志记录器
from ....核心.脚本 import 加载所有脚本, 获取加载脚本错误信息字典, 获取导入脚本信息字典, 获取导入脚本模块名列表, 获取脚本, 脚本目录, 重载脚本


日志 = 获取日志记录器(__name__)
脚本蓝图 = Blueprint(
    "脚本",
    __name__,
    url_prefix="/脚本",
    template_folder=脚本目录.resolve(),
)


def 标准化(要标准化数据: Any) -> NoneType | str | int | float | bool | list | dict:
    if isinstance(要标准化数据, (str, int, float, bool, NoneType)):
        return 要标准化数据
    elif isinstance(要标准化数据, (list, tuple, set)):
        return [
            标准化(子数据)
            for 子数据 in 要标准化数据
        ]
    elif isinstance(要标准化数据, dict):
        return {
            子键: 标准化(子数据)
            for 子键, 子数据 in 要标准化数据.items()
        }
    else:
        return str(要标准化数据)

@脚本蓝图.route("/导入脚本信息字典", methods=["GET"])
def 返回导入脚本信息字典() -> dict[str, NoneType | str | int | float | bool | list | dict]:
    导入脚本信息字典: dict[str, dict[str, Any]] = 获取导入脚本信息字典()
    return jsonify(标准化(导入脚本信息字典))

# https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Methods
HTTP请求方法 = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]

def 处理路由(脚本模块名, 子路径):
    if 脚本模块名 not in 获取导入脚本模块名列表():
        return jsonify(f"脚本模块“{脚本模块名}”不存在"), 404
    脚本 = 获取脚本(脚本模块名)
    if 脚本["flask路由"] is None:
        return jsonify("脚本未启用 Flask"), 400
    return 脚本["flask路由"](子路径=子路径)

@脚本蓝图.route("/路由/<package>/<path:subpath>", methods=HTTP请求方法)
def 处理子路径(package, subpath):
    return 处理路由(脚本模块名=package, 子路径="/"+subpath)

@脚本蓝图.route("/路由/<package>/", methods=HTTP请求方法)
def 处理路径(package):
    return 处理路由(脚本模块名=package, 子路径="/")

@脚本蓝图.route("/路由/<package>", methods=HTTP请求方法)
def 处理模块(package):
    return 处理路由(脚本模块名=package, 子路径="")

@脚本蓝图.route("/重载/<package>", methods=["GET"])
def 重载指定脚本蓝图(package):
    脚本模块名:str = package
    try:
        重载脚本(脚本模块名)
        return jsonify(f"已重载脚本：{脚本模块名}")
    except ImportError as e:
        return jsonify(str(e)), 404

@脚本蓝图.route("/重载", methods=["GET"])
def 重载所有脚本蓝图():
    return jsonify(加载所有脚本())

@脚本蓝图.route("/加载脚本错误信息字典", methods=["GET"])
def 获取加载脚本错误信息字典路由():
    return jsonify(获取加载脚本错误信息字典())
