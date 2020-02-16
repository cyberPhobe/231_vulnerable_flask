from flask import Flask, render_template, request, url_for, redirect, session, g
import os

app = Flask(__name__)
app.secret_key = os.urandom(90)

@app.errorhandler(404)
def notFound(e):
    return render_template('not_found.html')

@app.route('/')
def home():
    #Do somehting evil here like ufw allow a port or add a user and change their password
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    #SQL Injection
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('loggedin'))
    return render_template('login.html')

@app.route('/loggedin')
def loggedin():
    if g.user:
        return render_template('loggedin.html', user=session['user'])
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')

@app.route('/products')
def products():

    return render_template('products.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/employees')
def ptoAdmin():
    return render_template('employee.html')

@app.route('/testing')
def testing():
    return render_template('testing.html')

@app.route('/bulletin')
def board():
    return render_template('bulletin.html')

@app.route('/addUser')
def addUser():
    #Oooo!! Some logic to add a user, eh?
    return render_template('adduser.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')