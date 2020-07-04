from flask import render_template, url_for, flash, redirect, request
from fuelapp import app, db, bcrypt
from fuelapp.forms import registrationForm, loginForm, quoteForm, profileForm
from fuelapp.models import User, Profile, QuoteHistory
from flask_login import login_user, current_user, logout_user, login_required


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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
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
@login_required
def quote():
    form = quoteForm()
    if form.validate_on_submit():
        toadd = Quote(gallons = form.gallonsRequested.data, deliveryDate= form.deliveryDate.data
                    ,address = form.deliveryAddress.data, rate = form.rate.data
                    ,total =form.total.data, quoteid= current_user)
        db.session.add(toadd)
        db.session.commit()
        flash('okaaay')
        return redirect(url_for('quote'))
    return render_template('quote.html', title = 'Get your quote', form = form)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = profileForm()
    if form.validate_on_submit():
        #broken, needs work. Entry is overwriten.
        info = Profile(name = form.name.data, address1 = form.address1.data, address2 = form.address2.data
        ,city = form.city.data, state = form.state.data, zipcode = form.zipcode.data, profileid= current_user)
        db.session.add(info)
        db.session.commit()
        flash('Your information has been saved', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Please provide valid input', 'danger')
    return render_template('profile.html', title = 'Personalize', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
