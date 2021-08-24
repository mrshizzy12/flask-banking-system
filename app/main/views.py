from flask import render_template, url_for, redirect
from . import main
from flask_login import current_user



@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('transaction.index'))
    return render_template('main/home.html')