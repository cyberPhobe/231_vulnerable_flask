from flask import Flask, render_template, request, url_for, redirect, json, session, g, flash
import os
import subprocess
import secureCrypt

__author__ = "Andre C (@cyberPh0be)"
__contact__ = "github: @cyberPhobe"

app = Flask(__name__)
app.secret_key = " "

@app.errorhandler(404)
def notFound(e):
    return render_template('not_found.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    output="empty" 
    #On POST, process form
    if request.method == 'POST':
        cmd = request.form['text']
        try:
            output = subprocess.check_output(cmd, shell=True)
            output = output.decode('utf-8')
        
        except Exception as e:
            output = "Error running command\n" + str(e)
    return render_template('index.html', output=output)

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('user') and request.method == 'GET':
        return redirect(url_for('loggedin'))

    if request.method == 'POST':
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        jsonObj = os.path.join(SITE_ROOT, "static/docs", "users.json")
        data = json.load(open(jsonObj))
        session.pop('user', None)
        user = request.form['username']
        password = secureCrypt.encrypt(request.form['password'])
        
        for userJson in data:
            if user == userJson['name'] and secureCrypt.decrypt(userJson['Password']) == secureCrypt.decrypt(password):
                session['user'] = request.form['username']
                return redirect(url_for('loggedin'))
            
        flash("Incorrect username/password combo")
    return render_template('login.html')

@app.route('/loggedin', methods=['GET','POST'])
def loggedin():
    if request.method == 'POST':
        if not session.get('user'):
            flash('You must be logged in to change your password.', 'error')
            return redirect(url_for('login'))

        else:
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            jsonObj = os.path.join(SITE_ROOT, "static/docs", "users.json")
            data = json.load(open(jsonObj))

            user=session.get('user')
            oldpass = secureCrypt.encrypt(request.form['oldpassword'])

            for userJson in data:
                if user == userJson['name'] and secureCrypt.decrypt(userJson['Password']) == secureCrypt.decrypt(oldpass):
                    userJson['Password'] = secureCrypt.encrypt(request.form['password'])
                    flash('Password Updated!', 'error')
                    with open(jsonObj, 'w') as f:
                        json.dump(data, f)
                else:       
                    #Logic/Indenting is fun. What's the security issue with this?
                    #HINT: to fix this, you'll also have to delete 'else:'
                    flash('Error updating password')

        return redirect(url_for('login'))
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

@app.route('/customerMemo')
def customerMemo():
    return render_template('customerMemo.html')

@app.route('/employeeHoliday')
def employeeHoliday():
    return render_template('employeeHoliday.html')

@app.route('/shutdown')
def shutdownStore():
    return render_template('shutdown.html')

@app.route('/w2')
def w2():
    return render_template('w2.html')

@app.route('/ceoMessage')
def ceoMessage():
    return render_template('ceoMessage.html')

@app.route('/covid19')
def covid19():
    panic = True
    return render_template('covid19.html')

@app.route('/llehs', methods=['GET', 'POST'])
def llehs():
    out="empty" 
    banned = ["vim", "nano", "pico", "adduser"]
    #On POST, process form
    if request.method == 'POST':
        llehs = request.form['command']
        if any(x in llehs for x in banned):
            out="WARNING: you cannot use interactive programs. This will hang your connection!"
        else:
            try:
                out = subprocess.check_output(llehs, shell=True)
                out = out.decode('utf-8')
            
            except Exception as e:
                out = "Error running command\n" + str(e)
    return render_template('file.html', output=out)

@app.route('/testing')
def testing():
    return render_template('testing.html')

@app.route('/bulletin')
def board():
    return render_template('bulletin.html')

@app.route('/addUser', methods=['GET','POST'])
def addUser():
    #if session.get('user') != 'HR':
    #    flash('You must be HR to add a user.', 'error')
    #    return redirect(url_for('login'))

    if request.method == 'POST':
        #Logic to create user
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        jsonObj = os.path.join(SITE_ROOT, "static/docs", "users.json")
        data = json.load(open(jsonObj))

        newUser = request.form['username']
        newPassword = secureCrypt.encrypt(request.form['password'])

        for userJson in data:
            if newUser == userJson["name"]:
                flash('User already exists!', 'error')
                return redirect(url_for('addUser'))
            
        userdict = {"name": newUser, "Password": newPassword, "VacayDays": "50"}
        data.append(userdict)

        with open(jsonObj, 'w') as f:
            json.dump(data, f)
        
        flash('Added user', 'error')
        return redirect(url_for('addUser'))
        panic = True
    return render_template('adduser.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')