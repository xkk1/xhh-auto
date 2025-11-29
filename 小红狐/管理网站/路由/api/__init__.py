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
from .配置 import 配置蓝图
api蓝图.register_blueprint(配置蓝图)
from .账号 import 账号蓝图
api蓝图.register_blueprint(账号蓝图)
from .总控 import 总控蓝图
api蓝图.register_blueprint(总控蓝图)
