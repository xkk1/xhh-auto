from ... import __package__ as 小红狐模块名


页面操作脚本名: str = "页面管理"
名称: str = "小红狐页面管理"
开启脚本页面名列表: list[str] = []


def 入口函数(页面名: str | None = None):
    assert not(页面名 == None), "页面名不能为空"
    if 页面名 in 开启脚本页面名列表:
        return
    else:
        开启脚本页面名列表.append(页面名)

def 关闭函数(页面名: str | None = None):
    if 页面名 == None:
        开启脚本页面名列表.clear()
        return
    if 页面名 in 开启脚本页面名列表:
        开启脚本页面名列表.remove(页面名)
    else:
        assert False, "无法手动关闭，若想关闭请关闭“自动开启”"

def 脚本状态(页面名: str | None = None) -> bool:
    if 页面名 == None:
        return False
    elif 页面名 in 开启脚本页面名列表:
        return True
    else:
        from ...核心.页面 import 获取页面操作自动开启脚本
        页面操作自动开启脚本: dict[str, list[str]] = 获取页面操作自动开启脚本(页面名=页面名)
        # 当前脚本在页面操作自动开启脚本列表中则默认开启
        if 页面操作脚本名 in 页面操作自动开启脚本.get(小红狐模块名, []):
            return True
        return False

def 配置页面(页面名: str) -> dict[str, str]:
    from ...核心.页面 import 获取页面配置名
    配置名: str = 获取页面配置名(页面名)
    页面: dict[str, str] = {
        f"/api/目录/小红狐/内置脚本/网站/配置.html?页面名={页面名}&配置名={配置名}": "页面管理",
    }
    if 页面名 in ["小喾苦", "xkk1"]:
        页面.update({
            "https://www.120107.xyz": "小喾苦的个人网站",
        })
    return 页面

