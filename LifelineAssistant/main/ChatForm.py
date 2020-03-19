from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


# Real time chat room login form -- NOT IN USE
class TicketForm(Form):
    """Accepts a nickname and a room."""
    nonuser_email = StringField('Enter your Email', validators=[Required()])
    room = TextAreaField('Subject of Chat', validators=[Required()])
    submit = SubmitField('Submit Issue')

class CommentForm(Form):
    """ Accepts email, ticket title and additional description """
    contact = StringField('Enter your Email', validators=[Required()])
    title = StringField('Type a brief description of your problem')
    info = TextAreaField('Type any additional information here (optional)')
    submit = SubmitField('Submit Issue')
