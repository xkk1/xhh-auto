from typing import Any
from flask import Blueprint, jsonify, request


from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....核心.账号 import 获取全部账号名


日志 = 获取日志记录器(__name__)
账号蓝图 = Blueprint(
    "账号",
    __name__,
    url_prefix="/账号"
)

@账号蓝图.route("/账号名", methods=["GET"])
def 全部配置名():
    return jsonify(获取全部账号名())
