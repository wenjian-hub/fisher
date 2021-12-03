from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from app.web import web

"""
@login_required 装饰器判断用户是否登录，没有登录，不能执行下一步操作
权限分级

current_user 是实例化的User模型
"""


@web.route("/my/gifts")
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_count(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template("my_gifts.html", gifts=view_model.gifts)


@web.route("/gifts/book/<isbn>")
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            db.session.add(gift)
    else:
        flash("书籍已添加在心愿清单中或者已在您赠送清单中")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route("/123")
def redraw_from_gifts():
    pass

