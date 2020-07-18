from flask import render_template, url_for, flash, redirect, request
from fuelapp import app, db, bcrypt
from fuelapp.forms import registrationForm, loginForm, quoteForm, profileForm
from fuelapp.models import User, Profile, Quote
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
            checkProfile = Profile.query.filter_by(user_id = current_user.id).first()
            if checkProfile != None:
                return redirect(url_for('quote'))
            else:
                return redirect(url_for('profile'))
        else:
            flash('Login failed. Check username and password', 'danger')
    # print(form.errors.items())
    return render_template('home.html', title = 'Login', form = form)

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        checkProfile = Profile.query.filter_by(user_id = current_user.id).first()
        if checkProfile != None:
            return redirect(url_for('quote'))
        else:
            return redirect(url_for('profile'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/quote', methods = ['GET', 'POST'])
@login_required
def quote():
    form = quoteForm()
    checkProfile = Profile.query.filter_by(user_id = current_user.id).first()
    if checkProfile == None:
        return redirect(url_for('profile'))

    concatAdd = current_user.profileObj.address1+" "+current_user.profileObj.address2 +" "+current_user.profileObj.city+" "+str(current_user.profileObj.zipcode)+" "+current_user.profileObj.state
    form.deliveryAddress.data = concatAdd

    #if user presses the calculate button grab the quote
    if form.validate_on_submit() and form.calQuote.data:
        gallonsReq = form.gallonsRequested.data
        suggestRate, total = calculateRateAndTotal(gallonsReq)
        form.rate.raw_data = [suggestRate]
        form.total.raw_data = [total]
        flash("Your quote has been calculated", "success")

    #if user has a already calculated a quote then the submit button will store quote in db
    elif form.validate_on_submit() and form.submit.data and form.total.data!= None:
        quote = Quote(gallonsRequest = form.gallonsRequested.data, deliveryDate = form.deliveryDate.data, address = concatAdd, rate = form.rate.data, totalAmt = form.total.data, userQ = current_user)
        db.session.add(quote)
        db.session.commit()
        flash('Your quote was submitted!', "success")
    #Tell user to calculate quote prior to submitting. Buttons basically disabled    
    elif form.submit.data and form.total.data== None: 
        flash("Please calculate quote before submitting", "danger")
    return render_template('quote.html', title = 'Get your quote', form = form)

def calculateRateAndTotal(amtRequested):

    basePrice = 1.50
    companyProfitFactor = 0.10

    if current_user.profileObj.state == "TX":
        locationFactor = 0.02
    else:
        locationFactor = 0.04
    if current_user.quote:
        rateHistory = 0.01
    else:
        rateHistory = 0.00
    if amtRequested >= 1000:
        amtFactor = 0.02
    else:
        amtFactor = 0.03

    margin = basePrice * (locationFactor-rateHistory+amtFactor+companyProfitFactor)
    suggestedRate = basePrice + margin
    total = suggestedRate * amtRequested

    return suggestedRate, total

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = profileForm()

    if not current_user.profile:
        if form.validate_on_submit():
            if not current_user.profile:
                info = Profile(name = form.name.data, address1 = form.address1.data, address2 = form.address2.data
                ,city = form.city.data, state = form.state.data, zipcode = form.zipcode.data, user_id = current_user.id)
                db.session.add(info)
                db.session.commit()
                flash('Your information has been saved', 'success')
    else:
        if form.validate_on_submit():
            current_user.profileObj.name = form.name.data
            current_user.profileObj.address1 = form.address1.data
            current_user.profileObj.address2= form.address2.data
            current_user.profileObj.city = form.city.data
            current_user.profileObj.state = form.state.data
            current_user.profileObj.zipcode= form.zipcode.data
            db.session.commit()
            flash(f'Your profile has been updated', 'success')

    return render_template('profile.html', title = 'Personalize', form = form)

@app.route('/history', methods = ['GET', 'POST'])
@login_required
def history():
    checkProfile = Profile.query.filter_by(user_id = current_user.id).first()
    if checkProfile == None:
        return redirect(url_for('profile'))
    quotes = Quote.query.filter_by(user_id=current_user.id)
    return render_template('history.html', title = 'Personalize', quotes = quotes)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
