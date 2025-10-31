// 获取页面名
let 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;

// 初始化多页面
function 初始化多页面() {
    let iframe容器元素 = document.querySelector("#main");
    多页面 = 小红狐工具.获取多页面(iframe容器元素);
    window.多页面 = 多页面;
    let 标签页父元素 = document.querySelector("ul#标签页");
    小红狐工具.多页面切换(标签页父元素, 多页面.打开页面);
}

// 获取并设置页面配置标签页
function 页面配置标签页() {
    let 标签页元素 = document.querySelector("ul#标签页");
    标签页元素.innerHTML = ""
    小红狐.页面.获取页面配置标签页(页面名=页面名)
        .then(function (配置标签页) {
            for (let 标签页 of 配置标签页) {
                let a = document.createElement("a");
                a.href = 标签页.url;
                a.textContent = 标签页.标题;
                a.classList.add("打开页面");
                a.role = "tab";
                let li = document.createElement("li");
                li.appendChild(a);
                li.role = "none";
                标签页元素.appendChild(li);
            }
            // 打开第一个标签页
            document.querySelector("ul#标签页>li>a").click();
            // 显示标签页
            document.querySelector("#header").style.display = "block";
            // 隐藏加载
            document.querySelector("#加载").style.display = "none";
        })
        .catch(function (错误) {
            console.error(错误);
        });
}

function 添加标签页(标题, url) {
    let 标签页元素 = document.querySelector("ul#标签页");
    if (!标签页元素) return false;
    let 旧a = 标签页元素.querySelector("a[href='" + url + "']");
    if (旧a) {
        旧a.textContent = 标题;
        return true;
    } else {
        let a = document.createElement("a");
        a.href = url;
        a.textContent = 标题;
        a.classList.add("打开页面");
        a.role = "tab";
        let li = document.createElement("li");
        li.appendChild(a);
        li.role = "none";
        标签页元素.appendChild(li);
        return true;
    }
}

function 删除标签页(url) {
    let 标签页元素 = document.querySelector("ul#标签页");
    if (!标签页元素) return false;
    let 旧a = 标签页元素.querySelector("a[href='" + url + "']");
    if (旧a) {
        let 新url = window.多页面.关闭页面(url);
        if (新url) {
            let 新a = 标签页元素.querySelector("a[href='" + 新url + "']");
            if (新a) {
                新a.click();
            }
        }
        旧a.parentNode.remove();
        return true;
    } else {
        return true;
    }
}

function 初始化拖拽标签页() {
    let 标签页元素 = document.querySelector("ul#标签页");
    let 拖拽元素 = null;
    // 拖拽开始
    标签页元素.ondragstart = (事件) => {
        setTimeout(() => {
            事件.target.parentNode.classList.add("拖拽");
        }, 0);
        拖拽元素 = 事件.target.parentNode;
        事件.dataTransfer.effectAllowed = "move";
    };
    // 拖拽移入结束
    标签页元素.ondragover = (事件) => {
        事件.preventDefault();
    };
    // 拖拽移入
    标签页元素.ondragenter = (事件) => {
        事件.preventDefault();
        if (事件.target === 标签页元素 || 事件.target === 拖拽元素 ||事件.target.parentNode === 拖拽元素) {
            return;
        }
        let 目标元素 = 事件.target;
        // 若是 a 标签则改为父元素
        if (目标元素.tagName === "A") {
            目标元素 = 目标元素.parentNode;
        }
        const 子元素数组 = Array.from(标签页元素.children);
        const 拖拽元素下标 = 子元素数组.indexOf(拖拽元素);
        const 目标元素下标 = 子元素数组.indexOf(目标元素);
        if (拖拽元素下标 < 目标元素下标) {
            // 事件.target.parentNode.before(拖拽元素);
            标签页元素.insertBefore(拖拽元素, 目标元素.nextElementSibling);
        } else {
            // 事件.target.parentNode.after(拖拽元素);
            标签页元素.insertBefore(拖拽元素, 目标元素);
        }
    };
    // 拖拽结束
    标签页元素.ondragend = (事件) => {
        事件.target.parentNode.classList.remove("拖拽");
        const 子元素数组 = Array.from(标签页元素.children);
        const 配置页面URL排序 = 子元素数组.map(function (元素) {
            return 元素.querySelector("a").getAttribute('href');
        });
        // console.log(配置页面URL排序);
        小红狐.页面.修改配置页面URL排序(页面名, 配置页面URL排序)
            .then(function (结果) {
                // console.log(结果);
            })
            .catch(function (错误) {
                console.error(错误);
            });
    };
}

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    初始化多页面();
    页面配置标签页();
    初始化拖拽标签页();
});