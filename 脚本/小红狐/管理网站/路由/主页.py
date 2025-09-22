from flask import Blueprint, render_template


主页蓝图 = Blueprint('主页', __name__)

@主页蓝图.route('/')
def 主页():
    return render_template('主页.html')  # 假设你有这个模板
