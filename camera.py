from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import io
import threading

from motion import MotionDetector

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buffer):
        with self.condition:
            self.frame = bytes(buffer)
            self.condition.notify_all()
	

        return len(buffer)


camera = Picamera2()

camera.configure(
    camera.create_video_configuration(
        main={"size": (640, 480)}
    )
)

output = StreamingOutput()
motion_detector = MotionDetector()

camera.start_recording(
    JpegEncoder(),
    FileOutput(output)
)


def generate_frames():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        
        colour_frame, motion_regions = motion_detector.detect(frame)

        annotated_frame = motion_detector.annotate(
            colour_frame,
            motion_regions
        )

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + annotated_frame
            + b"\r\n"
        )
def get_motion_status():
    return motion_detector.get_status()
