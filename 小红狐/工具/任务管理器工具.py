import asyncio
import time
import traceback
from typing import Dict, Callable, Optional
import threading

from .日志工具 import 获取日志记录器


日志 = 获取日志记录器(__name__)


class 异步任务管理器类:
    def __init__(self, 事件循环: asyncio.AbstractEventLoop=None, 使用全局事件循环=True):
        # 当前正在运行的任务：任务名称 → asyncio.Task
        self.正在运行的任务: Dict[str, asyncio.Task] = {}

        # asyncio 事件循环
        self.事件循环 = self.获取或创建事件循环(事件循环, 使用全局事件循环)
    
    def __del__(self):
        # 停止所有任务
        for 任务名称 in self.获取任务列表():
            self.停止任务(任务名称)
        日志.信息("已停止所有任务")

    def 获取或创建事件循环(self, 事件循环: asyncio.AbstractEventLoop, 使用全局事件循环: bool) -> asyncio.AbstractEventLoop:
        if 事件循环:
            return 事件循环
        
        if 使用全局事件循环:
            global _事件循环
            try:
                if _事件循环:
                    return _事件循环
            except NameError:
                pass
        
        try:
            # 尝试获取当前正在运行的事件循环
            事件循环 = asyncio.get_running_loop()
            日志.信息("使用当前正在运行的事件循环")
            return 事件循环
        except RuntimeError:
            # 如果没有正在运行的事件循环，则创建一个新的
            日志.信息("没有正在运行的事件循环，创建新的事件循环")
            事件循环 = asyncio.new_event_loop()
            asyncio.set_event_loop(事件循环)  # 设为当前线程默认

            def 启动事件循环(事件循环):
                日志.信息("启动事件循环")
                事件循环.run_forever()

            if 使用全局事件循环:
                global _事件循环线程
                _事件循环 = 事件循环

            _事件循环线程 = threading.Thread(target=启动事件循环, args=(事件循环,), daemon=True)
            _事件循环线程.start()
            return 事件循环

    def 启动任务(self, 任务名称: str, 异步函数: Callable[[], None], 超时=None, *args, **kwargs) -> bool:
        """
        启动一个异步任务，并确认已成功添加到事件循环。
        """

        if 任务名称 in self.正在运行的任务:
            日志.警告(f"任务 '{任务名称}' 已经在运行中")
            return False

        # 包装成一个可以被 asyncio 运行的协程
        async def 包装后的任务(*args, **kwargs):
            try:
                await 异步函数(*args, **kwargs)
            except asyncio.CancelledError:
                日志.信息(f"任务 '{任务名称}' 已被用户停止")
            except Exception as 错误:
                日志.错误(f"任务 '{任务名称}' 发生异常：{错误}\n{traceback.format_exc()}")
            日志.信息(f"任务 '{任务名称}' 已完成")

        # ✅ 使用 Event 确认任务是否成功创建
        已启动 = threading.Event()

        def 安排任务(任务名称):
            任务对象 = self.事件循环.create_task(包装后的任务(*args, **kwargs), name=任务名称)
            self.正在运行的任务[任务名称] = 任务对象
            日志.信息(f"已启动任务：'{任务名称}'")
            已启动.set()

        # 把任务调度到事件循环线程
        self.事件循环.call_soon_threadsafe(安排任务, 任务名称)

        # 等待任务真正启动
        if 超时 and (not 已启动.wait(timeout=超时)):
            日志.错误(f"任务 '{任务名称}' 启动超时")
            return False

        return True

    def 停止任务(self, 任务名称: str, 超时=None) -> bool:
        """
        停止一个正在运行的任务（通过取消 asyncio.Task），并确认已取消。
        """
        任务对象 = self.正在运行的任务.get(任务名称)
        if not 任务对象:
            日志.警告(f"任务 '{任务名称}' 未在运行")
            return False

        已停止 = threading.Event()

        def 取消任务():
            if not 任务对象.done():
                任务对象.cancel()
            日志.信息(f"已发送停止信号给任务：'{任务名称}'")
            已停止.set()

        # 调度到 loop 线程执行
        self.事件循环.call_soon_threadsafe(取消任务)
        del self.正在运行的任务[任务名称]

        # 等待确认停止
        if 超时 and (not 已停止.wait(timeout=超时)):
            日志.错误(f"任务 '{任务名称}' 停止超时")
            return False

        return True
    
    def 获取任务(self, 任务名称: str) -> Optional[asyncio.Task]:
        """
        获取一个正在运行的任务对象
        """
        if 任务名称 not in self.正在运行的任务:
            日志.警告(f"任务 '{任务名称}' 未在运行")
            return None
        return self.正在运行的任务.get(任务名称)
    
    def 获取任务列表(self):
        """
        返回所有任务的名称
        """
        return list(self.正在运行的任务.keys())

    def 获取所有任务状态(self):
        """
        返回所有任务的状态：是否正在运行
        """
        return {
            任务名称: not 任务对象.done()
            for 任务名称, 任务对象 in self.正在运行的任务.items()
        }
    
    def 获取任务状态(self, 任务名称: str):
        """
        返回指定任务的状态：是否正在运行
        """
        if 任务名称 not in self.正在运行的任务:
            日志.警告(f"任务 '{任务名称}' 未在运行")
            return False
        return not self.正在运行的任务.get(任务名称).done()

异步任务管理器 = 异步任务管理器类()

def main():
    异步任务管理器 = 异步任务管理器类()

    async def foo():
        i = 0
        while i < 10:
            i += 1
            日志.信息(f"任务1 正在运行 {i = }")
            await asyncio.sleep(1)

    if 异步任务管理器.启动任务("任务1", foo):
        日志.信息("任务1 已确认启动成功")
    if 异步任务管理器.启动任务("任务2", foo, 超时=0.001):
        日志.信息("任务2 已确认启动成功")

    time.sleep(3)

    if 异步任务管理器.停止任务("任务1", 超时=0.001):
        日志.信息("任务1 已确认停止成功")
    else:
        日志.信息("停止任务1 失败")
    del 异步任务管理器

    time.sleep(3)


if __name__ == "__main__":
    main()
