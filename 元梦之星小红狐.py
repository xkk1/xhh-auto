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
    # 导入脚本
    小红狐 = importlib.import_module("小红狐")
    # 运行脚本
    小红狐.主函数()


if __name__ == "__main__":
    主函数()
