from flask import Blueprint, jsonify, request

from ....工具.日志工具 import 获取日志记录器
from ....工具.目录工具 import 数据目录
from ....工具.数据工具 import 获取本地数据, 获取内存数据
from ....核心 import 页面


日志 = 获取日志记录器(__name__)
页面蓝图 = Blueprint(
    "页面",
    __name__,
    url_prefix="/页面"
)


@页面蓝图.route("/页面名", methods=["GET"])
def 获取所有页面():
    return jsonify(页面.获取全部页面名())

# 新建页面 post
@页面蓝图.route("/", methods=["POST"])
def 新建页面():
    if not request.json or "页面名" not in request.json:
        return jsonify({"错误": "缺少页面名"}), 400
    页面名 = request.json["页面名"]
    页面.新建页面(页面名)
    return jsonify({"页面名": 页面名}), 201
