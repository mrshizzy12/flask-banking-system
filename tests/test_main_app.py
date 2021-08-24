import unittest
from flask import current_app
from app import create_app, db
from config import Config
from app.models import User, UserBankAccount, UserAddress
from dateutil.parser import parse


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # use an in-memeory database
    
    
class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig, False)
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.populate_db()
        self.client = self.app.test_client()
        
    def tearDown(self):
       db.drop_all()
       self.appctx.pop()
       self.app = None
       self.appctx = None
       self.client = None
       
    def populate_db(self):
        new_user = User(
                username='janedoe', 
                email='janedoe@example.com', 
                password='mars'
            )        

        accout_details = UserBankAccount(
                account_no='0123456789',
                first_name='jane',
                last_name='doe',
                phone_number='+2341234567890',
                gender='M',
                date_of_birth= parse('2021-01-01')
            )

        address = UserAddress(
                country='nigeria',
                city='lagos',
                street_address='lekki'
            )
                   
        db.session.add_all([accout_details, address])
        new_user.account = accout_details
        new_user.address = address
        db.session.add(new_user)
        db.session.commit()
        
    def login(self):
        self.client.post('/auth/login', data={
            'username': 'janedoe',
            'password': 'mars',
        })
        
    def get_api_token(self):
        response = self.client.post('/api/tokens', auth=('janedoe', 'mars'))
        return response.json['token']
       
    def test_app(self):
        assert self.app is not None
        assert current_app == self.app
        
    def test_registration_form(self):
        response = self.client.get('/auth/register')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        assert 'name="username"' in html
        assert 'name="first_name"' in html
        assert 'name="last_name"' in html
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'name="date_of_birth"' in html
        assert 'name="street_address"' in html
        assert 'name="password2"' in html
        assert 'name="submit"' in html
        assert 'name="gender"' in html
        assert 'name="country"' in html
        assert 'name="phone_number"' in html
        assert 'name="city"' in html
        
        
    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'first_name': 'john',
            'last_name': 'doe',
            'gender': 'M',
            'country': 'nigeria',
            'city': 'lagos',
            'street_address': 'lagos lekki',
            'date_of_birth': '1990-09-30',
            'phone_number': '+23460961861',
            'password': 'somthing',
            'password2': 'somthing',
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        print(html)
        assert response.request.path == '/auth/login' # redirected to login

        # login with new user
        response = self.client.post('/auth/login', data={
            'username': 'johndoe',
            'password': 'somthing',
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        print(html)
        assert 'Welcome, John Doe!' in html
        
        
    def test_register_user_mismatched_passwords(self):
        response = self.client.post('/auth/register', data={
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'first_name': 'john',
            'last_name': 'doe',
            'gender': 'M',
            'country': 'nigeria',
            'city': 'lagos',
            'street_address': 'lagos lekki',
            'date_of_birth': '1990-09-30',
            'phone_number': '+23460961861',
            'password': 'somthing',
            'password2': 'somthing4',
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Field must be equal to password.' in html
        
        
        
    def test_deposit(self):
        self.login()
        response = self.client.post('/transaction/deposit', data={'amount': int('1000')},
                                    follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'You Have Deposited $1000.' in html
                         
    
    
    ######################
    # test api endpoints #
    ######################
    
    def test_api_register_user(self):
        response = self.client.post('/api/create_user', json={
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'first_name': 'john',
            'last_name': 'doe',
            'gender': 'M',
            'country': 'nigeria',
            'city': 'lagos',
            'street_address': 'lagos lekki',
            'date_of_birth': '1990-09-30',
            'phone_number': '+23460961861',
            'password': 'somthing',
            'password2': 'somthing4',
        })
        assert response.status_code == 201

        # make sure the user is in the database
        user = User.query.filter_by(username='johndoe').first()
        assert user is not None
        assert user.email == 'johndoe@example.com'
        
    
    def test_api_get_user(self):
        token = self.get_api_token()
        response = self.client.get(
            '/api/user_account_details/', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert response.json['username'] == 'janedoe'
        
        
    def test_api_deposit_withdrawal(self):
        token = self.get_api_token()
        response = self.client.post(
            '/api/deposit/', headers={'Authorization': f'Bearer {token}'}, json={'amt': int('1000')}
        )
        assert response.status_code == 201
        assert response.json['message'] == 'success'
        
        user = User.query.filter_by(token=token).first()
        assert user.account.balance == 1000
        
        response = self.client.post(
            '/api/withdraw/', headers={'Authorization': f'Bearer {token}'}, json={'amt': int('2000')}
        )
        assert response.status_code == 200
        assert response.json['message'] == 'insufficient funds'
        
        response = self.client.post(
            '/api/withdraw/', headers={'Authorization': f'Bearer {token}'}, json={'amt': int('1000')}
        )
        assert response.status_code == 201
        assert response.json['message'] == 'success'
        
        user = User.query.filter_by(token=token).first()
        assert user.account.balance == 0