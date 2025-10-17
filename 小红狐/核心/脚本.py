import importlib
import pathlib
import sys
from types import ModuleType
from typing import Any

from ..工具.目录工具 import 脚本目录


def 初始化脚本():
    # 将脚本目录添加到系统路径中
    if str(脚本目录) not in sys.path:
        sys.path.append(str(脚本目录))


class 小红狐脚本信息:
    class 脚本默认替换变量:
        def __init__(self, 替换表达式: str):
            self.替换表达式 = 替换表达式
        def 值(self, 脚本模块) -> Any:
            try:
                return eval(self.替换表达式)
            except:
                return None
    
    小红狐脚本信息字典: dict[str, Any] = {
        "模块": 脚本默认替换变量("脚本模块"),  # 脚本模块
        "路径": 脚本默认替换变量("pathlib.Path(脚本模块.__file__).parent"),  # 脚本路径
        "名称": 脚本默认替换变量("脚本模块.__package__"),  # 脚本名称
        "简介": 脚本默认替换变量("脚本模块.__doc__"),  # 脚本简介
        "作者": 脚本默认替换变量("脚本模块.__author__"),  # 脚本作者
        "版本": 脚本默认替换变量("[脚本模块.__version__]"),  # 脚本版本
        "调试": False, # 仅开启调试模式时启用脚本
        "总控URL": None, # 总控 URL
        "配置URL": None, # 配置 URL
        "flask_route": None, # flask 路由 api
        "页面生成": None, # 页面生成同步函数
        "页面操作": None, # 页面操作异步函数
    }

    @classmethod
    def 获取脚本信息(cls, 模块: ModuleType) -> dict[str, Any]:
        信息字典 = {}
        for 键, 值 in cls.小红狐脚本信息字典.items():
            if hasattr(模块, 键):
                信息字典[键] = getattr(模块, 键)
            elif isinstance(值, cls.脚本默认替换变量):
                信息字典[键] = 值.值(模块)
            else:
                信息字典[键] = 值
        for 键 in dir(模块):
            if not 键.startswith("_") and (键 not in cls.小红狐脚本信息字典):
                信息字典[键] = getattr(模块, 键)
        return 信息字典
    
    def __init__(self, 模块: ModuleType):
        self.模块 = 模块
        self.脚本信息字典 = self.获取脚本信息(模块)
    
    def __getitem__(self, 键):
        return self.脚本信息字典[键]
    
    def __str__(self):
        return str(self.脚本信息字典)
    
    def __repr__(self):
        return repr(self.脚本信息字典)
    
    def 脚本信息(self) -> dict[str, Any]:
        return self.脚本信息字典


导入脚本信息字典: dict[str, 小红狐脚本信息] = {}

def 重载脚本(模块名: str) -> ModuleType:
    if 模块名 in 导入脚本信息字典:
        模块 = importlib.reload(导入脚本信息字典[模块名].模块)
        导入脚本信息字典[模块名] = 小红狐脚本信息(模块)
        return 导入脚本信息字典[模块名]
    else:
        raise ImportError(f"无法重载脚本：{模块名}, 脚本未导入")

def 导入脚本(模块名: str) -> ModuleType:
    if 模块名 in 导入脚本信息字典:
        return 重载脚本(模块名)
    try:
        模块 = importlib.import_module(模块名 + ".小红狐脚本")
        导入脚本信息字典[模块名] = 小红狐脚本信息(模块)
        return 导入脚本信息字典[模块名]
    except ImportError as e:
        raise ImportError(f"无法导入脚本：{模块名}, 错误信息：{e}")

def 获取导入脚本模块名列表() -> list[str]:
    return list(导入脚本信息字典.keys())

def 获取脚本(模块名: str) -> 小红狐脚本信息:
    return 导入脚本信息字典[模块名]

def 删除脚本(模块名: str) -> bool:
    if 模块名 in 导入脚本信息字典:
        del 导入脚本信息字典[模块名]
        return True
    else:
        return False

def 获取脚本目录(模块名: str | None = None) -> pathlib.Path:
    if 模块名:
        return 脚本目录 / 模块名
    else:
        return 脚本目录

def 获取脚本目录所有模块名() -> list[str]:
    """
    获取脚本目录下的所有模块名，模块是目录且有“小红狐脚本.py” 文件
    """
    return ["小红狐"] + [模块名.name for 模块名 in 获取脚本目录().iterdir() if 模块名.is_dir() and (模块名 / "小红狐脚本.py").exists()]

加载脚本错误信息字典: dict[str, ImportError] = {}

def 加载所有脚本() -> dict[str, ImportError]:
    # 错误信息字典: dict[str, ImportError] = {}
    加载脚本错误信息字典.clear()
    for 模块名 in 获取脚本目录所有模块名():
        try:
            导入脚本(模块名)
        except ImportError as e:
            加载脚本错误信息字典[模块名] = e
    return 加载脚本错误信息字典

def 获取加载脚本错误信息字典() -> dict[str, ImportError]:
    return 加载脚本错误信息字典
