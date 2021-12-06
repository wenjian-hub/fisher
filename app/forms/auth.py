
from wtforms import Form, PasswordField, StringField
from wtforms.validators import Length, DataRequired, Email, ValidationError

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    password = StringField(validators=[DataRequired(message="密码不能为空，请重新输入"), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message="昵称最少2个字符，最多10个字符")])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("昵称已存在")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    password = StringField(validators=[DataRequired(message="密码不能为空，请重新输入"), Length(6, 32)])

    def validate_email(self, field):
        userInfo = User.query.filter_by(email=field.data).first()
        if not userInfo:
            raise ValidationError("请检查账号和密码是否正确")


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮件格式错误，请重新输送")])