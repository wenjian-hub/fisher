from app.forms.auth import RegisterForm, LoginForm, EmailForm, RestPasswordForm, ChangePasswordForm
from app.models.base import db
from app.models.user import User
from app.web import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user


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
    form = EmailForm(request.form)
    if request.method == "POST":
        if form.validate():
            account_eamil = form.email.data
            user = User.query.filter_by(email=account_eamil).first_or_404()
            # first_or_404() , 如果user没有查询到数据，就不会执行后续的代码
            from app.libs.email import send_mail
            send_mail(form.email.data, "重置您的密码", "email/reset_password.html", user=user, token=user.generate_token())
            flash("重置邮件已发送" + account_eamil + "中，请注意查收")
            # return redirect(url_for("web.login"))
    return render_template("auth/forget_password_request.html", form=form)


@web.route("/reset/password/<token>", methods=["GET", "POST"])
def forget_password(token):
    form = RestPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash("密码已重置，请使用新密码登录")
            return redirect(url_for("web.login"))
        else:
            flash("重置密码失败")
    return render_template("auth/forget_password.html", form=form)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            current_user.password = form.new_password1.data
        flash('密码已更新成功')
        return redirect(url_for('web.personal'))
    return render_template('auth/change_password.html', form=form)


@web.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("web.index"))

