from flask import Blueprint, jsonify

from ....工具.日志工具 import 获取日志记录器
from ....核心.脚本 import 获取导入脚本模块名列表, 获取脚本


日志 = 获取日志记录器(__name__)
脚本蓝图 = Blueprint(
    "脚本",
    __name__,
    url_prefix="/脚本"
)
HTTP方法 = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']

def 处理接口(脚本模块名, 子路径):
    if 脚本模块名 not in 获取导入脚本模块名列表():
        return jsonify({"错误": f"脚本模块“{脚本模块名}”不存在"}), 404
    脚本 = 获取脚本(脚本模块名)
    if 脚本["flask_route"] is None:
        return jsonify({"错误": "脚本未启用 Flask"}), 400
    return 脚本["flask_route"](子路径=子路径)

@脚本蓝图.route("/<package>/<path:subpath>", methods=HTTP方法)
def 处理子路径(package, subpath):
    return 处理接口(脚本模块名=package, 子路径="/"+subpath)
@脚本蓝图.route("/<package>/", methods=HTTP方法)
def 处理路径(package):
    return 处理接口(脚本模块名=package, 子路径="/")

@脚本蓝图.route("/<package>", methods=HTTP方法)
def 处理模块(package):
    return 处理接口(脚本模块名=package, 子路径="")
