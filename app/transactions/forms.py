from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError



class DepositForm(FlaskForm):
    amount = IntegerField('amount', validators=[DataRequired()])
    #submit = SubmitField('Deposit')


class WithdrawalForm(FlaskForm):
    amount = IntegerField('amount', validators=[DataRequired()])

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def validate_amount(self, amount):
        if self.user.account.balance < amount.data:
            raise ValidationError('You Can Not Withdraw More Than Your Balance.')