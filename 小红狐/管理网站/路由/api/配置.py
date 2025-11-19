from typing import Any
from flask import Blueprint, jsonify, request

from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....核心.配置 import 获取全部配置名, 获取配置数据


日志 = 获取日志记录器(__name__)
配置蓝图 = Blueprint(
    "配置",
    __name__,
    url_prefix="/配置"
)


@配置蓝图.route("/配置名", methods=["GET"])
def 全部配置名():
    return jsonify(获取全部配置名())

# 获取配置数据
def 配置数据(配置名: str = "默认", 脚本模块名: str = 小红狐模块名):
    默认值: dict[str, Any] = {}
    json_data = request.get_json(silent=True)  # JSON 请求体，silent=True 避免解析失败报错
    if json_data:
        默认值 = json_data
        print(默认值)
    return jsonify(获取配置数据(配置名=配置名, 脚本模块名=脚本模块名, 默认值=默认值).数据)

@配置蓝图.route("/数据/<config_name>", methods=["GET"])
def 小红狐配置数据(config_name):
    配置名: str = config_name
    return 配置数据(配置名=配置名, 脚本模块名=小红狐模块名)

@配置蓝图.route("/数据/<config_name>/<package_name>", methods=["GET"])
def 脚本配置数据(config_name, package_name):
    配置名: str = config_name
    脚本模块名: str = package_name
    return 配置数据(配置名=配置名, 脚本模块名=脚本模块名)
