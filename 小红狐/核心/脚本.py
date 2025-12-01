import importlib
import pathlib
import sys
from types import ModuleType
from typing import Any, Callable


from .. import __package__ as 小红狐模块名
from ..工具.目录工具 import 脚本目录
from ..核心.小红狐配置 import 获取调试
from ..工具.日志工具 import 获取异步日志记录器


调试 = 获取调试()
日志 = 获取异步日志记录器(__name__)


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
        "总控页面": {}, # 总控页面: dict[str, str] = {URL: 标题}
        "页面生成": {}, # 页面生成脚本: dict[str, dict[str, Any]]
        "页面操作": {}, # 页面操作脚本: dict[str, dict[str, Any]]
        "flask路由": None, # flask 路由 api
    }

    @classmethod
    def 获取脚本信息(cls, 模块: ModuleType) -> dict[str, Any]:
        信息字典: dict[str, Any] = {}
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
        # 非调试模式下删除调试模式的脚本
        if not 调试:
            # 删除调试模式的页面生成脚本
            调试页面生成脚本名列表 = []
            for 页面生成脚本名 in 信息字典["页面生成"]:
                try:
                    if 信息字典["页面生成"][页面生成脚本名]["调试"]:
                        调试页面生成脚本名列表.append(页面生成脚本名)
                except:
                    pass
            for 调试页面生成脚本名 in 调试页面生成脚本名列表:
                del 信息字典["页面生成"][调试页面生成脚本名]
            # 删除调试模式的页面操作脚本
            调试页面操作脚本名列表 = []
            for 页面操作脚本名 in 信息字典["页面操作"]:
                try:
                    if 信息字典["页面操作"][页面操作脚本名]["调试"]:
                        调试页面操作脚本名列表.append(页面操作脚本名)
                except:
                    pass
            for 调试页面操作脚本名 in 调试页面操作脚本名列表:
                del 信息字典["页面操作"][调试页面操作脚本名]
        return 信息字典
    
    def __init__(self, 模块: ModuleType, 父模块: ModuleType | None = None):
        self.模块: ModuleType = 模块
        self.父模块: ModuleType | None = 父模块
        self.脚本信息字典: dict[str, Any] = self.获取脚本信息(模块)
    
    def __getitem__(self, 键):
        return self.脚本信息字典[键]
    
    def __str__(self):
        return str(self.脚本信息字典)
    
    def __repr__(self):
        return repr(self.脚本信息字典)
    
    def 脚本信息(self) -> dict[str, Any]:
        return self.脚本信息字典
    @staticmethod
    def 获取配置页面(配置页面生成函数: Callable[..., dict[str, str]], args: tuple = (), kwargs: dict[str, Any] | None = None) -> dict[str, str]:
        if kwargs is None:
            kwargs = {}
        if not isinstance(配置页面生成函数, Callable):
            return {}
        try:
            配置页面 = 配置页面生成函数(*args, **kwargs)
            if not 配置页面:
                return {}
            if isinstance(配置页面, dict):
                for 键, 值 in 配置页面.items():
                    if not isinstance(键, str):
                        raise TypeError(f"配置页面字典的键必须为字符串，但为 {type(值)}")
                    if not isinstance(值, str):
                        raise TypeError(f"配置页面字典的值必须为字符串，但 {键} 的值为 {type(值)}")
            else:
                raise TypeError(f"配置页面必须返回字典，但返回了 {type(配置页面)}")
            return 配置页面
        except Exception as e:
            日志.警告(f"获取配置页面失败：{e}")
            return {}
    
    def 获取总控页面配置页面(self):
        return self.获取配置页面(lambda : self.脚本信息字典["总控页面"])
    
    def 获取页面生成配置页面(self, 页面生成脚本名: str, 页面名: str):
        return self.获取配置页面(
            self.脚本信息字典["页面生成"][页面生成脚本名]["配置页面"],
            kwargs={"页面名": 页面名}
        )
    
    def 获取页面操作配置页面(self, 页面操作脚本名: str, 页面名: str):
        return self.获取配置页面(
            self.脚本信息字典["页面操作"][页面操作脚本名]["配置页面"],
            kwargs={"页面名": 页面名}
        )



导入脚本信息: dict[str, 小红狐脚本信息] = {}

def 重载脚本(模块名: str) -> ModuleType:
    if 模块名 in 导入脚本信息:
        父模块 = importlib.reload(导入脚本信息[模块名].父模块)
        模块 = importlib.reload(导入脚本信息[模块名].模块)
        导入脚本信息[模块名] = 小红狐脚本信息(模块)
        return 导入脚本信息[模块名]
    else:
        raise ImportError(f"无法重载脚本：{模块名}, 脚本未导入")

def 导入脚本(模块名: str) -> 小红狐脚本信息 | None | ImportError:
    if 模块名 in 导入脚本信息:
        return 重载脚本(模块名)
    try:
        父模块 = importlib.import_module(模块名)
        模块 = importlib.import_module(模块名 + ".小红狐脚本")
        脚本信息 = 小红狐脚本信息(模块, 父模块)
        if 脚本信息["调试"] == True and not 调试:
            return None  # 仅开启调试模式时启用脚本
        导入脚本信息[模块名] = 脚本信息
        return 导入脚本信息[模块名]
    except ImportError as e:
        raise ImportError(f"无法导入脚本：{模块名}, 错误信息：{e}")

def 获取导入脚本模块名列表() -> list[str]:
    return list(导入脚本信息.keys())

def 获取导入脚本信息() -> dict[str, 小红狐脚本信息]:
    return 导入脚本信息

def 获取导入脚本信息字典() -> dict[str, dict[str], Any]:
    return {键: 值.脚本信息字典 for 键, 值 in 导入脚本信息.items()}

def 获取导入脚本信息列表() -> list[dict[str], Any]:
    return [{"模块名": 键, **值.脚本信息字典} for 键, 值 in 导入脚本信息.items()]

def 获取脚本(模块名: str) -> 小红狐脚本信息:
    if 模块名 not in 导入脚本信息:
        raise ImportError(f"无法获取脚本：{模块名}, 脚本未导入")
    return 导入脚本信息[模块名]

def 删除脚本(模块名: str) -> bool:
    if 模块名 in 导入脚本信息:
        del 导入脚本信息[模块名]
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
    模块名列表 = [模块名.name for 模块名 in 获取脚本目录().iterdir() if 模块名.is_dir() and (模块名 / "小红狐脚本.py").exists()]
    if 小红狐模块名 not in 模块名列表:
        模块名列表.insert(0, 小红狐模块名)
    return 模块名列表

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
