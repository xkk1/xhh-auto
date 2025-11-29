from flask import Blueprint, jsonify, request

from ....工具.日志工具 import 获取日志记录器
from ....核心.总控 import 修改标签页URL排序, 获取标签页列表


日志 = 获取日志记录器(__name__)
总控蓝图 = Blueprint(
    "总控",
    __name__,
    url_prefix="/总控"
)


@总控蓝图.route("/标签页列表", methods=["GET"])
def 获取标签页列表路由():
    标签页列表: list[dict[str, str]] = 获取标签页列表()
    return jsonify(标签页列表)

@总控蓝图.route("/标签页URL排序", methods=["PUT"]) 
def 修改标签页URL排序路由():
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    if not isinstance(json, list):
        return jsonify({"错误": "配置格式错误"}), 400
    标签页URL排序: list[str] = json
    if not isinstance(标签页URL排序, list):
        return jsonify({"错误": "配置格式错误"}), 400
    修改标签页URL排序(标签页URL排序=标签页URL排序)
    return jsonify({"状态": "成功"})
