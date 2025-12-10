const urlParams = new URLSearchParams(window.location.search);
const 渠道名 = urlParams.get('渠道名') || '小红狐通知';
document.title = 渠道名 + ' - ' + document.title;

let 显示最新 = true;

function 开始接收实时日志() {
    const 日志容器 = document.getElementById('日志容器');
    const URL = `/api/脚本/路由/小红狐日志/api/日志/服务器发送事件?渠道名=${encodeURIComponent(渠道名)}&显示历史上限=256`
    const 服务器发送事件 = new EventSource(URL);

    服务器发送事件.onmessage = function(event) {
        console.log(event.data);
        const 日志元素 = document.createElement('pre');
        日志元素.classList.add('日志');
        日志元素.textContent = event.data;
        日志容器.appendChild(日志元素);
        if (日志容器.children.length > 256) {
            日志容器.removeChild(日志容器.firstElementChild);
        }
        if (显示最新) {
            日志容器.scrollTop = 日志容器.scrollHeight; // 自动滚动到底部
        }
    };

    服务器发送事件.onerror = function() {
        console.error('EventSource failed.');
    };
}

function 初始化切换显示最新按钮() {
    const 切换显示最新按钮 = document.getElementById('切换显示最新');
    切换显示最新按钮.addEventListener('click', function () {
        显示最新 = !显示最新;
        切换显示最新按钮.textContent = 显示最新 ? '取消显示最新' : '自动显示最新';
    });
}

document.addEventListener('DOMContentLoaded', function () {
    初始化切换显示最新按钮();
    开始接收实时日志();
})