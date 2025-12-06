import io
import traceback

from flask import Response, jsonify, request, send_file

from 小红狐.核心.页面 import 获取页面状态, 获取页面
from 小红狐.工具.任务管理器工具 import 异步任务管理器

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
        f"/api/目录/脚本/{模块名}/网页/页面截图.html?页面名={页面名}": "页面截图",
    }
    return 页面

def 文本响应(string: str):
    return Response(
        string,
        mimetype='text/plain',
        content_type='text/plain; charset=utf-8'  # 显式声明 charset
    )

def 路由():
    if not request.is_json:
        return 文本响应("请求头 Content-Type 必须是 application/json"), 400
    json = request.get_json(silent=True)
    if json is None:
        return 文本响应("无效的 JSON 格式，请检查请求体"), 400
    # json 为 str
    if not isinstance(json, dict):
        return 文本响应("配置格式错误"), 400
    if "页面名" not in json:
        return 文本响应("json 缺少页面名"), 400
    页面名: str = json["页面名"]
    if not isinstance(页面名, str):
        return 文本响应("页面名必须是字符串"), 400
    页面状态 = 获取页面状态(页面名=页面名)
    if 页面状态 == None:
        return 文本响应(f"页面“{页面名}”未创建"), 404
    elif 页面状态 == False:
        return 文本响应(f"页面“{页面名}”手动关闭"), 404
    try:
        page = 获取页面(页面名=页面名)
        image_bytes = 异步任务管理器.运行(page.screenshot(type="png", scale="css"))
        # 将 bytes 包装为 BytesIO 流
        image_stream = io.BytesIO(image_bytes)
        image_stream.seek(0)  # 确保指针在开头
        return send_file(
            image_stream,
            mimetype='image/png',
            as_attachment=False,  # 设为 True 可触发下载
            download_name=页面名 + '截图.png'  # Flask 2.0+
        )
    except:
        return jsonify(f"获取页面截图错误！\n" + traceback.format_exc()), 500
