from flask import Blueprint, jsonify, request

from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....工具.目录工具 import 数据目录
from ....工具.数据工具 import 数据类, 获取本地数据, 获取内存数据
from ....核心 import 页面
from ....核心.页面 import 修改标签页URL排序, 修改页面生成脚本, 获取标签页URL排序, 获取页面操作自动开启脚本, 获取页面生成脚本, 获取页面配置名
from ....核心.配置 import 获取配置数据
from ....核心.脚本 import 小红狐脚本信息, 获取脚本
from ....小红狐脚本 import 默认启用页面生成脚本名


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
    页面名: str = request.json["页面名"]
    页面.新建页面(页面名)
    return jsonify({"页面名": 页面名}), 201

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
        # 失败时使用默认页面生成脚本，并修改为默认页面生成脚本
        日志.信息("使用默认页面生成脚本")
        修改页面生成脚本(页面名=页面名, 脚本模块名=小红狐模块名, 页面生成脚本名=默认启用页面生成脚本名)
        脚本模块: 小红狐脚本信息 = 获取脚本(模块名=小红狐模块名)
        标签页字典.update(脚本模块.获取页面生成配置页面(页面生成脚本名=默认启用页面生成脚本名, 页面名=页面名))
    # TODO: 实现获取当前运行脚本标签页。而不是下面
    # 获取页面操作脚本标签页字典
    页面操作自动开启脚本: dict[str, list[str]] = 获取页面操作自动开启脚本(页面名=页面名)
    for 页面操作脚本模块名, 页面操作脚本名列表 in 页面操作自动开启脚本.items():
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

@页面蓝图.route("/标签页URL排序/<page_name>", methods=["PUT"]) 
def 修改标签页URL排序路由(page_name):
    页面名: str = page_name
    # 检查请求是否为有效的 JSON
    if not request.is_json:
        return jsonify({"错误": "请求格式错误"}), 400
    标签页URL排序: list[str] = request.json
    if not isinstance(标签页URL排序, list):
        return jsonify({"错误": "配置格式错误"}), 400
    修改标签页URL排序(页面名=页面名, 标签页URL排序=标签页URL排序)
    return jsonify({"状态": "成功"})

# 给指定页面添加脚本
@页面蓝图.route("/脚本/<page_name>/<package_name>", methods=["POST"])
def 添加脚本(page_name, package_name):
    页面名: str = page_name
    配置名: str = 获取页面配置名(页面名=页面名)
    脚本模块名: str = package_name
    页面数据: 数据类 = 页面.获取页面数据(
        页面名=页面名, 脚本模块名=小红狐模块名,
        默认值={
            "启用脚本模块名": [小红狐模块名],
        })
    if 脚本模块名 not in 页面数据["启用脚本模块名"]:
        页面数据["启用脚本模块名"].append(脚本模块名)
        页面数据.保存()
        return jsonify({"状态": "成功"})
    else:
        return jsonify({"状态": "失败", "信息": "脚本已存在"})

# 删除指定页面的脚本
@页面蓝图.route("/脚本/<pagename>/<packagename>", methods=["DELETE"])
def 删除脚本(pagename, packagename):
    页面名: str = pagename
    脚本模块名: str = packagename
    页面数据: 数据类 = 页面.获取页面数据(
        页面名=页面名, 脚本模块名=小红狐模块名,
        默认值={
            "启用脚本模块名": [小红狐模块名],
        })
    if 脚本模块名 in 页面数据["启用脚本模块名"]:
        页面数据["启用脚本模块名"].remove(脚本模块名)
        页面数据.保存()
        return jsonify({"状态": "成功"})
    else:
        return jsonify({"状态": "失败", "信息": "脚本不存在"})

# 获取指定页面的脚本
@页面蓝图.route("/启用脚本模块名/<pagename>", methods=["GET"])
def 获取启用脚本模块名(pagename):
    页面名: str = pagename
    页面数据: 数据类 = 页面.获取页面数据(
        页面名=页面名, 脚本模块名=小红狐模块名,
        默认值={
            "启用脚本模块名": [小红狐模块名],
        })
    return jsonify(页面数据["启用脚本模块名"])

# 获取页面配置
@页面蓝图.route("/配置/<pagename>", methods=["GET"])
def 获取页面配置(pagename):
    页面名: str = pagename
    页面配置: str = 页面.获取页面配置(页面名=页面名)
    return jsonify({"配置": 页面配置})

# 修改页面配置
@页面蓝图.route("/配置/<pagename>", methods=["PUT"])
def 修改页面配置(pagename):
    页面名: str = pagename
    if not request.json or "配置" not in request.json:
        return jsonify({"错误": "缺少配置"}), 400
    配置: str = request.json["配置"]
    页面.修改页面配置(页面名=页面名, 配置=配置)
    return jsonify({"状态": "成功"})
