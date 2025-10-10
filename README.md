# 元梦之星小红狐

## 项目介绍

## 运行环境

1. 安装 Python 3.12
2. 安装 git 克隆仓库 `https://gitee.com/xkk1/letsgo-xhh.git` 或前往 <https://gitee.com/xkk1/letsgo-xhh/repository/archive/main.zip> 下载压缩包解压，进入项目目录下
3. 安装依赖包 `python -m pip install -e .`
4. 安装 Playwright 浏览器 `python 安装浏览器.py`
5. 运行程序 `python 元梦之星小红狐.py`

可通过设置环境变量来改变运行设置：

- `DATA_PATH` 数据目录，默认为 `数据`
- `SCRIPT_PATH` 脚本目录，默认为 `小红狐/脚本`
- `PLAYWRIGHT_BROWSERS_PATH` Playwright 浏览器目录，默认为 `浏览器`，可以设置为空使用默认 Playwright 浏览器位置
- `PLAYWRIGHT_BROWSERS_TYPE` 浏览器类型，默认为 `chromium`，可选 `chromium` `firefox` `webkit`
- `PORT` 管理网站端口，默认为 `44321`
- `DEBUG` 是否开启调试模式，默认为 `False`，有且仅当为 `True` 时生效调试模式