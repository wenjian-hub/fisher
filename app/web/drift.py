from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewMode
from app.view_models.drift import DriftCollection
from app.web import web
from app.forms.book import DriftForm


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_yourself_gift(current_user.id):
        flash("该书籍您已拥有，不能进行索要")
        return redirect(url_for("web.book_detail", isbn=current_gift.isbn))

    can = current_user.can_send_drift()

    if not can:
        return render_template("not_enough_beans.html", beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == "POST" and form.validate():
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, "有人想要一本书", "email/get_gift.html", wisher=current_user, gift=current_gift)
        return redirect(url_for("web.pending"))
    # Gift 关联 User
    gifter = current_gift.user.summary
    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans, form=form)


@web.route("/pending")
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id))\
        .order_by(desc(Drift.create_time)).all()
    view = DriftCollection(drifts, current_user.id)
    return render_template("pending.html", drifts=view.data)


@web.route("/drift/<int:did>/redraw")
@login_required
def redraw_drift(did):
    """
    撤销按钮
    安全问题：越权

    """
    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404(description="drift is null")
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for("web.pending"))


@web.route("/drift/<int:did>/reject")
@login_required
def reject_drift(did):
    """
    书籍赠送着才能拒绝
    """
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id, Gift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for("web.pending"))


@web.route("/drift/<int:did>/mailed")
@login_required
def mailed_drift(did):
    """邮寄书籍"""
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1

        # 数据库更新两种写法
        gift = Gift.query.filter_by(id=drift.gifter_id).first_or_404()
        gift.launched = True

        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id, launched=True).update({Wish.launched: True})
    return redirect(url_for("web.pending"))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        """
        populate_obj
        模型和表单字段需要保持一致，才能复制
        """
        drift_form.populate_obj(drift)
        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewMode(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        current_user.beans -= 1
        db.session.add(drift)
