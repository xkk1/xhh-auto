from flask import Blueprint, jsonify, request

from ....工具.日志工具 import 获取日志记录器
from ....核心.总控 import 修改标签页URL排序, 获取标签页列表, 获取脚本配置页面


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
        return jsonify("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify("无效的 JSON 格式，请检查请求体"), 400
    if not isinstance(json, list):
        return jsonify("配置格式错误"), 400
    标签页URL排序: list[str] = json
    修改标签页URL排序(标签页URL排序=标签页URL排序)
    return jsonify("成功")

# 获取指定脚本总控配置页面
@总控蓝图.route("/配置页面/<package>", methods=["GET"])
def 获取脚本配置页面路由(package: str):
    脚本模块名:str = package
    try:
        return jsonify(获取脚本配置页面(脚本模块名=脚本模块名))
    except Exception as e:
        return jsonify(f"获取脚本配置页面错误：{e}")

# 关闭浏览器
@总控蓝图.route("/关闭浏览器", methods=["GET"])
def 关闭浏览器():
    try:
        from ....核心.浏览器 import 关闭
        from ....工具.任务管理器工具 import 异步任务管理器
        异步任务管理器.运行(关闭())
        return jsonify("成功")
    except Exception as e:
        return jsonify(f"关闭浏览器错误：{e}")
