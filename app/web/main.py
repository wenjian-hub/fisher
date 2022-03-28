from flask import render_template
from flask_login import current_user

from app.models.gift import Gift
from app.view_models.book import BookViewMode
from app.web import web


@web.route("/")
def index():
    recent_gifts = Gift.recent()
    books = [BookViewMode(gift.book) for gift in recent_gifts]
    return render_template("index.html", recent=books)


@web.route("/personal")
def personal_center():
    return render_template("personal.html", user=current_user.summary)