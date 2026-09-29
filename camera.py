from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import io
import threading


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

camera.start_recording(
    JpegEncoder(),
    FileOutput(output)
)


def generate_frames():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame
            + b"\r\n"
        )
