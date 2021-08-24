from app import celery, db
from app.models import User, Interest




@celery.task(bind=True, name="count_interest")
def count_interest(self):
    users = User.query.filter(User.balance != None).all()
    if users:
        for user in users:
            balance = user.balance
            # calculates users interest
            amount = (balance * 10) / 100
            interest = Interest(user_id=user.id, amount=int(amount))
            db.session.add(interest)
            db.session.commit()
            # adds users interest to balance.
            user.account.balance += amount
            db.session.commit()
