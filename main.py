# https://pythonhow.com/how-a-flask-app-works/
from flask import Flask, render_template, Response, redirect, url_for, request
from camara import VideoCamera
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import hashlib

app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id, "temp")


class User(UserMixin):
    def __init__(self, id, username):
        self.username = username
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@app.route('/')
def gotologin():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            login_user(User(0, password))
            return redirect(url_for('home'))
    return render_template('login.html', error=error)



[0]
"""

try:  # opens the files to read to see if a username exists and write new usernames and passwords
    file = open("user.txt", "r")
except IOError:
    print("can't find password file")

temp_list = sign_in()  # calls the function
account_username = request.form['username'] # the first part of the list is the username input

hasher = hashlib.md5()  # the hasher import is called
hasher.update(request.form['password']('utf-8'))  # the hasher is hashing the password input from the list
password = hasher.hexdigest()  # the hashed password is linked to account_password string

"""










@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.config["SECRET_KEY"] = 'ITSASECRET'
    app.run(host='0.0.0.0', debug=True)

# add login blocker
# add colour mode

# use command ./ngrok http 5000
