import cv2

class Camera:
    def __init__(self, index=0, width=640, height=480):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ok, frame = self.cap.read()
        return frame if ok else None

    def release(self):
        if self.cap:
            self.cap.release()