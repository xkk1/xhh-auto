// 获取页面名
const 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;

let 页面初始URL = "";

async function 更新页面初始URL() {
    页面初始URL = await 小红狐.页面.获取页面初始URL(页面名);
}

function 渲染页面初始() {
    const 页面容器 = document.querySelector("#页面初始容器");
    页面容器.replaceChildren();

    页面容器.append("页面初始URL：");
    if (页面初始URL === "") {
        页面容器.append("空");
    } else {
        const 页面初始URL元素 = document.createElement("a");
        页面初始URL元素.href = 页面初始URL;
        try {
            页面初始URL元素.textContent = decodeURI(页面初始URL);
        } catch (error) {
            页面初始URL元素.textContent = 页面初始URL;
        }
        页面初始URL元素.target = "_blank";
        页面容器.appendChild(页面初始URL元素);
    }
    const 修改页面初始URL按钮 = document.createElement("button");
    修改页面初始URL按钮.type = "button";
    修改页面初始URL按钮.id = "修改页面初始URL按钮";
    修改页面初始URL按钮.classList.add("加载按钮");
    修改页面初始URL按钮.textContent = "修改页面初始URL";
    修改页面初始URL按钮.addEventListener("click", function () {
        this.classList.add("加载中");
        const 新页面初始URL = prompt("请输入页面初始URL：", 页面初始URL);
        if (新页面初始URL === null) {
            this.classList.remove("加载中");
            return;
        }
        小红狐.页面.修改页面初始URL(页面名, 新页面初始URL)
            .then(() => {
                alert("修改页面初始URL成功！");
                刷新页面初始();
            })
            .catch(error => {
                console.error("修改页面初始URL失败:", error);
                alert("修改页面初始URL失败!\n" + error);
            })
            .finally(() => {
                修改页面初始URL按钮.classList.remove("加载中");
            })
    });
    页面容器.appendChild(修改页面初始URL按钮);
}

function 刷新页面初始() {
    const 刷新页面初始按钮 = document.querySelector("#刷新页面初始按钮");
    刷新页面初始按钮.classList.add("加载中");
    更新页面初始URL()
        .then(() => {
            渲染页面初始();
        })
        .catch(error => {
            console.error("获取页面初始失败:", error);
            document.querySelector("#页面初始容器").textContent = "获取页面初始失败：" + error;
        })
        .finally(() => {
            刷新页面初始按钮.classList.remove("加载中");
        });
}

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    刷新页面初始();
});
