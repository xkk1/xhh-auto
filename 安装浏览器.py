import os

# 设置一个临时环境变量指定浏览器存放目录
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.path.dirname(__file__), "浏览器")

print("正在安装浏览器...")
os.system("playwright install chromium --no-shell")
print("浏览器安装完成！")
