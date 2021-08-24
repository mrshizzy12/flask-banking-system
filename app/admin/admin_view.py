from flask_admin.contrib.sqla import ModelView
from wtforms.validators import Email, EqualTo
from wtforms.fields import PasswordField, SelectField
from flask_admin.form import SecureForm
from werkzeug.security import generate_password_hash
from app.auth.views import generate_account_no

class BaseView(ModelView):
    can_create = True
    form_base_class = SecureForm
    
   
class UserModelView(BaseView):
    ''' user class to be registerd with flask admin '''
   
    column_exclude_list = ['password_hash','token', 'token_expiration']
    column_searchable_list = ['username', 'email']
    column_editable_list = ['username', 'email']
    can_view_details = True
    create_modal = True
    edit_modal = True
    can_export = True
    column_labels = {"account": "Account Number"}
    form_excluded_columns = ['deposits', 'withdrawals', 'interests', 'token', 'token_expiration', 'account', 'address']
    form_args = {
        'email': {
        'validators': [Email()]
        },
        'password_hash': {
            'label': 'Password',
            'validators': [EqualTo('password2')]
        }
    }
    form_overrides = {
        'password_hash': PasswordField
    }
    form_extra_fields = {
        'password2': PasswordField('Password2')
    }
    
    def on_model_change(self, form, model, is_created):
        model.password_hash = generate_password_hash(model.password_hash)


class AddressModelView(BaseView):
    ''' user address class to be registerd with flask admin '''
    


class AccountModelView(BaseView):
    ''' user account class to be registerd with flask admin '''
    

    form_excluded_columns = ['created_at', 'initital_deposit_date', 'account_no']
    form_args = {
        'gender': {
            'choices': [('M', 'Male'), ('F', 'Female')]
        }
    }

    form_overrides = {
        'gender': SelectField
    }

    def on_model_change(self, form, model, is_created):
        model.account_no = generate_account_no()
        
        
