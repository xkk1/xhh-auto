function 添加标签页(url, 标题, 打开页面=false) {
    let 标签页元素 = document.querySelector("ul#标签页");
    if (!标签页元素) return false;
    let 旧a = 标签页元素.querySelector("a[href='" + url + "']");
    if (旧a) {
        旧a.textContent = 标题;
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
    }
    if (打开页面) {
        标签页元素.querySelector("a[href='" + url + "']").click();
    }
    return true;
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

// 非主按钮标签页配置
function 非主按钮标签页关闭() {
    let 标签页元素 = document.querySelector("ul#标签页");
    标签页元素.addEventListener('auxclick', function (event) {
        if (event.target.tagName === 'A') {
            // 进一步判断该 <a> 是否包含 class="打开页面"
            if (event.target.classList.contains('打开页面')) {
                event.preventDefault(); // 阻止默认跳转行为
                let url = event.target.getAttribute('href'); // 获取链接地址
                删除标签页(url);
            }
        }
    });
}

function 初始化拖拽标签页(标签页URL排序更改回调) {
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
        if (!拖拽元素 || 事件.target === 标签页元素 || 事件.target === 拖拽元素 ||事件.target.parentNode === 拖拽元素) {
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
        拖拽元素 = null;
        const 子元素数组 = Array.from(标签页元素.children);
        const 页面URL排序 = 子元素数组.map(function (元素) {
            return 元素.querySelector("a").getAttribute('href');
        });
        // console.log(配置页面URL排序);
        标签页URL排序更改回调(页面URL排序);
    };
    标签页元素.ondrop = (事件) => {
        事件.preventDefault();
        if (拖拽元素) return;
        url = 事件.dataTransfer.getData("text/plain");
        // 验证 url
        if (!url) return;
        try {
            new URL(url);
        } catch (错误) {
            return;
        }
        // 请求用户输入添加标签页标题
        let 标题 = window.prompt(url + "\n请输入标签页标题：");
        if (标题) {
            // 添加标签页
            添加标签页(url, 标题);
        }
    };
    非主按钮标签页关闭();
}