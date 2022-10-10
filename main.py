import sqlite3
from flask import Flask, request, redirect, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

import base64

from repository.UserRepository import UserRepository
from repository.ShortURLRepository import ShortURLRepository

from service.ShortURLService import ShortURLService

userRepository = UserRepository()
shortURLRepository = ShortURLRepository()

shortURLService = ShortURLService()

app = Flask(__name__)

loginManage = LoginManager()
loginManage.init_app(app)
loginManage.login_view = 'login'


class SLUser(UserMixin):
    def __init__(self, email):
        self.id = email


@loginManage.unauthorized_handler
def unauthorized_handler():
    return redirect('/login')


@loginManage.user_loader
def user_loader(email):
    return SLUser(email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        enPassword = base64.b64encode(request.form['password'].encode('ascii')).decode('ascii')
        if userRepository.isExistUserByEmailAndPassword(email, enPassword):
            login_user(SLUser(email))
            return redirect('/')
        return render_template('Login.html', error='Invalid Credentials!', email=email)
    return render_template('Login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        CREATE_USER = '''
            INSERT INTO user(email, enPassword) values(?, ?);
        '''
        FIND_USER_BY_EMAIL = '''
            SELECT email
            FROM user
            WHERE email = ?
        '''
        email = request.form['email']
        enPassword = base64.b64encode(request.form['password'].encode('ascii')).decode('ascii')
        with sqlite3.connect("short-links-demo.db") as con:
            result = con.execute(FIND_USER_BY_EMAIL, [email])
            print(result.rowcount)
            if(result.rowcount == -1):
                result = con.execute(CREATE_USER, (email, enPassword))
                login_user(SLUser(email))
                return redirect('/')
            else:
                error = "Email with Email already exists!"
                return render_template("SignUp.html", error = error)
    return render_template('SignUp.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/', methods=['GET'])
def index():
    return redirect('/home')


@app.route('/home', methods=['GET'])
@login_required
def home():
    urls = shortURLRepository.findShortURLByEmail(current_user.id)
    return render_template('Home.html', email=current_user.id, urls=urls)


@app.route('/home/createSL', methods=['POST'])
@login_required
def createSL():
    nextId = shortURLRepository.nextID()
    email = current_user.id
    label = request.form['label']
    shortURL = shortURLService.idToShortURL(nextId)
    actualURL = request.form['actualURL']
    enPassword = base64.encode(request.form['password'].encode('ascii')).decode('ascii') if request.form['password'] else ''
    if shortURLRepository.createSHORTURL(nextId, email, label, shortURL, actualURL, 2, enPassword):
        return redirect('/')
    return redirect('/home?page=createSL&error=ServerError')


@app.route('/<shortURL>', methods=['GET'])
def redirectToActualURL(shortURL):
    shortURLObj = shortURLRepository.findShortURLByShortURL(shortURL)
    print(shortURLObj)
    if shortURLObj is None:
        return f'Oops! {shortURL} does not exist!<a href="/">Home</a>'
    return redirect(shortURLObj[4])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'secret'
    app.run(host='0.0.0.0', port=3000)
