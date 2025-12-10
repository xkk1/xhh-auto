import threading
from typing import Any, Iterable

from flask import Response, jsonify, request
import flask

from . import __package__ as 模块名


日志字典: dict[str, dict[str, list[str] | threading.Condition | int]] = {
    # "渠道名": {
    #     "内容列表": [
    #         "111",
    #         "222"
    #     ],
    #     "条件锁": threading.Condition(),
    #     "内容上限": 16,
    # }
}

def 获取渠道名列表() -> list[str]:
    return list(日志字典.keys())

def 获取渠道日志(渠道名: str = 模块名) -> dict[str, list[str] | threading.Condition | int]:
    日志字典[渠道名] = 日志字典.get(渠道名, {
        "内容列表": [],
        "条件锁": threading.Condition(),
        "内容上限": 16,
    })
    return 日志字典[渠道名]

def 获取内容上限(渠道日志: dict[str, list[str] | threading.Condition | int]) -> int:
    with 渠道日志["条件锁"]:
        return 渠道日志["内容上限"]

def 设置内容上限(渠道日志: dict[str, list[str] | threading.Condition | int], 内容上限: int):
    with 渠道日志["条件锁"]:
        渠道日志["内容上限"] = 内容上限
        if 内容上限 > 0 and len(渠道日志["内容列表"]) > 内容上限:
                渠道日志["内容列表"] = 渠道日志["内容列表"][-内容上限:]

def 获取历史日志(渠道日志: dict[str, list[str] | threading.Condition | int], 显示历史上限: int | None = None) -> list[str]:
    with 渠道日志["条件锁"]:
        if 显示历史上限 and 显示历史上限 > 0:
            return 渠道日志["内容列表"][-显示历史上限:]
        return 渠道日志["内容列表"]

def 渠道日志新增日志(日志内容: str, 渠道日志: dict[str, list[str] | threading.Condition | int]) -> None:
    with 渠道日志["条件锁"]:
        渠道日志["内容列表"].append(日志内容)
        if 渠道日志["内容上限"] > 0 and len(渠道日志["内容列表"]) > 渠道日志["内容上限"]:
            渠道日志["内容列表"] = 渠道日志["内容列表"][-渠道日志["内容上限"]:]
        渠道日志["条件锁"].notify_all()  # 唤醒所有等待的 SSE 连接
        return

def 新增日志(日志内容: str, 渠道名: str = 模块名) -> None:
    渠道日志: dict = 获取渠道日志(渠道名)
    return 渠道日志新增日志(日志内容, 渠道日志)

def 获取最新日志(渠道日志: dict[str, list[str]]) -> str | None:
    with 渠道日志["条件锁"]:
        if len(渠道日志["内容列表"]) > 0:
            return 渠道日志["内容列表"][-1]
        else:
            return None

def 字符串转SSE数据(string: str | None) -> str:
    # None 返回心跳数据
    if string is None:
        return ": ping\n\n"
    return "data: " + string.replace("\n", "\ndata: ") + "\n\n"

def 日志服务器发送事件路由():
    渠道名: str = request.args.get('渠道名', 模块名, type=str)
    设置内容上限数值: int | None = request.args.get('设置内容上限', None, type=int)
    显示历史上限数值: int | None = request.args.get('显示历史上限', None, type=int)
    渠道日志 = 获取渠道日志(渠道名)
    if 设置内容上限数值:
        设置内容上限(渠道日志, 设置内容上限数值)
    # server-sent events SSE
    def event_stream() -> Iterable[str]:
        for 日志内容 in 获取历史日志(渠道日志, 显示历史上限数值):
            yield 字符串转SSE数据(日志内容)
        while True:
            with 渠道日志["条件锁"]:
                # 等待直到日志更新 或 超时（用于心跳）
                if not 渠道日志["条件锁"].wait(timeout=16):  # 16 秒超时发心跳
                    yield ": ping\n\n"
                    continue
                yield 字符串转SSE数据(获取最新日志(渠道日志))
                continue
    return Response(event_stream(), mimetype="text/event-stream")

def 获取渠道名列表路由():
    return jsonify(获取渠道名列表())

def 获取最新日志路由():
    渠道名: str = request.args.get('渠道名', 模块名, type=str)
    return jsonify(获取最新日志(获取渠道日志(渠道名)))

def 获取历史日志路由():
    渠道名: str = request.args.get('渠道名', 模块名, type=str)
    显示历史上限数值: int | None = request.args.get('显示历史上限', None, type=int)
    渠道日志 = 获取渠道日志(渠道名)
    return jsonify(获取历史日志(渠道日志, 显示历史上限数值))

def 获取内容上限路由():
    渠道名: str = request.args.get('渠道名', 模块名, type=str)
    渠道日志 = 获取渠道日志(渠道名)
    return jsonify(获取内容上限(渠道日志))

def 设置内容上限路由():
    请求方法 = flask.request.method
    if 请求方法 == "GET":
        渠道名: str = request.args.get('渠道名', 模块名, type=str)
        设置内容上限数值: int | None = request.args.get('设置内容上限', None, type=int)
    elif 请求方法 == "POST":
        数据 = request.get_json(silent=True)
        渠道名: str = 数据.get('渠道名', 模块名, type=str)
        设置内容上限数值: int | None = 数据.get('设置内容上限', None, type=int)
    else:
        return jsonify("请求方法错误"), 400
    渠道日志 = 获取渠道日志(渠道名)
    设置内容上限(渠道日志, 设置内容上限数值)
    return jsonify("成功"), 200

def 新增日志路由():
    请求方法 = flask.request.method
    if 请求方法 == "GET":
        渠道名: str = request.args.get('渠道名', 模块名, type=str)
        内容: str = request.args.get('内容', type=str)
    elif 请求方法 == "POST":
        数据 = request.get_json(silent=True)
        渠道名: str = 数据.get('渠道名', 模块名, type=str)
        内容: str = 数据.get('内容', type=str)
    else:
        return jsonify("请求方法错误"), 400
    if not 内容:
        return jsonify("内容不能为空"), 400
    新增日志(内容, 渠道名)
    return jsonify("成功"), 200
