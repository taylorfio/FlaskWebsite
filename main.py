# https://pythonhow.com/how-a-flask-app-works/
from flask import Flask, render_template, Response, redirect, url_for, request
from camara import VideoCamera

app = Flask(__name__)
colour = 'light'


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/colourmode')
def colourmode():
    global colour
    if colour == 'light':
        colour = 'dark'
        return render_template('home.html', color=colour)
    elif colour == 'dark':
        colour = 'light'
        return render_template('home.html', color=colour)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# add login blocker
# add colour mode

# use command ./ngrok http 5000
