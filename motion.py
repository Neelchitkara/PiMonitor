import cv2
import numpy as np


def prepare_frame(jpeg_bytes):
    encoded_frame = np.frombuffer(jpeg_bytes, dtype=np.uint8)

    colour_frame = cv2.imdecode(
        encoded_frame,
        cv2.IMREAD_COLOR
    )

    gray_frame = cv2.cvtColor(
        colour_frame,
        cv2.COLOR_BGR2GRAY
    )

    blurred_frame = cv2.GaussianBlur(
        gray_frame,
        (21, 21),
        0
    )

    return colour_frame, blurred_frame

class MotionDetector:
    def __init__(self, minimum_area=1500, pixel_threshold=25):
        self.minimum_area = minimum_area
        self.pixel_threshold = pixel_threshold
        self.previous_frame = None

    def detect(self, jpeg_bytes):
        colour_frame, current_frame = prepare_frame(jpeg_bytes)

        if self.previous_frame is None:
            self.previous_frame = current_frame
            return colour_frame, []

        frame_difference = cv2.absdiff(
            self.previous_frame,
            current_frame
        )

        threshold_image = cv2.threshold(
            frame_difference,
            self.pixel_threshold,
            255,
            cv2.THRESH_BINARY
        )[1]

        threshold_image = cv2.dilate(
            threshold_image,
            None,
            iterations=2
        )

        contours, _ = cv2.findContours(
            threshold_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        motion_regions = []

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < self.minimum_area:
                continue

            motion_regions.append(
                cv2.boundingRect(contour)
            )

        self.previous_frame = current_frame

        return colour_frame, motion_regions
    def annotate(self, colour_frame, motion_regions):
        motion_detected = len(motion_regions) > 0

        if motion_detected:
            colour = (0, 0, 255)
            label = "MOTION DETECTED"
        else:
            colour = (0, 180, 0)
            label = "CLEAR"

        for x, y, width, height in motion_regions:
            cv2.rectangle(
                colour_frame,
                (x, y),
                (x + width, y + height),
                colour,
                2
            )

        cv2.putText(
            colour_frame,
            label,
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            colour,
            2
        )

        encoded_successfully, encoded_frame = cv2.imencode(
            ".jpg",
            colour_frame
        )

        if not encoded_successfully:
            raise RuntimeError(
                "OpenCV could not encode the camera frame"
            )

        return encoded_frame.tobytes()
