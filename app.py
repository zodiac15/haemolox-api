from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_restful import Api
import resources
import requests
import hashlib

app = Flask(__name__)
api = Api(app)
app.secret_key = '2147aa348383f7cc243fbb58bd89ebe161e80d69'


@app.route("/")
def index():
    return render_template('index.html', title='Haemolox')


@app.route("/donors")
def donors():
    if 'logged_in' in session and session['logged_in'] is True:
        return render_template('donors.html', title='Haemolox | Find Donors')
    else:
        return redirect(url_for('login'))


@app.route('/validate/search', methods=['GET', 'POST'])
def search_result():
    city = request.form.get('city').lower()
    params = {'city': city}
    response = requests.post('https://haemolox-api.herokuapp.com/api/finduser', data=params).json()

    return render_template('donors.html', title='Haemolox | Find Donors', city=city.capitalize(),
                           result=response['users'])


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    email = request.form.get('email')
    params = {'to': email,
              'from': session['email']}
    response = requests.post('https://haemolox-api.herokuapp.com/api/createrequest', data=params).json()
    if response['created']:
        flash('The user was contacted')
        return redirect(url_for('donors'))
    else:
        flash(response['error'])
        return redirect(url_for('donors'))

@app.route("/accept", methods=['GET', 'POST'])
def accept():
    email = request.form.get('email')
    params = {'from': email,
              'to': session['email'],
              'accepted': '1'}
    response = requests.post('https://haemolox-api.herokuapp.com/api/updaterequest', data=params).json()
    if response['updated']:
        # mail
        flash('The user was contacted')
        return redirect(url_for('user'))


@app.route("/register")
def register():
    if 'logged_in' in session and session['logged_in'] is True:
        return redirect(url_for('user'))
    else:
        return render_template('register.html', title='Haemolox | Register')


@app.route('/validate/register', methods=['GET', 'POST'])
def validate_register():
    f_name = request.form.get('first_name')
    l_name = request.form.get('last_name')
    email = request.form.get('email')
    password = hashlib.sha1(request.form.get('password').encode('utf-8')).hexdigest()
    p_number = request.form.get('phone_no')
    address = request.form.get('address')
    state = request.form.get('state')
    city = request.form.get('city')
    blood_grp = request.form.get('blood_grp')
    age = request.form.get('age')
    params = {'first_name': f_name.capitalize(), 'last_name': l_name.capitalize(), 'email': email, 'password': password,
              'phone_no': p_number,
              'address': address, 'state': state, 'city': city, 'blood_grp': blood_grp, 'age': age}
    response = requests.post("https://haemolox-api.herokuapp.com/api/createuser", data=params).json()
    if response['created']:
        session['name'] = f_name + " " + l_name
        session['email'] = email
        session['ph'] = p_number
        session['logged_in'] = True
        return redirect(url_for('user'))
    else:
        return render_template('register.html', error=response['error'])


@app.route("/user")
def user():
    if 'logged_in' in session and session['logged_in'] is True:
        params = {'email': session['email']}
        response = requests.post('https://haemolox-api.herokuapp.com/api/requests', data=params).json()
        if 'users' in response:
            return render_template('user.html', name=session['name'], title='Haemolox | User', result=response['users'])
        else:
            return render_template('user.html', name=session['name'], title='Haemolox | User')
    else:
        return redirect(url_for('login'))


@app.route("/login")
def login():
    if 'logged_in' in session and session['logged_in'] is True:
        return redirect(url_for('user'))
    else:
        return render_template('login.html', title='Haemolox | Login')


@app.route('/validate/login', methods=['GET', 'POST'])
def validate_login():
    email = request.form.get('email_id')
    password = hashlib.sha1(request.form.get('password').encode('utf-8')).hexdigest()

    params = {'email': email, 'password': password}
    response = requests.post("https://haemolox-api.herokuapp.com/api/authenticate", data=params).json()
    if response['Authenticated'] is False or 'Authenticated' not in response:
        return render_template('login.html', error=response['error'])

    else:
        session['name'] = response['Name']
        session['email'] = email
        session['logged_in'] = True

        return redirect(url_for('user'))


@app.route('/logout', methods=['post'])
def logout():
    session.pop('name')
    session.pop('email')
    session.pop('ph')
    session.pop('logged_in')
    return redirect(url_for('index'))


# bind resources to endpoints
api.add_resource(resources.CreateUser, '/api/createuser')
api.add_resource(resources.FindUser, '/api/finduser')
api.add_resource(resources.CreateRequest, '/api/createrequest')
api.add_resource(resources.UpdateRequest, '/api/updaterequest')
api.add_resource(resources.DeleteUser, '/api/deleteuser')
api.add_resource(resources.AuthenticateUser, '/api/authenticate')
api.add_resource(resources.Requests, '/api/requests')

if __name__ == '__main__':
    app.run(debug=True)
