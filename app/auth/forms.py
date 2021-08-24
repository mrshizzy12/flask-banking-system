from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError, InputRequired
from wtforms.fields.html5 import DateField
from app.models import User, UserBankAccount
import phonenumbers



class RegisterForm(FlaskForm):
    username = StringField('user name', validators=[DataRequired(), Length(min=5, max=20)])
    first_name = StringField('first name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name  = StringField('last name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('email', validators=[DataRequired(), Email()])
    gender = SelectField('gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = DateField('date of birth(yyyy-mm-dd)', validators=[InputRequired()])
    country = StringField('country', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    street_address = TextAreaField('street address', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 =  PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already exist, please pick another email.')

    def validate_username(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user:
            raise ValidationError('user already exist, please pick another user name.')

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
            if UserBankAccount.query.filter_by(phone_number=phone_number.data).first():
                raise ValidationError('Phone number already exist.')
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    username = StringField('user name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Log in')