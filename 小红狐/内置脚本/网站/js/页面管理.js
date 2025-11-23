// 获取页面名
const 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;
// 获取配置名
const 配置名 = 小红狐工具.获取Get参数("配置名") || 页面名;
let 导入脚本信息字典 = {};
let 页面操作自动开启脚本 = {};
let 页面操作开启脚本 = {};
let 页面生成脚本 = {};

async function 更新导入脚本信息字典() {
    导入脚本信息字典 = await 小红狐.脚本.获取导入脚本信息字典();
}

async function 更新页面操作自动开启脚本() {
    页面操作自动开启脚本 = await 小红狐.页面.获取页面操作自动开启脚本(页面名);
}

async function 更新页面操作开启脚本() {
    页面操作开启脚本 = await 小红狐.页面.获取页面操作开启脚本(页面名);
}

async function 更新页面生成脚本() {
    页面生成脚本 = await 小红狐.页面.获取页面生成脚本(页面名);
}

function 渲染页面生成脚本() {
    const 页面生成脚本容器元素 = document.querySelector("#页面生成脚本容器");
    页面生成脚本容器元素.innerHTML = "";
    const 当前页面生成脚本span = document.createElement("span");
    当前页面生成脚本span.textContent = 
        导入脚本信息字典?.[页面生成脚本?.脚本模块名]?.页面生成?.[页面生成脚本?.页面生成脚本名].名称 ||
        页面生成脚本?.页面生成脚本名 || "获取页面生成脚本失败！";
    页面生成脚本容器元素.appendChild(当前页面生成脚本span);
}

function 刷新页面生成脚本() {
    const 刷新页面生成脚本按钮 = document.querySelector("#刷新页面生成脚本按钮");
    刷新页面生成脚本按钮.classList.add("加载中");
    // 发起两个 GET 请求，并在都完成后渲染
    Promise.all([
        更新导入脚本信息字典(),
        更新页面生成脚本(),
    ])
        .then(() => {
            // 调用渲染函数
            渲染页面生成脚本();
        })
        .catch(error => {
            console.error("获取页面生成脚本失败:", error);
            document.querySelector("#当前页面生成脚本").textContent = "获取页面脚本脚本失败" + error;
        })
        .finally(() => {
            刷新页面生成脚本按钮.classList.remove("加载中");
        });
}


function 渲染页面操作脚本表格() {
    let 页面操作脚本表格元素 = document.querySelector("#页面操作脚本表格");
    页面操作脚本表格元素.innerHTML = "";
    // 创建表头元素
    表头 = document.createElement("thead");
    ["页面操作脚本", "状态 / 自动开启"].forEach(function (标题) {
        let th = document.createElement("th");
        th.innerHTML = 标题;
        表头.appendChild(th);
    });
    页面操作脚本表格元素.appendChild(表头);
    // 创建表体
    表体 = document.createElement("tbody");
    for (const [脚本模块名, 导入脚本信息] of Object.entries(导入脚本信息字典)) {
        // 跳过渲染没有页面操作的脚本  Object.prototype.toString.call(value) === '[object Object]'
        if (Object.prototype.toString.call(导入脚本信息.页面操作) !== "[object Object]") continue;
        const 名称 = 导入脚本信息.名称;
        for (const [页面操作脚本名, 页面操作脚本信息] of Object.entries(导入脚本信息.页面操作)) {
            // 跳过渲染非法页面操作的脚本
            if (Object.prototype.toString.call(页面操作脚本信息) !== "[object Object]") continue;
            const 脚本名称 = 页面操作脚本信息.名称 || 页面操作脚本名;
            // 新建一行
            let tr = document.createElement("tr");
            tr.dataset.脚本模块名 = 脚本模块名;
            tr.dataset.页面操作脚本名 = 页面操作脚本名;
            // 名称
            td = document.createElement("td");
            td.textContent = 脚本名称;
            td.classList.add("页面操作脚本");
            td.addEventListener("click", function () {
                const 脚本模块名 = this.parentElement.dataset.脚本模块名;
                const 页面操作脚本名 = this.parentElement.dataset.页面操作脚本名;
                const 脚本名称 = 导入脚本信息字典?.[脚本模块名]?.名称;
                const 脚本简介 = 导入脚本信息字典?.[脚本模块名]?.简介;
                const 页面操作脚本名称 = 导入脚本信息字典?.[脚本模块名]?.页面操作?.[页面操作脚本名]?.名称;
                const 页面操作脚本简介 = 导入脚本信息字典?.[脚本模块名]?.页面操作?.[页面操作脚本名]?.简介;
                let 信息 = "";
                if (页面操作脚本名称) 信息 += `页面操作脚本名称：${页面操作脚本名称}\n`;
                信息 += `页面操作脚本名：${页面操作脚本名}\n`;
                if (页面操作脚本简介) 信息 += `页面操作脚本简介：\n${页面操作脚本简介}\n`;
                信息 += "\n所属脚本信息\n";
                if (脚本名称) 信息 += `脚本名称：${脚本名称}\n`;
                信息 += `脚本模块名：${脚本模块名}\n`
                if (脚本简介) 信息 += `脚本简介：\n${脚本简介}\n`;
                alert(信息);
            });
            tr.appendChild(td);
            td = document.createElement("td");
            // 状态切换：开启、关闭
            let span = document.createElement("span");
            span.classList.add("页面操作脚本状态");
            if (页面操作开启脚本?.[脚本模块名]?.includes(页面操作脚本名)) {
                span.textContent = "开启";
                span.classList.add("开启");
                span.title = "点击关闭脚本";
            } else {
                span.textContent = "关闭";
                span.classList.add("关闭");
                span.title = "点击开启脚本";
            }
            span.addEventListener("click", function () {
                this.classList.add("加载中");
                const 页面操作脚本状态span = this;
                if (this.classList.contains("开启")) {
                    // 若已开启则关闭
                    小红狐.页面.关闭页面操作脚本(页面名, 脚本模块名, 页面操作脚本名)
                        .then(() => {
                            // 关闭成功
                            if (window !== parent && parent.删除标签页) {
                                小红狐.页面.获取页面操作配置页面(页面名, 脚本模块名, 页面操作脚本名)
                                    .then((页面操作配置页面) => { 
                                        for (const [URL, 标题] of Object.entries(页面操作配置页面)) {
                                            parent.删除标签页(URL);
                                        }
                                        刷新页面操作脚本();
                                    });
                            } else {
                                刷新页面操作脚本();
                            }
                        })
                        .catch((错误) => {
                            console.error(错误);
                            alert("关闭失败\n信息：" + 错误.信息);
                            页面操作脚本状态span.classList.remove("加载中");
                        });
                } else {
                    // 若未开启则开启
                    小红狐.页面.开启页面操作脚本(页面名, 脚本模块名, 页面操作脚本名)
                        .then(() =>{
                            // 开启成功
                            刷新页面操作脚本();
                        })
                        .catch((错误) => {
                            console.error(错误);
                            alert("开启失败\n信息：" + 错误.信息);
                            页面操作脚本状态span.classList.remove("加载中");
                        });
                }
            });
            td.appendChild(span);
            td.append(" / ");
            // 自动开启 多选
            let label = document.createElement("label");
            label.classList.add("自动开启多选");
            let input = document.createElement("input");
            input.type = "checkbox";
            input.checked = Boolean(页面操作自动开启脚本?.[脚本模块名]?.includes(页面操作脚本名));
            input.addEventListener("change", function (事件) {
                this.checked = !this.checked;
                const label = this.parentElement;
                label.classList.add("加载中");
                const 脚本模块名 = label.parentElement.parentElement.dataset.脚本模块名;
                const 页面操作脚本名 = label.parentElement.parentElement.dataset.页面操作脚本名;
                if (!this.checked) {
                    // 若未选中则添加页面操作脚本
                    小红狐.页面.添加页面操作自动开启脚本(页面名, 脚本模块名 ,页面操作脚本名)
                        .then(() => {
                            // 添加成功
                            this.checked = true;
                        })
                        .catch((e) => {
                            // 添加失败
                            this.checked = false;
                            alert(`添加失败：${e}`);
                        })
                        .finally(() => {
                            label.classList.remove("加载中");
                        });
                } else {
                    if (脚本模块名 === "小红狐" && 页面操作脚本名 === "页面管理") {
                        // 获取输入
                        let 输入 = prompt("警告：取消启用小红狐页面管理可能会无法管理页面！\n请输入“取消启用小红狐页面管理”确认取消启用小红狐页面管理，输入其他取消本次操作：");
                        if (输入 !== "取消启用小红狐页面管理") {
                            // 选中多选
                            this.checked = true;
                            label.classList.remove("加载中");
                            return;
                        }
                    }
                    小红狐.页面.删除页面操作自动开启脚本(页面名, 脚本模块名, 页面操作脚本名)
                        .then(() => {
                            // 删除成功
                            this.checked = false;
                        })
                        .catch((e) => {
                            // 删除失败
                            this.checked = true;
                            alert(`删除失败：${e}`);
                        })
                        .finally(() => {
                            label.classList.remove("加载中");
                        });
                }
            });
            label.appendChild(input);
            td.appendChild(label);
            tr.appendChild(td);
            表体.appendChild(tr);
        }
    }
    页面操作脚本表格元素.appendChild(表体);
    // 添加页面操作开启脚本的标签页
    if (window !== parent && parent.添加标签页) {
        for (const 脚本模块名 in 页面操作开启脚本) {
            for (const 页面操作脚本名 of 页面操作开启脚本[脚本模块名]) {
                小红狐.页面.获取页面操作配置页面(页面名, 脚本模块名, 页面操作脚本名)
                    .then(function (页面操作配置页面) {
                        for (const [URL, 标题] of Object.entries(页面操作配置页面)) {
                            parent.添加标签页(标题, URL);
                        }
                    })
                    .catch(function (错误) {
                        console.error(错误);
                    });
            }
        }
    }
}

function 刷新页面操作脚本() {
    const 刷新页面操作脚本按钮 = document.querySelector("#刷新页面操作脚本按钮");
    刷新页面操作脚本按钮.classList.add("加载中");
    // 刷新页面操作脚本表格
    Promise.all([
        更新导入脚本信息字典(),
        更新页面操作自动开启脚本(),
        更新页面操作开启脚本(),
    ])
        .then(() => {
            // 调用渲染函数
            渲染页面操作脚本表格();
        })
        .catch(error => {
            console.error("获取页面操作脚本失败:", error);
            document.querySelector("#页面操作脚本表格").textContent = "获取页面操作脚本失败" + error;
        })
        .finally(() => {
            刷新页面操作脚本按钮.classList.remove("加载中");
        });
}

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    // 显示配置名
    document.querySelector("#配置名").textContent = 配置名;
    刷新页面生成脚本();
    刷新页面操作脚本();
});