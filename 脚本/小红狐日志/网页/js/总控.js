async function 刷新日志渠道列表() {
    const 日志渠道列表元素 = document.getElementById("日志渠道列表");
    const URL = "/api/脚本/路由/小红狐日志/api/日志/渠道名"
    fetch(URL)
        .then(response => response.json())
        .then(data => {
            // 清空列表
            日志渠道列表元素.replaceChildren();
            // 添加列表项
            data.forEach(渠道名 => {
                const listItem = document.createElement("li");
                const aElement = document.createElement("a");
                aElement.href = `/api/目录/脚本/小红狐日志/网页/实时.html?渠道名=${encodeURIComponent(渠道名)}`
                aElement.textContent = 渠道名;
                aElement.target = "_blank";
                aElement.classList.add("渠道链接");
                listItem.appendChild(aElement);
                日志渠道列表元素.appendChild(listItem);
            });
        })
        .catch(error => {
            日志渠道列表元素.textContent = "获取日志渠道列表失败！\n" + error;
        })
}

function 初始化日志渠道列表事件委托() {
    const 日志渠道列表元素 = document.getElementById("日志渠道列表");
    日志渠道列表元素.addEventListener("click", function (event) { 
        if (event.target.tagName === 'A' && parent !== window) {
            if (event.target.classList.contains('渠道链接')) {
                event.preventDefault(); // 阻止默认跳转行为

                const href = event.target.getAttribute('href'); // 获取链接地址
                const 渠道名 = event.target.textContent
                parent.添加标签页(href, 渠道名 + " - 实时日志", true);
            }
        }
    });
    
}


document.addEventListener("DOMContentLoaded", async function () {
    初始化日志渠道列表事件委托();
    await 刷新日志渠道列表();
});