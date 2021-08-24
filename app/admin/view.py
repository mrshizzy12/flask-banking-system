from app import db
from app.models import User, UserAddress, UserBankAccount
from . admin_view import UserModelView, AddressModelView, AccountModelView
from app import admin
from flask_admin.menu import MenuLink



''' register admin view with flask-admin '''
admin.add_view(UserModelView(User, db.session))
admin.add_view(AddressModelView(UserAddress, db.session))
admin.add_view(AccountModelView(UserBankAccount, db.session))
admin.add_link(MenuLink(name='Logout', category='', url='/auth/logout?next=auth/login'))