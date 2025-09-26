#!/usr/bin/env python3
"""
元梦之星小红狐启动器
"""
import importlib
import pathlib
import sys
import os

# 预导入 方便打包识别
import logging

import playwright
import flask
import waitress

def 主函数():
    # 当前目录
    启动器目录 = pathlib.Path(__file__).parent.resolve()
    # 设置一个临时环境变量指定浏览器存放目录
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = (启动器目录 / "浏览器").as_posix()
    # 设置数据目录
    os.environ["DATA_DIR"] = (启动器目录 / "数据").as_posix()
    # 设置 Debug 模式
    os.environ["DEBUG"] = "True"
    # 导入脚本
    小红狐 = importlib.import_module("小红狐")
    # 运行脚本
    小红狐.主函数()


if __name__ == "__main__":
    主函数()
