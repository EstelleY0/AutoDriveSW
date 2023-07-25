import cv2
import numpy as np
from module import *
import serial

#TODO
#case of one-side lane detected.
#written code is based on case of both lane are detected

# Open video capture
cap = CameraModule(width = 640, height=480)
cap.open_cam(0)

#fourcc = cv2.VideoWriter_fourcc(*'MP4V')
#out1 = cv2.VideoWriter('drive.mp4', fourcc, 20.0, (640,480))

# serial
ser = serial.Serial('COM10', 9600)


#mode = input()
mode = '0'
ser.write(mode.encode())

while mode == '0':
    frame = cap.read()
    cv2.imshow("original", frame)

    birdeye = imagePreprocess.bird_eye(frame)
    cv2.imshow("birdeye", birdeye)
        
    # Apply image processing pipeline
    edges = imagePreprocess.apply_canny(birdeye)
    cv2.imshow("canny", edges)
    
    # roi = imagePreprocess.get_roi_vertices(edges)
    # masked = cv2.fillPoly(edges, roi, (0, 0, 0))
    # cv2.imshow("mask", masked)
    masked = edges
    # roi = edges
    # Get lane lines, get alane from left/right each
    lines = lineModule.get_lines(masked)
    right_lane = lineModule.classify_lines(frame, lines)

    # Draw lane lines
    cv2.imshow("linnes", edges)
    rx1,ry1,rx2,ry2 = right_lane[0]
    cv2.line(frame, (rx1,ry1),(rx2,ry2), (0, 255,0), 5)
    
    # Calculate slope and direction
    slope, command = lineModule.get_command(frame, [rx1, ry1, rx2, ry2])

    # Display slope and direction on the frame
    cv2.putText(frame, f"Slope: {slope:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Command: {command}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Lane Detection", frame)
    try:
        ser.write(str(command).encode())
    except serial.SerialTimeoutException:
        ser.write('4'.encode())

    # 동영상 녹화
    #out1.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
# ser.close()
cv2.destroyAllWindows()
