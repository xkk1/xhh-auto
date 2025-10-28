from flask import Blueprint, jsonify, request

from ....工具.日志工具 import 获取日志记录器
from ....核心.配置 import 获取全部配置名


日志 = 获取日志记录器(__name__)
配置蓝图 = Blueprint(
    "配置",
    __name__,
    url_prefix="/配置"
)


# 返回内存数据 json
@配置蓝图.route("/配置名", methods=["GET"])
def 内存数据():
    return jsonify(获取全部配置名())
