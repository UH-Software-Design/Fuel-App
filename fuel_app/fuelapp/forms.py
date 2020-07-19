from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, SelectField, TextAreaField#, DecimalField
from wtforms.fields.html5 import DateField, IntegerField, EmailField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional, Regexp, ValidationError
from wtforms.widgets import TextInput, PasswordInput
from wtforms.widgets.html5 import NumberInput
from fuelapp.models import User
# from decimal import Decimal



class registrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min = 2, max = 25)])
    email = EmailField('E-mail', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6, max = 30)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), Length(min = 6, max = 30), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username is already taken')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email is already in use')

class loginForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min = 2, max = 25)])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6, max = 30)], widget=PasswordInput(hide_value=False))
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

# class BetterDecimalField(DecimalField):
#     def __init__(self, label=None, validators=None, places=2, rounding=None,
#                  round_always=False, **kwargs):
#         super(BetterDecimalField, self).__init__(
#             label=label, validators=validators, places=places, rounding=
#             rounding, **kwargs)
#         self.round_always = round_always
#
#     def process_formdata(self, valuelist):
#         if valuelist:
#             try:
#                 self.data = decimal.Decimal(valuelist[0])
#                 if self.round_always and hasattr(self.data, 'quantize'):
#                     exp = decimal.Decimal('.1') ** self.places
#                     if self.rounding is None:
#                         quantized = self.data.quantize(exp)
#                     else:
#                         quantized = self.data.quantize(
#                             exp, rounding=self.rounding)
#                     self.data = quantized
#             except (decimal.InvalidOperation, ValueError):
#                 self.data = None
#                 raise ValueError(self.gettext('Not a valid decimal value'))

class quoteForm(FlaskForm):
    gallonsRequested = IntegerField('Gallons Requested: ', validators = [DataRequired(), NumberRange(min = 50, max = 3500)], widget=NumberInput(min = 0, max = 3501))
    deliveryDate = DateField('Delivery Date:', format = '%Y-%m-%d', validators = [DataRequired(message="You need to enter a date")])
    deliveryAddress = StringField('Delivery address: ', validators = [DataRequired("Update your profile with an address")])
    rate = DecimalField("Price per Gallon:", places = 2, validators = [Optional()])
    total = DecimalField("Total Amount:", places =2, validators = [Optional()])
    # rate = BetterDecimalField("Price per Gallon:", places = 2,round_always="True", validators = [Optional()])
    # total = BetterDecimalField("Total Amount:", places =2,round_always="True", validators = [Optional()])
    submit = SubmitField(label="Submit")
    calQuote = SubmitField(label="Get Quote")

class profileForm(FlaskForm):
    name = StringField('Name: ', validators = [DataRequired(), Length(min=3, max =50)])
    address1 = StringField('Address 1: ', validators = [DataRequired(), Length(min =10, max = 100)])
    address2 = StringField('Address 2: ', validators = [Optional()])
    city = StringField('City: ', validators = [DataRequired(), Length(min=2, max =30)])
    state = SelectField ('State: ', validators = [DataRequired()],choices = [('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),
    ('DE','Delaware'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),
    ('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NV','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),
    ('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),
    ('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')])
    zipcode = IntegerField('Zip Code: ', validators= [DataRequired()], widget=NumberInput(min = 501, max = 99950))
    submit = SubmitField('Submit')
