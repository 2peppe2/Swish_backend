from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField 
from wtforms.validators import DataRequired,Length

class CreatePaymentForm(FlaskForm):
    payeePaymentReference = StringField('payeePaymentReference', validators=[DataRequired()])
    payerAlias = StringField('payerAlias', validators=[DataRequired(), Length(min=8, max=15)])
    amount = IntegerField('amount', validators=[DataRequired()])
    message = StringField('message', validators=[DataRequired(), Length(min=1, max=50)])