__author__ = 'Jetfire'


from flask import Flask, render_template, request, session, make_response, flash, jsonify
#from flask_avatars import Avatars
import hashlib
import datetime
import base64
from models.users import User
from common.database import Database
from flask_pymongo import PyMongo


app = Flask(__name__)  # '__main__'
app.secret_key = "Hero"
app.config['MONGO_URI']= "mongodb+srv://sharpnel:qwerty123@powersystem-chebt.mongodb.net/test?retryWrites=true"
mongo = PyMongo(app)
#avatars = Avatars(app)
BASECOORD = [22.3511148, 78.6677428]


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/index_template')
def index_template1():
    session.clear()
    return render_template('index_home.html')


@app.route('/')
def index_template():
    session.clear()
    return render_template('index.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.route('/auth_register', methods=['POST'])
def register_user():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    phone = request.form['mobile']
    photo = request.files['file']
    mongo.save_file(photo.filename, photo)
    picture = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    User.register(email, username, password, first_name, last_name, gender, phone, picture, photo.filename)
    flash("Registered Successfully", category='success')
    return render_template("register.html")


@app.route('/login')
def login_template():
    session.clear()
    return render_template('login.html')


@app.route('/auth_login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    if User.login_valid(username, password):
        User.login(username)
    else:
        session['username'] = None
        return render_template("index_home.html")

    user = mongo.db.users.find_one_or_404({'username':username})

    return render_template("home.html", username=session['username'],user=user)


@app.route('/logout')
def logout_user():
    User.logout()
    return render_template('index_home.html')


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


if __name__ == '__main__':
    app.run(port=5001, debug=True)