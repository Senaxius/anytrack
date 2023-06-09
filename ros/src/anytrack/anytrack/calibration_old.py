import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

import cv2
import numpy as np
from scipy.spatial.transform import Rotation   
import threading as th
import json

from interfaces.msg import CameraLocationList, Object2dList
from interfaces.msg import Object2d
from interfaces.msg import CameraLocation
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
        # self.device_count = 2
        # self.width = 1280
        # self.height = 720

        self.get_logger().info("Starting calibrator...")

        loop_group = MutuallyExclusiveCallbackGroup()
        tracks_group = ReentrantCallbackGroup()
        info_group = ReentrantCallbackGroup()

        # create calibration publisher
        self.publisher = self.create_publisher(msg_type=CameraLocationList, topic="calibration", qos_profile=10)

        # create variables to store output and input for calibration
        self.output = dict()
        self.input = dict()
        self.average = dict()

        # create subscribers
        for i in range(self.device_count):
            self.create_subscription(msg_type=Object2dList, topic=('/cam' + str(i) + '/tracks'), callback=self.create_tracks_callback(i), qos_profile=10, callback_group=tracks_group)
            self.create_subscription(msg_type=CameraInfo, topic=('/cam' + str(i) + '/camera_info'), callback=self.create_info_callback(i), qos_profile=10, callback_group=info_group)
            self.output.update({i: {
                'x': float(i * 1.5),
                'y': 0.0,
                'z': 0.0,
                'ax': 0.0,
                'ay': 0.0,
                'az': 0.0,
                'scale': 1.0
            }})
            self.average.update({i: {
                'x': [],
                'y': [],
                'z': [],
                'ax': [],
                'ay': [],
                'az': [],
            }})
            self.input.update({i: {
                'time': 0,
                'camera_matrix': [],
                'dist_matrix': [],
                'buffer': [],
                'objects': [],
            }})
        
        self.average_counter = 10
        
        # reset camera position
        self.publish_calibration()

        # checks
        self.info_check = 0
        self.date_check = 0

        self.key = 0
        th.Thread(target=self.key_capture, args=(), name='key_capture_thread', daemon=True).start()

        # main loop
        self.loop = self.create_timer(0.1, self.loop_callback, callback_group=loop_group)

    def key_capture(self):
        input()
        self.key += 1

    def loop_callback(self):
        # check if input is good to calibrate
        if self.info_check == 0:
            for cam in self.input:
                self.info_check = 1
                if len(self.input[cam]['camera_matrix']) == 0:
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
            if len(input['buffer']) != 1:
                print("ohno")
                return
            distorted_point = (input['buffer'][0].x, input['buffer'][0].y)
            camera_matrix = input['camera_matrix']
            dist_matrix = input['dist_matrix']
            point = cv2.undistortPoints(distorted_point, cameraMatrix=camera_matrix, distCoeffs=dist_matrix, P=None)
            point = point.flatten()
            point = (point[0], point[1])
            # print(point)
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

            # diff = abs((self.input[0]['time'] - self.input[index]['time']) / 1000000000)
            # print(diff)
            # if diff >= 0.01:
            #     print("time difference too big!")
            #     return

            try: 
                E, _ = cv2.findEssentialMat(
                    points1 = cam0_points,
                    points2 = cam1_points,
                    focal = 1.0,
                    pp = (0.0, 0.0),
                    method = cv2.RANSAC,
                    prob = 0.999,
                    threshold = 0.001,
                    maxIters = None,
                )
            except:
                print("Error occurd, try again!")
                return
            
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
            self.output[index]['x'] =  t[0] * -1
            self.output[index]['y'] =  t[1] * -1
            self.output[index]['z'] =  t[2] * -1
            self.output[index]['ax'] = angles[0] * -1
            self.output[index]['ay'] = angles[1] * -1
            self.output[index]['az'] = angles[2] * -1

            # Filter
            self.average[index]['x'].append(self.output[index]['x'])
            self.average[index]['y'].append(self.output[index]['y'])
            self.average[index]['z'].append(self.output[index]['z'])
            self.average[index]['ax'].append(self.output[index]['ax'])
            self.average[index]['ay'].append(self.output[index]['ay'])
            self.average[index]['az'].append(self.output[index]['az'])

            if len(self.average[index]['x']) > self.average_counter:
                self.average[index]['x'].pop(0)
                self.average[index]['y'].pop(0)
                self.average[index]['z'].pop(0)
                self.average[index]['ax'].pop(0)
                self.average[index]['ay'].pop(0)
                self.average[index]['az'].pop(0)

            self.output[index]['x']  = sum(self.average[index]['x']) / len(self.average[index]['x'])
            self.output[index]['y']  = sum(self.average[index]['y']) / len(self.average[index]['y']) 
            self.output[index]['z']  = sum(self.average[index]['z']) / len(self.average[index]['z']) 
            self.output[index]['ax'] = sum(self.average[index]['ax']) / len(self.average[index]['ax'])
            self.output[index]['ay'] = sum(self.average[index]['ay']) / len(self.average[index]['ay'])
            self.output[index]['az'] = sum(self.average[index]['az']) / len(self.average[index]['az'])

            self.output[index]['x']  = round(self.output[index]['x'], 2)
            self.output[index]['y']  = round(self.output[index]['y'], 2) 
            self.output[index]['z']  = round(self.output[index]['z'], 2) 
            self.output[index]['ax'] = round(self.output[index]['ax'], 3)
            self.output[index]['ay'] = round(self.output[index]['ay'], 3)
            self.output[index]['az'] = round(self.output[index]['az'], 3)


            # publish calibration data for live preview
            self.publish_calibration()
            print(self.output[index])

            # k=ord(getch.getch())
            if self.key >= 1:
                self.write_config()
                self.destroy_node()
    
    def create_tracks_callback(self, index):
        return lambda msg:self.tracks_callback(msg, index)
    def create_info_callback(self, index):
        return lambda msg:self.info_callback(msg, index)
    
    def tracks_callback(self, msg, index):
        self.input[index]['time'] = msg.header.stamp.sec * 1000000000 + msg.header.stamp.nanosec
        self.input[index]['buffer'] = []
        for object in msg.tracks:
            self.input[index]['buffer'].append(object)
    def info_callback(self, msg, index):
        k = msg.k
        d = msg.d
        self.input[index]['camera_matrix'] = np.matrix([[k[0], k[1], k[2]], [k[3], k[4], k[5]], [k[6], k[7], k[8]]])
        self.input[index]['dist_matrix'] = np.array([d[0], d[1], d[2], d[3], d[4]])

    def publish_calibration(self):
        msg = CameraLocationList()
        for i in range(self.device_count):
            location = CameraLocation()
            location.id = i
            location.x = self.output[i]['x']
            location.y = self.output[i]['y']
            location.z = self.output[i]['z']
            location.ax = self.output[i]['ax']
            location.ay = self.output[i]['ay']
            location.az = self.output[i]['az']
            msg.locations.append(location)
        self.publisher.publish(msg)
    
    def write_config(self):
        config = {}
        for i in range(self.device_count):
            config.update({str(i): self.output[i]})
        file = json.dumps(config)
        name = input("Config File Name: ")
        with open(("/home/ALEX/anytrack/config/positions/" + name + ".json"), "w") as outfile:
            outfile.write(file)
        print("Calibration done!")

def main(args=None):
    rclpy.init(args=args)
    node = calibration()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
