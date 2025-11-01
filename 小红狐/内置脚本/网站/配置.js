// 获取页面名
let 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;
// 获取配置名
let 配置名 = 小红狐工具.获取Get参数("配置名") || 页面名;

function 渲染启用脚本表格(导入脚本信息列表, 启用脚本模块名) {
    启用脚本表格元素 = document.querySelector("#启用脚本表格");
    启用脚本表格元素.innerHTML = "";
    // 创建表头元素
    表头 = document.createElement("thead");
    ["启用", "脚本名称<span class='模块名'>脚本模块名</span>", "简介", "操作"].forEach(function (标题) {
        let th = document.createElement("th");
        th.innerHTML = 标题;
        表头.appendChild(th);
    });
    启用脚本表格元素.appendChild(表头);
    // 创建表体
    表体 = document.createElement("tbody");
    导入脚本信息列表.forEach(function (导入脚本信息) {
        // 跳过渲染没有页面操作的脚本
        if (导入脚本信息.页面操作 === null) return;
        // 新建一行
        let tr = document.createElement("tr");
        // 启用 多选
        let td = document.createElement("td");
        let input = document.createElement("input");
        input.type = "checkbox";
        input.checked = 启用脚本模块名.includes(导入脚本信息.模块名);
        input.dataset.package = 导入脚本信息.模块名;
        input.addEventListener("change", function () {
            if (this.checked) {
                Promise.all([
                    小红狐.页面.添加脚本(页面名, this.dataset.package),
                    小红狐.脚本.获取脚本配置标签页(this.dataset.package ,页面名)
                ])
                    .then(([添加脚本状态, 脚本配置标签页]) => {
                        console.log(添加脚本状态);
                        console.log(脚本配置标签页);
                        if (window !== parent && parent.添加标签页) {
                            脚本配置标签页.forEach((标签页) => {
                                parent.添加标签页(标签页.标题, 标签页.url);
                            });
                        }
                    });
            } else {
                if (this.dataset.package === "小红狐") {
                    // 获取输入
                    let 输入 = prompt("警告：取消启用小红狐脚本可能会无法管理页面！\n请输入“取消启用小红狐脚本”确认取消启用小红狐脚本，输入其他取消本次操作：");
                    if (输入 !== "取消启用小红狐脚本") {
                        // 选中多选
                        this.checked = true;
                        return;
                    }
                }
                Promise.all([
                    小红狐.页面.删除脚本(页面名, this.dataset.package),
                    小红狐.脚本.获取脚本配置标签页(this.dataset.package, 页面名)
                ])
                    .then(([删除脚本状态, 脚本配置标签页]) => {
                        console.log(删除脚本状态);
                        console.log(脚本配置标签页);
                        if (window !== parent && parent.删除标签页) {
                            脚本配置标签页.forEach((标签页) => {
                                parent.删除标签页(标签页.url);
                            })
                        }
                    })
            }
        });
        td.appendChild(input);
        tr.appendChild(td);
        // 名称
        td = document.createElement("td");
        td.textContent = 导入脚本信息.名称;
        let span = document.createElement("span");
        span.textContent = 导入脚本信息.模块名;
        span.className = "模块名";
        td.appendChild(span);
        tr.appendChild(td);
        // 简介
        td = document.createElement("td");
        td.textContent = 导入脚本信息.简介;
        tr.appendChild(td);
        // 操作
        td = document.createElement("td");
        tr.appendChild(td);
        表体.appendChild(tr);
    });
    启用脚本表格元素.appendChild(表体);
}

function 刷新启用脚本表格() {
    // 发起两个 GET 请求，并在都完成后渲染
    Promise.all([
        小红狐.脚本.获取导入脚本信息列表(),
        小红狐.页面.获取启用脚本模块名(页面名)
    ])
        .then(([导入脚本信息列表, 启用脚本模块名]) => { // 解构获取两个结果
            // 调用渲染函数，传入两个数据
            渲染启用脚本表格(导入脚本信息列表, 启用脚本模块名);
        })
        .catch(error => {
            console.error('请求失败:', error);
            document.querySelector("#启用脚本表格").textContent = "请求失败" + error;
        });
}

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    // 显示配置名
    document.querySelector("#配置名").textContent = 配置名;
    刷新启用脚本表格();
});