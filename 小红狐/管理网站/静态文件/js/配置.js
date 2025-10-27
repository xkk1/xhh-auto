// 获取页面名
let 页面名 = 小红狐工具.获取Get参数("页面名") || "页面名六个字";
// 标题添加页面名
document.title = 页面名 + "-" + document.title;

// 获取并设置页面配置标签页
function 页面配置标签页() {
    let 标签页元素 = document.querySelector("ul#标签页");
    标签页元素.innerHTML = ""
    小红狐.获取页面配置标签页(页面名=页面名)
        .then(function (配置标签页) {
            for (let 标签页 of 配置标签页) {
                let a = document.createElement("a");
                a.href = 标签页.url;
                a.textContent = 标签页.标题;
                a.role = "tab";
                let li = document.createElement("li");
                li.appendChild(a);
                li.role = "none";
                标签页元素.appendChild(li);
            }
            document.querySelector("#header").style.display = "block";
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
    页面配置标签页();

});