#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def video_publisher():
    rospy.init_node('video_publisher', anonymous=True)
    video_file = 'neel_Roxbury11.mp4'  # Replace this with your video file path
    video_capture = cv2.VideoCapture(video_file)

    if not video_capture.isOpened():
        rospy.logerr("Error opening video file!")
        return

    frame_rate = rospy.Rate(30)  # Adjust frame rate as needed
    bridge = CvBridge()
    publisher = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

    while not rospy.is_shutdown() and video_capture.isOpened():
        ret, frame = video_capture.read()
        
        if ret:
            # Convert the frame to a ROS image message
            ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
            # Publish the frame as a ROS message
            publisher.publish(ros_image)
        else:
            break

        frame_rate.sleep()

    video_capture.release()

if __name__ == '__main__':
    try:
        video_publisher()
    except rospy.ROSInterruptException:
        pass
