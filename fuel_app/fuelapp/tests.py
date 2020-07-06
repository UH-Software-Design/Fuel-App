from run import app
import unittest

class FlaskTestCases(unittest.TestCase):

    #Login Redirection Test Cases
    #Tests that the login page was served when the root was requested.
    def test_root(self):
        tester = app.test_client(self)
        response = tester.get('/',content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #Tests that the login page was returned when requested.
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login',content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #Tests that the correct file was served after the given values were inputed.
    def test_correct_redirect_after_login(self):
        tester=app.test_client(self)
        response = tester.post('/quoteform',data=dict(username='username',password='password'),
        follow_redirects=True)
        self.assertIn(b'Quote Form',response.data)

    #Login Page Input Test Cases
    #Test correct error is returned for usernames above 25 characters.
    def test_correct_error_message_login_invalid_username_short(self):
        tester=app.test_client(self)
        response = tester.post('/login',data=dict(username='uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu',password='123456'),
        follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.', response.data)

    #Tests that correct error is returned for username less than 2 characters.
    def test_correct_error_message_login_invalid_username_long(self):
        tester=app.test_client(self)
        response = tester.post('/login',data=dict(username='u',password='123456'),
        follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.', response.data)

    #Tests that correct error is returned for password less than 6 characters.
    def test_correct_error_message_login_invalid_password_short(self):
        tester=app.test_client(self)
        response = tester.post('/login',data=dict(username='usernmae',password='12345'),
        follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.', response.data)

    #Tests that correct error is returned for password more than 30 characters.
    def test_correct_error_message_login_invalid_password_long(self):
        tester=app.test_client(self)
        response = tester.post('/login',data=dict(username='usernmae',password='12345678900000000000000000000000'),
        follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.', response.data)
    
    #Registration Redirection Test Cases
    #Tests if the registration page redirects to profile page after successfull registration
    def test_correct_redirect_after_registration(self):
        tester=app.test_client(self)
        response = tester.post('/profile',data=dict(email='name@email.com',username='username',password='password'),
        follow_redirects=True)
        self.assertIn(b'Profile Management',response.data)
    
    #Registration Input Test Cases
    #Tests if the correct error ir returned for username
    def test_correct_error_message_registration_invalid_username_short(self):
        tester=app.test_client(self)
        response=tester.post('/register',data=dict(username="u"),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.', response.data)
    def test_correct_error_message_registration_invalid_username_long(self):
        tester=app.test_client(self)
        response=tester.post('/register',data=dict(username="uuuuuuuuuuuuuuuuuuuuuuuuuuu"),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 25 characters long.', response.data)
    def test_correct_error_message_registration_invalid_password_short(self):
        tester=app.test_client(self)
        response=tester.post('/register',data=dict(password="12345"),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.', response.data)
    def test_correct_error_message_registration_invalid_password_long(self):
        tester=app.test_client(self)
        response=tester.post('/register',data=dict(password="uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.', response.data)
        
        #Profile Input Test Cases
    def test_correct_error_message_registration_invalid_fullname_short(self):
        tester=app.test_client(self)
        response=tester.post('/profile',data=dict(fullname="qq"),follow_redirects=True)
        self.assertIn(b'Field must be between 3 and 50 characters long.', response.data)
    def test_correct_error_message_registration_invalid_fullname_long(self):
        tester=app.test_client(self)
        response=tester.post('/profile',data=dict(fullname="qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"),follow_redirects=True)
        self.assertIn(b'Field must be between 3 and 50 characters long.', response.data)
    def test_correct_error_message_registration_invalid_address1_short(self):
        tester=app.test_client(self)
        response=tester.post('/profile',data=dict(address1="street"),follow_redirects=True)
        self.assertIn(b'Field must be between 10 and 100 characters long.', response.data)
    def test_correct_error_message_registration_invalid_address1_long(self):
        tester=app.test_client(self)
        response=tester.post('/profile',data=dict(address1="1234567890 streeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeet"),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 30 characters long.', response.data)
    def test_correct_error_message_registration_invalid_city_short(self):
        tester=app.test_client(self)
        response=tester.post('/profile',data=dict(city="c"),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 30 characters long.', response.data)
    def test_correct_error_message_registration_invalid_city_long(self):
        tester=app.test_client(self)
        response=tester.post('/profile',data=dict(city="cccccciiiiiiiitttttttttyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"),follow_redirects=True)
        self.assertIn(b'Field must be between 2 and 30 characters long.', response.data)
    
    #Quote Test cases
    def test_correct_error_message_quote_invalid_gallonsrequested_short(self):
        tester=app.test_client(self)
        response=tester.post('/quote',data=dict(gallonsRequested=49),follow_redirects=True)
        self.assertIn(b'Value must be between 50 and 100.', response.data)
    def test_correct_error_message_quote_invalid_deliveryDate_short(self):
        tester=app.test_client(self)
        response=tester.post('/quote',data=dict(deliveryDate=6-12-2000),follow_redirects=True)
        self.assertIn(b'Value for month must be betwwen 1 and 12. Value for date must be between 1 and 31. Value for year must be between 1950 and 2050.' response.data)
    def test_correct_error_message_quote_invalid_deliveryAddress_long(self):
        tester=app.test_client(self)
        response=tester.post('/quote',data=dict(deliveryAddress="0123456789 streeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeet ciiiiiiiiiiiity"),follow_redirects=True)
        self.assertIn(b'Field must be between 6 and 50 characters long.', response.data)
        
if __name__ == "__main__":
    unittest.main()
