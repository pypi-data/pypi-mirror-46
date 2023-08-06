from distutils.sysconfig import get_python_lib
from os import path
from pathlib import Path

import numpy as np

from video_pipeline.frame_filter import FrameFilter


class FaceTrackerFrameFilter(FrameFilter):
    """Frame filter for visualizing the default opencv face detection.

    Taken directly from the [opencv-python-tutorials](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html#basics).
    """  # noqa: E501

    def _get_cv2_data_file(self, file_path: str) -> Path:
        return Path(path.join(get_python_lib(), 'cv2/data/', file_path))

    def __init__(self) -> None:
        # External Dependencies.
        import cv2

        self._face_cascade = cv2.CascadeClassifier(str(self._get_cv2_data_file('haarcascade_frontalface_default.xml')))
        self._eye_cascade = cv2.CascadeClassifier(str(self._get_cv2_data_file('haarcascade_eye.xml')))

    def process_frame(self, frame: np.array) -> np.array:
        # External Dependencies.
        import cv2

        # Process.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self._eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        return frame
