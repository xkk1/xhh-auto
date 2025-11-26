import pathlib
from typing import Any

from playwright.async_api import Playwright, Browser, BrowserContext, Page

from ..工具.日志工具 import 获取异步日志记录器
from ..工具.浏览器工具 import 获取Playwright异步上下文管理器
from ..工具.浏览器工具 import 获取Playwright异步浏览器
from ..工具.浏览器工具 import 获取Playwright异步浏览器上下文
from ..工具.浏览器工具 import 获取Playwright异步页面
from ..核心.账号 import 获取账号浏览器存储状态文件


日志 = 获取异步日志记录器(__name__)
playwright异步上下文管理器: Playwright = None
playwright异步浏览器: Browser = None
playwright异步浏览器上下文字典: dict[str, BrowserContext] = {}
playwright异步页面字典: dict[str, Page] = {}


async def 获取上下文管理器() -> Playwright:
    global playwright异步上下文管理器
    if not playwright异步上下文管理器:
        日志.调试("初始化Playwright异步上下文管理器")
        playwright异步上下文管理器 = await 获取Playwright异步上下文管理器()
    return playwright异步上下文管理器

async def 获取浏览器(args: tuple = (), kwargs: dict[str, Any] | None = None) -> Browser:
    from .小红狐配置 import 获取浏览器类型
    global playwright异步浏览器
    if not playwright异步浏览器:
        if kwargs is None:
            kwargs = {}
        playwright异步上下文管理器 = await 获取上下文管理器()
        playwright异步浏览器 = await 获取Playwright异步浏览器(playwright异步上下文管理器, 浏览器类型=获取浏览器类型(), args=args, kwargs=kwargs)
    return playwright异步浏览器

async def 获取账号浏览器上下文(账号名: str ,args: tuple = (), kwargs: dict[str, Any] | None = None) -> BrowserContext:
    if 账号名 in playwright异步浏览器上下文字典:
        playwright异步浏览器上下文 = playwright异步浏览器上下文字典[账号名]
        if not playwright异步浏览器上下文:
            playwright异步浏览器上下文字典.pop(账号名)
        else:
            return playwright异步浏览器上下文
    if kwargs is None:
        kwargs = {}
    账号浏览器存储状态文件: pathlib.Path = 获取账号浏览器存储状态文件(账号名=账号名)
    kwargs["storage_state"] = 账号浏览器存储状态文件
    playwright异步浏览器 = await 获取浏览器()
    playwright异步浏览器上下文 = await 获取Playwright异步浏览器上下文(异步浏览器=playwright异步浏览器, args=args, kwargs=kwargs)
    playwright异步浏览器上下文字典[账号名] = playwright异步浏览器上下文
    return playwright异步浏览器上下文

async def 保存浏览器上下文账号(账号名: str, indexed_db=True):
    账号浏览器存储状态文件: pathlib.Path = 获取账号浏览器存储状态文件(账号名=账号名)
    playwright异步浏览器上下文: BrowserContext = await 获取账号浏览器上下文(账号名)
    await playwright异步浏览器上下文.storage_state(path=账号浏览器存储状态文件, indexed_db=indexed_db)

async def 获取页面(页面名: str) -> Page | None:
    if 页面名 in playwright异步页面字典:
        playwright异步页面 = playwright异步页面字典[页面名]
        if playwright异步页面.is_closed():
            playwright异步页面字典.pop(页面名)
        else:
            return playwright异步页面
    return None

async def 新建页面(
        页面名: str, 账号名: str, 
        args: tuple = (), kwargs: dict[str, Any] | None = None,
        args上下文: tuple = (), kwargs上下文: dict[str, Any] | None = None,
        ) -> Page:
    if 页面名 in playwright异步页面字典:
        playwright异步页面 = playwright异步页面字典[页面名]
        if playwright异步页面.is_closed():
            playwright异步页面字典.pop(页面名)
        else:
            await playwright异步页面.bring_to_front()
            return playwright异步页面
    if kwargs is None:
        kwargs = {}
    if kwargs上下文 is None:
        kwargs上下文 = {}
    账号浏览器上下文: BrowserContext = await 获取账号浏览器上下文(账号名=账号名, args=args上下文, kwargs=kwargs上下文)
    playwright异步页面 = await 获取Playwright异步页面(异步浏览器=账号浏览器上下文, args=args, kwargs=kwargs)
    playwright异步页面字典[页面名] = playwright异步页面
    return playwright异步页面

async def 关闭页面(页面名: str) -> None:
    if 页面名 in playwright异步页面字典:
        playwright异步页面 = playwright异步页面字典[页面名]
        if playwright异步页面 and not playwright异步页面.is_closed():
            await playwright异步页面.close()
        playwright异步页面字典.pop(页面名)

async def 关闭():
    # playwright._impl._errors.TargetClosedError
    for 页面名, playwright异步页面 in playwright异步页面字典.items():
        if playwright异步页面 and not playwright异步页面.is_closed():
            await playwright异步页面.close()
    playwright异步浏览器上下文字典.clear()
    for 账号名, playwright异步浏览器上下文 in playwright异步浏览器上下文字典.items():
        if playwright异步浏览器上下文:
            await playwright异步浏览器上下文.close()
    playwright异步浏览器上下文字典.clear()
    playwright异步页面字典.clear()
    if playwright异步浏览器:
        await playwright异步浏览器.close()
    playwright异步浏览器 = None
    if playwright异步上下文管理器:
        await playwright异步上下文管理器.close()
    playwright异步上下文管理器 = None
