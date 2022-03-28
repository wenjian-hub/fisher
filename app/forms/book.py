from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, length, Regexp


class SearchForm(Form):
    query = StringField(validators=[DataRequired(), length(min=1, max=20)])
    page = IntegerField(validators=[NumberRange(min=1, max=13)], default=1)


class DriftForm(Form):
    recipient_name = StringField("收件人姓名", validators=[DataRequired(), Length(min=2, max=20, message=" 收件人长度为2~20")])
    mobile = StringField("手机号", validators=[DataRequired(), Regexp('^1[0-9]{10}$', 0, message="请输入正确的手机号")])
    message = StringField("留言")
    address = StringField("邮寄地址", validators=[DataRequired(), Length(min=2, max=70, message="邮寄地址在2~70个字，请重新填写")])