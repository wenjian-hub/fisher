from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_eamil(app, msg):
    # 需要将创建的线程注入flask栈中
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e


def send_mail(to, subject, template, **kwargs):
    # msg = Message("邮件测试", sender="709889894@qq.com", body="Test", recipients=["2180199696@qq.com"])
    msg = Message("[wenjian]" + " " + subject, sender=current_app.config["MAIL_USERNAME"], recipients=[to])
    msg.html = render_template(template, **kwargs)

    """  
    current_app._get_current_object()  返回当前的核心对象，这个核心对象，可以用于不同的上下文
    """
    app = current_app._get_current_object()

    # 创建一个线程
    thread = Thread(target=send_async_eamil, args=[app, msg])
    thread.start()
