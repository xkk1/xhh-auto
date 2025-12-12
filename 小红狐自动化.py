#!/usr/bin/env python3
"""
小红狐启动器
"""
import sys
import os

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 将脚本目录添加到Python路径
sys.path.insert(0, script_dir)


def 主函数():
    # 导入脚本
    import 小红狐
    # 小红狐 = importlib.import_module("小红狐")
    # 运行脚本
    小红狐.主函数()


if __name__ == "__main__":
    主函数()
