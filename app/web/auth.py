from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from app.web import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user


@web.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        with db.auto_commit():
            # 模型操作
            user = User()

            # 客户端数据提交到model模型  User
            user.set_attr(form.data)

            # 数据库操作，数据库关联模型
            db.session.add(user)

        return redirect(url_for("web.login"))
        # 密码加密
        # user.set_attr(form.data)
        # user.password = generate_password_hash(user.password.data)

    return render_template("auth/register.html", form=form)


@web.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    print(form.data)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # remeber = True 免登陆
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or next.startswith("/"):
                next = url_for("web.index")
            return redirect(next)
        else:
            flash("账号或密码不正确")
    return render_template("auth/login.html", form=form)


@web.route("/reset/password", methods=["GET", "POST"])
def forget_password_request():
    pass


@web.route("/reset/password/<token>", methods=["GET", "POST"])
def forget_password(token):
    pass