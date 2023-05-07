import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from scanner_interfaces.msg import CameraLocations
from scanner_interfaces.msg import Location

import numpy as np
import cv2
from scipy.spatial.transform import Rotation   

class test(Node): 
    def __init__(self):
        super().__init__("test") 

        self.device_count = 2

        # publisher
        self.publisher = self.create_publisher(msg_type=CameraLocations, topic="calibration", qos_profile=10)

        for i in range(self.device_count):
            self.output.update({i: {
                'x': float(i*1.5),
                'y': 0.0,
                'z': 0.0,
                'ax': 0.0,
                'ay': 0.0,
                'az': 0.0,
            }})
            self.input.update({i: {
                'time': 0,
                'camera_matrix': [],
                'dist_matrix': [],
                'buffer': [],
                'objects': [],
            }})
        
        cam0_points = np.array([])
        cam1_points = np.array([])

        R = np.zeros(shape=(3, 3))
        t = np.zeros(shape=(3, 3))
        E = np.zeros(shape=(3, 3))

        E, _ = cv2.findEssentialMat(
            points1 = cam0_points,
            points2 = cam1_points,
            focal = 1.0,
            pp = (0.0, 0.0),
            method = cv2.RANSAC,
            prob = 0.999,
            threshold = 0.0001,
            maxIters = None,
        )

        _, R, t, _ = cv2.recoverPose(
            E,
            cam0_points,
            cam1_points,
            focal=1.0,
            pp=(0, 0),
            mask=None,
        )

        t = np.matmul(np.linalg.inv(R), t)
        t = t.flatten()
        r = Rotation.from_matrix(R)
        angles = r.as_euler("zyx", degrees=False)

        # write into calibration buffer to publish
        self.output[1]['x'] =  round(t[0] * -1, 2)
        self.output[1]['y'] =  round(t[1] * -1, 2)
        self.output[1]['z'] =  round(t[2] * -1, 2)
        self.output[1]['ax'] = round(angles[0] * -1, 2)
        self.output[1]['ay'] = round(angles[1] * -1, 2)
        self.output[1]['az'] = round(angles[2] * -1, 2)

        self.publish_calibration()

    def publish_calibration(self):
        msg = CameraLocations()
        for i in range(self.device_count):
            location = Location()
            location.id = i
            location.x = self.output[i]['x']
            location.y = self.output[i]['y']
            location.z = self.output[i]['z']
            location.ax = self.output[i]['ax']
            location.ay = self.output[i]['ay']
            location.az = self.output[i]['az']
            msg.locations.append(location)
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = test() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
