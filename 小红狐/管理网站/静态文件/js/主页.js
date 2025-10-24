// 页面缓存，保存已打开的页面 URL
let pageCache = [];

// 当前激活的页面 URL
let currentPage = null;

/**
 * 打开页面
 * @param {string} url 页面 URL
 */
function openPage(url) {
    // 如果页面已经打开，则什么都不做
    if (currentPage === url) {
        return;
    }
    // 如果页面已经打开过，显示页面
    if (pageCache.includes(url)) {
        // 显示页面
        document.getElementById(url).style.display = 'block';
        // 隐藏之前打开的页面
        if (currentPage) {
            document.getElementById(currentPage).style.display = 'none';
        }
        // 更新当前页面
        currentPage = url;
        return;
    }
    // 如果页面未打开，则新建一个页面
    const newIframe = document.createElement('iframe');
    newIframe.src = url;
    newIframe.id = url;
    // 隐藏旧页面
    if (currentPage) {
        document.getElementById(currentPage).style.display = 'none';
    }
    // 显示新页面
    document.getElementById('content-iframe').appendChild(newIframe);
    // 更新当前页面
    currentPage = url;
    // 缓存页面
    pageCache.push(url);
}

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
    
    // 事件委托阻止 #nav 下链接 a.open-page 点击事件冒泡
    nav.addEventListener('click', function (event) {
        if (event.target.tagName === 'A') {
            // 进一步判断该 <a> 是否包含 class="open-page"
            if (event.target.classList.contains('open-page')) {
                event.preventDefault(); // 阻止默认跳转行为

                let href = event.target.getAttribute('href'); // 获取链接地址
                openPage(href);

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
                页面列表元素.innerHTML = 页面名数组.map(页面名 => `<li><a href="#${页面名}" class="open-page">${页面名}</a></li>`).join('');
            })
            .catch(错误 => {
                console.error('获取页面名失败:', 错误);
            }
        );
    }
    更新页面名();
    window.更新页面名 = 更新页面名;
});
