from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


class CreatePaymentForm(FlaskForm):
    class Meta:
        csrf = False

    payeePaymentReference = StringField(
        "payeePaymentReference",
        validators=[DataRequired(message="payeePaymentReference is required")],
    )
    payerAlias = StringField(
        "payerAlias",
        validators=[
            DataRequired(message="payerAlias is required"),
            Length(
                min=8, max=15, message="payerAlias must be between 8 and 15 characters"
            ),
        ],
    )
    amount = IntegerField(
        "amount", validators=[DataRequired(message="amount is required")]
    )
    message = StringField(
        "message",
        validators=[
            Length(min=0, max=50, message="message must be between 0 and 50 characters")
        ],
    )
    redirectCallbackUrl = StringField(
        "redirectCallbackUrl",
        validators=[DataRequired(message="redirectCallbackUrl is required")],
    )


class CancelPaymentForm(FlaskForm):
    class Meta:
        csrf = False

    id = StringField(
        "id",
        validators=[DataRequired(message="id is required"), Length(min=32, max=32)],
    )


class StartPaymentForm(FlaskForm):
    class Meta:
        csrf = False

    id = StringField(
        "id",
        validators=[DataRequired(message="id is required"), Length(min=32, max=32)],
    )
    phoneNumber = StringField(
        "phoneNumber",
        validators=[
            DataRequired(message="phoneNumber is required"),
            Length(min=8, max=15),
        ],
    )

class StatusPaymentForm(FlaskForm):
    class Meta:
        csrf = False

    id = StringField(
        "id",
        validators=[DataRequired(message="id is required"), Length(min=32, max=32)],
    )
