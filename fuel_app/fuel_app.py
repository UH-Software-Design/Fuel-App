from flask import Flask, render_template
app = Flask (__name__)

@app.route('/')
@app.route("/index.html")
def home():
    return render_template('index.html')

@app.route("/profile.html")
def profile():
    return render_template('profile.html')

@app.route("/quote.html")
def quote():
    return render_template('quote.html')

@app.route("/history.html")
def history():
    return render_template('history.html')

@app.route("/registration.html")
def registration():
    return render_template("registration.html")

if __name__ =='__main__':
    app.run(debug=True)