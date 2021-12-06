
from app import mail
from flask_mail import Message


def send_mail():
    msg = Message("邮件测试", sender="709889894@qq.com", body="Test", recipients=["2180199696@qq.com"])
    mail.send(msg)
