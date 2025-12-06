// 获取页面名
const 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;
let 导入脚本信息字典 = {};
let 页面操作自动开启脚本 = {};
let 页面操作开启脚本 = {};
let 页面生成脚本 = {};
let 页面状态 = null;
let 账号名 = "默认";
let 全部账号名 = [账号名];
let 配置名 = 页面名;
let 全部配置名 = [配置名];


function 对话框元素添加关闭按钮(对话框元素, 关闭按钮文本="关闭") {
    const 对话框表单 = document.createElement("form");
    对话框表单.method = "dialog";
    对话框表单.style.textAlign = "center";
    const 关闭按钮 = document.createElement('button');
    关闭按钮.textContent = 关闭按钮文本;
    对话框表单.appendChild(关闭按钮);
    对话框元素.appendChild(对话框表单);
}

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

async function 更新页面状态() {
    页面状态 = await 小红狐.页面.获取页面状态(页面名);
}

async function 更新账号名() {
    账号名 = await 小红狐.页面.获取页面账号名(页面名);
}

async function 更新全部账号名() {
    全部账号名 = await 小红狐.账号.获取全部账号名();
}

async function 更新配置名() {
    配置名 = await 小红狐.页面.获取页面配置名(页面名);
}

async function 更新全部配置名() {
    全部配置名 = await 小红狐.配置.获取全部配置名();
}


function 渲染页面操作() {
    const 页面操作容器元素 = document.querySelector("#页面操作容器");
    页面操作容器元素.replaceChildren();

    页面操作容器元素.append("状态：")
    const 页面状态元素 = document.createElement("span");
    页面状态元素.id = "页面状态";
    if (页面状态 === null) {
        页面状态元素.textContent = "未创建";
        页面状态元素.classList.add("未创建");
    } else if (页面状态 === false) {
        页面状态元素.textContent = "手动关闭";
        页面状态元素.classList.add("关闭");
    } else {
        页面状态元素.textContent = "开启";
        页面状态元素.classList.add("开启");
    }
    页面操作容器元素.appendChild(页面状态元素);
    页面操作容器元素.append(" ")

    const 新建页面按钮 = document.createElement("button");
    新建页面按钮.id = "新建页面按钮";
    新建页面按钮.classList.add("加载按钮")
    新建页面按钮.textContent = "新建页面"
    新建页面按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        小红狐.页面.新建页面(页面名)
            .then(() => {
                小红狐.页面.开启页面操作自动开启脚本(页面名).then(() => {
                    刷新页面操作脚本();
                });
                刷新页面操作();
            })
            .catch(async error => {
                console.error("新建页面失败:", error);
                await 小红狐工具.对话框.提示("新建页面失败!\n" + error);
            })
            .finally(() => {
                新建页面按钮.classList.remove("加载中");
            });
    });
    页面操作容器元素.appendChild(新建页面按钮);

    const 关闭页面按钮 = document.createElement("button");
    关闭页面按钮.id = "关闭页面按钮";
    关闭页面按钮.classList.add("加载按钮")
    关闭页面按钮.textContent = "关闭页面"
    关闭页面按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        小红狐.页面.关闭页面操作自动开启脚本(页面名)
            .then(() => {})
            .finally(() => {
                小红狐.页面.关闭页面(页面名)
                    .then(() => {
                        刷新页面操作();
                    })
                    .catch(async error => {
                        console.error("关闭页面失败:", error);
                        await 小红狐工具.对话框.提示("关闭页面失败!\n" + error);
                    })
                    .finally(() => {
                        刷新页面操作脚本();
                        关闭页面按钮.classList.remove("加载中");
                    });
            });
    });
    页面操作容器元素.appendChild(关闭页面按钮);

    const 重启页面按钮 = document.createElement("button");
    重启页面按钮.id = "重启页面按钮";
    重启页面按钮.classList.add("加载按钮")
    重启页面按钮.textContent = "重启页面"
    重启页面按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        try {
            await 小红狐.页面.关闭页面操作自动开启脚本(页面名);
        } catch (error) {}
        try {
            await 小红狐.页面.关闭页面(页面名);
        } catch (error) {}
        try {
            await 小红狐.页面.新建页面(页面名);
            try {
                await 小红狐.页面.开启页面操作自动开启脚本(页面名);
            } catch (error) {}
        } catch (error) {
            console.error("重启页面失败:", error);
            await 小红狐工具.对话框.提示("重启页面失败!\n" + error);
        }
        刷新页面操作();
        刷新页面操作脚本();
    });
    页面操作容器元素.appendChild(重启页面按钮);
}

function 刷新页面操作() {
    const 刷新页面操作按钮 = document.querySelector("#刷新页面操作按钮");
    刷新页面操作按钮.classList.add("加载中");
    更新页面状态()
        .then(() => {
            渲染页面操作();
        })
        .catch(error => {
            console.error("获取页面操作失败:", error);
            document.querySelector("#页面操作容器").textContent = "获取页面操作失败" + error;
        })
        .finally(() => {
            刷新页面操作按钮.classList.remove("加载中");
        });
}
function 渲染页面生成脚本() {
    const 页面生成脚本容器元素 = document.querySelector("#页面生成脚本容器");
    页面生成脚本容器元素.replaceChildren();

    const 页面生成脚本下拉列表 = document.createElement("select");
    页面生成脚本下拉列表.id = "页面生成脚本下拉列表";
    for (const [脚本模块名, 导入脚本信息] of Object.entries(导入脚本信息字典)) {
        // 跳过渲染没有页面生成的脚本
        if (Object.prototype.toString.call(导入脚本信息.页面生成) !== "[object Object]") continue;
        const 名称 = 导入脚本信息.名称;
        for (const [页面生成脚本名, 页面生成脚本信息] of Object.entries(导入脚本信息.页面生成)) {
            // 跳过渲染非法页面生成的脚本
            if (Object.prototype.toString.call(页面生成脚本信息) !== "[object Object]") continue;
            const 脚本名称 = 页面生成脚本信息.名称 || 页面生成脚本名;
            const 选项 = document.createElement("option");
            选项.value = 脚本模块名 + "/" + 页面生成脚本名;
            选项.textContent = 脚本名称;
            if (脚本模块名 === 页面生成脚本?.脚本模块名 && 页面生成脚本名 === 页面生成脚本?.页面生成脚本名) {
                选项.textContent = "[当前] " + 选项.textContent;
                选项.selected = true;
            }
            页面生成脚本下拉列表.appendChild(选项);
        }
    }
    页面生成脚本容器元素.appendChild(页面生成脚本下拉列表);

    const 页面生成脚本操作容器 = document.createElement("span");
    const 详细信息按钮 = document.createElement("button");
    详细信息按钮.type = "button";
    详细信息按钮.id = "详细信息按钮";
    详细信息按钮.textContent = "详细信息";
    详细信息按钮.addEventListener("click", function () {
        const 对话框元素 = document.querySelector("#对话框");
        对话框元素.replaceChildren();
        const [脚本模块名, 页面生成脚本名] = 页面生成脚本下拉列表.value.split("/");
        const 脚本名称 = 导入脚本信息字典?.[脚本模块名]?.名称;
        const 脚本简介 = 导入脚本信息字典?.[脚本模块名]?.简介;
        const 页面生成脚本名称 = 导入脚本信息字典?.[脚本模块名]?.页面生成?.[页面生成脚本名]?.名称;
        const 页面生成脚本简介 = 导入脚本信息字典?.[脚本模块名]?.页面生成?.[页面生成脚本名]?.简介;
        const 信息元素 = document.createElement("p");
        信息元素.style.whiteSpace = "pre-wrap";
        let 信息 = "";
        if (页面生成脚本名称) 信息 += `页面生成脚本名称：${页面生成脚本名称}\n`;
        信息 += `页面生成脚本名：${页面生成脚本名}\n`;
        if (页面生成脚本简介) 信息 += `页面生成脚本简介：\n${页面生成脚本简介}\n`;
        信息元素.append(信息);
        const 标签页容器 = document.createElement("span")
        信息元素.appendChild(标签页容器);
        信息 = "\n所属脚本信息\n";
        if (脚本名称) 信息 += `脚本名称：${脚本名称}\n`;
        信息 += `脚本模块名：${脚本模块名}\n`
        if (脚本简介) 信息 += `脚本简介：\n${脚本简介}\n`;
        信息元素.append(信息);
        对话框元素.appendChild(信息元素);
        对话框元素添加关闭按钮(对话框元素);
        对话框元素.showModal();
        小红狐.页面.获取页面生成配置页面(页面名, 脚本模块名, 页面生成脚本名)
            .then((页面生成配置页面) => {
                if (Object.entries(页面生成配置页面).length > 0) {
                    标签页容器.append("页面生成配置页面：");
                    标签页容器.append(document.createElement("br"));
                    for (const [URL, 标题] of Object.entries(页面生成配置页面)) {
                        const a = document.createElement("a");
                        a.href = URL;
                        a.textContent = 标题;
                        a.target = "_blank";
                        标签页容器.appendChild(a);
                        标签页容器.appendChild(document.createElement("br"));
                    }
                    // 事件委托重写 a 标签的点击事件
                    if (window !== parent && parent.添加标签页) {
                        标签页容器.addEventListener("click", function (e) {
                            if (e.target.tagName === "A") {
                                e.preventDefault();
                                const 标题 = e.target.textContent;
                                const URL = e.target.getAttribute("href");
                                parent.添加标签页(URL, 标题, true);
                            }
                        })
                    }
                }
            });
    });
    页面生成脚本操作容器.appendChild(详细信息按钮);
    const 设置为当前页面生成脚本按钮 = document.createElement("button");
    设置为当前页面生成脚本按钮.type = "button";
    设置为当前页面生成脚本按钮.id = "设置为当前页面生成脚本按钮";
    设置为当前页面生成脚本按钮.classList.add("加载按钮");
    设置为当前页面生成脚本按钮.textContent = "设置为当前页面生成脚本";
    设置为当前页面生成脚本按钮.style.display = "none";
    设置为当前页面生成脚本按钮.style.color = "orange";
    设置为当前页面生成脚本按钮.addEventListener("click", async function () {
        const [脚本模块名, 页面生成脚本名] = 页面生成脚本下拉列表.value.split("/");
        if (await 小红狐工具.对话框.确认(`确定要设置为当前页面生成脚本吗？\n脚本模块名：${脚本模块名}\n页面生成脚本名：${页面生成脚本名}`)) {
            设置为当前页面生成脚本按钮.classList.add("加载中");
            小红狐.页面.修改页面生成脚本(页面名, 脚本模块名, 页面生成脚本名)
                .then(() => {
                    if (window !== parent && parent.删除标签页) {
                        小红狐.页面.获取页面生成配置页面(页面名, 页面生成脚本?.脚本模块名, 页面生成脚本?.页面生成脚本名)
                            .then(function (页面生成配置页面) {
                                for (const [URL, 标题] of Object.entries(页面生成配置页面)) {
                                    parent.删除标签页(URL);
                                }
                            })
                            .catch(function (错误) {
                                console.error(错误);
                            })
                            .finally(() => {
                                刷新页面生成脚本();
                            });
                    } else {
                        刷新页面生成脚本();
                    }
                })
                .catch(async 错误 => {
                    console.error(错误);
                    await 小红狐工具.对话框.提示("修改页面生成脚本失败，错误信息：\n" + 错误);
                    设置为当前页面生成脚本按钮.classList.remove("加载中");
                })
        }
    });
    页面生成脚本操作容器.appendChild(设置为当前页面生成脚本按钮);
    页面生成脚本容器元素.appendChild(页面生成脚本操作容器);

    页面生成脚本下拉列表.addEventListener("change", function () {
        const [脚本模块名, 页面生成脚本名] = this.value.split("/");
        if (!脚本模块名 || !页面生成脚本名) {
            return;
        }
        if (页面生成脚本?.脚本模块名 === 脚本模块名 && 页面生成脚本?.页面生成脚本名 === 页面生成脚本名) {
            设置为当前页面生成脚本按钮.style.display = "none";
        } else {
            设置为当前页面生成脚本按钮.dataset.脚本模块名 = 脚本模块名;
            设置为当前页面生成脚本按钮.dataset.页面生成脚本名 = 页面生成脚本名;
            设置为当前页面生成脚本按钮.style.display = "inline-block";
        }
    });

    // 添加页面生成开启脚本的标签页
    if (window !== parent && parent.添加标签页) {
        小红狐.页面.获取页面生成配置页面(页面名, 页面生成脚本?.脚本模块名, 页面生成脚本?.页面生成脚本名)
            .then(function (页面生成配置页面) {
                for (const [URL, 标题] of Object.entries(页面生成配置页面)) {
                    parent.添加标签页(URL, 标题);
                }
            })
            .catch(function (错误) {
                console.error(错误);
            });
    }
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
    页面操作脚本表格元素.replaceChildren();
    // 创建表头元素
    表头 = document.createElement("thead");
    ["页面操作脚本", "状态 / <span id='自动开启'>自动开启</span>"].forEach(function (标题) {
        let th = document.createElement("th");
        th.innerHTML = 标题;
        表头.appendChild(th);
    });
    页面操作脚本表格元素.appendChild(表头);
    const 自动开启元素 = document.querySelector("#自动开启");
    自动开启元素.addEventListener("click", function () {
        const 对话框元素 = document.querySelector("#对话框");
        对话框元素.replaceChildren();
        const 自动开启介绍元素 = document.createElement("p");
        自动开启介绍元素.textContent = "自动开启功能：新建页面时自动开启脚本，页面关闭时停止自动开启脚本。";
        对话框元素.appendChild(自动开启介绍元素);
        const 自动开启操作容器 = document.createElement("div");
        const 批量开启按钮 = document.createElement("button");
        批量开启按钮.id = "批量开启";
        批量开启按钮.classList.add("加载按钮");
        批量开启按钮.type = "button";
        批量开启按钮.textContent = "批量开启";
        批量开启按钮.addEventListener("click", function () {
            this.classList.add("加载中");
            小红狐.页面.开启页面操作自动开启脚本(页面名)
                .then(async function (结果) {
                    批量开启按钮.classList.remove("加载中");
                    await 小红狐工具.对话框.提示("批量开启脚本成功");
                    刷新页面操作脚本();
                })
                .catch(async function (错误) {
                    批量开启按钮.classList.remove("加载中");
                    console.error(错误);
                    await 小红狐工具.对话框.提示("批量开启脚本失败，错误信息：\n" + 错误);
                });
        });
        自动开启操作容器.appendChild(批量开启按钮);
        自动开启操作容器.style.textAlign = "center";
        自动开启操作容器.style.paddingBottom = "1rem";
        const 批量关闭按钮 = document.createElement("button");
        批量关闭按钮.id = "批量关闭";
        批量关闭按钮.classList.add("加载按钮");
        批量关闭按钮.type = "button";
        批量关闭按钮.textContent = "批量关闭";
        批量关闭按钮.addEventListener("click", function () {
            this.classList.add("加载中");
            小红狐.页面.关闭页面操作自动开启脚本(页面名)
                .then(async function (结果) {
                    批量关闭按钮.classList.remove("加载中");
                    await 小红狐工具.对话框.提示("批量关闭脚本成功");
                    刷新页面操作脚本();
                })
                .catch(async function (错误) {
                    批量关闭按钮.classList.remove("加载中");
                    console.error(错误);
                    await 小红狐工具.对话框.提示("批量关闭脚本失败，错误信息：\n" + 错误);
                });
        });
        自动开启操作容器.appendChild(批量关闭按钮);
        对话框元素.appendChild(自动开启操作容器);
        对话框元素添加关闭按钮(对话框元素, "确定");
        对话框元素.showModal();
        });
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
                const 对话框元素 = document.querySelector("#对话框");
                对话框元素.replaceChildren();
                const 脚本模块名 = this.parentElement.dataset.脚本模块名;
                const 页面操作脚本名 = this.parentElement.dataset.页面操作脚本名;
                const 脚本名称 = 导入脚本信息字典?.[脚本模块名]?.名称;
                const 脚本简介 = 导入脚本信息字典?.[脚本模块名]?.简介;
                const 页面操作脚本名称 = 导入脚本信息字典?.[脚本模块名]?.页面操作?.[页面操作脚本名]?.名称;
                const 页面操作脚本简介 = 导入脚本信息字典?.[脚本模块名]?.页面操作?.[页面操作脚本名]?.简介;
                const 信息元素 = document.createElement("p");
                信息元素.style.whiteSpace = "pre-wrap";
                let 信息 = "";
                if (页面操作脚本名称) 信息 += `页面操作脚本名称：${页面操作脚本名称}\n`;
                信息 += `页面操作脚本名：${页面操作脚本名}\n`;
                if (页面操作脚本简介) 信息 += `页面操作脚本简介：\n${页面操作脚本简介}\n`;
                信息元素.append(信息);
                const 标签页容器 = document.createElement("span")
                信息元素.appendChild(标签页容器);
                信息 = "\n所属脚本信息\n";
                if (脚本名称) 信息 += `脚本名称：${脚本名称}\n`;
                信息 += `脚本模块名：${脚本模块名}\n`
                if (脚本简介) 信息 += `脚本简介：\n${脚本简介}\n`;
                信息元素.append(信息);
                对话框元素.appendChild(信息元素);
                对话框元素添加关闭按钮(对话框元素);
                对话框元素.showModal();
                小红狐.页面.获取页面操作配置页面(页面名, 脚本模块名, 页面操作脚本名)
                    .then((页面操作配置页面) => {
                        if (Object.entries(页面操作配置页面).length > 0) {
                            标签页容器.append("页面操作配置页面：");
                            标签页容器.append(document.createElement("br"));
                            for (const [URL, 标题] of Object.entries(页面操作配置页面)) {
                                const a = document.createElement("a");
                                a.href = URL;
                                a.textContent = 标题;
                                a.target = "_blank";
                                标签页容器.appendChild(a);
                                标签页容器.appendChild(document.createElement("br"));
                            }
                            // 事件委托重写 a 标签的点击事件
                            if (window !== parent && parent.添加标签页) {
                                标签页容器.addEventListener("click", function (e) {
                                    if (e.target.tagName === "A") {
                                        e.preventDefault();
                                        const 标题 = e.target.textContent;
                                        const URL = e.target.getAttribute("href");
                                        parent.添加标签页(URL, 标题, true);
                                    }
                                })
                            }
                        }
                    });
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
                                    })
                                    .finally(() => {
                                        刷新页面操作脚本();
                                    });
                            } else {
                                刷新页面操作脚本();
                            }
                        })
                        .catch(async (错误) => {
                            console.error(错误);
                            await 小红狐工具.对话框.提示("关闭失败\n" + 错误);
                            页面操作脚本状态span.classList.remove("加载中");
                        });
                } else {
                    // 若未开启则开启
                    小红狐.页面.开启页面操作脚本(页面名, 脚本模块名, 页面操作脚本名)
                        .then(() =>{
                            // 开启成功
                            刷新页面操作脚本();
                        })
                        .catch(async (错误) => {
                            console.error(错误);
                            await 小红狐工具.对话框.提示("开启失败\n" + 错误);
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
            input.addEventListener("change", async function (事件) {
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
                        .catch(async (e) => {
                            // 添加失败
                            this.checked = false;
                            await 小红狐工具.对话框.提示(`添加失败：${e}`);
                        })
                        .finally(() => {
                            label.classList.remove("加载中");
                        });
                } else {
                    if (脚本模块名 === "小红狐" && 页面操作脚本名 === "页面管理") {
                        // 获取输入
                        let 输入 = await 小红狐工具.对话框.输入("警告：取消启用小红狐页面管理可能会无法管理页面！\n请输入“取消启用小红狐页面管理”确认取消启用小红狐页面管理，输入其他取消本次操作：");
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
                        .catch(async(e) => {
                            // 删除失败
                            this.checked = true;
                            await 小红狐工具.对话框.提示(`删除失败：${e}`);
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
                            parent.添加标签页(URL, 标题);
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

function 渲染账号() {
    const 账号容器 = document.querySelector("#账号容器");
    账号容器.replaceChildren();

    const 账号下拉列表 = document.createElement("select");
    账号下拉列表.id = "账号下拉列表";
    // 如果账号名不在全部账号名中，则添加
    if (!全部账号名.includes(账号名)) {
        全部账号名.push(账号名);
    }
    for (const 子账号名 of 全部账号名) {
        const 账号选项 = document.createElement("option");
        账号选项.value = 子账号名;
        账号选项.textContent = 子账号名;
        if (子账号名 === 账号名) {
            账号选项.textContent = "[当前] " + 账号选项.textContent;
            账号选项.selected = true;
        }
        账号下拉列表.appendChild(账号选项);
    }
    账号下拉列表.value = 账号名;
    账号容器.appendChild(账号下拉列表);

    const 账号操作容器 = document.createElement("span");
    账号操作容器.id = "账号操作容器";
    const 保存账号状态按钮 = document.createElement("button");
    保存账号状态按钮.type = "button";
    保存账号状态按钮.id = "保存账号状态按钮";
    保存账号状态按钮.classList.add("加载按钮");
    保存账号状态按钮.textContent = "保存账号状态";
    保存账号状态按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        const 当前账号名 = 账号下拉列表.value;
        小红狐.账号.保存账号状态(当前账号名)
            .then(async () => {
                await 小红狐工具.对话框.提示("保存账号状态成功！");
            })
            .catch(async error => {
                console.error("保存账号状态失败:", error);
                await 小红狐工具.对话框.提示("保存账号状态失败!\n" + error);
            })
            .finally(() => {
                保存账号状态按钮.classList.remove("加载中");
            })
    });
    账号操作容器.appendChild(保存账号状态按钮);
    const 设置为当前账号按钮 = document.createElement("button");
    设置为当前账号按钮.type = "button";
    设置为当前账号按钮.id = "设置为当前账号按钮";
    设置为当前账号按钮.classList.add("加载按钮");
    设置为当前账号按钮.textContent = "设置为当前账号";
    设置为当前账号按钮.style.color = "orange";
    设置为当前账号按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        const 当前账号名 = 账号下拉列表.value;
        小红狐.页面.修改页面账号名(页面名, 当前账号名)
            .then(async () => {
                await 小红狐工具.对话框.提示("修改页面账号成功！\n关闭页面再新建页面后生效！");
                刷新账号();
            })
            .catch(async error => {
                console.error("修改页面账号失败:", error);
                await 小红狐工具.对话框.提示("修改页面账号失败!\n" + error);
            })
            .finally(() => {
                设置为当前账号按钮.classList.remove("加载中");
            })
    });
    设置为当前账号按钮.style.display = "none";
    账号操作容器.appendChild(设置为当前账号按钮);
    const 修改账号名按钮 = document.createElement("button");
    修改账号名按钮.type = "button";
    修改账号名按钮.id = "修改账号名按钮";
    修改账号名按钮.classList.add("加载按钮");
    修改账号名按钮.textContent = "修改账号名";
    修改账号名按钮.style.display = "none";
    修改账号名按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        const 当前账号名 = 账号下拉列表.value;
        const 新账号名 = await 小红狐工具.对话框.输入("请输入账号名：", 当前账号名);
        if (!新账号名) {
            this.classList.remove("加载中");
            return;
        }
        if (新账号名 === 当前账号名) {
            await 小红狐工具.对话框.提示("账号名未改变！");
            this.classList.remove("加载中");
            return;
        }
        小红狐.账号.修改账号名(当前账号名, 新账号名)
            .then(async () => {
                await 小红狐工具.对话框.提示("修改账号名成功！");
                刷新账号();
            })
            .catch(async error => {
                console.error("修改账号名失败:", error);
                await 小红狐工具.对话框.提示("修改账号名失败!\n" + error);
            })
            .finally(() => {
                修改账号名按钮.classList.remove("加载中");
            });
    });
    账号操作容器.appendChild(修改账号名按钮);
    const 删除账号按钮 = document.createElement("button");
    删除账号按钮.type = "button";
    删除账号按钮.id = "删除账号按钮";
    删除账号按钮.classList.add("加载按钮");
    删除账号按钮.textContent = "删除账号";
    删除账号按钮.style.display = "none";
    删除账号按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        const 当前账号名 = 账号下拉列表.value;
        // 二次确认
        if (!await 小红狐工具.对话框.确认(`确定要删除账号“${当前账号名}”吗？`)) {
            this.classList.remove("加载中");
            return;
        }
        小红狐.账号.删除账号(当前账号名)
            .then(async () => {
                await 小红狐工具.对话框.提示("删除账号成功！");
                刷新账号();
            })
            .catch(async error => {
                console.error("删除账号失败:", error);
                await 小红狐工具.对话框.提示("删除账号失败!\n" + error);
            })
            .finally(() => {
                删除账号按钮.classList.remove("加载中");
            });
    });
    账号操作容器.appendChild(删除账号按钮);
    const 复制账号按钮 = document.createElement("button");
    复制账号按钮.type = "button";
    复制账号按钮.id = "复制账号按钮";
    复制账号按钮.classList.add("加载按钮");
    复制账号按钮.textContent = "复制账号";
    复制账号按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        const 当前账号名 = 账号下拉列表.value;
        const 新账号名 = await 小红狐工具.对话框.输入("请输入新账号名：", 当前账号名);
        if (!新账号名) {
            this.classList.remove("加载中");
            return;
        }
        if (新账号名 === 当前账号名) {
            await 小红狐工具.对话框.提示("账号名未改变！");
            this.classList.remove("加载中");
            return;
        }
        小红狐.账号.复制账号(当前账号名, 新账号名)
            .then(async () => {
                await 小红狐工具.对话框.提示("复制账号成功！");
                刷新账号();
            })
            .catch(async error => {
                console.error("复制账号失败:", error);
                await 小红狐工具.对话框.提示("复制账号失败!\n" + error);
            })
            .finally(() => {
                复制账号按钮.classList.remove("加载中");
            })
    });
    账号操作容器.appendChild(复制账号按钮);
    const 新建账号按钮 = document.createElement("button");
    新建账号按钮.type = "button";
    新建账号按钮.id = "新建账号按钮";
    新建账号按钮.classList.add("加载按钮");
    新建账号按钮.textContent = "新建账号";
    新建账号按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        const 新建账号名 = await 小红狐工具.对话框.输入("请输入账号名：");
        if (!新建账号名) {
            this.classList.remove("加载中");
            return;
        }
        小红狐.账号.新建账号(新建账号名)
            .then(async () => {
                await 小红狐工具.对话框.提示("新建账号成功！");
                刷新账号();
            })
            .catch(async error => {
                console.error("新建账号失败:", error);
                await 小红狐工具.对话框.提示("新建账号失败!\n" + error);
            })
            .finally(() => {
                新建账号按钮.classList.remove("加载中");
            });
    });
    账号操作容器.appendChild(新建账号按钮);
    账号容器.appendChild(账号操作容器);

    账号下拉列表.addEventListener("change", function () {
        const 选中账号名 = this.value;
        if (选中账号名 === 账号名) {
            保存账号状态按钮.style.display = "inline-block";
            设置为当前账号按钮.style.display = "none";
            修改账号名按钮.style.display = "none";
            删除账号按钮.style.display = "none";
        } else {
            保存账号状态按钮.style.display = "none";
            设置为当前账号按钮.style.display = "inline-block";
            修改账号名按钮.style.display = "inline-block";
            删除账号按钮.style.display = "inline-block";
        }
    });
}

function 刷新账号() {
    const 刷新账号按钮 = document.querySelector("#刷新账号按钮");
    刷新账号按钮.classList.add("加载中");
    Promise.all([
        更新账号名(),
        更新全部账号名()
    ])
        .then(() => {
            渲染账号();
        })
        .catch(error => {
            console.error("获取账号名失败:", error);
            document.querySelector("#账号容器").textContent = "获取账号失败：" + error;
        })
        .finally(() => {
            刷新账号按钮.classList.remove("加载中");
        });
}

function 渲染配置名() { 
    const 配置名容器 = document.querySelector("#配置名容器");
    配置名容器.replaceChildren();
    const 配置名下拉列表 = document.createElement("select");
    配置名下拉列表.id = "配置名下拉列表";
    // 如果配置名不在全部配置名中，则添加
    if (!全部配置名.includes(配置名)) {
        全部配置名.push(配置名);
    }
    for (const 子配置名 of 全部配置名) {
        const 配置项 = document.createElement("option");
        配置项.value = 子配置名;
        配置项.textContent = 子配置名;
        if (子配置名 === 配置名) {
            配置项.textContent = "[当前] " + 配置项.textContent;
            配置项.selected = true;
        }
        配置名下拉列表.appendChild(配置项);
    }
    配置名容器.appendChild(配置名下拉列表);

    const 设置为当前配置按钮 = document.createElement("button");
    设置为当前配置按钮.type = "button";
    设置为当前配置按钮.id = "设置为当前配置按钮";
    设置为当前配置按钮.classList.add("加载按钮");
    设置为当前配置按钮.textContent = "设置为当前配置";
    设置为当前配置按钮.style.display = "none";
    设置为当前配置按钮.style.color = "orange";
    设置为当前配置按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        const 当前配置名 = 配置名下拉列表.value;
        小红狐.页面.修改页面配置名(页面名, 当前配置名)
            .then(async () => {
                await 小红狐工具.对话框.提示("修改页面配置成功！\n关闭页面再新建页面后生效！");
                刷新配置名();
            })
            .catch(async error => {
                console.error("修改页面配置失败:", error);
                await 小红狐工具.对话框.提示("修改页面配置失败!\n" + error);
            })
    });
    配置名容器.appendChild(设置为当前配置按钮);
    const 修改配置名按钮 = document.createElement("button");
    修改配置名按钮.type = "button";
    修改配置名按钮.id = "修改配置名按钮";
    修改配置名按钮.classList.add("加载按钮");
    修改配置名按钮.textContent = "修改配置名";
    修改配置名按钮.style.display = "none";
    修改配置名按钮.addEventListener("click", async function () {
        const 当前配置名 = 配置名下拉列表.value;
        const 新配置名 = await 小红狐工具.对话框.输入("请输入新配置名：", 当前配置名);
        if (!新配置名) {
            return;
        }
        if (新配置名 === 当前配置名) {
            await 小红狐工具.对话框.提示("配置名未改变！");
            return;
        }
        this.classList.add("加载中");
        小红狐.配置.修改配置名(当前配置名, 新配置名)
            .then(async () => {
                await 小红狐工具.对话框.提示("修改配置名成功！");
                刷新配置名();
            })
            .catch(async error => {
                console.error("修改配置名失败:", error);
                await 小红狐工具.对话框.提示("修改配置名失败!\n" + error);
            })
            .finally(() => {
                修改配置名按钮.classList.remove("加载中");
            });
    });
    配置名容器.appendChild(修改配置名按钮);
    const 删除配置按钮 = document.createElement("button");
    删除配置按钮.type = "button";
    删除配置按钮.id = "删除配置按钮";
    删除配置按钮.classList.add("加载按钮");
    删除配置按钮.textContent = "删除配置";
    删除配置按钮.style.display = "none";
    删除配置按钮.addEventListener("click", async function () {
        const 当前配置名 = 配置名下拉列表.value;
        // 二次确认
        const 确认 = await 小红狐工具.对话框.确认(`确定要删配置“${当前配置名}”吗？`);
        if (!确认) {
            return;
        }
        this.classList.add("加载中");
        小红狐.配置.删除配置(当前配置名)
            .then(async () => {
                await 小红狐工具.对话框.提示("删除配置成功！");
                刷新配置名();
            })
            .catch(async error => {
                console.error("删除页面失败:", error);
                await 小红狐工具.对话框.提示("删除配置失败!\n" + error);
            })
            .finally(() => {
                删除配置按钮.classList.remove("加载中");
            });
    });
    配置名容器.appendChild(删除配置按钮);
    配置名下拉列表.addEventListener("change", function () {
        const 选中配置名 = this.value;
        if (选中配置名 === 配置名) {
            设置为当前配置按钮.style.display = "none";
            修改配置名按钮.style.display = "none";
            删除配置按钮.style.display = "none";
        } else {
            设置为当前配置按钮.style.display = "inline-block";
            修改配置名按钮.style.display = "inline-block";
            删除配置按钮.style.display = "inline-block";
        }
    });
    const 复制配置按钮 = document.createElement("button");
    复制配置按钮.type = "button";
    复制配置按钮.id = "复制配置按钮";
    复制配置按钮.classList.add("加载按钮");
    复制配置按钮.textContent = "复制配置";
    复制配置按钮.addEventListener("click", async function () {
        const 当前配置名 = 配置名下拉列表.value;
        const 新配置名 = await 小红狐工具.对话框.输入("请输入新配置名：", 当前配置名);
        if (!新配置名) {
            return;
        }
        if (当前配置名 === 新配置名) {
            await 小红狐工具.对话框.提示("配置名未改变！");
            return;
        }
        this.classList.add("加载中");
        小红狐.配置.复制配置(当前配置名, 新配置名)
            .then(async () => {
                await 小红狐工具.对话框.提示("复制配置成功！");
                刷新配置名();
            })
            .catch(async error => {
                console.error("复制配置失败:", error);
                await 小红狐工具.对话框.提示("复制配置失败!\n" + error);
            })
            .finally(() => {
                复制配置按钮.classList.remove("加载中");
            });
    });
    配置名容器.appendChild(复制配置按钮);
    const 新建配置按钮 = document.createElement("button");
    新建配置按钮.type = "button";
    新建配置按钮.id = "新建配置按钮";
    新建配置按钮.classList.add("加载按钮");
    新建配置按钮.textContent = "新建配置";
    新建配置按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        const 新建配置名 = await 小红狐工具.对话框.输入("请输入配置名：");
        if (!新建配置名) {
            this.classList.remove("加载中");
            return;
        }
        小红狐.配置.新建配置(新建配置名)
            .then(async () => {
                await 小红狐工具.对话框.提示("新建页面配置成功！");
                刷新配置名();
            })
            .catch(async error => {
                console.error("新建页面配置失败:", error);
                await 小红狐工具.对话框.提示("新建页面配置失败!\n" + error);
            })
            .finally(() => {
                新建配置按钮.classList.remove("加载中");
            });
    });
    配置名容器.appendChild(新建配置按钮);
}

function 刷新配置名() {
    const 刷新配置名按钮 = document.querySelector("#刷新配置名按钮");
    刷新配置名按钮.classList.add("加载中");
    Promise.all([
        更新配置名(),
        更新全部配置名()
    ])
        .then(() => {
            渲染配置名();
        })
        .catch(error => {
            console.error("获取配置名失败:", error);
            document.querySelector("#配置名容器").textContent = "获取配置名失败：" + error;
        })
        .finally(() => {
            刷新配置名按钮.classList.remove("加载中");
        });
}

function 渲染页面名() {
    const 页面名容器 = document.querySelector("#页面名容器");
    页面名容器.replaceChildren();
    
    页面名容器.append(`页面名：${页面名} `);

    const 修改页面名按钮 = document.createElement("button");
    修改页面名按钮.type = "button";
    修改页面名按钮.id = "修改页面名按钮";
    修改页面名按钮.classList.add("加载按钮");
    修改页面名按钮.textContent = "修改页面名";
    修改页面名按钮.style.color = "red";
    修改页面名按钮.addEventListener("click", async function () {
        this.classList.add("加载中");
        const 新页面名 = await 小红狐工具.对话框.输入("请输入新页面名：", 页面名);
        if (!新页面名) {
            this.classList.remove("加载中");
            return;
        }
        小红狐.页面.关闭页面(页面名)
            .then(() => {
                小红狐.页面.修改页面名(页面名, 新页面名)
                    .then(async (结果) => {
                        await 小红狐工具.对话框.提示("修改页面账号成功！\n即将关闭管理页面！");
                        if (window !== parent) {
                            // 刷新页面列表
                            if (parent.parent.刷新页面列表) {
                                parent.parent.刷新页面列表();
                            }
                            // 关闭管理页面
                            if (parent.parent?.多页面?.关闭页面) {
                                parent.parent.多页面.关闭页面(`./html/配置.html?页面名=${encodeURIComponent(页面名)}`);
                            }
                        }
                        // 关闭当前页面
                        window.close();
                    })
                    .catch(async error => {
                        console.error("修改页面账号失败:", error);
                        await 小红狐工具.对话框.提示("页面账号失败!\n" + error);
                    })
                    .finally(() => {
                        修改页面名按钮.classList.remove("加载中");
                    })
            })
            .catch(async error => {
                console.error("关闭页面失败:", error);
                await 小红狐工具.对话框.提示("关闭页面失败!无法在关闭页面前重命名账号名！\n" + error);
                修改页面名按钮.classList.remove("加载中");
            });
    });
    页面名容器.appendChild(修改页面名按钮);

    const 删除页面名按钮 = document.createElement("button");
    删除页面名按钮.type = "button";
    删除页面名按钮.id = "删除页面名按钮";
    删除页面名按钮.classList.add("加载按钮");
    删除页面名按钮.textContent = `删除“${页面名}”页面`;
    删除页面名按钮.style.color = "red";
    删除页面名按钮.addEventListener("click", async function () {
        //二次确认
        if (!await 小红狐工具.对话框.确认(`确定要删除“${页面名}”页面吗？`)) {
            return;
        }
        this.classList.add("加载中");
        小红狐.页面.关闭页面(页面名)
            .then(() => {
                小红狐.页面.删除页面(页面名)
                    .then(async (结果) => {
                        await 小红狐工具.对话框.提示("删除页面账号成功！\n即将关闭管理页面！");
                        if (window !== parent) {
                            // 刷新页面列表
                            if (parent.parent.刷新页面列表) {
                                parent.parent.刷新页面列表();
                            }
                            // 关闭管理页面
                            if (parent.parent?.多页面?.关闭页面) {
                                parent.parent.多页面.关闭页面(`./html/配置.html?页面名=${encodeURIComponent(页面名)}`);
                            }
                        }
                        // 关闭当前页面
                        window.close();
                    })
                    .catch(async error => {
                        console.error("删除页面账失败:", error);
                        await 小红狐工具.对话框.提示("删除页面账失败!\n" + error);
                    })
                    .finally(() => {
                        删除页面名按钮.classList.remove("加载中");
                    })
            })
            .catch(async error => {
                console.error("关闭页面失败:", error);
                await 小红狐工具.对话框.提示("关闭页面失败!无法在关闭页面前删除账号！\n" + error);
                删除页面名按钮.classList.remove("加载中");
            });
    });
    页面名容器.appendChild(删除页面名按钮);

    const 复制页面按钮 = document.createElement("button");
    复制页面按钮.type = "button";
    复制页面按钮.id = "复制页面按钮";
    复制页面按钮.classList.add("加载按钮");
    复制页面按钮.textContent = `复制“${页面名}”页面`;
    复制页面按钮.addEventListener("click", async function () {
        // 获取新页面名
        const 新页面名 = await 小红狐工具.对话框.输入("请输入新页面名：", 页面名);
        if (!新页面名) {
            return;
        }
        if (新页面名 === 页面名) {
            await 小红狐工具.对话框.提示("新页面名不能与原页面名相同！");
            return;
        }
        this.classList.add("加载中");
        小红狐.页面.复制页面(页面名, 新页面名)
            .then(async (结果) => {
                if (window !== parent) {
                    // 刷新页面列表
                    if (parent.parent.刷新页面列表) {
                        parent.parent.刷新页面列表();
                    }
                }
                await 小红狐工具.对话框.提示("复制页面成功！");
            })
            .finally(() => {
                复制页面按钮.classList.remove("加载中");
            });
    });
    页面名容器.appendChild(复制页面按钮);
}

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    刷新页面操作();
    刷新页面操作脚本();
    渲染页面名();
    刷新账号();
    刷新配置名();
    刷新页面生成脚本();
});