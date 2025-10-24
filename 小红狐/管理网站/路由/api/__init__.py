from flask import Blueprint

from ....工具.日志工具 import 获取日志记录器


日志 = 获取日志记录器(__name__)
api蓝图 = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


from .目录 import 目录蓝图
api蓝图.register_blueprint(目录蓝图)
from .数据 import 数据蓝图
api蓝图.register_blueprint(数据蓝图)
from .脚本 import 脚本蓝图
api蓝图.register_blueprint(脚本蓝图)
from .页面 import 页面蓝图
api蓝图.register_blueprint(页面蓝图)
