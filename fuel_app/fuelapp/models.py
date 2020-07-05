from fuelapp import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    quote = db.relationship('Quote', backref='userQ', lazy =  True)
    profile = db.relationship('Profile', backref=backref('userP',lazy = True, uselist=False))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    gallonsRequest = db.Column(db.Integer)#, nullable = False)
    deliveryDate = db.Column(db.Date, nullable = False)
    address = db.Column(db.String(200), nullable =False)
    rate = db.Column(db.Float, nullable = False)
    totalAmt = db.Column(db.Float, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Quote('{self.gallonsRequest}', '{self.deliveryDate}', '{self.address}', '{self.rate}', '{self.totalAmt}', '{self.user_id}')"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    address1 = db.Column(db.String(200), nullable = False)
    address2 = db.Column(db.String(200), nullable = True)
    city = db.Column(db.String(70), nullable = False)
    state = db.Column(db.String(2), nullable =False)
    zipcode = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=backref("profileObj", lazy=True, uselist=False))

    def __repr__(self):
        return f"Profile('{self.name}', '{self.address1}, '{self.city}', '{self.zipcode}', '{self.state}', {self.user_id})"
