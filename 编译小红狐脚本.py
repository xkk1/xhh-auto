import compileall
from pathlib import Path
import shutil
import sys

# Path(__file__).parent
小红狐脚本包路径 = Path(".") / "小红狐"
print(f"{小红狐脚本包路径 = }")

if not 小红狐脚本包路径.exists():
    print("# 小红狐脚本包不存在，无法打包！")
    sys.exit(-1)

临时打包路径 = Path(".") / "dist" / "元梦之星小红狐" / "小红狐"
print(f"{临时打包路径 = }")

if 临时打包路径.exists():
    print("# 临时打包路径已存在，删除")
    shutil.rmtree(临时打包路径)
print("# 复制小红狐脚本包到临时打包路径")
shutil.copytree(src=小红狐脚本包路径, dst=临时打包路径)

print("# 删除 __pycache__")
for path in 临时打包路径.rglob("__pycache__"):
    print(f"删除 {path}")
    shutil.rmtree(path)

print("# 编译为 pyc")
compileall.compile_dir(dir=临时打包路径, force=True, legacy=True)

print("# 删除 *.py")
for path in 临时打包路径.rglob("*.py"):
    print(f"删除 {path}")
    path.unlink()

# print("# 打包为 zip")
# shutil.make_archive(base_name=小红狐脚本包路径, format="zip", root_dir=临时打包路径)

# print(f"# 重命名打包文件扩展名为 pyz")
# shutil.move(src=小红狐脚本包路径.with_suffix(".zip"), dst=小红狐脚本包路径.with_suffix(".pyz"))

# print("# 删除临时文件")
# shutil.rmtree(临时打包路径)

print("打包完成")
