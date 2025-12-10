function 添加标签页(url, 标题, 打开页面=false) {
    if (打开页面) {
        window.open(url, '_blank');
        return;
    }
}