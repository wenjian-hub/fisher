from flask import Flask
from app.models.book import db

# 导入插件
from flask_login import LoginManager

# 初始化插件
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.setting")
    app.config.from_object("app.secure")

    # 注册蓝图
    register_blueprint(app)
    
    # 插件注入核心对象app
    login_manager.init_app(app)
    login_manager.login_view = "web.login"
    login_manager.login_message = "请先登录或者注册账号"

    # 初始化数据库
    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)



