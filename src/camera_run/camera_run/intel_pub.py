import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import pyrealsense2 as rs
import numpy as np
 

class IntelPublisher(Node):
    def __init__(self):
        super().__init__("intel_publisher")
        self.intel_publisher_rgb = self.create_publisher(Image, "rgb_frame", 10) #datatype, topic name, queue list of 10

        timer_period = 0.05
        self.br_rgb = CvBridge()         # convert between numpy into image

        try:
            
            self.pipe = rs.pipeline()                                   # connection to camera
            self.cfg  = rs.config()
            self.cfg.enable_stream(rs.stream.color, 1280,720, rs.format.bgr8, 10)
            self.pipe.start(self.cfg)                                 #  connection to camera
            self.timer = self.create_timer(timer_period, self.timer_callback)
        except Exception as e:
            print(e)
            self.get_logger().error("INTEL REALSENSE IS NOT CONNECTED")

    def timer_callback(self):                                                # sending frames
        frames = self.pipe.wait_for_frames()                                 
        color_frame = frames.get_color_frame()               
        color_image = np.asanyarray(color_frame.get_data())

        self.intel_publisher_rgb.publish(self.br_rgb.cv2_to_imgmsg(color_image))     # here we publish color_image
        Image= cv2.imwrite('src/test.jpeg', color_image)
        # self.br_rgb.cv2_to_imgmsg(color_image))
        self.get_logger().info("Publishing rgb frame")
        print('frames:',type(frames))
        print('color_frame:',type(color_frame))
        print('color_image:',type(color_image))
        
        current_frame = color_image
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        img2 = cv2.medianBlur(gray,5)
        cannyed = cv2.Canny(gray, 200,300)
        #cv2.imshow('frames',color_frame)
        cv2.imshow('image',color_image)
        cv2.imshow('Cannyed',cannyed)
        cv2.waitKey(1)
   

def main(args = None):
    rclpy.init(args = None)
    intel_publisher = IntelPublisher()
    rclpy.spin(intel_publisher)
    intel_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()