import cv2


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # deletes the old frames
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # OpenCV defaults to capture raw images so it must be encoded into JPEG in order to correctly display the video stream
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
