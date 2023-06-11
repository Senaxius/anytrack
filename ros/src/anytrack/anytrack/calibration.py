import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

import cv2
import numpy as np
from scipy.spatial.transform import Rotation   
import threading as th
import json
import sys
import math as m
import time

from interfaces.msg import CameraLocationList
from interfaces.msg import Object2dList
from interfaces.msg import CameraLocation
from sensor_msgs.msg import CameraInfo

from visualization_msgs.msg import MarkerArray

sys.path.append('/home/ALEX/anytrack/python/lib')
import marker as mrk

class calibration(Node): 
    def __init__(self):
        super().__init__("calibration") 
        # declare Parameters
        self.declare_parameter("device_count", 2)
        self.declare_parameter("width", 1280)
        self.declare_parameter("height", 720)

        # import parameters
        self.device_count = self.get_parameter("device_count").value

        self.get_logger().info("Starting calibrator...")

        loop_group = MutuallyExclusiveCallbackGroup()
        tracks_group = ReentrantCallbackGroup()
        info_group = ReentrantCallbackGroup()

        # create calibration publisher
        self.publisher = self.create_publisher(msg_type=CameraLocationList, topic="calibration", qos_profile=10)
        self.marker_publisher = self.create_publisher(msg_type=MarkerArray, topic=('/test'), qos_profile=10)

        # create variables to store output and input for calibration
        self.output = dict()
        self.scale_data = dict()
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
                'scale': 1.0,
            }})
            self.scale_data.update({i: {
                'points': [],
                'T': [],
                'R': [],
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
                'guesses': [],
                'distance': -1,
            }})

        self.scale_data[0]['T'] = np.array([0.0, 0.0, 0.0])
        self.scale_data[0]['R'] = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        self.output[0]['scale'] = 1.000
        # self.scale_data[1]['T'] = np.array([0.0, 0.0, 0.0])
        # self.scale_data[1]['R'] = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        # self.scale_data[0]['T'] = np.array([0.0, 0.0, 0.0])
        # self.scale_data[0]['R'] = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        # self.output[1]['scale'] = 3.456
        # self.average_counter = 10
        
        # reset camera position
        # self.publish_calibration()

        # checks
        self.info_check = 0
        self.date_check = 0

        self.key = 0
        self.scale_calibration = 0
        th.Thread(target=self.key_capture, args=(), name='key_capture_thread', daemon=True).start()

        # main loop
        self.loop = self.create_timer(0.1, self.loop_callback, callback_group=loop_group)

    def key_capture(self):
        input()
        self.key += 1

    def loop_callback(self):
        if self.key == 1:
            if self.scale_calibration == 0:
                self.scale_calibration = 1
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
            if len(self.input[cam]['buffer']) != 1 and self.scale_calibration != 1:
                print("Hold the Calibration-Stick in front of all Cameras")
                return
            if len(self.input[cam]['buffer']) < 1 and self.scale_calibration == 1:
                print("Hold the Calibration-Wand in front of two Cameras")
                return
        
        # add the object to the calibration data
        for cam in self.input:
            # undistort Points
            input = self.input[cam]
            if self.scale_calibration == 0:
                distorted_point = (input['buffer'][0].x, input['buffer'][0].y)
                camera_matrix = input['camera_matrix']
                dist_matrix = input['dist_matrix']
                point = cv2.undistortPoints(distorted_point, cameraMatrix=camera_matrix, distCoeffs=dist_matrix, P=None)
                point = point.flatten()
                point = (point[0], point[1])
                input['objects'].append(point)
            else:
                input['objects'] = []
                for point in input['buffer']:
                    distorted_point = (point.x, point.y)
                    camera_matrix = input['camera_matrix']
                    dist_matrix = input['dist_matrix']
                    point = cv2.undistortPoints(distorted_point, cameraMatrix=camera_matrix, distCoeffs=dist_matrix, P=None)
                    point = point.flatten()
                    point = (point[0], point[1])
                    input['objects'].append(point)

        # check if there is enough data to start calibration 
        if self.date_check == 0:
            if self.scale_calibration == 0:
                for cam in self.input:
                    self.date_check = 1
                    if len(self.input[cam]['objects']) <= 7:
                        self.date_check = 0
                        print("not enough data to calibrate")
                        return

        # Calibrate scale
        if self.scale_calibration == 1:
            id = 0
            # check for cameras with Magic Wand in View
            ready_cams = []
            for cam_index, cam in enumerate(self.input):
                if len(self.input[cam]['objects']) == 5:
                    ready_cams.append(cam_index)
            if len(ready_cams) == 0:
                print("Hold the Calibration-Wand in front of two Cameras")
            # if enough data
            if 0 in ready_cams and len(ready_cams) >= 2:
                # get lines
                for index in ready_cams:
                    raw_points = np.array(self.input[index]['objects'])
                    start = self.scale_data[index]['T']
                    self.scale_data[index]['points'] = []
                    for i in range(len(raw_points)):
                        end = np.array([raw_points[i][0], raw_points[i][1], 1])
                        end = np.matmul(end, self.scale_data[index]['R'])
                        end = np.array([end[0] + start[0], end[1] + start[1], end[2] + start[2]]) 
                        self.scale_data[index]['points'].append((end[0], end[1], end[2], i))

                # calculate corners and center of Wand
                points = self.scale_data[0]['points']
                corners = []
                center = None
                for point in points:
                    if point[3] == max(points, key=lambda x: x[0])[3]:
                        corners.append(point)
                    elif point[3] == min(points, key=lambda x: x[0])[3]:
                        corners.append(point)
                    elif point[3] == max(points, key=lambda y: y[1])[3]:
                        corners.append(point)
                    elif point[3] == min(points, key=lambda y: y[1])[3]:
                        corners.append(point)
                    else:
                        center = point
                    
                # calculate distances between corners
                distances = []
                for corner in corners:
                    for corner2 in [probe for probe in corners if probe[3] != corner[3]]:
                        dis = self.distanceBetweenPoints(np.array(corner), np.array(corner2))
                        distances.append(dis)
                if len(distances) <= 6:
                    return
                for i in range(4):
                    distances.remove(max(distances))
                score = 0
                for dis in distances:
                    percent = distances[0]/dis
                    score += percent
                score /= len(distances)
                score *= 100
                print("Score: " + str(score))
                # proceed only, if wand is parallel enough
                if score <= 99.8 or score >= 100.2:
                    return
                # calculate distance from center point
                dis = sum(distances) / len(distances)
                scale = 1.55 / dis
                print("scale calibration data gathered, calculating scale...")
                if center != None:
                    center = np.array([center[0], center[1], center[2]]) * scale
                else:
                    return
                # calculate necesarry changes to scale for the next camera to match this distance
                # get line that goes through center line of cam0
                data = self.scale_data[ready_cams[1]]
                start = data['T']
                mini = -1
                line = [np.array(start), np.array([0,0,0])]
                for end in data['points']:
                    _, _, dis = self.closestDistanceBetweenLines(np.array([0.,0.,0.]), np.array(center), np.array(start), np.array([end[0], end[1], end[2]]))
                    if mini == -1 or dis < mini:
                        mini = dis
                        line[1] = np.array([end[0], end[1], end[2]])
                scale = 1
                while (1):
                    a, _, _ = self.closestDistanceBetweenLines(np.array([0.,0.,0.]), np.array(center), line[0] * scale, line[1] * scale)
                    prev_dis = self.distanceBetweenPoints(a, center)
                    scale += 0.0004
                    a, _, _ = self.closestDistanceBetweenLines(np.array([0.,0.,0.]), np.array(center), line[0] * scale, line[1] * scale)
                    dis = self.distanceBetweenPoints(a, center)
                    print(dis)
                    if dis > prev_dis:
                        scale -= 0.0008
                    if dis < 0.001:
                        self.output[ready_cams[1]]['scale'] = scale
                        self.publish_calibration()
                        self.scale_calibration = 2
                        print(scale)
                        print("done")
                        break
            return

        if self.scale_calibration == 2:
            markerarray = MarkerArray()
            id = 0
            # get real point
            real_point = None
            for index in self.output:
                out = self.output[index]
                if out['scale'] == 1.0:
                    continue
                start0 = np.array([0,0,0])
                end0 = self.input[0]['objects'][0]
                end0 = (end0[0], end0[1], 1)

                scale = self.output[index]['scale']
                start1 = np.array(self.scale_data[index]['T'])
                end1 = self.input[index]['objects'][0]            # get lines
                end1 = (end1[0], end1[1], 1)
                end1 = np.matmul(end1, self.scale_data[index]['R'])
                end1 = np.array([end1[0] + start1[0], end1[1] + start1[1], end1[2] + start1[2]]) * scale
                start1 = start1 * scale
                real_point, _, _ = self.closestDistanceBetweenLines(start0, end0, start1, end1)

            for index in self.output:
                out = self.output[index]
                if out['scale'] != 1.0 or index == 0: 
                    continue
                raw_points = np.array(self.input[index]['objects'])
                # start = self.scale_data[index]['T']
                start = np.array([self.output[index]['x'], self.output[index]['y'], self.output[index]['z']])
                self.scale_data[index]['points'] = []
                end = np.array([raw_points[0][0], raw_points[0][1], 1])
                end = np.matmul(end, self.scale_data[index]['R'])
                end = np.array([end[0] + start[0], end[1] + start[1], end[2] + start[2]]) 
                marker = mrk.create_line(start, end, "test", id, 'world', self.get_clock().now().to_msg(), (255, 255, 0, 0), lifetime=(1, 50000000))
                id += 1
                markerarray.markers.append(marker)
                scale = 1
                while (1):
                    start0 = np.array([0,0,0])
                    end0 = np.array(real_point)
                    start1 = np.array(start)
                    end1 = np.array(end)
                    a, _, _ = self.closestDistanceBetweenLines(start0, end0, start1, end1)
                    prev_dis = self.distanceBetweenPoints(np.array(a), np.array(real_point))
                    scale += 0.0004
                    a, _, _ = self.closestDistanceBetweenLines(np.array([0.,0.,0.]), real_point, start * scale, end * scale)
                    dis = self.distanceBetweenPoints(np.array(a), np.array(real_point))
                    print(dis)
                    if dis > prev_dis:
                        scale -= 0.0009
                    if dis < 0.001:
                        self.output[index]['scale'] = scale
                        self.publish_calibration()
                        print("done")
                        break

            self.marker_publisher.publish(markerarray)
            self.destroy_node()
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
                    threshold = 0.003,
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
            # r = Rotation.from_matrix(R)
            # angles = r.as_euler("xyz", degrees=False)

            # calculate score v2
            input = self.input[index]

            T = np.array([t[0] * -1, t[1] * -1, t[2] * -1])
            input['guesses'].append((T, R))

            best_guess = (T, R)
            self.scale_data[index]['T'] = T
            self.scale_data[index]['R'] = R
            previous_distance = -1
            for guess in input['guesses']:
                start0 = np.array([0,0,0])
                start1 = guess[0]
                distances = []
                for i in range(len(cam1_points)):
                    end0 = np.array([cam0_points[i][0], cam0_points[i][1], 1])
                    end1 = np.array([cam1_points[i][0], cam1_points[i][1], 1])
                    end1 = np.matmul(end1, guess[1])
                    end1 = (guess[0][0] + end1[0], guess[0][1] + end1[1], guess[0][2] + end1[2])
                    _, _, dis = self.closestDistanceBetweenLines(start0,end0,start1,end1)
                    distances.append(dis)
                average_dis = sum(distances) / len(distances)
                # print(average_dis)
                if previous_distance == -1:
                    previous_distance = average_dis
                    best_guess = guess
                else:
                    if average_dis < previous_distance:
                        previous_distance = average_dis
                        best_guess = guess

                self.output[index]['x'] =  best_guess[0][0]
                self.output[index]['y'] =  best_guess[0][1]
                self.output[index]['z'] =  best_guess[0][2]
                r = Rotation.from_matrix(best_guess[1])
                angles = r.as_euler("xyz", degrees=False)
                self.output[index]['ax'] = angles[0] * -1
                self.output[index]['ay'] = angles[1] * -1
                self.output[index]['az'] = angles[2] * -1

                self.scale_data[index]['T'] = best_guess[0]
                self.scale_data[index]['R'] = best_guess[1]
            
            # for index in self.output:
            #     print(index)
            #     print(self.scale_data[index])
            
            # publish calibration data for live preview
            self.publish_calibration()
            # print(self.output[index])


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
            location.scale = self.output[i]['scale']
            msg.locations.append(location)
        self.publisher.publish(msg)
    
    def write_config(self):
        for i in self.output:
            print(i)
            print(self.output[i])
            print(self.scale_data[i])
        # config = {}
        # for i in range(self.device_count):
        #     config.update({str(i): self.output[i]})
        # file = json.dumps(config)
        # name = input("Config File Name: ")
        # with open(("/home/ALEX/anytrack/config/positions/" + name + ".json"), "w") as outfile:
        #     outfile.write(file)
        # print("Calibration done!")

    def distanceBetweenPoints(self, a, b):
        dif = a - b
        return m.sqrt(m.pow(dif[0], 2) + m.pow(dif[1], 2) + m.pow(dif[2], 2))

    def closestDistanceBetweenLines(self, a0,a1,b0,b1):
        # Calculate denomitator
        A = a1 - a0
        B = b1 - b0
        magA = np.linalg.norm(A)
        magB = np.linalg.norm(B)
        
        _A = A / magA
        _B = B / magB
        
        cross = np.cross(_A, _B);
        denom = np.linalg.norm(cross)**2
        
        # If lines are parallel (denom=0) test if lines overlap.
        # If they don't overlap then there is a closest point solution.
        # If they do overlap, there are infinite closest positions, but there is a closest distance
        if not denom:
            d0 = np.dot(_A,(b0-a0))
            
            return None,None,np.linalg.norm(((d0*_A)+a0)-b0)
            
        # Lines criss-cross: Calculate the projected closest points
        t = (b0 - a0);
        detA = np.linalg.det([t, _B, cross])
        detB = np.linalg.det([t, _A, cross])

        t0 = detA/denom;
        t1 = detB/denom;

        pA = a0 + (_A * t0) # Projected closest point on segment A
        pB = b0 + (_B * t1) # Projected closest point on segment B

        return np.array(pA),np.array(pB),np.linalg.norm(pA-pB)

def main(args=None):
    rclpy.init(args=args)
    node = calibration()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
