import cv2
import numpy as np

class CameraModule():
    """Additional module that process the camera data 
       for window laptop which are not working properly
       when just using Videocapture.
       So if there's no error occuring when just using cv itself,
       no need to use it.
       
    open_cam(self, cam_num)
        Start the camera
        
        Args(int): 
            cam_num (int): default 0
            
    read(self)
        Read the video by frame
        
        Returns: 
            cam_img (array): frame image if camera is opened
    
    close_cam(self)
        Close the camera
        
        Returns: 
            Bool : True if camera is opened, False if not
    """
    def __init__(self, width, height):
        self.image_width = width
        self.image_height = height

    def open_cam(self, cam_num):
        self.cam = cv2.VideoCapture(cv2.CAP_DSHOW + cam_num)
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)

    def read(self):
        if self.cam.isOpened():
            _, cam_img = self.cam.read()
            return cam_img
        else:
            return False, []    

    def close_cam(self):
        if self.cam.isOpened():
            self.cam.release()
            return True
        else:
            return False
        
class imagePreprocess():
    """Module for preprocessing
    
    get_roi_vertices(image)
        Defining the region of interest

        Args:
            image (array): image to define region of interest

        Returns:
            array: matrix of the region of interest
            
    apply_canny(image)
        Apply Canny edge detection

        Args:
            image (array): array to detect edges

        Returns:
            edges: edges in white, backgrounds in black.
    """
    
    def get_roi_vertices(image):
        """Defining the region of interest

        Args:
            image (array): image to define region of interest

        Returns:
            array: matrix of the region of interest
        """
        
        #get the shape of the image
        height, width = image.shape[:2]
        
        #set the region of interest, modify if needed
        roi_bottom_left = (width // 2 - 50, height - 300)
        roi_top_left = (width // 2 - 400, height // 2 + 100)
        roi_top_right = (width // 2 + 400, height // 2 + 100)
        roi_bottom_right = (width // 2 + 50, height - 300)

        return np.array([[roi_bottom_left, roi_top_left, roi_top_right, roi_bottom_right]], dtype=np.int32)

    def apply_canny(image):
        """Apply Canny edge detection

        Args:
            image (array): array to detect edges

        Returns:
            edges: edges in white, backgrounds in black.
        """
        
        #convert to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #blur the noise
        blur = cv2.GaussianBlur(gray, (5, 7), 0)

        # Threshold the image to extract white lane markings
        _, thresholded = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
        
        #find the edges
        edges = cv2.Canny(thresholded, 50, 150)
        
        return edges
    
    def bird_eye(image):
        # Define the source and destination points for perspective transformation
        src_points = np.float32([[320, 400], [640, 400], [320, 300], [450, 300]])
        dst_points = np.float32([[0, 480], [640, 480], [0, 0], [640, 0]])

        # Perform perspective transformation
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        warped = cv2.warpPerspective(image, M, (640, 480))
        
        return warped
    
    

class lineModule():

    def get_lines(frame):
        """Get lines from the frame image

        Args:
            frame (array): frame image in array

        Returns:
            lines: all line from the frame
        """
        
        #modify params
        lines = cv2.HoughLinesP(frame, rho=1, 
                                theta=np.pi / 180, 
                                threshold=100, 
                                minLineLength= 100, 
                                maxLineGap=50)
        return lines
    
    global first
    global pos
    first = True
    pos = 450
    
    def classify_lines(frame, lines):
        """classify lane lines into left and right

        Args:
            frame (array): frame image in array
            lines (list): list of lane lines

        Returns:
            left_lane: mean of lane in left side
            right_lane: mean of lane in right side
        """
        dup_frame = frame
        
        #get shape of frame
        height, width = frame.shape[:2]
        
        #initiate list of left/right lanes
        right_lane_lines = []
        # Add a lane with slope 0 at the right end as a fallback
        right_lane_lines.append([[width - 1, 480, width - 1, 0]])


        #classify
        if lines is not None:    
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)        #get points
                slope = (y2 - y1) / (x2 - x1 + 1e-6)    #calculate slope
                right_lane_lines.append(line)
                # cv2.line(dup_frame, tuple(line[0][:2]), tuple(line[0][2:]), (0, 0, 255), 5)

        cv2.imshow("Line", dup_frame)
        
        #get the mean lane line

        right_lane = np.mean(np.array(right_lane_lines), axis=0, dtype=np.int32)
        if first:
            pos = (right_lane[0][0]+right_lane[0][2])/2
    
        return right_lane
    
    def get_command(image, right_lane):
        """make a command left most to 0, right most to 8, 9 for connercase

        Args:
            image (array): frame image in array
            left_lane (list): left lane [x1, y1, x2, y2]
            right_lane (list): right lane [x1, y1, x2, y2]

        Returns:
            median_slope: median slope of left/right lane
            command: command for driving
        """
        
        #shape of image
        height, width = image.shape[:2]
        
        # #calculate slope of left lane
        # x1, y1, x2, y2 = left_lane
        # left_slope = (y2 - y1) / (x2 - x1 + 1e-6)
        # # if y1 <y2:
        #     medx = x1*0.5
        # else:
        #     medx = x2*0.5

        #calculate slope of right lane
        x1, y1, x2, y2 = right_lane
        slope = (y2 - y1) / (x2 - x1 + 1e-6)
        c_pos = (x1+x2)/2
        # #median of both slope
        # median_slope = (left_slope + right_slope) / 2

        #need tomodify
        if c_pos > 638:
            command = 2
        elif c_pos > pos + 150:
            command = 6
        elif c_pos > pos + 30:
            command = 5
            
        elif c_pos > pos - 30:
            command = 4
        elif c_pos > pos - 80:
            command = 3
        else:
            command = 2

        return c_pos, command
