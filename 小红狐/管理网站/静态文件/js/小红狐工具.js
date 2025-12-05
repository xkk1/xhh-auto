// 小红狐工具函数 IIFE（立即调用函数表达式）
(function (全局对象) {
    // 私有函数：执行实际的 HTTP 请求
    function 执行请求(请求方式, 网址, 数据 = null, 查询参数 = {}) {
        let 请求网址 = 网址;

        // 如果是 GET 请求，且带有查询参数，则拼接到 URL 上
        if (请求方式 === 'GET' && Object.keys(查询参数).length > 0) {
            const 查询字符串 = new URLSearchParams(查询参数).toString();
            请求网址 = `${网址}?${查询字符串}`;
        }

        const 请求配置 = {
            method: 请求方式, // GET, POST, PUT, DELETE
            headers: {
                'Content-Type': 'application/json',
            },
        };

        // 如果不是 GET 请求，并且有数据，则放入请求体中
        if (数据 !== null && 请求方式 !== 'GET') {
            请求配置.body = JSON.stringify(数据);
        }

        return fetch(请求网址, 请求配置)
            .then((响应) => {
                if (!响应.ok) {
                    // 如果响应失败（如 4xx, 5xx），尝试解析错误信息并 reject
                    return 响应.json().then((错误信息) => Promise.reject(错误信息));
                }

                const 内容类型 = 响应.headers.get('content-type');
                if (内容类型 && 内容类型.includes('application/json')) {
                    return 响应.json(); // 解析 JSON 数据
                }
                return 响应.text(); // 或者返回文本
            })
            .catch((错误) => {
                console.error('[请求工具] 请求出错:', 错误);
                return Promise.reject(错误);
            });
    }

    // 对外提供的 RESTful 中文接口
    const 请求 = {
        获取: (网址, 查询参数) => 执行请求('GET', 网址, null, 查询参数),           // 查
        新增: (网址, 数据) => 执行请求('POST', 网址, 数据),                       // 增
        修改: (网址, 数据) => 执行请求('PUT', 网址, 数据),                        // 改
        删除: (网址, 数据) => 执行请求('DELETE', 网址, 数据),                     // 删
        执行: 执行请求,  // 执行 HTTP 请求
    };

    // 获取 URL 的 GET 参数
    function 获取Get参数(参数名) {
        参数名 = decodeURIComponent(参数名);
        let 查询字符串 = window.location.search.substring(1);
        let 参数列表 = 查询字符串.split("&");
        for (let 索引 = 0; 索引 < 参数列表.length; 索引++) {
            let 键值对 = 参数列表[索引].split("=");
            if (decodeURIComponent(键值对[0]) == 参数名) {
                return decodeURIComponent(键值对[1]);
            }
        }
        return null;
    }

    // 修改 URL 的 GET 参数
    function 修改Get参数(参数名, 参数值) {
        参数名 = decodeURIComponent(参数名);
        let 查询字符串 = window.location.search.substring(1);
        let 键值对列表 = 查询字符串.split("&");
        let 存在参数 = false;
        for (let 索引 = 0; 索引 < 键值对列表.length; 索引++) {
            let 键值对 = 键值对列表[索引].split("=");
            if (decodeURIComponent(键值对[0]) == 参数名) {
                // 如果已经存在该参数，则更新参数值
                键值对列表[索引] = encodeURIComponent(参数名) + "=" + encodeURIComponent(参数值);
                存在参数 = true;
                break;
            }
        }
        if (!存在参数) {
            // 如果不存在该参数，则添加参数
            键值对列表.push(encodeURIComponent(参数名) + "=" + encodeURIComponent(参数值));
        }
        // 构建新的 URL
        let 新的URL = window.location.origin + window.location.pathname + "?" + 键值对列表.join("&") + window.location.hash;
        window.history.replaceState({}, "", 新的URL);
    }

    /**
     * 复制文字到剪贴板
     * 
     * @param {string} 要复制的文字 要复制的文字
     */
    let 复制文字到剪贴板 = function (要复制的文字) { };
    // 判断是否支持现代剪贴板 API
    if (navigator.clipboard) {
        // 如果支持，使用现代 API
        复制文字到剪贴板 = function (要复制的文字) {
            navigator.clipboard.writeText(要复制的文字);
        };
    } else {
        // 如果不支持，使用传统 execCommand 方式
        复制文字到剪贴板 = function (要复制的文字) {
            let 临时文本框 = document.createElement("textarea");
            // 为了避免影响原页面布局，不建议隐藏，或者可以设置 position: absolute + left: -9999px
            // 临时文本框.style.position = 'absolute';
            // 临时文本框.style.left = '-9999px';
            // 临时文本框.style.display = 'none'; // 如果要隐藏可以取消注释
            document.body.appendChild(临时文本框);
            临时文本框.value = 要复制的文字;
            临时文本框.select();
            // 执行复制命令
            document.execCommand("copy");
            // 移除临时元素
            document.body.removeChild(临时文本框);
        };
    }

    /**
     * 防抖函数 debounce
     * 频繁操作、耗时操作、仅关心最后一次操作
     * 
     * @param {function} fn 要防抖的函数
     * @param {number} duration 防抖时间
     * @returns {function} 防抖后的函数
     */
    function 防抖(fn, duration = 300) {
        let timerId = null;
        return function () {
            if (timerId) {
                clearTimeout(timerId);
            }
            let args = arguments;
            timerId = setTimeout(() => {
                fn.apply(this, args);
            }, duration);
        }
    }

    /**
     * 节流函数 throttle
     * 频繁操作、耗时操作、仅关心连续操作
     * 
     * @param {function} fn 要节流的函数
     * @param {number} duration 节流时间
     * @returns {function} 节流后的函数
     */
    function 节流(fn, duration = 300) {
        let lastTime = 0;
        return function () {
            let nowTime = Date.now();
            if (nowTime - lastTime > duration) {
                fn.apply(this, arguments);
                lastTime = nowTime;
            }
        }
    }

    function 获取多页面(iframe容器元素) {
        // 页面缓存，保存已打开的页面 URL 和 iframe 元素
        let 打开页面缓存 = {};

        // 当前激活的页面 URL
        let 当前页面URL = null;

        /**
         * 打开页面
         * @param {string} url 页面 URL
         */
        function 打开页面(url) {
            // 如果页面已经打开，则什么都不做
            if (当前页面URL === url) {
                return;
            }
            // 如果页面已经打开过，显示页面
            if (打开页面缓存.hasOwnProperty(url)) {
                // 显示页面
                打开页面缓存[url].style.display = 'block';
                // 隐藏之前打开的页面
                if (当前页面URL && 打开页面缓存.hasOwnProperty(当前页面URL)) {
                    打开页面缓存[当前页面URL].style.display = 'none';
                }
                // 更新当前页面
                当前页面URL = url;
                return;
            }
            // 如果页面未打开，则新建一个页面
            const 新建iframe元素 = document.createElement('iframe');
            新建iframe元素.src = url;
            新建iframe元素.id = url;
            // 隐藏旧页面
            if (当前页面URL) {
                打开页面缓存[当前页面URL].style.display = 'none';
            }
            // 显示新页面
            iframe容器元素.appendChild(新建iframe元素);
            // 更新当前页面
            当前页面URL = url;
            // 缓存页面
            打开页面缓存[url] = 新建iframe元素;
        }

        function 关闭页面(url) {
            url = url || 当前页面URL;
            // 如果页面未打开，则什么也不做
            if (!url || !打开页面缓存.hasOwnProperty(url)) {
                return null;
            }
            // 删除页面缓存
            打开页面缓存[url].remove();
            delete 打开页面缓存[url];
            // 如果关闭的是当前页面，则显示第一个打开的页面
            if (当前页面URL === url) {
                第一个URL = Object.keys(打开页面缓存)[0];
                if (第一个URL) {
                    打开页面(第一个URL);
                    return 第一个URL;
                }
            }
            return null;
        }

        function 获取当前页面URL() {
            return 当前页面URL;
        }

        function 获取打开页面列表() {
            return Object.keys(打开页面缓存);
        }

        return {
            打开页面: 打开页面,
            关闭页面: 关闭页面,
            获取当前页面URL: 获取当前页面URL,
            获取打开页面列表: 获取打开页面列表,
        };
    }

    function 多页面切换(标签页父元素, 打开页面) {
        let 选中元素 = null;
        标签页父元素.addEventListener('click', function (event) {
            if (event.target.tagName === 'A') {
                // 进一步判断该 <a> 是否包含 class="打开页面"
                if (event.target.classList.contains('打开页面')) {
                    event.preventDefault(); // 阻止默认跳转行为

                    let href = event.target.getAttribute('href'); // 获取链接地址
                    if (选中元素 && 选中元素 !== event.target) {
                        选中元素.classList.remove('选中'); // 移除之前选中的元素
                    }
                    event.target.classList.add('选中'); // 添加选中样式
                    选中元素 = event.target; // 记录当前选中的元素
                    打开页面(href);
                }
            }
        });
    }

    /**
     * 创建并显示基于 <dialog> 的模态对话框
     * @param {Object} options - 配置选项
     * @param {string} options.type - 对话框类型 ('alert', 'confirm', 'prompt')
     * @param {string} options.message - 显示的消息内容
     * @param {string} [options.title] - 对话框标题
     * @param {string} [options.defaultValue] - prompt 类型的默认值
     * @param {string} [options.confirmText] - 确认按钮文本
     * @param {string} [options.cancelText] - 取消按钮文本
     * @returns {Promise} - 返回一个 Promise，解析为用户操作结果
     */
    function createDialog(options) {
        return new Promise((resolve) => {
            // 创建 dialog 元素
            const dialog = document.createElement('dialog');
            dialog.className = '对话框';

            // 创建内容容器
            const content = document.createElement('div');
            content.className = '内容容器';

            // 如果提供了标题，则创建并添加标题元素
            if (options.title) {
                const title = document.createElement('h3');
                title.className = '标题';
                title.textContent = options.title;
                content.appendChild(title);
            }

            // 创建并添加消息内容元素
            const message = document.createElement('pre');
            message.className = '消息内容';
            message.textContent = options.message;
            content.appendChild(message);

            // 如果是 prompt 类型，则创建并添加输入框
            let input;
            if (options.type === 'prompt') {
                input = document.createElement('input');
                input.className = '输入框';
                input.type = 'text';
                input.value = options.defaultValue || '';
                input.placeholder = '请输入...';
                content.appendChild(input);
            }

            // 创建按钮区域容器
            const buttons = document.createElement('div');
            buttons.className = '按钮容器';

            // 如果不是 alert 类型（即 confirm 或 prompt），则添加取消按钮
            if (options.type !== 'alert') {
                const cancel = document.createElement('button');
                cancel.textContent = options.cancelText || '取消';
                cancel.className = '取消按钮';
                cancel.onclick = () => {
                    // 关闭对话框，并返回 false（confirm）或 null（prompt）
                    dialog.close();
                    resolve(options.type === 'prompt' ? null : false);
                };
                buttons.appendChild(cancel);
            }

            // 创建确认按钮
            const confirm = document.createElement('button');
            confirm.textContent = options.confirmText || '确定';
            confirm.className = '确认按钮';
            confirm.onclick = () => {
                // 关闭对话框，并根据类型返回相应结果
                dialog.close();
                if (options.type === 'prompt') {
                    // prompt 类型返回用户输入的值
                    resolve(input.value);
                } else {
                    // alert 类型返回 undefined，confirm 类型返回 true
                    resolve(options.type === 'alert' ? undefined : true);
                }
            };
            buttons.appendChild(confirm);

            // 将按钮区域添加到内容容器
            content.appendChild(buttons);
            // 将内容容器添加到 dialog
            dialog.appendChild(content);

            // 监听 dialog 关闭事件（例如按 ESC 键）
            dialog.addEventListener('close', () => {
                // 如果用户通过 ESC 或点击遮罩层关闭，则返回默认值
                if (options.type === 'alert') {
                    resolve(undefined);
                } else if (options.type === 'confirm') {
                    resolve(false);
                } else if (options.type === 'prompt') {
                    resolve(null);
                }
            });

            // 将 dialog 添加到页面 body
            document.body.appendChild(dialog);

            // 打开模态对话框
            dialog.showModal();

            // 如果是 prompt 类型，自动聚焦到输入框
            if (input) {
                input.focus();
            } else {
                // 否则聚焦到确认按钮
                confirm.focus();
            }
        });
    }

    const 对话框 = {
        提示: 
            async function(message, title = '提示') {
                return await createDialog({ type: 'alert', message, title });
            },
        确认:
            async function(message, title = '确认') {
                return await createDialog({ type: 'confirm', message, title });
            },
        输入:
            async function(message, defaultValue = '', title = '输入') {
                return await createDialog({ type: 'prompt', message, defaultValue, title });
            },
    }

    // 对外暴露的 小红狐工具 方法
    const 小红狐工具 = {
        请求: 请求,
        获取Get参数: 获取Get参数,
        修改Get参数: 修改Get参数,
        复制文字到剪贴板: 复制文字到剪贴板,
        防抖: 防抖,
        节流: 节流,
        获取多页面: 获取多页面,
        多页面切换: 多页面切换,
        对话框: 对话框,
    };

    // 将 小红狐工具 挂载到全局对象上（比如 window），这样外部可直接使用
    if (typeof 全局对象 !== 'undefined') {
        全局对象.小红狐工具 = 小红狐工具;
    }

})(typeof window !== 'undefined' ? window : this);
