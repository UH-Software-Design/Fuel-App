from run import app
import unittest
from fuelapp import db
from fuelapp.models import User, Profile, Quote

class FlaskTestCases(unittest.TestCase):

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
    def test_correct_response_after_Valid_login(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        user = User(username="Chase", email="chase@gmail.com", password="123456")
        db.session.add(user)
        db.session.commit()
        response=tester.post('/home',data=dict(username='Chaseee',password='heyhey'), follow_redirects=True)#, follow_redirects=True
        self.assertIn(b'Change Profile',response.data)


    # def test_register_logged_out(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/registration',content_type='html/text')
    #     self.assertTrue(b'Register Here' in response.data)

if __name__ == "__main__":
    unittest.main()
