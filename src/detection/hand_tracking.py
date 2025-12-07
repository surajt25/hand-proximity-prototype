import cv2
import numpy as np
from utils.constants import MIN_CONTOUR_AREA, EXCLUDE_TOP_RATIO

class HandTracker:
    def __init__(self, min_contour_area=MIN_CONTOUR_AREA):
        self.min_contour_area = min_contour_area

    def get_skin_mask(self, frame):
        blurred = cv2.GaussianBlur(frame, (7, 7), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(blurred, cv2.COLOR_BGR2YCrCb)
       
        mask_hsv = cv2.inRange(hsv, (0, 30, 60), (25, 255, 255)) | \
                   cv2.inRange(hsv, (160, 30, 60), (179, 255, 255))
        mask_ycrcb = cv2.inRange(ycrcb, (0, 133, 77), (255, 173, 127))
        mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        return mask

    
    def process_frame(self, frame):
        mask = self.get_skin_mask(frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, (None, None)

        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) < self.min_contour_area:
            return None, (None, None)

        M = cv2.moments(cnt)
        if M["m00"] == 0:
            return None, (None, None)
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        # ignoring  top region (face area)
        if cy < int(EXCLUDE_TOP_RATIO * frame.shape[0]):
            return None, (None, None)
        
        return cnt, (cx, cy)