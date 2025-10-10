import os
from pathlib import Path


数据目录 = Path(os.environ.get("DATA_PATH", "数据")).resolve()
日志目录 = 数据目录 / "日志"
账号目录 = 数据目录 / "账号"
页面目录 = 数据目录 / "页面"
配置目录 = 数据目录 / "配置"
全局配置目录 = 数据目录 / "全局配置"

小红狐目录 = Path(__file__).parent.parent.resolve()
脚本目录 = 小红狐目录 / "脚本"
