# https://pythonhow.com/how-a-flask-app-works/
from flask import Flask, render_template, Response
from camara import VideoCamera

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
