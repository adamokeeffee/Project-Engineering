from picamera2 import Picamera2
import time

def start_camera():
    camera = Picamera2()
    config = camera.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    camera.configure(config)
    camera.start()

    try:
        while True:
            frame = camera.capture_array()
            print("Frame captured:", frame.shape)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        camera.close()