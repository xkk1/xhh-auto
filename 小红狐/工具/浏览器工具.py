import pathlib
from typing import Any, Literal

from playwright.async_api import Playwright, Browser, BrowserType, BrowserContext, Page
from playwright.async_api import async_playwright


async def 获取Playwright异步上下文管理器() -> Playwright:
    return await async_playwright().start()

async def 获取Playwright异步浏览器(
        异步上下文管理器: Playwright,
        浏览器类型: Literal['chromium', 'chromium_headless_shell', 'firefox', 'webkit'] = 'chromium',
        启动方式: Literal['launch', 'connect_over_cdp'] = 'launch',
        CDP端点URL: str = "http://127.0.0.1:9222",
        args: tuple = (), kwargs: dict[str, Any] | None = None
) -> Browser:
    if kwargs is None:
        kwargs = {}
    # 处理 CDP 连接模式
    if 启动方式 == 'connect_over_cdp':
        if 浏览器类型 not in ('chromium', 'chromium_headless_shell'):
            raise ValueError("CDP 连接仅支持 Chromium 类型浏览器")
        kwargs["endpoint_url"] = kwargs.get("endpoint_url", CDP端点URL)
        return await 异步上下文管理器.chromium.connect_over_cdp(*args, **kwargs)
    match 浏览器类型:
        case 'chromium':
            浏览器类型 = 异步上下文管理器.chromium
            kwargs["headless"] = kwargs.get("headless", False)
        case 'chromium_headless_shell':
            浏览器类型 = 异步上下文管理器.chromium
            kwargs["headless"] = kwargs.get("headless", True)
        case 'firefox':
            浏览器类型 = 异步上下文管理器.firefox
            kwargs["headless"] = kwargs.get("headless", False)
        case 'webkit':
            浏览器类型 = 异步上下文管理器.webkit
            kwargs["headless"] = kwargs.get("headless", False)
        case _:
            raise ValueError(f"不支持的浏览器类型：{浏览器类型}")
    浏览器: BrowserType = await 浏览器类型.launch(*args, **kwargs)
    return 浏览器

async def 获取Playwright异步浏览器上下文(异步浏览器: Browser, args: tuple = (), kwargs: dict[str, Any] | None = None) -> BrowserContext:
    if kwargs is None:
        kwargs = {}
    浏览器上下文 = await 异步浏览器.new_context(*args, **kwargs)
    return 浏览器上下文

async def 获取Playwright异步页面(异步浏览器: Browser | BrowserContext, args: tuple = (), kwargs: dict[str, Any] | None = None) -> Page:
    if kwargs is None:
        kwargs = {}
    异步页面 = await 异步浏览器.new_page(*args, **kwargs)
    return 异步页面
