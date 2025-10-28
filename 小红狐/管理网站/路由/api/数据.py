from flask import Blueprint, jsonify, request

from ....工具.日志工具 import 获取日志记录器
from ....工具.目录工具 import 数据目录
from ....工具.数据工具 import 获取本地数据, 获取内存数据


日志 = 获取日志记录器(__name__)
数据蓝图 = Blueprint(
    "数据",
    __name__,
    url_prefix="/数据"
)


# 返回内存数据 json
@数据蓝图.route("/", methods=["GET"])
def 内存数据():
    标识 = request.args.get("标识", default="")
    return jsonify(获取内存数据(标识).数据)

# 创建或更新内存数据 json
@数据蓝图.route("/", methods=["POST"])
def 创建或更新内存数据():
    标识 = request.args.get("标识", default="")
    数据 = request.get_json()
    # 检查是否成功获取到 JSON（客户端必须设置 Content-Type: application/json）
    if 数据 is None:
        return jsonify({
            "状态": "错误",
            "信息": "请发送有效的 JSON 数据，并设置 Content-Type: application/json"
        }), 400
    内存数据 = 获取内存数据(标识)
    内存数据.更新(数据)
    return jsonify(内存数据.数据)

# 返回数据目录指定存储 json 文件最新值
@数据蓝图.route("/<path:filename>", methods=["GET"])
def 本地数据(filename):
    本地数据 = 获取本地数据(数据目录 / filename)
    # 立刻保存数据
    保存 = request.args.get("保存", default=False)
    if 保存 != False:
        本地数据.保存()
    return jsonify(本地数据.数据)

# 创建或更改数据目录指定存储 json 文件最新值
@数据蓝图.route("/<path:filename>", methods=["POST"])
def 创建或更改本地数据(filename):
    数据 = request.get_json()
    # 检查是否成功获取到 JSON（客户端必须设置 Content-Type: application/json）
    if 数据 is None:
        return jsonify({
            "状态": "错误",
            "信息": "请发送有效的 JSON 数据，并设置 Content-Type: application/json"
        }), 400
    本地数据 = 获取本地数据(数据目录 / filename)
    本地数据.数据 = 数据
    # 立刻保存数据
    保存 = request.args.get("保存", default=False)
    if 保存 != False:
        本地数据.保存()
    return jsonify(本地数据.数据)

# 创建或更新数据目录指定存储 json 文件最新值
@数据蓝图.route("/<path:filename>", methods=["PUT"])
def 创建或合并本地数据(filename):
    数据 = request.get_json()
    # 检查是否成功获取到 JSON（客户端必须设置 Content-Type: application/json）
    if 数据 is None:
        return jsonify({
            "状态": "错误",
            "信息": "请发送有效的 JSON 数据，并设置 Content-Type: application/json"
        }), 400
    本地数据 = 获取本地数据(数据目录 / filename)
    本地数据.合并(数据)
    # 立刻保存数据
    保存 = request.args.get("保存", default=False)
    if 保存 != False:
        本地数据.保存()
    return jsonify(本地数据.数据)
