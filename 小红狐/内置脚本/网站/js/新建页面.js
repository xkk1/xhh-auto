// 获取页面名
const 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;

let 账号名 = "默认";
let 全部账号名 = ["默认"];

async function 更新账号名() {
    账号名 = await 小红狐.页面.获取页面账号名(页面名);
}

async function 更新全部账号名() {
    全部账号名 = await 小红狐.账号.获取全部账号名();
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

    const 账号操作容器 = document.createElement("div");
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
            .then(() => {
                alert("保存账号状态成功！");
            })
            .catch(error => {
                console.error("保存账号状态失败:", error);
                alert("保存账号状态失败!\n" + error);
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
    设置为当前账号按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        const 当前账号名 = 账号下拉列表.value;
        小红狐.页面.修改页面账号名(页面名, 当前账号名)
            .then(() => {
                alert("修改页面账号成功！\n关闭页面再新建页面后生效！");
                刷新账号();
            })
            .catch(error => {
                console.error("修改页面账号失败:", error);
                alert("修改页面账号失败!\n" + error);
            })
            .finally(() => {
                设置为当前账号按钮.classList.remove("加载中");
            })
    });
    设置为当前账号按钮.style.display = "none";
    账号操作容器.appendChild(设置为当前账号按钮);
    const 新建账号按钮 = document.createElement("button");
    新建账号按钮.type = "button";
    新建账号按钮.id = "新建账号按钮";
    新建账号按钮.classList.add("加载按钮");
    新建账号按钮.textContent = "新建账号";
    新建账号按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        const 新建账号名 = prompt("请输入账号名：");
        if (!新建账号名) {
            this.classList.remove("加载中");
            return;
        }
        小红狐.账号.新建账号(新建账号名)
            .then(() => {
                alert("新建账号成功！");
                刷新账号();
            })
            .catch(error => {
                console.error("新建账号失败:", error);
                alert("新建账号失败!\n" + error);
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
        } else {
            保存账号状态按钮.style.display = "none";
            设置为当前账号按钮.style.display = "inline-block";
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


// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    刷新账号();
});
