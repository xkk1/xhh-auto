def 初始化小红狐():
    from .核心.小红狐配置 import 初始化小红狐配置
    初始化小红狐配置()
    from .核心.脚本 import 初始化脚本
    初始化脚本()

def 主函数():
    初始化小红狐()

    from .工具.日志工具 import 获取日志记录器
    日志 = 获取日志记录器(__name__)
    日志.信息("🚀小红狐启动中…")

    try:
        from .核心 import 脚本
        日志.信息(f"加载所有脚本")
        脚本.加载所有脚本()
        日志.信息(f"导入脚本模块名列表：{脚本.获取导入脚本模块名列表()}")

        from . import 管理网站
        管理网站.主函数()
    except Exception as e:
        import traceback
        日志.严重(f"❌小红狐灾难性故障：{e}\n{traceback.format_exc()}")
        from . import 错误
        错误.显示错误(错误=e, 标题="小红狐灾难性故障", 内容="小红狐灾难性故障！\n错误信息：")
        raise e


if __name__ == "__main__":
    主函数()
