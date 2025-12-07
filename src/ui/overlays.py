import cv2
import numpy as np
from utils.constants import OBJECT_RADIUS, LINE_X, DANGER_THRESHOLD, WARNING_THRESHOLD

class Overlays:
    def __init__(self):
        pass

    def draw_object_and_line(self, frame, line_x):
        h, _ = frame.shape[:2]
        cv2.line(frame, (line_x, 0), (line_x, h), (0, 255, 255), 3)
        cv2.putText(frame, "DANGER LINE", (line_x - 70, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    def draw_status(self, frame, state, fps):
        h, w = frame.shape[:2]
        color = (0, 255, 0) if state == "SAFE" else (0, 165, 255) if state == "WARNING" else (0, 0, 255)
        cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"State: {state}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        if state == "DANGER":
            cv2.putText(frame, "DANGER DANGER", (w // 2 - 170, h // 2),
                        cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 4)


    def draw_hand(self, frame, contour, centroid):
        if contour is not None:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        if centroid[0] is not None:
            cv2.circle(frame, centroid, 6, (255, 0, 255), -1)