from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.wish import Wish
from app.view_models.trade import MyTrade
from app.web import web


@web.route("/my/wish")
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_count(isbn_list)
    view_model = MyTrade(wishes_of_mine, gift_count_list)
    return render_template("my_wish.html", wishes=view_model.trades)


@web.route("/wish/book/<isbn>")
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():

            # wish 先模型化
            wish = Wish()

            # wish表字段赋值
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash("书籍已添加在心愿清单中或者已在您赠送清单中")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route("/redraw_from_wish")
def redraw_from_wish():
    pass
