import traceback
from .核心.小红狐配置 import 初始化环境变量


def 主函数():
    初始化环境变量()

    from .工具.日志工具 import 获取日志记录器
    日志 = 获取日志记录器(__name__)
    日志.信息("🚀小红狐启动中…")

    try:
        from . import 管理网站
        管理网站.主函数()
    except Exception as e:
        日志.严重(f"❌小红狐灾难性故障：{e}\n{traceback.format_exc()}")
        raise e


if __name__ == "__main__":
    主函数()
