from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


# Chat Room login form
class TicketForm(Form):
    """Accepts a nickname and a room."""
    email = StringField('Enter your Email', validators=[Required()])
    room = TextAreaField('Subject of Chat', validators=[Required()])
    submit = SubmitField('Submit Issue')
