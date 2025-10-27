// 小红狐 API 函数 IIFE（立即调用函数表达式）
(function (全局对象) {
    function 获取页面名() {
        return 小红狐工具.请求.获取("/api/页面/页面名")
    }

    function 新增页面(页面名) {
        return 小红狐工具.请求.新增("/api/页面", {
            页面名: 页面名,
        })
    }

    function 获取页面配置标签页(页面名="页面名六个字") {
        return 小红狐工具.请求.获取(`/api/页面/配置标签页/${页面名}`)
    }

    // 对外暴露的 小红狐 方法
    const 小红狐 = {
        获取页面名: 获取页面名,
        新增页面: 新增页面,
        获取页面配置标签页: 获取页面配置标签页,
    };

    // 将 小红狐 挂载到全局对象上（比如 window），这样外部可直接使用
    if (typeof 全局对象 !== 'undefined') {
        全局对象.小红狐 = 小红狐;
    }

})(typeof window !== 'undefined' ? window : this);
