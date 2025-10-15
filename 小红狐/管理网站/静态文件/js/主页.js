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

                var href = event.target.getAttribute('href'); // 获取链接地址
                console.log('阻止跳转，open-page 链接是：', href);

                // 你也可以弹窗提示或做其他逻辑
                // alert('特殊链接，地址为：' + href);
            }
        }
    });
});
