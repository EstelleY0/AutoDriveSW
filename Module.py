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
        roi_bottom_left = (width // 2 - 50, height - 50)
        roi_top_left = (width // 2 - 400, height // 2 + 100)
        roi_top_right = (width // 2 + 400, height // 2 + 100)
        roi_bottom_right = (width // 2 + 50, height - 50)

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
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        #find the edges
        edges = cv2.Canny(blur, 50, 150)
        return edges
    
    
class lineModule():


    def get_lines(image):
        lines = cv2.HoughLinesP(image, rho=1, theta=np.pi / 180, threshold=100, minLineLength=50, maxLineGap=50)
        return lines


    def classify_lines(image, lines):
        height, width = image.shape[:2]
        left_lane_lines = []
        right_lane_lines = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            if slope < 0 and x1 < width / 2:
                left_lane_lines.append(line)
            elif slope > 0 and x1 > width / 2:
                right_lane_lines.append(line)

        left_lane = np.mean(np.array(left_lane_lines), axis=0, dtype=np.int32)
        right_lane = np.mean(np.array(right_lane_lines), axis=0, dtype=np.int32)

        return left_lane, right_lane

