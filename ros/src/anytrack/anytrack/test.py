import subprocess
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
 
class test(Node): 
    def __init__(self):
        super().__init__("test") 

        self.FFMPEG_CMD = "ffmpeg -nostdin -i <rtsp_stream> -pix_fmt bgr24 -r 12 -an -vcodec rawvideo -f rawvideo -".split(" ")
        self.WIDTH = 800
        self.HEIGHT = 600
        self.process = subprocess.Popen(self.FFMPEG_CMD, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        self.bridge = CvBridge()
        self.publisher = self.create_publisher(msg_type=CompressedImage, topic="test", qos_profile=10)
    
    def ffmpeg_pipe(self):
        while True:
            raw_frame = self.process.stdout.read(self.WIDTH*self.HEIGHT*3)
            frame = np.frombuffer(raw_frame, np.uint8) 
            frame = frame.reshape((self.HEIGHT, self.WIDTH, 3))
            yield frame

    def stream_pub(self):
        generate = self.ffmpeg_pipe()
        while True:
            try:
                frame = next(generate)
                msg = self.bridge.cv2_to_compressed_imgmsg(frame, encoding="bgr8")
                # msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8)
                self.publisher.publish(msg)
            except CvBridgeError as e:
                print(str(e))

def main(args=None):
    rclpy.init(args=args)
    node = test() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
