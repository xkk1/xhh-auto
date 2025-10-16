import atexit
import copy
import json
import pathlib
from typing import Any


class 数据类:
    def __init__(self, 默认值: dict[str, Any] | None = None, 路径: pathlib.Path | str | None = None):
        self.默认值: dict | None = 默认值
        self.数据: dict = copy.deepcopy(self.默认值) if 默认值 else {}
        self.路径: pathlib.Path | str | None = 路径
        self.加载()
        if self.路径:
            atexit.register(self.保存)  # 注册退出时保存
    
    def 加载(self) -> None:
        # 加载数据
        if (not self.路径 is None) and (pathlib.Path(self.路径).exists()):
            with open(self.路径, "r", encoding="utf-8") as 文件:
                新数据 = json.load(文件)
                if self.默认值:
                    self.数据 = self.合并字典(self.默认值, 新数据)
                else:
                    self.数据 = 新数据

    def 合并字典(self, 默认值, 新数据) -> dict:
        """递归合并字典"""
        if isinstance(默认值, dict) and isinstance(新数据, dict):
            合并结果 = 默认值.copy()
            for k, v in 新数据.items():
                if k in 合并结果:
                    合并结果[k] = self.合并字典(合并结果[k], v)  # 递归合并
                else:
                    合并结果[k] = v
            return 合并结果
        return 新数据
    
    def 保存(self) -> None:
        # 保存数据
        if self.路径 is None:
            return
        if not pathlib.Path(self.路径).parent.exists():
            pathlib.Path(self.路径).parent.mkdir(parents=True)
        with open(self.路径, "w", encoding="utf-8") as 文件:
            json.dump(self.数据, 文件, ensure_ascii=False, indent=4)

    def 更新(self, 数据: dict[str, Any]) -> None:
        self.数据.update(数据)

    def __del__(self):
        # 析构函数
        try:
            self.保存()
        except Exception:
            pass  # 忽略 Python 解释器关机时的异常

    def __getitem__(self, 键) -> Any:
        # 获取值
        return self.数据[键]

    def __setitem__(self, 键, 值) -> None:
        # 设置值
        self.数据[键] = 值
    
    def __delitem__(self, 键) -> None:
        # 删除键
        del self.数据[键]
    
    def __contains__(self, 键) -> bool:
        # 判断键是否存在
        return 键 in self.数据

    def __len__(self) -> int:
        # 获取长度
        return len(self.数据)
    
    def __str__(self) -> str:
        # 转换为字符串
        return str(self.数据)
    
    def __repr__(self) -> str:
        # 获取 repr
        return repr(self.数据)
    
    def __iter__(self):
        # 迭代
        return iter(self.数据)
    
    def __reversed__(self):
        # 反向迭代
        return reversed(self.数据)
    
    def __eq__(self, other) -> bool:
        # 判断相等
        if isinstance(other, 数据类):
            return self.数据 == other.数据
        return self.数据 == other
    
    def __ne__(self, other) -> bool:
        # 判断不相等
        if isinstance(other, 数据类):
            return self.数据 != other.数据
        return self.数据 != other

本地数据字典: dict[str, 数据类] = {}

def 获取本地数据(路径: pathlib.Path | str, 默认值: dict[str, Any] | None = None) -> 数据类:
    """获取本地数据"""
    路径 = pathlib.Path(路径)
    路径字符串 = str(路径.resolve())
    if 路径字符串 in 本地数据字典:
        return 本地数据字典[路径字符串]
    本地数据字典[路径字符串] = 数据类(默认值=默认值, 路径=路径)
    return 本地数据字典[路径字符串]

内存数据字典: dict[str, 数据类] = {}

def 获取内存数据(标识: str, 默认值: dict[str, Any] | None = None) -> 数据类:
    """获取内存数据"""
    if 标识 in 内存数据字典:
        return 内存数据字典[标识]
    内存数据字典[标识] = 数据类(默认值=默认值)
    return 内存数据字典[标识]
