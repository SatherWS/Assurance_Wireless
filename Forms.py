from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required

class TicketForm(Form):
    """ Form to create a new ticket """
    contact = StringField('Enter your Email', validators=[Required()])
    title = TextAreaField('Type any additional information here (optional)')
    category = SelectField(
            'Categories',
            choices=[('category a', 'category a'), ('category b', 'category b'), ('category c', 'category c')]
        )
    submit = SubmitField('Submit Issue')

class MessageForm(Form):
    """ Message form sent by employee users """
    msg = StringField('Enter Message', validators=[Required()])
    submit = SubmitField('Submit Message')
