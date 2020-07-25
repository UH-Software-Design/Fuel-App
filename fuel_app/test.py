from run import app
import unittest
from fuelapp import db
from fuelapp.models import User, Profile, Quote
from fuelapp import bcrypt
from flask_login import login_user, current_user
from fuelapp.routes import calculateRateAndTotal
from decimal import Decimal

class FlaskTestCases(unittest.TestCase):

    #Setup for testing
    def setUp(self):
        app.config['TESTING'] = True
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
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            hashed_password = bcrypt.generate_password_hash("123456")#.decode('utf-8')
            user = User(username="bob", email="bob@gmail.com", password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            profile = Profile(name="bob", address1="Sample Drive", address2="", city="Houston",state="TX", zipcode="77777", user_id=current_user.id)
            db.session.add(profile)
            db.session.commit()
            response = tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            self.assertIn(b'Get Your Quote', response.data)

    def test_redirection_to_quote_from_registration(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            hashed_password = bcrypt.generate_password_hash("123456")#.decode('utf-8')
            user = User(username="bob", email="bob@gmail.com", password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            profile = Profile(name="bob", address1="Sample Drive", address2="", city="Houston",state="TX", zipcode="77777", user_id=current_user.id)
            db.session.add(profile)
            db.session.commit()

            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            response = tester.get('/registration',content_type='html/text', follow_redirects=True)
            self.assertIn(b'Get Your Quote', response.data)

    def test_redirection_to_profile_from_registration(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            hashed_password = bcrypt.generate_password_hash("123456")#.decode('utf-8')
            user = User(username="bob", email="bob@gmail.com", password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            response = tester.get('/registration',content_type='html/text', follow_redirects=True)
            self.assertIn(b'Change Profile', response.data)

    def test_user_registration(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        response = tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        self.assertIn(b'Change Profile', response.data)

    def test_redirection_to_profile_from_quote(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        response = tester.get('/quote',content_type='html/text', follow_redirects=True)
        self.assertIn(b'Change Profile', response.data)

    def test_initial_profile_submission(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        response = tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="TX",zipcode='45454'), follow_redirects=True)
        self.assertIn(b'Your information has been saved', response.data)

    def test_existing_profile_data_recall(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='45454'), follow_redirects=True)
        response = tester.get('/profile',content_type='html/text')
        self.assertIn(b'bob', response.data)

    def test_profile_update(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='45454'), follow_redirects=True)
        response = tester.post('/profile',data=dict(name="bobby",address1='123456123456',address2="789456789456",city="Houston",state="TX",zipcode='45454'), follow_redirects=True)
        self.assertIn(b'Your profile has been updated', response.data)

    def test_if_quote_calculates_and_fills_fields(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='45454'), follow_redirects=True)
        response = tester.post('/quote',data=dict(gallonsRequested="546",deliveryDate='2020-07-20',calQuote="True"), follow_redirects=True)
        self.assertIn(b'Your quote has been calculated', response.data)

    def test_if_quote_fails_to_calculate_before_submission(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='45454'), follow_redirects=True)
        response = tester.post('/quote',data=dict(gallonsRequested="546",deliveryDate='2020-07-20',submit="True"), follow_redirects=True)
        self.assertIn(b'Please calculate quote before submitting', response.data)


    def test_if_quote_submits(self):
        tester=app.test_client(self)
        db.drop_all()
        db.create_all()
        tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
        tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
        tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='45454'), follow_redirects=True)
        response = tester.post('/quote',data=dict(gallonsRequested="546",deliveryDate='2020-07-20',deliveryAddress="123456123456 Sample Drive",rate="2.00",total="1092",submit="True"), follow_redirects=True)
        self.assertIn(b'Your quote has been saved', response.data)


    def test_rate_for_new_texans_with_less_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Houston",state="TX",zipcode='77777'), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(546)
            self.assertEqual(suggestRate,Decimal('1.72'))
            self.assertEqual(total,Decimal('939.12'))

    def test_rate_for_new_texans_with_more_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Houston",state="TX",zipcode='77777'), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(1000)
            self.assertEqual(suggestRate,Decimal('1.71'))
            self.assertEqual(total,Decimal('1710'))

    def test_rate_for_old_texans_with_less_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Houston",state="TX",zipcode='77777'), follow_redirects=True)
            tester.post('/quote',data=dict(gallonsRequested="546",deliveryDate='2020-07-20',deliveryAddress="123456123456 Sample Drive",rate="2.00",total="1092",submit="True"), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(784)
            self.assertEqual(suggestRate,Decimal('1.71'))
            self.assertEqual(total,Decimal('1340.64'))

    def test_rate_for_old_texans_with_more_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Houston",state="TX",zipcode='77777'), follow_redirects=True)
            tester.post('/quote',data=dict(gallonsRequested="546",deliveryDate='2020-07-20',deliveryAddress="123456123456 Sample Drive",rate="2.00",total="1092",submit="True"), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(2002)
            self.assertEqual(suggestRate,Decimal('1.7'))
            self.assertEqual(total,Decimal('3403.4'))

    def test_rate_for_new_non_texans_with_less_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='80228'), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(811)
            self.assertEqual(suggestRate,Decimal('1.76'))
            self.assertEqual(total,Decimal('1427.36'))

    def test_rate_for_new_non_texans_with_more_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='80228'), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(1234)
            self.assertEqual(suggestRate,Decimal('1.74'))
            self.assertEqual(total,Decimal('2147.16'))

    def test_rate_for_old_non_texans_with_less_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='80228'), follow_redirects=True)
            tester.post('/quote',data=dict(gallonsRequested="899",deliveryDate='2020-07-20',deliveryAddress="123456123456 789456789456",rate="1.73",total="1555.27",submit="True"), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(777)
            self.assertEqual(suggestRate,Decimal('1.74'))
            self.assertEqual(total,Decimal('1351.98'))

    def test_rate_for_old_non_texans_with_more_than_1000_gallons(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='80228'), follow_redirects=True)
            tester.post('/quote',data=dict(gallonsRequested="899",deliveryDate='2020-07-20',deliveryAddress="123456123456 789456789456",rate="1.73",total="1555.27",submit="True"), follow_redirects=True)
            suggestRate, total = calculateRateAndTotal(2255)
            self.assertEqual(suggestRate,Decimal('1.72'))
            self.assertEqual(total,Decimal('3878.6'))

    def test_check_history_table(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            tester.post('/profile',data=dict(name="bob",address1='123456123456',address2="789456789456",city="Denver",state="CO",zipcode='80228'), follow_redirects=True)

            gallons = 975
            day = 1
            rates = []
            totals = []

            for quote in range(31):
                suggestRate, total = calculateRateAndTotal(gallons)
                rates.append(bytes(str(suggestRate),"ascii"))
                totals.append(bytes(str(total),"ascii"))
                tester.post('/quote',data=dict(gallonsRequested=str(gallons),deliveryDate='2020-07-'+str(day),deliveryAddress="123456123456 789456789456",rate=str(suggestRate),total=str(total),submit="True"), follow_redirects=True)
                gallons += 1
                day += 1

            response = tester.get('/history',content_type='html/text')

            for quote in range(31):
                self.assertIn(rates[quote],response.data)
                self.assertIn(totals[quote],response.data)

    def test_check_history_redirect_to_profile(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            response = tester.get('/history',content_type='html/text', follow_redirects=True)
            self.assertIn(b"Change Profile", response.data)

    def test_logout_redirect(self):
        with app.test_request_context():
            tester=app.test_client(self)
            db.drop_all()
            db.create_all()
            tester.post('/registration',data=dict(username='bob', email='bob@gmail.com', password='123456', confirm_password='123456'))
            tester.post('/home',data=dict(username="bob",password='123456'), follow_redirects=True)
            login_user(User.query.first())
            response = tester.get('/logout',content_type='html/text', follow_redirects=True)
            self.assertIn(b"Login Here", response.data)


if __name__ == "__main__":
    unittest.main()
