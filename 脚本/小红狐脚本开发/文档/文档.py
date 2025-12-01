from pathlib import Path

from flask import render_template, send_from_directory


from .. import __package__ as 模块名
文档路径 = Path(__file__).parent.resolve()


def markdown路由(子路径: str):
    markdown文件路径 = 文档路径 / 子路径
    markdown模板文件 = 模块名 + "/文档/markdown模板.html"
    markdown文件名 = "文档"
    markdown内容 = """# 404 File Not Found"""
    if markdown文件路径.exists():
        markdown文件名 = markdown文件路径.name
        with markdown文件路径.open(encoding="utf-8") as f:
            markdown内容 = f.read()
    return render_template(markdown模板文件, markdown文件名=markdown文件名, markdown内容=markdown内容)

def 路由(子路径: str):
    子路径 = 子路径[1:]  # 去掉开头的 "/"
    
    文件路径 = 文档路径 / 子路径
    if not 文件路径.exists() and 子路径.endswith(".html"):
        markdown子路径 = 子路径[:-5] + ".md"
        if (文档路径 / markdown子路径).exists():
            return markdown路由(markdown子路径)
    return send_from_directory(文档路径, 子路径)
