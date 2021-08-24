from . import transaction
from app import db
from datetime import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.transactions.forms import DepositForm, WithdrawalForm
from app.models import Deposit, Withdrawal, Interest



@transaction.route('/index', methods=['GET'])
@login_required
def index():
    user = current_user
    deposit = Deposit.query.filter_by(user=user).all()
    deposit_sum = sum([i.amount for i in deposit])
    withdrawal = Withdrawal.query.filter_by(user=user).all()
    withdrawal_sum = sum([i.amount for i in withdrawal])
    interest = Interest.query.filter_by(user=user).all()
    interest_sum = sum([i.amount for i in interest])

    context = {
                "user": user,
                "deposit": deposit,
                "deposit_sum": deposit_sum,
                "withdrawal": withdrawal,
                "withdrawal_sum": withdrawal_sum,
                "interest": interest,
                "interest_sum": interest_sum,
                }
    return render_template( "transaction/index.html", **context)


@transaction.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit_view():
    form = DepositForm()

    if form.validate_on_submit():
        deposit = Deposit(amount=form.amount.data, user=current_user)
        db.session.add(deposit)
        
        current_user.account.balance += deposit.amount
        if not current_user.account.initial_deposit_date:
            current_user.account.initial_deposit_date = datetime.utcnow()
        db.session.commit()
        flash('You Have Deposited ${}.'.format(deposit.amount), 'success')
        return redirect(url_for('.index'))
    context = {
        'title': "Deposit",
        'form': form,
    }
    return render_template('transaction/form.html', **context)


@transaction.route('/withdrawal', methods=['GET', 'POST'])
@login_required
def withdrawal_view():
    form = WithdrawalForm(current_user)

    if form.validate_on_submit():
        withdrawal = Withdrawal(amount=form.amount.data, user=current_user)
        db.session.add(withdrawal)

        current_user.account.balance -= withdrawal.amount
        db.session.commit()
        flash('You Have Withdrawn ${}.'.format(withdrawal.amount), 'success')
        return redirect(url_for('.index'))

    context = {
        'title': "Withdraw",
        'form': form,
    }
    return render_template('transaction/form.html', **context)