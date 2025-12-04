// ==UserScript==
// @name         全屏鼠标坐标监听
// @namespace    http://tampermonkey.net/
// @version      2025-12-04
// @description  监听并在控制台显示全屏鼠标坐标，支持点击和左键拖动
// @author       小喾苦
// @match        *://*/*
// @grant        none
// ==/UserScript==


(function () {
    'use strict';

    // 仅在顶层窗口运行，iframe 中不生效
    if (window.top !== window.self) {
        return;
    }

    let isDragging = false;
    let startPoint = null;
    const MOVE_THRESHOLD = 4;

    // 定义具名事件处理函数（必须是同一个引用才能 remove）
    function handleMouseDown(e) {
        if (e.button !== 0) return;
        startPoint = { x: e.clientX, y: e.clientY };
        isDragging = false;
    }

    function handleMouseMove(e) {
        if (!startPoint) return;
        if (!isDragging) {
            const dx = e.clientX - startPoint.x;
            const dy = e.clientY - startPoint.y;
            if (Math.sqrt(dx * dx + dy * dy) > MOVE_THRESHOLD) {
                isDragging = true;
            }
        }
    }

    function handleMouseUp(e) {
        if (!startPoint) return;

        if (isDragging) {
            console.log('【拖动】起点:', startPoint, '终点:', { x: e.clientX, y: e.clientY });
        } else {
            console.log('【点击】位置:', { x: e.clientX, y: e.clientY });
        }

        startPoint = null;
        isDragging = false;
    }

    function handleMouseLeave() {
        startPoint = null;
        isDragging = false;
    }

    // 添加监听器
    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mouseleave', handleMouseLeave);

    // 暴露关闭函数到全局（可通过控制台调用）
    window.stopMouseDragClickListener = function () {
        // 移除所有监听器
        document.removeEventListener('mousedown', handleMouseDown);
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
        document.removeEventListener('mouseleave', handleMouseLeave);

        // 清理状态
        isDragging = false;
        startPoint = null;

        // 可选：从 window 移除自身（避免污染）
        delete window.stopMouseDragClickListener;

        console.log('✅ 鼠标点击/拖动监听已关闭');
        return true;
    };

})();
