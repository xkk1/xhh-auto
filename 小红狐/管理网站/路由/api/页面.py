from typing import Any, Callable
from flask import Blueprint, jsonify, request

from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....核心 import 页面
from ....核心.页面 import 修改标签页URL排序, 修改页面生成脚本, 修改页面账号名, 修改页面配置名, 关闭页面操作脚本, 删除页面操作自动开启脚本, 开启页面操作脚本, 添加页面操作自动开启脚本, 获取标签页URL排序, 获取页面操作开启脚本, 获取页面操作自动开启脚本, 获取页面生成脚本, 获取页面账号名, 获取页面配置名
from ....核心.脚本 import 小红狐脚本信息, 获取导入脚本信息字典, 获取脚本
from ....小红狐脚本 import 默认启用页面生成脚本名
from .脚本 import 标准化


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
@页面蓝图.route("/页面名", methods=["POST"])
def 新建页面():
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    # json 为 str
    if not isinstance(json, str):
        return jsonify({"错误": "配置格式错误"}), 400
    页面名: str = json
    页面.新建页面(页面名)
    return jsonify({"状态": "成功"}), 200

@页面蓝图.route("/标签页列表/<page_name>", methods=["GET"])
def 获取标签页列表路由(page_name):
    页面名: str = page_name

    标签页字典: dict[str, str] = {}
    # 页面生成脚本标签页字典
    页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
    try:
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
        标签页字典.update(脚本模块.获取页面生成配置页面(页面生成脚本名=页面生成脚本["页面生成脚本名"], 页面名=页面名))
    except:
        pass
    # # TODO: 实现获取当前运行脚本标签页。而不是下面
    # # 获取页面操作脚本标签页字典
    # 页面操作自动开启脚本: dict[str, list[str]] = 获取页面操作自动开启脚本(页面名=页面名)
    # for 页面操作脚本模块名, 页面操作脚本名列表 in 页面操作自动开启脚本.items():
    #     try:
    #         脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面操作脚本模块名)
    #         for 页面操作脚本名 in 页面操作脚本名列表:
    #             try:
    #                 标签页字典.update(脚本模块.获取页面操作配置页面(页面操作脚本名=页面操作脚本名, 页面名=页面名))
    #             except:
    #                 日志.警告(f"获取页面操作脚本“{页面操作脚本模块名}”页面“{页面名}”失败: {e}")
    #     except Exception as e:
    #         日志.警告(f"获取页面操作脚本“{页面操作脚本模块名}”失败: {e}")
    # 获取当前开启脚本的标签页
    页面操作开启脚本: dict[str, list[str]] = 获取页面操作开启脚本(页面名=页面名)
    for 页面操作脚本模块名, 页面操作脚本名列表 in 页面操作开启脚本.items():
        try:
            脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面操作脚本模块名)
            for 页面操作脚本名 in 页面操作脚本名列表:
                try:
                    标签页字典.update(脚本模块.获取页面操作配置页面(页面操作脚本名=页面操作脚本名, 页面名=页面名))
                except:
                    日志.警告(f"获取页面操作脚本“{页面操作脚本模块名}”页面“{页面名}”失败: {e}")
        except Exception as e:
            日志.警告(f"获取页面操作脚本“{页面操作脚本模块名}”失败: {e}")

    标签页URL排序: list[str] = 获取标签页URL排序(页面名=页面名)
    标签页列表: list[dict[str, str]] = []
    for 标签页URL in 标签页URL排序:
        if 标签页URL in 标签页字典:
            标签页列表.append({
                "url": 标签页URL,
                "标题": 标签页字典[标签页URL],
            })
            标签页字典.pop(标签页URL)
    for 标签页URL, 标签页标题 in 标签页字典.items():
        标签页列表.append({
            "url": 标签页URL,
            "标题": 标签页标题,
        })
    return jsonify(标签页列表)


@页面蓝图.route("/页面操作开启脚本/<page_name>", methods=["GET"])
def 获取页面操作开启脚本路由(page_name):
    页面名: str = page_name
    页面操作开启脚本: dict[str, list[str]] = 获取页面操作开启脚本(页面名=页面名)
    return jsonify(页面操作开启脚本)

@页面蓝图.route("/标签页URL排序/<page_name>", methods=["PUT"]) 
def 修改标签页URL排序路由(page_name):
    页面名: str = page_name
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
    修改标签页URL排序(页面名=页面名, 标签页URL排序=标签页URL排序)
    return jsonify({"状态": "成功"})

# 给指定页面添加页面操作自动开启脚本
@页面蓝图.route("/页面操作自动开启脚本/<page_name>", methods=["POST"])
def 添加页面操作自动开启脚本路由(page_name):
    页面名: str = page_name
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    if "脚本模块名" not in json:
        return jsonify({"错误": "缺少脚本模块名"}), 400
    脚本模块名: str = json["脚本模块名"]
    if "页面操作脚本名" not in json:
        return jsonify({"错误": "缺少页面操作脚本名"}), 400
    页面操作脚本名: str = request.json["页面操作脚本名"]
    添加页面操作自动开启脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)
    return jsonify({"状态": "成功"})

# 删除指定页面的页面操作自动开启脚本
@页面蓝图.route("/页面操作自动开启脚本/<page_name>/<package_name>/<page_script_name>", methods=["DELETE"])
def 删除页面操作自动开启脚本路由(page_name, package_name, page_script_name):
    页面名: str = page_name
    脚本模块名: str = package_name
    页面操作脚本名: str = page_script_name
    删除页面操作自动开启脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)
    return jsonify({"状态": "成功"})

@页面蓝图.route("/页面操作/配置页面/<page_name>/<package_name>/<page_script_name>", methods=["GET"])
def 获取页面操作配置页面路由(page_name, package_name, page_script_name):
    页面名: str = page_name
    脚本模块名: str = package_name
    页面操作脚本名: str = page_script_name
    try:
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=脚本模块名)
        return jsonify(脚本模块.获取页面操作配置页面(页面操作脚本名=页面操作脚本名, 页面名=页面名))
    except Exception as e:
        日志.警告(f"获取页面操作配置页面失败，页面：“{页面名}”，脚本模块名：“{脚本模块名}”，页面操作脚本名“{页面操作脚本名}”: {e}")
        return jsonify({})

@页面蓝图.route("/页面生成/配置页面/<page_name>/<package_name>/<page_script_name>", methods=["GET"])
def 获取页面生成配置页面路由(page_name, package_name, page_script_name):
    页面名: str = page_name
    脚本模块名: str = package_name
    页面生成脚本名: str = page_script_name
    try:
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=脚本模块名)
        return jsonify(脚本模块.获取页面生成配置页面(页面生成脚本名=页面生成脚本名, 页面名=页面名))
    except Exception as e:
        日志.警告(f"获取页面生成置页面失败，页面：“{页面名}”，脚本模块名：“{脚本模块名}”，页面生成脚本名“{页面生成脚本名}”: {e}")
        return jsonify({})

# 获取指定页面的页面操作自动开启脚本
@页面蓝图.route("/页面操作自动开启脚本/<page_name>", methods=["GET"])
def 获取页面操作自动开启脚本路由(page_name):
    页面名: str = page_name
    return jsonify(获取页面操作自动开启脚本(页面名=页面名))

# 获取页面配置
@页面蓝图.route("/配置名/<page_name>", methods=["GET"])
def 获取页面配置名路由(page_name):
    页面名: str = page_name
    页面配置: str = 获取页面配置名(页面名=页面名)
    return jsonify(页面配置)

# 修改页面配置
@页面蓝图.route("/配置名/<page_name>", methods=["PUT"])
def 修改页面配置名路由(page_name):
    页面名: str = page_name
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    # json 为 str
    if not isinstance(json, str):
        return jsonify({"错误": "配置格式错误"}), 400
    配置: str = json
    修改页面配置名(页面名=页面名, 配置名=配置)
    return jsonify({"状态": "成功"})

# 获取页面生成脚本
@页面蓝图.route("/页面生成脚本/<page_name>", methods=["GET"])
def 获取页面生成脚本路由(page_name):
    页面名: str = page_name
    页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
    return jsonify(页面生成脚本)

# 修改页面生成脚本
@页面蓝图.route("/页面生成脚本/<page_name>", methods=["PUT"])
def 修改页面生成脚本路由(page_name):
    页面名: str = page_name
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    if "脚本模块名" not in json:
        return jsonify({"错误": "缺少脚本模块名"}), 400
    脚本模块名: str = json["脚本模块名"]
    if "页面生成脚本名" not in json:
        return jsonify({"错误": "缺少页面生成脚本名"}), 400
    页面生成脚本名: str = json["页面生成脚本名"]
    修改页面生成脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面生成脚本名=页面生成脚本名)
    return jsonify({"状态": "成功"})

@页面蓝图.route("/开启页面操作脚本/<page_name>/<package_name>/<page_script_name>", methods=["GET"])
def 开启页面操作脚本路由(page_name, package_name, page_script_name):
    页面名: str = page_name
    脚本模块名: str = package_name
    页面操作脚本名: str = page_script_name
    try:
        return jsonify(标准化(开启页面操作脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)))
    except Exception as e:
        日志.警告(f"开启页面操作脚本失败，页面：“{页面名}”，脚本模块名：“{脚本模块名}”，页面操作脚本名“{页面操作脚本名}”: {e}")
        return jsonify({"错误": "开启页面操作脚本失败", "信息": str(e)}), 500

@页面蓝图.route("/关闭页面操作脚本/<page_name>/<package_name>/<page_script_name>", methods=["GET"])
def 关闭页面操作脚本路由(page_name, package_name, page_script_name):
    页面名: str = page_name
    脚本模块名: str = package_name
    页面操作脚本名: str = page_script_name
    try:
        return jsonify(标准化(关闭页面操作脚本(页面名=页面名, 脚本模块名=脚本模块名, 页面操作脚本名=页面操作脚本名)))
    except Exception as e:
        日志.警告(f"关闭页面操作脚本失败，页面：“{页面名}”，脚本模块名：“{脚本模块名}”，页面操作脚本名“{页面操作脚本名}”: {e}")
        return jsonify({"错误": "关闭页面操作脚本失败", "信息": str(e)}), 500

@页面蓝图.route("/账号名/<page_name>", methods=["GET"])
def 获取页面账号名路由(page_name):
    页面名: str = page_name
    账号名: str = 获取页面账号名(页面名=页面名)
    return jsonify(账号名)

# 修改
@页面蓝图.route("/账号名/<page_name>", methods=["PUT"])
def 修改页面账号名路由(page_name):
    页面名: str = page_name
    if not request.is_json:
        return jsonify({"错误": "请求头 Content-Type 必须是 application/json"}), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify({"错误": "无效的 JSON 格式，请检查请求体"}), 400
    if not isinstance(json, str):
        return jsonify({"错误": "必须是字符串"}), 400
    账号名: str = json
    修改页面账号名(页面名=页面名, 账号名=账号名)
    return jsonify({"状态": "成功"})

@页面蓝图.route("/新建页面/<page_name>", methods=["GET"])
def 新建页面路由(page_name):
    页面名: str = page_name
    try:
        页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
        脚本模块["页面生成"][页面生成脚本["页面生成脚本名"]]["新建页面"](页面名=页面名)
        return jsonify({"状态": "成功"})
    except Exception as e:
        日志.警告(f"打开页面失败，页面名：{页面名}: {e}")
        return jsonify({"错误": "打开页面失败", "信息": e}), 500

# 关闭页面
@页面蓝图.route("/关闭页面/<page_name>", methods=["GET"])
def 关闭页面路由(page_name):
    页面名: str = page_name
    try:
        页面生成脚本: dict[str, str] = 获取页面生成脚本(页面名=页面名)
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=页面生成脚本["脚本模块名"])
        脚本模块["页面生成"][页面生成脚本["页面生成脚本名"]]["关闭页面"](页面名=页面名)
        return jsonify({"状态": "成功"})
    except Exception as e:
        日志.警告(f"关闭页面失败，页面名：{页面名}: {e}")
        return jsonify({"错误": "关闭页面失败", "信息": e}), 500
