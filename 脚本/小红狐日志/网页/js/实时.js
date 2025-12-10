const urlParams = new URLSearchParams(window.location.search);
const 渠道名 = urlParams.get('渠道名') || '小红狐通知';
document.title = 渠道名 + ' - ' + document.title;

function 开始接收实时日志() {
    const 日志容器 = document.getElementById('日志容器');
    const URL = `/api/脚本/路由/小红狐日志/api/日志/服务器发送事件?渠道名=${encodeURIComponent(渠道名)}&显示历史上限=64`
    const 服务器发送事件 = new EventSource(URL);

    服务器发送事件.onmessage = function(event) {
        console.log(event.data);
        const 日志元素 = document.createElement('pre');
        日志元素.textContent = event.data;
        日志容器.appendChild(日志元素);
        日志容器.scrollTop = 日志容器.scrollHeight; // 自动滚动到底部
    };

    服务器发送事件.onerror = function() {
        console.error('EventSource failed.');
    };
}

document.addEventListener('DOMContentLoaded', function () {
    开始接收实时日志();
})