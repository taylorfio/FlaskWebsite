"""
The purpose of this website is to demonstrate my understanding of Flask, open-cv and raspberry pi

This project is a webapp that runs from local server on a raspberry pi and takes inputs to control motors
to move the robot and to pull the trigger on a nerf gun while aiming through the live feed from a camera.

Note: I couldn't get it to run on the raspberry pi but separate they work. To run the website use main.py and to
control the raspberry pi use bettertest.py

look at SecurityWebsite in my github for an example of what this could have looked like
"""

# this can't be run but main.py can be
from flask import Flask, render_template, Response, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import hashlib
import RPi.GPIO as gpio  # works with raspberry pi
import time
from camara import VideoCamera  # imports file that runs video capture

app = Flask(__name__)

# flask-login set up
login_manager = LoginManager()
login_manager.init_app(app)


def init():  # creates a callable gpio set up for motor with wheel
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)


def forward(sec):  # orders gpio pins to create forwards motion
    init()  # calls gpio set up
    gpio.output(17, True)  # turns on True gpio
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()  # resets the gpio pins


def reverse(sec):  # orders gpio pins to create backwards motion
    init()  # calls gpio set up
    gpio.output(17, False)  # turns on True gpio
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()  # resets the gpio pins


def motor_on():
    gpio.setmode(gpio.BCM)
    gpio.setup(21, gpio.OUT)  # calls gpio pin
    gpio.output(21, gpio.HIGH)  # Turn relay motor on
    time.sleep(1)  # waits so it runs smoothly
    gpio.output(21, gpio.LOW)  # Turn relay motor off
    time.sleep(3)  # waits three second while it runs
    gpio.cleanup()  # resets the gpio pins to turn it off


@login_manager.user_loader  # loads and checks the user for login
def load_user(user_id):
    return User(user_id, "temp")  # returns user id


class User(UserMixin):  # sets user id
    def __init__(self, id, username):
        self.username = username
        self.id = id


@app.route('/')  # page that loads first
def gotologin():
    return redirect(url_for('login'))  # redirects for login


@app.route('/login', methods=['GET', 'POST'])  # login page
def login():
    error = None
    global file_password, file_user  # allows the variables to be called through out function
    if request.method == 'POST':  # if input for login is being entered

        try:  # opens the text file with the hashed password and username
            file = open("user.txt", "r")  # opens file
            file_user = file.readlines(1)  # reads the user from the first line
            file_password = file.readlines(0)  # reads the hashed password from the second line     PYTHON BROKEOZ
        except IOError:  # if file not found it print the error message
            print("can't find password file")

        hasher = hashlib.md5()  # the hasher import is called
        hasher.update(request.form['password'].encode('utf-8'))  # the hasher is hashing the password input
        password = hasher.hexdigest()  # the hashed password is linked to account_password string

        if request.form['username'] != file_user[0].strip() or password != file_password[0].strip():
            # compares the inputs to the saved user and password
            error = 'Invalid Credentials. Please try again.'  # error message if they don't match
        else:
            login_user(User(0, 'admin'))  # sets user for flask-login so you can get past @login_required
            return redirect(url_for('home'))  # redirects you to the home page
    return render_template('login.html', error=error)  # loads the login page


@app.route('/logout')
@login_required  # won't load page if login requirements not met
def logout():
    logout_user()  # runs the logout function from the flask-login module
    return redirect(url_for('login'))  # returns you to the login page


@app.route('/home', methods=['GET', 'POST'])
@login_required  # won't load page if login requirements not met
def home():
    if request.method == 'POST':  # if input entered
        if request.form['left']:  # if input is left
            reverse(1)  # runs motor reverse for 1 second
        elif request.form['right']:  # if input is right
            forward(1)  # runs motor forward for 1 second
        elif request.form['fire']:  # if input is fire
            motor_on()  # runs the motor controlled by a relay

    return render_template('home.html')  # loads the home page


def gen(camera):
    while True:
        frame = camera.get_frame()  # runs the camera file to get frames from camera
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
@login_required  # won't load if login requirements not met
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    # returns the video frames from camera


@app.route('/about')
@login_required  # won't load page if login requirements not met
def about():
    return render_template('about.html')  # loads the about page


if __name__ == '__main__':
    app.config["SECRET_KEY"] = 'ITSASECRET'  # sets the key for flask
    app.run(host='0.0.0.0', debug=True)  # runs the app

# note: use command ./ngrok http 5000 to host with ngrok
