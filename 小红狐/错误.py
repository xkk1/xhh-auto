import datetime
import traceback
import webbrowser

from . import __package__ as 小红狐模块名
from .工具.日志工具 import 获取日志目录


HTML模板 = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ 标题 }}</title>
    <style>
        @media (prefers-color-scheme: dark) {
            :root {
                color-scheme: dark;
            }
        }
    </style>
</head>
<body>
    <pre>
{{ 错误信息 }}
    </pre>
</body>
</html>"""


def 获取错误HTML文本(错误信息: str, 标题: str) -> str:
    return HTML模板.replace("{{ 错误信息 }}", 错误信息.replace("<", "&lt;")).replace("{{ 标题 }}", 标题)

def 生成错误HTML文件(错误信息: str, 标题: str, 模块名: str):
    日志目录 = 获取日志目录(脚本模块名=模块名)
    日志目录.mkdir(parents=True, exist_ok=True)
    错误HTML = 获取错误HTML文本(错误信息=错误信息, 标题=标题)
    错误HTML文件 = 日志目录 / "错误.html"
    错误HTML文件.write_text(data=错误HTML, encoding="utf-8")
    return 错误HTML文件.resolve()

def 获取错误信息(错误: Exception, 内容: str) -> str:
    错误信息 = 内容 + str(错误)
    错误信息 += f"\n时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    if 错误.__traceback__:
        错误信息 += "\n\n详细错误信息：\n" + "".join(traceback.format_exception(type(错误), 错误, 错误.__traceback__))
    return 错误信息

def 显示错误(错误: Exception, 标题:str = "小红狐错误", 内容: str = "", 模块名: str = 小红狐模块名):
    错误信息: str = 获取错误信息(错误, 内容)
    错误HTML文件 = 生成错误HTML文件(错误信息=错误信息, 标题=标题, 模块名=模块名)
    print(错误HTML文件, str(错误HTML文件))
    if not webbrowser.open(str(错误HTML文件)):
        print("请手动打开错误HTML文件：", str(错误HTML文件))
