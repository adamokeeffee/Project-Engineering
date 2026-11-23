from picamera2 import Picamera2
import time
import cv2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    camera = Picamera2()
    config = camera.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    camera.configure(config)
    camera.start()

    try:
        while True:
            frame = camera.capture_array()
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        camera.close()

        
@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_camera():
    app.run(host='0.0.0.0', port=5000, threaded=True)