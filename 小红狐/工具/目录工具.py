import os
from pathlib import Path


数据目录 = Path(os.environ.get("DATA_DIR", "数据")).resolve()
日志目录 = 数据目录 / "日志"

小红狐目录 = Path(__file__).parent.parent.resolve()
脚本目录 = 小红狐目录 / "脚本"
