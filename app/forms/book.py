from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired, length, NumberRange


class SearchForm(Form):
    query = StringField(validators=[DataRequired(), length(min=1, max=20)])
    page = IntegerField(validators=[NumberRange(min=1, max=13)], default=1)