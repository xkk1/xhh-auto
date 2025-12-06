// 检查是否为移动端
function 是否移动端() {
    // 获取根元素的 CSS 变量 --是否移动端 的值
    const rootStyles = getComputedStyle(document.documentElement);
    const 是否移动端值 = rootStyles.getPropertyValue('--是否移动端').trim(); // 得到 "0" 或 "1"
    
    const 是否移动端 = 是否移动端值 === '1'; // 转为布尔值
    return 是否移动端;
}

function 刷新页面列表() {
    const 页面列表元素 = document.getElementById("页面列表");
    const 刷新页面列表按钮 = document.getElementById("刷新页面列表按钮");
    刷新页面列表按钮.classList.add("加载中");
    // 请求页面名
    小红狐.页面.获取页面名()
        .then(页面名数组 => {
            页面列表元素.replaceChildren();
            if (页面名数组.length > 0) {
                for (const 页面名 of 页面名数组) {
                    const li = document.createElement("li");
                    li.role = "none";
                    const a = document.createElement("a");
                    a.href = `./html/配置.html?页面名=${encodeURIComponent(页面名)}`;
                    a.textContent = 页面名;
                    a.classList.add("打开页面");
                    a.role = "tab";
                    li.appendChild(a);
                    页面列表元素.appendChild(li);
                }
            } else {
                页面列表元素.textContent = "无页面，请先新建页面！";
            }
        })
        .catch(错误 => {
            console.error('获取页面名失败:', 错误);
            页面列表元素.textContent = '获取页面列表失败！\n' + 错误;
        }
        ).finally(() => {
            刷新页面列表按钮.classList.remove("加载中");
        });
}

// 新建页面
async function 新建页面() {
    const 新建页面按钮 = document.getElementById('新建页面按钮');
    const 页面名 = await 小红狐工具.对话框.输入('请输入页面名：');
    if (!页面名) {
        return;
    }
    新建页面按钮.classList.add("加载中");
    小红狐.页面.新增页面名(页面名)
        .then(async (响应) => {
            刷新页面列表();
            await 小红狐工具.对话框.提示(响应);
        })
        .catch(async error => {
            console.error("新增页面名失败：", error);
            await 小红狐工具.对话框.提示("新增页面名失败：" + error);
        })
        .finally(() => {
            新建页面按钮.classList.remove("加载中");
        });
}

// DOM 加载完成时执行
document.addEventListener('DOMContentLoaded', function () {
    // 侧边栏切换
    const 切换侧边栏按钮 = document.getElementById('切换侧边栏按钮');
    const 侧边栏容器 = document.getElementById('侧边栏容器');
    const 侧边栏 = document.getElementById('侧边栏');
    let 切换侧边栏 = function () {
        侧边栏容器.classList.toggle('收起');  // 切换 收起 类
        // 可选：根据状态更改按钮文字
        if (侧边栏容器.classList.contains('收起')) {
            切换侧边栏按钮.textContent = '展开侧边栏';
        } else {
            切换侧边栏按钮.textContent = '收起侧边栏';
        }
    };
    // 暴露 切换侧边栏 函数
    window.切换侧边栏 = 切换侧边栏;
    // 绑定点击事件
    切换侧边栏按钮.addEventListener('click', 切换侧边栏);
    // 侧边栏 wrap 点击收起
    侧边栏容器.addEventListener('click', function (event) {
        if (event.target === 侧边栏容器) {
            切换侧边栏();
        }
    });

    // 多页面
    window.多页面 = 小红狐工具.获取多页面(document.getElementById('iframe容器'));
    function 打开页面(页面名) {
        多页面.打开页面(页面名);
        if (是否移动端()) {
            切换侧边栏(); // 在移动端时，点击链接后自动收起侧边栏
        }
    }
    小红狐工具.多页面切换(侧边栏, 打开页面);

    // 更新显示所有页面名
    刷新页面列表();

    const 总控链接元素 = document.querySelector('#总控链接');
    总控链接元素?.click();
});
