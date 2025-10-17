# 小红狐

## 项目介绍

## 运行环境

1. 安装 Python 3.12
2. 安装 git 克隆仓库 `https://gitee.com/xkk1/xhh-auto.git` 或前往 <https://gitee.com/xkk1/xhh-auto/repository/archive/main.zip> 下载压缩包解压，进入项目目录下
3. 安装依赖包 `python -m pip install -e .`
4. 安装 Playwright 浏览器 `python 安装浏览器.py`
5. 运行程序 `python 小红狐自动化.py`

可通过设置环境变量来改变运行设置：

- `DATA_PATH` 数据目录，默认为 `数据`，以下配置可通过修改数据目录下的 `小红狐.json` 文件修改
- `SCRIPT_PATH` 脚本目录，默认为 `小红狐/脚本`
- `PLAYWRIGHT_BROWSERS_PATH` Playwright 浏览器目录，默认为 `浏览器`，可以设置为空使用默认 Playwright 浏览器位置
- `PLAYWRIGHT_BROWSERS_TYPE` 浏览器类型，默认为 `chromium`，可选 `chromium` `firefox` `webkit`
- `MANAGE_SITE_PORT` 管理网站端口，默认为 `44321`
- `MANAGE_SITE_AUTO_OPEN_BROWSER` 是否自动在浏览器打开管理网站，默认为 `True`
- `MANAGE_SITE_AUTO_OPEN_DELAY` 自动打开浏览器的延迟时间，默认为 `1`，单位秒
- `MANAGE_SITE_ROOT_REDIRECT_URL` 管理网站根目录重定向地址，默认为 `/小红狐.html`
- `DEBUG` 是否开启调试模式，默认为 `False`，设置为 `True` 时生效调试模式
