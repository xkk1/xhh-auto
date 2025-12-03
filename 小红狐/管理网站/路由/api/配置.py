from typing import Any
from flask import Blueprint, jsonify, request

from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....核心.配置 import 删除配置, 新建配置, 获取全部配置名, 获取配置数据


日志 = 获取日志记录器(__name__)
配置蓝图 = Blueprint(
    "配置",
    __name__,
    url_prefix="/配置"
)


@配置蓝图.route("/配置名", methods=["GET"])
def 全部配置名():
    return jsonify(获取全部配置名())

# 新建配置名
@配置蓝图.route("/配置名", methods=["POST"])
def 新建配置名路由():
    if not request.is_json:
        return jsonify("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify("无效的 JSON 格式，请检查请求体"), 400
    if not isinstance(json, str):
        return jsonify("必须是字符串"), 400
    配置名: str = json
    try:
        新建配置(配置名=配置名)
        return jsonify("成功"), 200
    except Exception as e:
        return jsonify(str(e)), 400

# 删除配置名
@配置蓝图.route("/配置名/<config_name>", methods=["DELETE"])
def 删除配置名路由(config_name):
    配置名: str = config_name
    try:
        删除配置(配置名=配置名)
        return jsonify("成功"), 200
    except Exception as e:
        return jsonify(str(e)), 400

# 获取配置数据
def 配置数据(配置名: str = "默认", 脚本模块名: str = 小红狐模块名):
    默认值: dict[str, Any] = {}
    json_data = request.get_json(silent=True)  # JSON 请求体，silent=True 避免解析失败报错
    if json_data:
        默认值 = json_data
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
