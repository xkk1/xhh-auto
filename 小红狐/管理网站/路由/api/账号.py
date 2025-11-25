from typing import Any
from flask import Blueprint, jsonify, request


from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....核心.账号 import 新建账号, 获取全部账号名


日志 = 获取日志记录器(__name__)
账号蓝图 = Blueprint(
    "账号",
    __name__,
    url_prefix="/账号"
)

@账号蓝图.route("/账号名", methods=["GET"])
def 获取全部账号名():
    return jsonify(获取全部账号名())

# 新建账号
@账号蓝图.route("/账号名", methods=["POST"])
def 新建账号路由():
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    # 判断 json 是否为字符串
    if isinstance(json, str):
        账号名: str = json
    else:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    账号名 = json
    try:
        新建账号(账号名)
        return jsonify({"信息": "账号新建成功"})
    except Exception as e:
        日志.警告(f"新建账号失败，账号名：“{账号名}”: {e}")
        return jsonify({"错误": "新建账号失败", "信息": f"账号名：“{账号名}”: {e}"}), 400
