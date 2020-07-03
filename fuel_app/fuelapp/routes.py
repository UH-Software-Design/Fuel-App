from flask import render_template, url_for, flash, redirect
from fuelapp import app, db, bcrypt
from fuelapp.forms import registrationForm, loginForm, quoteForm, profileForm
from fuelapp.models import User, Profile, Quote
from flask_login import login_user, current_user, logout_user


@app.route('/', methods = ['GET', 'POST'])
@app.route('/home',methods = ['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Check username and password', 'danger')
    return render_template('home.html', title = 'Login', form = form)

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        #flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    form = quoteForm()
    # if form.validate_on_submit():
    #     flash('Here is your quote. Enjoy!', 'success')
    # else:
    #     flash('Please provide valid input', 'danger')
    return render_template('quote.html', title = 'Get your quote', form = form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    form = profileForm()
    # if form.validate_on_submit():
    #     flash('Your information has been saved', 'success')
    # else:
    #     flash('Please provide valid input', 'danger')
    return render_template('profile.html', title = 'Personalize', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))