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

// DOM 加载完成时执行
document.addEventListener("DOMContentLoaded", function () {
    // 显示页面名
    document.querySelector("#页面名").textContent = 页面名;
    初始化多页面();
    页面配置标签页();
});