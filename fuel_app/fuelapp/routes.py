from flask import render_template, url_for, flash, redirect
from fuelapp import app
from fuelapp.forms import registrationForm, loginForm, quoteForm, profileForm
from fuelapp.models import User, Profile, Quote


@app.route('/', methods = ['GET', 'POST'])
@app.route('/home',methods = ['GET', 'POST'])
def home():
    form = loginForm()
    if form.validate_on_submit():
        if form.username.data == 'potatoman@me.com' and form.password.data == 'password':
            flash('You have successfully logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check username and password', 'danger')
    return render_template('home.html', title = 'Login', form = form)

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    form = registrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('quote'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    form = quoteForm()
    if form.validate_on_submit():
        flash('Here is your quote. Enjoy!', 'success')
    else:
        flash('Please provide valid input', 'danger')
    return render_template('quote.html', title = 'Get your quote', form = form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    form = profileForm()
    if form.validate_on_submit():
        flash('Your information has been saved', 'success')
    else:
        flash('Please provide valid input', 'danger')
    return render_template('profile.html', title = 'Personalize', form = form)