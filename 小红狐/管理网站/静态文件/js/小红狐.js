// 小红狐 API 函数 IIFE（立即调用函数表达式）
(function (全局对象) {
    let api前缀 = "/api";
    let 请求 = 小红狐工具.请求

    let 页面 = {
        api前缀: api前缀 + "/页面",
        获取页面名: function() {
            return 请求.获取(this.api前缀 + "/页面名");
        },
        新增页面: function(页面名) {
            return 请求.新增(this.api前缀 + "/", {
                页面名: 页面名,
            });
        },
        获取页面配置标签页: function(页面名="页面名六个字") {
            return 请求.获取(this.api前缀 + `/配置标签页/${页面名}`);
        },
        获取启用脚本模块名: function(页面名="页面名六个字") {
            return 请求.获取(this.api前缀 + `/启用脚本模块名/${页面名}`);
        },
        添加脚本: function(页面名="页面名六个字", 脚本模块名="小红狐") {
            return 请求.新增(this.api前缀 + `/添加脚本/${页面名}/${脚本模块名}`);
        },
        删除脚本: function(页面名="页面名六个字", 脚本模块名="小红狐") {
            return 请求.删除(this.api前缀 + `/删除脚本/${页面名}/${脚本模块名}`);
        },
    };

    let 脚本 = {
        api前缀: api前缀 + "/脚本",
        获取导入脚本信息列表: function() {
            return 请求.获取(this.api前缀 + "/");
        },
        获取脚本配置标签页: function(脚本模块名="小红狐", 页面名="页面名六个字") {
            return 请求.获取(this.api前缀 + `/配置标签页/${脚本模块名}/${页面名}`);
        },
    }

    // 对外暴露的 小红狐 方法
    const 小红狐 = {
        页面: 页面,
        脚本: 脚本,
    };

    // 将 小红狐 挂载到全局对象上（比如 window），这样外部可直接使用
    if (typeof 全局对象 !== 'undefined') {
        全局对象.小红狐 = 小红狐;
    }

})(typeof window !== 'undefined' ? window : this);
