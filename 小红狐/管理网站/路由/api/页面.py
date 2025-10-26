from flask import Blueprint, jsonify, request

from .... import __package__ as 小红狐模块名
from ....工具.日志工具 import 获取日志记录器
from ....工具.目录工具 import 数据目录
from ....工具.数据工具 import 数据类, 获取本地数据, 获取内存数据
from ....核心 import 页面
from ....核心.脚本 import 小红狐脚本信息, 获取脚本


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

@页面蓝图.route("/配置页面/<pagename>", methods=["GET"])
def 获取脚本管理页面(pagename):
    页面名: str = pagename
    页面数据: 数据类 = 页面.获取页面数据(
        页面名=pagename, 脚本模块名=小红狐模块名,
        默认值={
            "启用脚本包名": [小红狐模块名],
            "配置页面URL排序": list(获取脚本(模块名=小红狐模块名).获取配置页面(页面名=页面名).keys()),
        })
    配置页面: dict[str, str] = {}
    配置页面URL排序: list[str] = 页面数据["配置页面URL排序"]
    for 包名 in 页面数据["启用脚本包名"]:
        try:
            脚本模块: 小红狐脚本信息 = 获取脚本(模块名=包名)
            配置页面.update(脚本模块.获取配置页面(页面名=页面名))
        except:
            continue
    return jsonify({"配置页面": 配置页面, "配置页面URL排序": 配置页面URL排序})

# 给指定页面添加脚本
@页面蓝图.route("/添加脚本/<pagename>/<packagename>", methods=["POST"])
def 添加脚本(pagename, packagename):
    页面名: str = pagename
    脚本模块名: str = packagename
    页面数据: 数据类 = 页面.获取页面数据(
        页面名=页面名, 脚本模块名=小红狐模块名,
        默认值={
            "启用脚本包名": [小红狐模块名],
        })
    if 脚本模块名 not in 页面数据["启用脚本包名"]:
        页面数据["启用脚本包名"].append(脚本模块名)
        页面数据.保存()
        return jsonify({"状态": "成功"})
    else:
        return jsonify({"状态": "失败", "信息": "脚本已存在"})

# 删除指定页面的脚本
@页面蓝图.route("/删除脚本/<pagename>/<packagename>", methods=["DELETE"])
def 删除脚本(pagename, packagename):
    页面名: str = pagename
    脚本模块名: str = packagename
    页面数据: 数据类 = 页面.获取页面数据(
        页面名=页面名, 脚本模块名=小红狐模块名,
        默认值={
            "启用脚本包名": [小红狐模块名],
        })
    if 脚本模块名 in 页面数据["启用脚本包名"]:
        页面数据["启用脚本包名"].remove(脚本模块名)
        页面数据.保存()
        return jsonify({"状态": "成功"})
    else:
        return jsonify({"状态": "失败", "信息": "脚本不存在"})
