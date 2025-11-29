import asyncio
from typing import Any

import playwright.async_api

from ... import __package__ as 小红狐模块名
from ...工具.任务管理器工具 import 异步任务管理器


页面生成脚本名: str = "新建页面"
名称: str = "小红狐新建页面"


async def 异步新建页面(页面名: str) -> playwright.async_api.Page:
    from ...核心.页面 import 获取页面账号名, 获取页面初始URL
    from ...核心.浏览器 import 新建页面 as 小红狐新建页面
    账号名: str = 获取页面账号名(页面名)
    页面: playwright.async_api.Page = await 小红狐新建页面(
        页面名=页面名, 账号名=账号名, 
        kwargs上下文={"no_viewport": True, "color_scheme": "no-preference"}
    )
    # 访问目标网页
    页面初始URL: str = 获取页面初始URL(页面名)
    if 页面初始URL != "":
        await 页面.goto(页面初始URL)
    return 页面

def 新建页面(页面名: str | None = None) -> playwright.async_api.Page:
    return 异步任务管理器.运行(异步新建页面(页面名=页面名))

def 关闭页面(页面名: str | None = None):
    from ...核心.浏览器 import 关闭页面 as 小红狐关闭页面
    异步任务管理器.运行(小红狐关闭页面(页面名=页面名))

def 获取页面(页面名: str | None = None) -> playwright.async_api.Page | None:
    from ...核心.浏览器 import 获取页面 as 小红狐获取页面
    return 异步任务管理器.运行(小红狐获取页面(页面名=页面名))

def 配置页面(页面名: str) -> dict[str, str]:
    from ...核心.页面 import 获取页面配置名
    配置名: str = 获取页面配置名(页面名)
    页面: dict[str, str] = {
        f"/api/目录/小红狐/内置脚本/网站/新建页面.html?页面名={页面名}&配置名={配置名}": "页面生成",
    }
    return 页面
