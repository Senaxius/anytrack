import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

import math as m
import cv2
import numpy as np
from scipy.spatial.transform import Rotation   

from scanner_interfaces.msg import CameraLocations
from scanner_interfaces.msg import Tracks
from scanner_interfaces.msg import Object
from scanner_interfaces.msg import Location
from sensor_msgs.msg import CameraInfo

class calibration(Node): 
    def __init__(self):
        super().__init__("calibration") 
        # declare Parameters
        self.declare_parameter("device_count", 2)
        self.declare_parameter("width", 1280)
        self.declare_parameter("height", 720)

        # import parameters
        self.device_count = self.get_parameter("device_count").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value

        # debug only
        self.device_count = 2
        self.width = 1280
        self.height = 720

        self.get_logger().info("Starting calibrator...")

        loop_group = MutuallyExclusiveCallbackGroup()
        tracks_group = ReentrantCallbackGroup()
        info_group = ReentrantCallbackGroup()

        # create calibration publisher
        self.publisher = self.create_publisher(msg_type=CameraLocations, topic="calibration", qos_profile=10)

        # create variables to store output and input for calibration
        self.output = dict()
        self.input = dict()

        # create subscribers
        for i in range(self.device_count):
            self.create_subscription(msg_type=Tracks, topic=('/cam' + str(i) + '/tracks'), callback=self.create_tracks_callback(i), qos_profile=10, callback_group=tracks_group)
            self.create_subscription(msg_type=CameraInfo, topic=('/cam' + str(i) + '/camera_info'), callback=self.create_info_callback(i), qos_profile=10, callback_group=info_group)
            self.output.update({i: {
                'x': float(i*1.5),
                'y': 0.0,
                'z': 0.0,
                'ax': 0.0,
                'ay': 0.0,
                'az': 0.0,
            }})
            self.input.update({i: {
                'fx': 0.0,
                'fy': 0.0,
                'cx': 0.0,
                'cy': 0.0,
                'camera_matrix': None,
                'dist_matrix': None,
                'buffer': [],
                'objects': [],
            }})
        
        # reset camera position
        self.publish_calibration()

        # checks
        self.info_check = 0
        self.date_check = 0
        # main loop
        self.loop = self.create_timer(0.1, self.loop_callback, callback_group=loop_group)


    def loop_callback(self):
        # check if input is good to calibrate
        if self.info_check == 0:
            for cam in self.input:
                self.info_check = 1
                if self.input[cam]['fx'] == 0.0:
                    self.info_check = 0
                    print("no camera_matrix received yet")
                    return
        
        # check if every camera detected one object
        for cam in self.input:
            if len(self.input[cam]['buffer']) != 1:
                print("not every camera detected one object")
                return
        
        # add the object to the calibration data
        for cam in self.input:
            # undistort Points
            input = self.input[cam]
            distorted_point = (input['buffer'][0].x, input['buffer'][0].y)
            camera_matrix = input['camera_matrix']
            # print(camera_matrix)
            point = cv2.undistortPoints(distorted_point, cameraMatrix=camera_matrix, distCoeffs=None, P=None)
            point = point.flatten()
            # print(distorted_point)
            # print(point)
            point = (point[0], point[1])
            # if cam == 1:
            #     self.output[1]['x'] = point[0]
            #     self.output[1]['y'] = point[1]
            #     self.output[1]['z'] = 2.0

            input['objects'].append(point)
            # input['objects'].append(distorted_point)

        # check if there is enough data to start calibration 
        if self.date_check == 0:
            for cam in self.input:
                self.date_check = 1
                if len(self.input[cam]['objects']) <= 7:
                    self.date_check = 0
                    print("not enough data to calibrate")
                    return


        # calculate position for number of cameras in relation to cam0
        for cam in range(self.device_count - 1):
            index = cam + 1

            cam0_points = np.array(self.input[0]['objects'])
            cam1_points = np.array(self.input[index]['objects'])

            R = np.zeros(shape=(3, 3))
            t = np.zeros(shape=(3, 3))
            E = np.zeros(shape=(3, 3))

            identity_matrix = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            # print(cam1_points[-1])

            E, _ = cv2.findEssentialMat(
                points1 = cam0_points,
                points2 = cam1_points,
                focal = 1.0,
                pp = (0.0, 0.0),
                # cameraMatrix = self.input[0]['camera_matrix'],
                # cameraMatrix = identity_matrix,
                method = cv2.LMEDS,
                prob = 0.999,
                threshold = 0.001,
                maxIters = None,
            )
            # print(E)

            _, R, t, _ = cv2.recoverPose(
                E,
                cam0_points,
                cam1_points,
                focal=self.input[0]['fx'],
                # focal=1.0,
                pp=(640.6, 360.5),
                # pp=(0, 0),
                mask=None,
            )

            t = np.matmul(np.linalg.inv(R), t)
            t = t.flatten()
            r = Rotation.from_matrix(R)
            angles = r.as_euler("zyx", degrees=False)

            # write into calibration buffer to publish
            self.output[index]['x'] =  round(t[0] * -2, 2)
            self.output[index]['y'] =  round(t[1] * -2, 2)
            self.output[index]['z'] =  round(t[2] * -2, 2)

            self.output[index]['ax'] = round(angles[0] * -1, 2)
            self.output[index]['ay'] = round(angles[1] * -1, 2)
            self.output[index]['az'] = round(angles[2] * -1, 2)

            # publish calibration data for live preview
            self.publish_calibration()

            print("translation: (" + str(round(t[2], 1)), end='')
            print(", " + str(round(t[0], 1)), end='')
            print(", " + str(round(t[1], 1)), end='')
            print(")")

            print("rotation (in degrees): (" + str(round(angles[1], 2)), end='')
            print(", " + str(round(angles[0], 2)), end='')
            print(", " + str(round(angles[2], 2)), end='')
            print(")")
    
    def create_tracks_callback(self, index):
        return lambda msg:self.tracks_callback(msg, index)
    def create_info_callback(self, index):
        return lambda msg:self.info_callback(msg, index)
    
    def tracks_callback(self, msg, index):
        self.input[index]['buffer'] = []
        for object in msg.tracks:
            self.input[index]['buffer'].append(object)
    def info_callback(self, msg, index):
        self.input[index]['fx'] = (msg.p[0] * (self.width / msg.width))
        self.input[index]['fy'] = (msg.p[5] * (self.height / msg.height))
        self.input[index]['cx'] = (msg.p[2] * (self.width / msg.width))
        self.input[index]['cy'] = (msg.p[6] * (self.height / msg.height))
        # self.input[index]['camera_matrix'] = msg.k
        k = msg.k
        self.input[index]['camera_matrix'] = np.matrix([[k[0], k[1], k[2]], [k[3], k[4], k[5]], [k[6], k[7], k[8]]])


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
    node = calibration() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
