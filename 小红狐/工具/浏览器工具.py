import pathlib
from typing import Any, Literal

from playwright.async_api import Playwright, Browser, BrowserType, BrowserContext, Page, Mouse, Keyboard
from playwright.async_api import async_playwright


async def 获取Playwright异步上下文管理器() -> Playwright:
    return await async_playwright().start()

async def 获取Playwright异步浏览器(
        异步上下文管理器: Playwright,
        浏览器类型: Literal['chromium', 'chromium_headless_shell', 'firefox', 'webkit'] = 'chromium',
        args: tuple = (), kwargs: dict[str, Any] | None = None
) -> Browser:
    if kwargs is None:
            kwargs = {}
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


class 页面类:
    def __init__(self, page: Page):
        self.page = page
        self.鼠标 = 鼠标类(self.page.mouse)
        self.键盘 = 键盘类(self.page.keyboard)

    def 置顶(self) -> None:
        """置顶页面

        将页面置于最前面（激活选项卡）

        Returns:
            None: 无返回值
        """
        return self.page.bring_to_front()
    
    def 关闭(self, 原因: str | None = None, 卸载前执行: bool | None = None) -> None:
        """关闭页面

        关闭当前页面

        Args:
            原因 (str | None): 要报告给因页面关闭而中断的作的原因。
            卸载前执行 (bool | None): 默认为 false, 不运行任何卸载处理程序并等待页面关闭，默认情况下不会在卸载处理程序之前运行。

        Returns:
            None: 无返回值
        """
        return self.page.close(reason=原因, run_before_unload=卸载前执行)
    
    def 导航(self, 网址: str, *args, **kwargs) -> None:
        """导航

        导航到新的 URL

        Args:
            网址 (str): 要导航到的网址。

        Returns:
            None: 无返回值
        """
        kwargs["url"] = 网址
        return self.page.goto(*args, **kwargs)
    
    def 刷新(self, *args, **kwargs) -> None:
        """刷新页面

        刷新当前页面

        Returns:
            None: 无返回值
        """
        return self.page.reload(*args, **kwargs)
    
    def 截图(
            self,
            区域: dict[str, float] | None = None,
            缩放: Literal['css', '设备'] | None = None,
            *args, **kwargs
    ) -> bytes:
        """截图

        返回包含捕获屏幕截图的缓冲区。
        参考：https://playwright.dev/python/docs/api/class-page#page-screenshot

        Args:
            区域 (dict[str, float] | None): 可选。指定截图的矩形区域，格式为：
                ```
                {
                    "x": float,    # 起始 X 坐标
                    "y": float,    # 起始 Y 坐标
                    "宽": float, # 区域宽度
                    "高": float # 区域高度
                }
                ```
                如果为 None，则截取整个视口
            缩放 (Literal['css', '设备'] | None): 可选。指定截图的缩放级别。
                - "css"：CSS 缩放级别（默认）
                - "设备"：设备缩放级别
        
        Returns:
            bytes
        """
        if 区域:
            kwargs["clip"] = {
                "x": 区域["x"],
                "y": 区域["y"],
                "width": 区域["宽"],
                "height": 区域["高"]
            }
        scale = {
            "css": "css",
            "设备": "device"
        }
        kwargs["scale"] = scale.get(缩放, "css")
        return self.page.screenshot(*args, **kwargs)
    
    def 设置视口大小(self, 宽度: int, 高度: int) -> None:
        """设置视口大小

        Args:
            宽度 (int): 页面宽度（以像素为单位）。
            高度 (int): 页面高度（以像素为单位）。
        
        Returns:
            None: 无返回值
        """
        return self.page.set_viewport_size({"width": 宽度, "height": 高度})
    
    def 添加初始化脚本(self, 路径: str | pathlib.Path | None = None, 脚本: str | None = None) -> None:
        """添加初始化脚本

        添加初始化脚本，在每个页面的每个导航中都会执行。
        参考：https://playwright.dev/python/docs/api/class-page#page-add-init-script
        
        Args:
            路径 (str | pathlib.Path | None): JavaScript 文件的路径。如果 path 是相对路径，则相对于当前工作目录进行解析。
            脚本 (str | None): 要在浏览器上下文中的所有页面中评估的脚本。
        
        Returns:
            None: 无返回值
        
        Example:
            >>> await page.add_init_script(path="./preload.js")
        """
        return self.page.add_init_script(path=路径, script=脚本)

class 鼠标类:
    def __init__(self, mouse: Mouse):
        self.mouse = mouse
    
    def 点击(self, x: float, y: float, 按钮: Literal['左', '中', '右'] | None = None, 点击次数: int | None = None, 延迟: float | None = None):
        """鼠标点击

        Args:
            x (float): X 相对于主框架视口的坐标（以 CSS 像素为单位）。
            y (int): Y 相对于主框架视口的坐标（以 CSS 像素为单位）。
            按钮 (Literal['左', '中', '右'] | None): 鼠标按钮，默认为 "左"。
            点击次数 (int | None): 点击次数，默认为 1。
            延迟 (float | None): 按下鼠标和鼠标向上之间的等待时间（以毫秒为单位）。默认为 0。
        
        Returns:
            None: 无返回值
        """
        return self.mouse.click(x, y, button=self._鼠标按钮转换英文(按钮)
                                , click_count=点击次数, delay=延迟)
    
    def 按下(self, 按钮: Literal['左', '中', '右'] | None = None, 点击次数: int | None = None) -> None:
        """鼠标按下

        Args:
            按钮 (Literal['左', '中', '右'] | None): 鼠标按钮，默认为 "左"。
            点击次数 (int | Non): 点击次数，默认为 1。
        
        Returns:
            None: 无返回值
        """
        return self.mouse.down(button=self._鼠标按钮转换英文(按钮), click_count=点击次数)
    
    def 抬起(self, 按钮: Literal['左', '中', '右'] | None = None, 点击次数: int | None = None) -> None:
        """鼠标抬起

        Args:
            按钮 (Literal['左', '中', '右'] | None): 鼠标按钮，默认为 "左"。
            点击次数 (int | None): 点击次数，默认为 1。
        
        Returns:
            None: 无返回值
        """
        return self.mouse.up(button=self._鼠标按钮转换英文(按钮), click_count=点击次数)

    def 移动(self, x: float, y: float, 步数: int | None = None) -> None:
        """鼠标移动

        Args:
            x (float): X 相对于主框架视口的坐标（以 CSS 像素为单位）。
            y (int): Y 相对于主框架视口的坐标（以 CSS 像素为单位）。
            步数 (int | None): 发送中间鼠标移动事件。
        
        Returns:
            None: 无返回值
        """
        return self.mouse.move(x, y, steps=步数)
    
    def 双击(self, x: float, y: float, 按钮: Literal['左', '中', '右'] | None = None, 延迟: float | None = None) -> None:
        """鼠标双击

        Args:
            x (float): X 相对于主框架视口的坐标（以 CSS 像素为单位）。
            y (int): Y 相对于主框架视口的坐标（以 CSS 像素为单位）。
            按钮 (Literal['左', '中', '右'] | None): 鼠标按钮，默认为"左"。
            延迟 (float | None): 按下鼠标和鼠标向上之间的等待时间（以毫秒为单位）。默认为 0。
        
        Returns:
            None: 无返回值
        """
        return self.mouse.dblclick(x, y, button=self._鼠标按钮转换英文(按钮), delay=延迟)
    
    def 滚动(self, x: float, y: float) -> None:
        """鼠标滚动

        Args:
            x (float): 要水平滚动的像素。
            y (float): 要垂直滚动的像素。

        Returns:
            None: 无返回值
        """
        return self.mouse.wheel(delta_x=x, delta_y=y)
    
    def _鼠标按钮转换英文(self, 按钮: Literal['左', '中', '右'] | None = None) -> Literal['left', 'middle', 'right'] | None:
        """鼠标转换按钮

        Args:
            按钮 (Literal['左', '中', '右'] | None): 鼠标按钮，默认为 "左"。

        Returns:
            Literal['left', 'middle', 'right'] | None: 鼠标按钮
        """
        match 按钮:
            case "左":
                return "left"
            case "中":
                return "middle"
            case "右":
                return "right"
            case _:
                return None

class 键盘类:
    def __init__(self, keyboard: Keyboard):
        self.keyboard = keyboard

    def 按下(self, 键: str) -> None:
        """按下按键

        按下一个键。https://playwright.dev/python/docs/api/class-keyboard#keyboard-down

        Args:
            键 (str): 要按下的键或要生成的字符的名称，例如 ArrowLeft 或 a。

        Returns:
            None: 无返回值
        """
        return self.keyboard.down(键)

    def 抬起(self, 键: str) -> None:
        """抬起按键

        抬起一个键。https://playwright.dev/python/docs/api/class-keyboard#keyboard-up

        Args:
            键 (str): 要抬起的键或要生成的字符的名称，例如 ArrowLeft 或 a。

        Returns:
            None: 无返回值
        """
        return self.keyboard.up(键)

    def 输入文本(self, 键: str) -> None:
        """输入文本

        输入一个字符串。

        Args:
            键 (str): 输入指定的文本。

        Returns:
            None: 无返回值

        Examples:
            >>> await page.keyboard.insert_text("嗨")
        """
        return self.keyboard.insert_text(键)
    
    def 按键(self, 键: str, 延迟: float = 0) -> None:
        """按一个键

        按下抬起一个键。https://playwright.dev/python/docs/api/class-keyboard#keyboard-press

        Args:
            键 (str): 要按下的键或要生成的字符的名称，例如 ArrowLeft 或 a。
            延迟 (float, optional): 按下和抬起按键之间的等待时间（以毫秒为单位）。默认为 0。

        Returns:
            None: 无返回值
        """
        return self.keyboard.press(键, delay=延迟)

    def 输入(self, 文本: str, 延迟: float | None = None) -> None:
        """为文本中的每个字符发送 按下、按键/输入 和 抬起 事件。

        输入一个键。https://playwright.dev/python/docs/api/class-keyboard#keyboard-type

        Args:
            文本 (str): 要键入焦点元素的文本。
            延迟 (float | None): 按键之间的等待时间（以毫秒为单位）。默认为 0。
            
        Returns:
            None: 无返回值
        
        Examples:
            >>> await page.keyboard.type("World", delay=100)
        """
        return self.keyboard.type(文本, delay=延迟)
