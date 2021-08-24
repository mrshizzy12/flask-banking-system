from flask import render_template, redirect, url_for, flash, request, current_app
from . import auth
from werkzeug.urls import url_parse
from app import db
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegisterForm, LoginForm
from random import randint
from app.models import *


def generate_account_no():
    num = ''.join([f"{randint(0, 9)}" for _ in range(0, 10)])
    return int(num)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('transaction.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            new_user = User(
                username=form.username.data, 
                email=form.email.data, 
                password=form.password.data
            )        

            accout_details = UserBankAccount(
                account_no=generate_account_no(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone_number=form.phone_number.data,
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data

            )

            address = UserAddress(
                country=form.country.data,
                city=form.city.data,
                street_address=form.street_address.data
            )

           
            db.session.add_all([accout_details, address])
            db.session.commit()

            new_user.account = accout_details
            new_user.address = address
            
            if new_user.email in current_app.config['ADMINS']:
                new_user.is_admin = True
                
            db.session.add(new_user)
            db.session.commit()
            
            flash('''Thank You For Creating A Bank Account {}.
                    Your Account Number is {}, Please use this number to login
                    s'''.format(new_user.full_name, new_user.account.account_no), 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            flash('Registration failed, please try again later', 'danger')
            return redirect(url_for('auth.register'))
        
    context = {
        'title': 'Create a Bank Account',
        'form': form,
    }

    return render_template('auth/register.html', **context)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('transaction.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'warning')
            return redirect(url_for('auth.login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('transaction.index')
        login_user(user, remember=form.remember_me.data)
        flash('Welcome, {}!'.format(user.full_name), 'success')
        return redirect(next_page)

    context = {
        'form': form,
        'title': "Load Account Details"
    }
    return render_template('auth/login.html', **context)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))