from types import NoneType
from typing import Any
from flask import Blueprint, Response, jsonify

from ....工具.日志工具 import 获取日志记录器
from ....核心.脚本 import 获取导入脚本信息列表, 获取导入脚本模块名列表, 获取脚本


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

@脚本蓝图.route("/", methods=["GET"])
def 返回导入脚本信息列表() -> Response[dict[str, NoneType | str | int | float | bool | list | dict]]:
    导入脚本信息列表 = 获取导入脚本信息列表()
    return jsonify(标准化(导入脚本信息列表))
