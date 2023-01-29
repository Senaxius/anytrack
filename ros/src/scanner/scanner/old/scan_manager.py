import rclpy
from rclpy.node import Node
import time
import os
import cv2

class scan_manager(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("scan_manager") # MODIFY NAME

        self.active_cams = []
        self.devices = []

        self.get_logger().info("Starting scan_manager...")

        while (1):
            self.get_logger().info("Searching for devices...")
            self.search_devices()
            self.check_devices()

            time.sleep(1)

    def search_devices(self):
        buffer = []
        stream = os.popen('ls /dev/ | grep video')
        output = stream.read()
        if (output == ''):
            self.devices = []
            return
        output = output.strip()
        output = output.replace("video", '')
        output = output.replace("\n", ',')

        untested_devices = output.split(',')

        for index in untested_devices:
            command = "v4l2-ctl -d /dev/video" + index + " -D | grep 'Video Pixel Formatter'"
            stream = os.popen(command)
            output = stream.read()
            if (output != ''):
                buffer.append(int(index))

        self.devices = buffer

    def check_devices(self):
        for dev in self.devices:
            if dev not in self.active_cams:
                self.get_logger().info("Found new camera with index: " + str(dev))
                self.active_cams.append(dev)
                self.activate_cam(dev)

        for cam in self.active_cams:
            if cam not in self.devices:
                self.get_logger().info("Camera with index " + str(cam) + " stopped working!")
                self.active_cams.remove(cam)
                self.deactivate_cam(dev)
    
    def activate_cam(self, index):
        pass

    def deactivate_cam(self, index):
        pass
        

 
def main(args=None):
    rclpy.init(args=args)
    node = scan_manager() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()



 
 
if __name__ == "__main__":
    main()
