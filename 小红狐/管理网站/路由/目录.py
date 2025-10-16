from flask import Blueprint, send_from_directory

from ...工具.日志工具 import 获取日志记录器
from ...工具.目录工具 import 数据目录, 小红狐目录, 脚本目录


日志 = 获取日志记录器(__name__)
目录蓝图 = Blueprint(
    "目录",
    __name__,
    url_prefix='/目录'
)

# 返回数据目录文件
@目录蓝图.route('/数据/<path:filename>')
def 数据目录文件(filename):
    return send_from_directory(数据目录, filename)

# 返回小红狐目录文件
@目录蓝图.route('/小红狐/<path:filename>')
def 小红狐目录文件(filename):
    return send_from_directory(小红狐目录, filename)

# 返回小红狐父目录文件
@目录蓝图.route('/小红狐父/<path:filename>')
def 小红狐父目录文件(filename):
    return send_from_directory(小红狐目录.parent, filename)

# 返回脚本目录文件
@目录蓝图.route('/脚本/<path:filename>')
def 脚本目录文件(filename):
    return send_from_directory(脚本目录, filename)
