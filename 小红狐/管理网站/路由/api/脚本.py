from types import NoneType
from typing import Any
from flask import Blueprint, jsonify

from ....工具.日志工具 import 获取日志记录器
from ....核心.脚本 import 小红狐脚本信息, 获取导入脚本信息列表, 获取导入脚本模块名列表, 获取脚本


日志 = 获取日志记录器(__name__)
脚本蓝图 = Blueprint(
    "脚本",
    __name__,
    url_prefix="/脚本"
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

@脚本蓝图.route("", methods=["GET"])
@脚本蓝图.route("/", methods=["GET"])
def 返回导入脚本信息列表() -> dict[str, NoneType | str | int | float | bool | list | dict]:
    导入脚本信息列表 = 获取导入脚本信息列表()
    return jsonify(标准化(导入脚本信息列表))

HTTP方法 = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']

def 处理接口(脚本模块名, 子路径):
    if 脚本模块名 not in 获取导入脚本模块名列表():
        return jsonify({"错误": f"脚本模块“{脚本模块名}”不存在"}), 404
    脚本 = 获取脚本(脚本模块名)
    if 脚本["flask_route"] is None:
        return jsonify({"错误": "脚本未启用 Flask"}), 400
    return 脚本["flask_route"](子路径=子路径)

@脚本蓝图.route("/接口/<package>/<path:subpath>", methods=HTTP方法)
def 处理子路径(package, subpath):
    return 处理接口(脚本模块名=package, 子路径="/"+subpath)

@脚本蓝图.route("/接口/<package>/", methods=HTTP方法)
def 处理路径(package):
    return 处理接口(脚本模块名=package, 子路径="/")

@脚本蓝图.route("/接口/<package>", methods=HTTP方法)
def 处理模块(package):
    return 处理接口(脚本模块名=package, 子路径="")

# 获取脚本配置标签页
@脚本蓝图.route("/配置标签页/<package>/<pagename>", methods=["GET"])
def 获取脚本配置标签页(package, pagename):
    模块名: str = package
    页面名: str = pagename
    脚本配置标签页: list[dict[str, str]] = []
    try:
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=模块名)
        配置页面: dict[str, str] = 脚本模块.获取配置页面(页面名=页面名)
        for 配置页面URL, 配置页面标题 in 配置页面.items():
            脚本配置标签页.append({
                "url": 配置页面URL,
                "标题": 配置页面标题,
            })
    except:
        pass
    return jsonify(脚本配置标签页)
