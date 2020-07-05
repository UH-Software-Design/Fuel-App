from flask import render_template, url_for, flash, redirect, request
from fuelapp import app, db, bcrypt
from fuelapp.forms import registrationForm, loginForm, quoteForm, profileForm, totalForm
from fuelapp.models import User, Profile, Quote
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods = ['GET', 'POST'])
@app.route('/home',methods = ['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('quote'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            # next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('profile'))
            checkProfile = Profile.query.filter_by(profile_id = current_user.id).first()
            return redirect(url_for('profile')) if checkProfile == None else redirect(url_for('quote'))
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
    checkProfile = Profile.query.filter_by(profile_id = current_user.id).first()
    if checkProfile == None:
        return redirect(url_for('profile'))
    if form.validate_on_submit():
        gals=form.gallonsRequested.data
        tots= gals * 2.5
        toadd = Quote(gallons = form.gallonsRequested.data, deliveryDate= form.deliveryDate.data
                    ,address = form.deliveryAddress.data, rate = form.rate.data
                    ,total =tots, quoteid= current_user)
        db.session.add(toadd)
        db.session.commit()
        return redirect(url_for('quote'))
    elif request.method == 'GET':
        form.deliveryAddress.data = checkProfile.address1
        form.rate.data = 2.5
        form.total.data = 8888
    return render_template('quote.html', title = 'Get your quote', form = form)

@app.route('/total', methods = ['GET'])
@login_required
def total():
    form = totalForm()
    checkHistory = Quote.query.filter_by(quote_id = current_user.id).first()
    checkProfile = Profile.query.filter_by(profile_id = current_user.id).first()
    if request.method == 'GET':
        form.gallonsRequested.data = checkHistory.gallons
        form.deliveryDate.data = checkHistory.deliveryDate
        form.deliveryAddress.data = checkProfile.address1
        form.rate.data = 2.5
        form.total.data = 9999
    return render_template('total.html', title = 'Get your quote', form = form)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = profileForm()
    if form.validate_on_submit():
        checkProfile = Profile.query.filter_by(profile_id = current_user.id).first()
        if checkProfile == None:
            info = Profile(name = form.name.data, address1 = form.address1.data, address2 = form.address2.data
            ,city = form.city.data, state = form.state.data, zipcode = form.zipcode.data, profile_id= current_user.id)
            db.session.add(info)
            db.session.commit()
        elif checkProfile.id == current_user.id:
            checkProfile.name = form.name.data
            checkProfile.address1 = form.address1.data
            checkProfile.address2 = form.address2.data
            checkProfile.city = form.city.data
            checkProfile.state = form.state.data
            checkProfile.zipcode =form.zipcode.data
            profile_id = current_user.id
            db.session.commit()

        flash('Your information has been saved', 'success')
        return redirect(url_for('quote'))
    else:
        flash('Please provide valid input', 'danger')
    return render_template('profile.html', title = 'Personalize', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))