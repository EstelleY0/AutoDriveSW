import cv2
import numpy as np
from module import *


# Calculate slope and direction
def calculate_slope_and_direction(image, left_lane, right_lane):
    height, width = image.shape[:2]
    x1, y1, x2, y2 = left_lane
    left_slope = (y2 - y1) / (x2 - x1 + 1e-6)

    x1, y1, x2, y2 = right_lane
    right_slope = (y2 - y1) / (x2 - x1 + 1e-6)

    median_slope = (left_slope + right_slope) / 2

    if median_slope < -0.1:
        direction = "Left"
    elif median_slope > 0.1:
        direction = "Right"
    else:
        direction = "Straight"

    return median_slope, direction

# Open video capture
cap = CameraModule(width = 640, height=480)
cap.open_cam(1)

while True:
    frame = cap.read()

    cv2.imshow("Lane Detection", frame)
    # Apply image processing pipeline
    edges = imagePreprocess.apply_canny(frame)
    roi = imagePreprocess.get_roi_vertices(edges)
    masked = cv2.fillPoly(edges, roi, (0, 0, 0))

    # Get Hough lines and fit lane lines
    lines = lineModule.get_lines(masked)
    left_lane, right_lane = lineModule.classsify_lines(frame, lines)

    # Draw lane lines
    cv2.line(frame, tuple(left_lane[0][:2]), tuple(left_lane[0][2:]), (0, 0, 255), 5)
    cv2.line(frame, tuple(right_lane[0][:2]), tuple(right_lane[0][2:]), (0, 0, 255), 5)

    # Calculate slope and direction
    slope, direction = calculate_slope_and_direction(frame, left_lane[0], right_lane[0])

    # Display slope and direction on the frame
    cv2.putText(frame, f"Slope: {slope:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Direction: {direction}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Lane Detection", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
