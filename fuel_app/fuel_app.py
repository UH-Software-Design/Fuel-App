from flask import Flask, render_template, url_for, flash, redirect
from forms import registrationForm, loginForm
app = Flask (__name__)
app.config['SECRET_KEY'] = '9e844a33fa6dff17d7f178b253442242614bfb6c189d6deed2830730d50f1ba5f80ee4c844364'

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
    
    return render_template('quote.html', title = 'Get your quote', form = form)



#code below works for old html code.
(''')
@app.route('/')
@app.route("/index.html")
def home():
    return render_template('index.html')

@app.route("/profile.html")
def profile():
    return render_template('profile.html', title = 'Profile management')

@app.route("/quote.html")
def quote():
    return render_template('quote.html', title = 'Quotes')

@app.route("/history.html")
def history():
    return render_template('history.html', title = 'Quote history')

@app.route("/registration.html")
def registration():
    return render_template("registration.html", title = 'Register')
''')

if __name__ =='__main__':
    app.run(debug=True)