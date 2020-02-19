from flask import Flask, render_template, request, url_for, redirect, session, g, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = " "

@app.errorhandler(404)
def notFound(e):
    return render_template('not_found.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    output=""
    #Secret command line for devs
    if request.method == 'POST':
        cmd = request.form['text']
        if "rm " in cmd:
            output="You may not destroy things. Do not run rm."
        else:
            try:
                output = subprocess.check_output(cmd, shell=True)
            except Exception as e:
                output = "Error running command\n" + str(e)
    return render_template('index.html', output=output)

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('user') and request.method == 'GET':
        return redirect(url_for('loggedin'))

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
    return render_template('logout.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/employees')
def ptoAdmin():
    if not session.get('user'):
        flash('You must be logged in to see the portal.', 'error')
        return redirect(url_for('login'))
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