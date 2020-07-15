from run import app
import unittest
from fuelapp import db
from fuelapp.models import User, Profile, Quote
from fuelapp import bcrypt
from flask_login import login_user, current_user


class FlaskTestCases(unittest.TestCase):

    #Setup for testing
    def setUp(self):
        app.config['TESTING'] = True
        # app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
        self.app = app.test_client()
        db.create_all()



    #Tests redirection to correct page when client is logged out.
    def test_root(self):
        tester = app.test_client(self)
        response = tester.get('/',content_type='html/text')
        self.assertEqual(response.status_code, 200)
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/home',content_type='html/text')
        self.assertEqual(response.status_code, 200)
    def test_register_logged_out(self):
        tester = app.test_client(self)
        response = tester.get('/registration',content_type='html/text')
        self.assertTrue(b'Register Here' in response.data)
    def test_quote_logged_out(self):
        tester = app.test_client(self)
        response = tester.get('/quote',follow_redirects=True)
        self.assertIn(b'Login Here',response.data)
    def test_profile_logged_out(self):
        tester = app.test_client(self)
        response = tester.get('/profile',follow_redirects=True)
        self.assertIn(b'Login Here',response.data)

    #Tests correct response to invalid login input
    def test_correct_redirection_after_successful_slash_short_username(self):
        tester=app.test_client(self)
        response=tester.post('/',data=dict(username='u'),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.',response.data)
    def test_correct_redirection_after_successful_login_short_username(self):
        tester=app.test_client(self)
        response=tester.post('/home',data=dict(username='u'),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.',response.data)
    def test_correct_redirection_after_successful_slash_short_password(self):
        tester=app.test_client(self)
        response=tester.post('/',data=dict(password='1'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_redirection_after_successful_login_short_password(self):
        tester=app.test_client(self)
        response=tester.post('/home',data=dict(password='1'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_redirection_after_successful_slash_long_username(self):
        tester=app.test_client(self)
        response=tester.post('/',data=dict(username='uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.',response.data)
    def test_correct_redirection_after_successful_login_long_username(self):
        tester=app.test_client(self)
        response=tester.post('/home',data=dict(username='uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.',response.data)
    def test_correct_redirection_after_successful_slash_long_password(self):
        tester=app.test_client(self)
        response=tester.post('/',data=dict(password='1111111111111111111111111111111111111111111111'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_redirection_after_successful_login_long_password(self):
        tester=app.test_client(self)
        response=tester.post('/home',data=dict(password='11111111111111111111111111111111111111111111111'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)

    #Test correct response to invalid registration input
    def test_correct_response_after_short_username_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(username='u'),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.',response.data)
    def test_correct_response_after_long_username_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(username='uuuuuuuuuuuuuuuuuuuuuuuuuuu'),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.',response.data)
    def test_correct_response_after_invalid_email_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(email='email'),follow_redirects=True)
        self.assertIn(b'Invalid email address.',response.data)
    def test_correct_response_after_short_password_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(password='1111'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_response_after_long_password_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(password='1111111111111111111111111111111111'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_response_after_short_confirmpassword_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(confirm_password='1111'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_response_after_long_confirmpassword_registration(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(confirm_password='1111111111111111111111111111111111'),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.',response.data)
    def test_correct_response_after_unequal_passwords(self):
        tester=app.test_client(self)
        response=tester.post('/registration',data=dict(password='123456',confirm_password='1234567'),follow_redirects=True)
        self.assertIn(b'Field must be equal to password.',response.data)

    #Test correct response to valid login input
    def test_valid_login(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        hashed_password = bcrypt.generate_password_hash("123456")#.decode('utf-8')
        user = User(username="bob", email="bob@gmail.com", password=hashed_password)
        db.session.add(user)
        db.session.commit()
        response=tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        self.assertIn(b'Change Profile',response.data)

    #Test correct response to invalid login credentials
    def test_invalid_login(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        response=tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        self.assertIn(b'Login failed. Check username and password',response.data)

    #Test redirection if authetnicated user revists login page
    def test_authenticated_user_redirect_from_login(self):
        with app.app_context():
            with app.test_request_context():
                tester=app.test_client(self)
                db.drop_all()
                db.create_all()
                hashed_password = bcrypt.generate_password_hash("123456")#.decode('utf-8')
                user = User(username="bob", email="bob@gmail.com", password=hashed_password)
                db.session.add(user)
                db.session.commit()
                response = tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
                response = tester.get('/home',content_type='html/text', follow_redirects=True)
                self.assertIn(b'Change Profile', response.data)

    #If a user's profile already exists, check that the user gets redirected to the quote page
    def test_redirection_to_quote_if_profile_exists(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        hashed_password = bcrypt.generate_password_hash("123456")#.decode('utf-8')
        user = User(username="bob", email="bob@gmail.com", password=hashed_password)
        db.session.add(user)
        db.session.commit()

        profile = Profile(name="bob", address1="Sample Drive", address2="", city="Houston",state="TX", zipcode="77777", user_id="123")
        db.session.add(profile)
        db.session.commit()

        response = tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        self.assertIn(b'Get Your Quote', response.data)












if __name__ == "__main__":
    unittest.main()
