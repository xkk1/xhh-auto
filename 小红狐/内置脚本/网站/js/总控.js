let 导入脚本信息字典 = {};
let 加载脚本错误信息字典 = {};

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

async function 更新加载脚本错误信息字典() {
    加载脚本错误信息字典 = await 小红狐.脚本.获取加载脚本错误信息字典();
}

function 渲染脚本信息() {
    const 脚本信息容器 = document.querySelector("#脚本信息容器");
    脚本信息容器.replaceChildren();

    const 脚本信息表格 = document.createElement("table");
    脚本信息表格.id = "脚本信息表格";
    // 创建表头元素
    const 表头 = document.createElement("thead");
    ["名称/点击查看详情", "作者", "版本", "操作"].forEach(function (标题) {
        let th = document.createElement("th");
        th.textContent = 标题;
        表头.appendChild(th);
    });
    脚本信息表格.appendChild(表头);
    // 创建表体
    表体 = document.createElement("tbody");
    for (const [脚本模块名, 导入脚本信息] of Object.entries(导入脚本信息字典)) {
        const 脚本名称 = 导入脚本信息.名称 || 脚本模块名;
        // 新建一行
        let tr = document.createElement("tr");
        tr.dataset.脚本模块名 = 脚本模块名;
        // 名称
        let td = document.createElement("td");
        td.textContent = 脚本名称;
        td.classList.add("脚本名称");
        td.addEventListener("click", function () {
            const 对话框元素 = document.querySelector("#对话框");
            对话框元素.replaceChildren();
            const 信息元素 = document.createElement("pre");
            let 信息 = ""
            if (导入脚本信息.名称) 信息 += `名称：${脚本名称}\n`;
            信息 += `脚本模块名：${脚本模块名}\n`;
            if (导入脚本信息.简介) 信息 += `简介：\n${导入脚本信息.简介}\n`;
            if (导入脚本信息.作者) 信息 += `作者：${导入脚本信息.作者.join("、")}\n`;
            if (导入脚本信息.版本) 信息 += `版本：${导入脚本信息.版本}\n`;
            信息元素.append(信息);
            信息 = "";
            const 标签页容器 = document.createElement("span");
            
            信息元素.appendChild(标签页容器);
            对话框元素.appendChild(信息元素);
            对话框元素添加关闭按钮(对话框元素, "确定");
            对话框元素.showModal();
            小红狐.总控.获取脚本配置页面(脚本模块名)
                .then(function (配置页面) {
                    if (Object.entries(配置页面).length > 0) {
                        标签页容器.append("总控配置页面：");
                        标签页容器.append(document.createElement("br"));
                        for (const [URL, 标题] of Object.entries(配置页面)) {
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
        })
        tr.appendChild(td);
        // 作者
        td = document.createElement("td");
        let 作者容器 = document.createElement("div");
        作者容器.classList.add("作者容器");
        作者数组 = 导入脚本信息.作者 || [];
        for (const 作者 of 作者数组) {
            let span = document.createElement("span");
            span.textContent = 作者;
            span.classList.add("作者");
            作者容器.appendChild(span);
        }
        td.appendChild(作者容器);
        tr.appendChild(td);
        // 版本
        td = document.createElement("td");
        td.textContent = 导入脚本信息.版本 || "未知";
        tr.appendChild(td);
        // 操作
        td = document.createElement("td");
        const 重载脚本按钮 = document.createElement("button");
        重载脚本按钮.type = "button";
        重载脚本按钮.classList.add("重载脚本按钮","加载按钮");
        重载脚本按钮.textContent = "重载";
        重载脚本按钮.addEventListener("click", function () {
            const 确认 = confirm(`确定要重载“${脚本名称}”吗？`);
            if (!确认) {
                return;
            }
            this.classList.add("加载中");
            小红狐.脚本.重载脚本(脚本模块名)
                .then((信息) => {
                    刷新脚本信息();
                    alert(信息);
                })
                .catch(error => {
                    更新加载脚本错误信息字典().then();
                    console.error("重载脚本失败:", error);
                    alert("重载脚本失败!\n" + error);
                })
                .finally(() => {
                    重载脚本按钮.classList.remove("加载中");
                })
        });
        td.appendChild(重载脚本按钮);
        tr.appendChild(td);
        表体.appendChild(tr);
    }
    脚本信息表格.appendChild(表体);
    脚本信息容器.appendChild(脚本信息表格);
}

function 刷新脚本信息() {
    const 刷新脚本信息按钮 = document.querySelector("#刷新脚本信息按钮");
    刷新脚本信息按钮.classList.add("加载中");
    Promise.all([
        更新导入脚本信息字典(),
        更新加载脚本错误信息字典(),
    ])
        .then(() => {
            渲染脚本信息();
        })
        .catch(error => {
            console.error("获取导入脚本信息字典失败:", error);
            document.querySelector("#导入脚本信息").textContent = "获取导入脚本信息字典失败" + error;
        })
        .finally(() => {
            刷新脚本信息按钮.classList.remove("加载中");
        });
}

function 重载所有脚本() {
    const 确认 = confirm("确定要重载所有脚本吗？");
    if (!确认) {
        return;
    }
    const 重载所有脚本按钮 = document.querySelector("#重载所有脚本按钮");
    重载所有脚本按钮.classList.add("加载中");
    小红狐.脚本.重载所有脚本()
        .then((信息) => {
            刷新脚本信息();
            if (Object.keys(信息).length === 0) {
                alert("重载所有脚本成功！");
            } else {
                alert("重载所有脚本成功！\n但有脚本加载失败，请查看加载脚本错误信息");
            }
        })
        .catch(error => {
            console.error("重载所有脚本失败:", error);
            alert("重载所有脚本失败!\n" + error);
        })
        .finally(() => {
            重载所有脚本按钮.classList.remove("加载中");
        })
}

function 显示加载脚本错误信息() {
    const 对话框元素 = document.querySelector("#对话框");
    对话框元素.replaceChildren();
    const 信息元素 = document.createElement("p");
    if (Object.keys(加载脚本错误信息字典).length === 0) {
        信息元素.textContent = "没有加载脚本错误";
    } else {
        const p = document.createElement("p");
        p.textContent = "加载脚本错误:";
        p.style.color = "red";
        对话框元素.appendChild(p);
        for (const [脚本模块名, 信息] of Object.entries(加载脚本错误信息字典)) {
            const p = document.createElement("pre");
            const strong = document.createElement("strong");
            strong.textContent = 脚本模块名;
            p.appendChild(strong);
            p.appendChild(document.createTextNode(": " + 信息));
            对话框元素.appendChild(p);
        }
    }
    对话框元素.appendChild(信息元素);
    对话框元素添加关闭按钮(对话框元素, "确定");
    对话框元素.showModal();
}

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    刷新脚本信息();
});