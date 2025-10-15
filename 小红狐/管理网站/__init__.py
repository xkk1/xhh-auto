import pathlib


网站目录 = pathlib.Path(__file__).parent.resolve()
静态文件目录 = 网站目录 / "静态文件"
模板目录 = 网站目录 / "模板"

from .网站 import 主函数
