import datetime
import io
import traceback
from urllib.parse import quote

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
        f"/api/目录/脚本/{模块名}/网页/简单远程控制.html?页面名={quote(页面名, safe="")}": "简单远程控制",
    }
    return 页面


def 文本响应(string: str):
    return Response(
        string,
        mimetype='text/plain',
        content_type='text/plain; charset=utf-8'  # 显式声明 charset
    )

def 路由(子路径: str):
    页面名: str = request.args.get('页面名', None)
    if 页面名 == None:
        return 文本响应("页面名不能为空"), 400
    
    页面状态 = 获取页面状态(页面名=页面名)
    if 页面状态 == None:
        return 文本响应(f"页面“{页面名}”未创建"), 404
    elif 页面状态 == False:
        return 文本响应(f"页面“{页面名}”手动关闭"), 404
    page = 获取页面(页面名=页面名)
    if 子路径 == "/点击":
        x: int = request.args.get('x', None, type=int)
        y: int = request.args.get('y', None, type=int)
        if x == None or y == None:
            return 文本响应("x, y 参数非法"), 400
        else:
            异步任务管理器.运行(page.mouse.click(x, y))
            return 文本响应(f"点击({x},{y})"), 200
    elif 子路径 == "/mousedown":
        x: int = request.args.get('x', None, type=int)
        y: int = request.args.get('y', None, type=int)
        if x == None or y == None:
            return 文本响应("x, y 参数非法"), 400
        else:
            异步任务管理器.运行(page.mouse.move(x, y))
            异步任务管理器.运行(page.mouse.down())
            return 文本响应(f"鼠标按下({x},{y})"), 200
    elif 子路径 == "/mouseup":
        x: int = request.args.get('x', None, type=int)
        y: int = request.args.get('y', None, type=int)
        if x == None or y == None:
            return 文本响应("x, y 参数非法"), 400
        else:
            异步任务管理器.运行(page.mouse.move(x, y))
            异步任务管理器.运行(page.mouse.up())
            return 文本响应(f"鼠标抬起({x},{y})"), 200
    elif 子路径 == "/mousemove":
        x: int = request.args.get('x', None, type=int)
        y: int = request.args.get('y', None, type=int)
        if x == None or y == None:
            return 文本响应("x, y 参数非法"), 400
        else:
            异步任务管理器.运行(page.mouse.move(x, y))
            return 文本响应(f"鼠标移动({x},{y})"), 200
    elif 子路径 == "/keydown":
        key: str = request.args.get('key', None, type=str)
        if key == None:
            return 文本响应("key 参数非法"), 400
        else:
            异步任务管理器.运行(page.keyboard.down(key))
            return 文本响应(f"按下 {key}"), 200
    elif 子路径 == "/keyup":
        key: str = request.args.get('key', None, type=str)
        if key == None:
            return 文本响应("key 参数非法"), 400
        else:
            异步任务管理器.运行(page.keyboard.up(key))
            return 文本响应(f"抬起 {key}"), 200
    elif 子路径 == "/输入":
        内容: str = request.args.get('内容', None, type=str)
        if 内容 == None:
            return 文本响应("内容参数非法"), 400
        else:
            异步任务管理器.运行(page.keyboard.insert_text(内容))
            return 文本响应(f"输入 {内容}"), 200
    elif 子路径 == "/DPR":
        DPR: float = 异步任务管理器.运行(page.evaluate("window.devicePixelRatio || 1"))
        return 文本响应(str(DPR)), 200
    return 文本响应("未知操作：" + 子路径), 404
