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
});
