from . import __author__, __version__
from . import __package__ as 模块名


名称: str = "小红狐自动化"  # 脚本名称，默认：__package__
简介: str = "小红狐自动化管理脚本"  # 脚本简介，默认：__doc__
作者: list[str] = [__author__]  # 脚本作者，默认：__author__
版本: str = __version__  # 脚本版本，默认：[__version__]
调试: bool = False  # 仅开启调试模式时启用脚本。默认：False
总控页面: dict[str, str] = {  # 总控页面 {URL: 标题}
    "/api/目录/小红狐/内置脚本/网站/总控.html": "总控",
}
def 配置页面(页面名: str) -> dict[str, str]:
    from .核心.页面 import 获取页面配置名
    配置名: str = 获取页面配置名(页面名)
    页面: dict[str, str] = {
        f"/api/目录/小红狐/内置脚本/网站/配置.html?页面名={页面名}&配置名={配置名}": "页面管理",
    }
    if 页面名 in ["小喾苦", "xkk1"]:
        页面.update({
            "https://www.120107.xyz": "小喾苦的个人网站",
        })
    return 页面

def 页面生成():
    ...

async def 页面操作():
    ...

def flask_route(子路径: str):
    import flask
    # 获取请求方法
    method = flask.request.method

    # 获取各种参数
    args = flask.request.args  # GET 参数
    form = flask.request.form  # POST 表单参数
    json_data = flask.request.get_json(silent=True)  # JSON 请求体，silent=True 避免解析失败报错

    所有数据 = {
        "子路径": 子路径,
        "method": method,
        "args": args,
        "form": form,
        "json_data": json_data
    }
    return flask.jsonify(所有数据), 200