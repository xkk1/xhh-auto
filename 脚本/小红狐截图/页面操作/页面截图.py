import datetime
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
    页面名: str = request.args.get('页面名', None)
    if 页面名 == None:
        return 文本响应("页面名不能为空"), 400
    类型: str = request.args.get('类型', "jpeg")
    if 类型 not in ["png", "jpeg"]:
        return 文本响应("不支持的类型，仅支持 png、jpeg"), 400
    缩放: str = request.args.get('缩放', "css")
    if 缩放 not in ["css", "device"]:
        return 文本响应("不支持的缩放类型，仅支持 css、device"), 400
    全屏: bool = '全屏' in request.args
    下载: bool = '下载' in request.args

    页面状态 = 获取页面状态(页面名=页面名)
    if 页面状态 == None:
        return 文本响应(f"页面“{页面名}”未创建"), 404
    elif 页面状态 == False:
        return 文本响应(f"页面“{页面名}”手动关闭"), 404
    try:
        page = 获取页面(页面名=页面名)
        image_bytes = 异步任务管理器.运行(page.screenshot(type=类型, scale=缩放, full_page=全屏))
        # 将 bytes 包装为 BytesIO 流
        image_stream = io.BytesIO(image_bytes)
        image_stream.seek(0)  # 确保指针在开头
        return send_file(
            image_stream,
            mimetype='image/' + 类型,
            as_attachment=下载,  # 设为 True 可触发下载
            download_name=页面名 + '截图' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.' + 类型
        )
    except:
        return 获取页面(f"获取页面截图错误！\n" + traceback.format_exc()), 500
