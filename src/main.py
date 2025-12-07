import time
import cv2
from camera import Camera
from detection.hand_tracking import HandTracker
from ui.overlays import Overlays
from utils.constants import LINE_X, DANGER_THRESHOLD, WARNING_THRESHOLD, LINE_THRESHOLD

dragging_line = False

def mouse_event(event, x, y, flags, param):
    global dragging_line, line_x
    if event == cv2.EVENT_LBUTTONDOWN:
        if abs(x - line_x) < LINE_THRESHOLD:
            dragging_line = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging_line:
            line_x = x
    elif event == cv2.EVENT_LBUTTONUP:
        dragging_line = False

def main():
    global line_x
    camera = Camera()
    hand_tracker = HandTracker()
    overlays = Overlays()

    line_x = LINE_X
    prev = time.time()

    cv2.namedWindow("Hand Proximity Prototype")
    cv2.setMouseCallback("Hand Proximity Prototype", mouse_event)

    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        frame = cv2.flip(frame, 1)

        hand_contour, centroid = hand_tracker.process_frame(frame)
        state = "NO HAND"

        if hand_contour is not None and centroid[0] is not None:
            cx, cy = centroid
            tip = max(hand_contour, key=lambda p: (p[0][0]-cx)**2 + (p[0][1]-cy)**2)[0]
            crossed = tip[0] < line_x
            # no distance check now; just line crossing
            if crossed:
                state = "DANGER"
            else:
                state = "SAFE"

        fps = int(1 / max(time.time() - prev, 1e-6))
        prev = time.time()

        overlays.draw_object_and_line(frame, line_x)
        overlays.draw_hand(frame, hand_contour, centroid)
        overlays.draw_status(frame, state, fps)

        cv2.imshow("Hand Proximity Prototype", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()