// 检查是否为移动端
function isMobile() {
    // 获取根元素的 CSS 变量 --is-mobile 的值
    const rootStyles = getComputedStyle(document.documentElement);
    const isMobileValue = rootStyles.getPropertyValue('--is-mobile').trim(); // 得到 "0" 或 "1"
    
    const isMobile = isMobileValue === '1'; // 转为布尔值
    return isMobile;
}

// DOM 加载完成时执行
document.addEventListener('DOMContentLoaded', function () {
    // 侧边栏切换
    const toggleBtn = document.getElementById('toggle-nav-btn');
    const navWrap = document.getElementById('nav-wrap');
    const nav = document.getElementById('nav');
    let toggleNav = function () {
        navWrap.classList.toggle('collapsed');  // 切换 collapsed 类
        // 可选：根据状态更改按钮文字
        if (navWrap.classList.contains('collapsed')) {
            toggleBtn.textContent = '展开侧边栏';
        } else {
            toggleBtn.textContent = '收起侧边栏';
        }
    };
    toggleBtn.addEventListener('click', toggleNav);
    // 侧边栏 wrap 点击收起
    navWrap.addEventListener('click', function (event) {
        if (event.target === navWrap) {
            toggleNav();
        }
    });

    // 多页面
    window.多页面 = 小红狐工具.获取多页面(document.getElementById('content-iframe'));
    window.打开页面 = window.多页面.打开页面;
    // 事件委托阻止 #nav 下链接 a.打开页面 点击事件冒泡
    nav.addEventListener('click', function (event) {
        if (event.target.tagName === 'A') {
            // 进一步判断该 <a> 是否包含 class="打开页面"
            if (event.target.classList.contains('打开页面')) {
                event.preventDefault(); // 阻止默认跳转行为

                let href = event.target.getAttribute('href'); // 获取链接地址
                打开页面(href);

                if (isMobile()) {
                    toggleNav(); // 在移动端时，点击链接后自动收起侧边栏
                }
            }
        }
    });

    // 更新显示所有页面名
    let 页面列表元素 = document.querySelector('ul#页面列表');
    function 更新页面名() {
        // 请求页面名
        小红狐.获取页面名()
            .then(页面名数组 => {
                页面列表元素.innerHTML = 页面名数组.map(页面名 => `<li><a href="#${页面名}" class="打开页面">${页面名}</a></li>`).join('');
            })
            .catch(错误 => {
                console.error('获取页面名失败:', 错误);
            }
        );
    }
    更新页面名();
    window.更新页面名 = 更新页面名;
});
