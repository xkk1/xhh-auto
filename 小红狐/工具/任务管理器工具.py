import asyncio
import time
import traceback
from typing import Any, Coroutine, Dict, Callable, Optional
import threading

from .日志工具 import 获取日志记录器


日志 = 获取日志记录器(__name__)


class 异步任务管理器类:
    def __init__(self, 事件循环: asyncio.AbstractEventLoop = None, 使用全局事件循环 = True):
        # 任务字典：任务名称 → asyncio.Task
        self.任务字典: Dict[str, asyncio.Task] = {}
        self.任务结果字典: Dict[str, Any] = {}

        # asyncio 事件循环
        self.事件循环 = self.获取或创建事件循环(事件循环, 使用全局事件循环)
    
    def __del__(self):
        # 停止并删除所有任务
        self.停止所有任务(删除任务=True)
        # 停止事件循环
        self.事件循环.close()

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

    def 启动任务(
            self,
            任务名称: str, 协程: Coroutine,
            超时: float | None = None
        ) -> bool:
        """
        启动一个异步任务，并确认已成功添加到事件循环。
        """

        if 任务名称 in self.任务字典:
            日志.警告(f"任务 '{任务名称}' 已经存在")
            return False
    
        # 包装成一个可以被 asyncio 运行的协程
        async def 包装后的任务():
            try:
                self.任务结果字典[任务名称] = await 协程
            except asyncio.CancelledError:
                日志.信息(f"任务 '{任务名称}' 已被用户停止")
            except Exception as 错误:
                日志.错误(f"任务 '{任务名称}' 发生异常：{错误}\n{traceback.format_exc()}")
            日志.信息(f"任务 '{任务名称}' 已完成")

        # ✅ 使用 Event 确认任务是否成功创建
        已启动 = threading.Event()

        def 安排任务(任务名称):
            任务对象 = self.事件循环.create_task(包装后的任务(), name=任务名称)
            self.任务字典[任务名称] = 任务对象
            日志.信息(f"已启动任务：'{任务名称}'")
            已启动.set()

        # 把任务调度到事件循环线程
        self.事件循环.call_soon_threadsafe(安排任务, 任务名称)

        # 等待任务真正启动
        if 超时 and (not 已启动.wait(timeout=超时)):
            日志.错误(f"任务 '{任务名称}' 启动超时")
            return False

        return True
    
    def 启动异步函数任务(
            self,
            任务名称: str, 异步函数: Callable[..., None],
            args: tuple = (), kwargs: dict[str, Any] | None = None,
            超时: float | None = None
        ) -> bool:
        """
        启动一个异步任务，并确认已成功添加到事件循环。
        """
        if kwargs is None:
            kwargs = {}
        协程: Coroutine = 异步函数(*args, **kwargs)
        return self.启动任务(任务名称, 协程, 超时)

    def 停止任务(self, 任务名称: str, 超时: float | None = None, 删除任务: bool = False) -> bool:
        """
        停止一个任务字典里的任务（通过取消 asyncio.Task），并确认已取消。
        """
        if not self.获取任务状态(任务名称=任务名称):
            任务对象: asyncio.Task = self.任务字典.get(key=任务名称, default=None)
            if not 任务对象:
                日志.警告(f"任务 '{任务名称}' 不存在")
                return False

            已停止 = threading.Event()

            def 取消任务():
                if not 任务对象.done():
                    任务对象.cancel()
                日志.信息(f"已发送停止信号给任务：'{任务名称}'")
                已停止.set()

            # 调度到 loop 线程执行
            self.事件循环.call_soon_threadsafe(取消任务)

            # 等待确认停止
            if 超时 and (not 已停止.wait(timeout=超时)):
                日志.错误(f"任务 '{任务名称}' 停止超时")
                return False
        
        if 删除任务:
            del self.任务字典[任务名称]
            self.任务结果字典.pop(任务名称, None)

        return True
    
    def 删除任务(self, 任务名称: str):
        """
        删除一个任务字典里的任务
        """
        if 任务名称 not in self.任务字典:
            日志.警告(f"任务 '{任务名称}' 不存在")
            return False
        self.停止任务(任务名称=任务名称, 删除任务=True)
        return True
    
    def 停止所有任务(self, 超时: float | None = None, 删除任务: bool = False):
        """
        停止所有任务
        """
        for 停止任务名称 in self.获取任务名称元组():
            self.停止任务(任务名称=停止任务名称, 超时=超时, 删除任务=删除任务)
        日志.信息("已停止所有任务")
    
    def 获取任务(self, 任务名称: str) -> Optional[asyncio.Task]:
        """
        获取一个任务字典里的任务对象
        """
        if 任务名称 not in self.任务字典:
            日志.警告(f"任务 '{任务名称}' 不存在")
            return None
        return self.任务字典.get(任务名称)
    
    def 获取任务名称元组(self) -> tuple[str, ...]:
        """
        返回所有任务字典里任务的名称
        """
        return tuple(self.任务字典.keys())

    def 获取所有任务状态(self):
        """
        返回所有任务字典里任务的状态：是否正在运行
        """
        return {
            任务名称: not 任务对象.done()
            for 任务名称, 任务对象 in self.任务字典.items()
        }
    
    def 获取任务状态(self, 任务名称: str) -> bool | None:
        """
        返回指定任务的状态：是否正在运行

        Returns:
            bool | None: 任务状态 true 运行 false 停止，None 表示任务不存在
        """
        if 任务名称 not in self.任务字典:
            日志.警告(f"任务 '{任务名称}' 不存在")
            return None
        return not self.任务字典.get(任务名称).done()
    
    def 获取任务结果(self, 任务名称: str, 默认: Any = None) -> Any:
        """
        获取一个任务字典里任务的结果
        """
        if 任务名称 not in self.任务结果字典:
            日志.警告(f"任务 '{任务名称}' 不存在")
            return 默认
        return self.任务结果字典.get(任务名称, 默认)

    def 运行(self, 协程: Coroutine):
        # 在运行中的事件循环中安全地运行协程并获取结果
        future = asyncio.run_coroutine_threadsafe(协程, self.事件循环)
        return future.result()  # 阻塞当前线程，直到协程完成并返回结果


异步任务管理器 = 异步任务管理器类()

def main():
    异步任务管理器 = 异步任务管理器类()

    async def foo():
        i = 0
        while i < 10:
            i += 1
            日志.信息(f"任务1 正在运行 {i = }")
            await asyncio.sleep(1)

    if 异步任务管理器.启动任务("任务1", foo()):
        日志.信息("任务1 已确认启动成功")
    if 异步任务管理器.启动异步函数任务("任务2", foo, 超时=0.001):
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
