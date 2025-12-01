from contextlib import redirect_stdout
import io
import traceback
from flask import jsonify, request
from .. import __package__ as 模块名

开启脚本页面名列表: list[str] = []

def 入口函数(页面名: str):
    if 页面名 in 开启脚本页面名列表:
        return
    else:
        开启脚本页面名列表.append(页面名)

def 关闭函数(页面名: str | None):
    if 页面名 in 开启脚本页面名列表:
        开启脚本页面名列表.remove(页面名)

def 脚本状态(页面名: str | None) -> bool:
    if 页面名 == None:
        return False
    elif 页面名 in 开启脚本页面名列表:
        return True

def 配置页面(页面名: str) -> dict[str, str]:
    页面: dict[str, str] = {
        f"/api/目录/脚本/{模块名}/网站/代码执行.html?页面名={页面名}": "代码执行",
    }
    return 页面

def 路由():
    if not request.is_json:
        return jsonify("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return jsonify("无效的 JSON 格式，请检查请求体"), 400
    # json 为 str
    if not isinstance(json, str):
        return jsonify("配置格式错误"), 400
    代码: str = json
    # 尝试执行代码
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(代码, {})
        结果 = f.getvalue()
        return jsonify(结果), 200
    except Exception as e:
        结果 = f.getvalue()
        return jsonify(结果 + traceback.format_exc()), 400
