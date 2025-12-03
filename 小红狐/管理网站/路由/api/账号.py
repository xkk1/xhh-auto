from typing import Any
from flask import Blueprint, jsonify, request


from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....核心.账号 import 保存账号状态, 修改账号名, 删除账号, 复制账号, 新建账号, 获取全部账号名


日志 = 获取日志记录器(__name__)
账号蓝图 = Blueprint(
    "账号",
    __name__,
    url_prefix="/账号"
)

@账号蓝图.route("/账号名", methods=["GET"])
def 获取全部账号名路由():
    return jsonify(获取全部账号名())

# 新建账号
@账号蓝图.route("/账号名", methods=["POST"])
def 新建账号路由():
    if not request.is_json:
        return jsonify("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify("无效的 JSON 格式，请检查请求体"), 400
    if not isinstance(json, str):
        return jsonify("必须是字符串"), 400
    账号名: str = json
    try:
        新建账号(账号名)
        return jsonify("账号新建成功")
    except Exception as e:
        日志.警告(f"新建账号失败，账号名：“{账号名}”: {e}")
        return jsonify(f"新建账号失败，账号名：“{账号名}”: {e}"), 400

# 修改账号名
@账号蓝图.route("/账号名", methods=["PUT"])
def 修改账号名路由():
    if not request.is_json:
        return jsonify("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify("无效的 JSON 格式，请检查请求体"), 400
    if not isinstance(json, dict):
        return jsonify("必须是字典"), 400
    if "账号名" not in json or "新账号名" not in json:
        return jsonify("缺少参数“账号名”"), 400
    账号名: str = json["账号名"]
    if not isinstance(账号名, str):
        return jsonify("账号名必须是字符串"), 400
    if "新账号名" not in json:
        return jsonify("缺少参数“新账号名”"), 400
    新账号名: str = json["新账号名"]
    if not isinstance(新账号名, str):
        return jsonify("新账号名必须是字符串"), 400
    try:
        修改账号名(账号名, 新账号名)
        return jsonify("修改账号名成功")
    except Exception as e:
        日志.警告(f"修改账号名失败，账号名：“{账号名}”: {e}")
        return jsonify(f"修改账号名失败!\n账号名“{账号名}”: {e}"), 500

# 删除账号
@账号蓝图.route("/账号名/<account_name>", methods=["DELETE"])
def 删除账号路由(account_name: str):
    账号名: str = account_name
    try:
        删除账号(账号名=账号名)
        return jsonify("删除账号成功")
    except Exception as e:
        日志.警告(f"删除账号失败，账号名：“{账号名}”: {e}")
        return jsonify(f"删除账号失败!\n账号名“{账号名}”: {e}"), 500

# 复制账号
@账号蓝图.route("/复制", methods=["POST"])
def 复制账号路由():
    if not request.is_json:
        return jsonify("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify("无效的 JSON 格式，请检查请求体"), 400
    if not isinstance(json, dict):
        return jsonify("必须是dict"), 400
    if "账号名" not in json:
        return jsonify("缺少参数“账号名”"), 400
    账号名: str = json["账号名"]
    if not isinstance(账号名, str):
        return jsonify("账号名必须是字符串"), 400
    if "新账号名" not in json:
        return jsonify("缺少参数“新账号名”"), 400
    新账号名: str = json["新账号名"]
    if not isinstance(新账号名, str):
        return jsonify("新账号名必须是字符串"), 400
    try:
        复制账号(账号名, 新账号名)
        return jsonify("复制账号成功")
    except Exception as e:
        日志.警告(f"复制账号失败，账号名：“{账号名}”: {e}")
        return jsonify(f"复制账号失败!\n账号名“{账号名}”: {e}"), 500

@账号蓝图.route("/保存账号状态/<account_name>", methods=["GET"])
def 保存账号状态路由(account_name: str):
    账号名: str = account_name
    try:
        保存账号状态(账号名)
        return jsonify("保存账号状态成功")
    except Exception as e:
        日志.警告(f"保存账号状态失败，账号名：“{账号名}”: {e}")
        return jsonify(f"保存账号状态失败!\n账号名“{账号名}”: {e}"), 500
