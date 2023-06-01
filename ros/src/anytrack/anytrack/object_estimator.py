import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
import time 
import sys

from interfaces.msg import Tracks
from sensor_msgs.msg import CameraInfo
from tf2_msgs.msg import TFMessage

from visualization_msgs.msg import MarkerArray

sys.path.append('/home/ALEX/anytrack/python/lib')
import vector as vec
import marker as mrk

class object_estimator(Node): 
    def __init__(self):
        super().__init__("object_estimator") 
        
        # declare Parameters
        self.declare_parameter("device_count", 0)

        # import parameters
        self.device_count = self.get_parameter("device_count").value 
        # debug only
        # self.device_count = 2

        if self.device_count == 0:
            self.get_logger().error("Number of devices wasn't specified!")
            exit()

        self.get_logger().info("Starting object_estimator...")

        tf_grp = MutuallyExclusiveCallbackGroup()
        tracks_grp = ReentrantCallbackGroup()
        info_grp = ReentrantCallbackGroup()
        loop_grp = MutuallyExclusiveCallbackGroup()

        # tracks_group = ReentrantCallbackGroup()
        # info_group = ReentrantCallbackGroup()

        # create object_estimator publisher
        # self.publisher = self.create_publisher(msg_type=CameraLocations, topic="object_estimator", qos_profile=10)

        # create variables to store output and input for object_estimator
        self.input = dict()
        self.output = []

        # create subscribers
        # self.tf_sub = self.create_subscription(msg_type=TransformStamped, topic=('/tf'), callback=self.tf_callback, qos_profile=10, callback_group=tf_grp)
        for i in range(self.device_count):
            self.create_subscription(msg_type=Tracks, topic=('/cam' + str(i) + '/tracks'), callback=self.create_tracks_callback(i), qos_profile=10, callback_group=tracks_grp)
            self.create_subscription(msg_type=CameraInfo, topic=('/cam' + str(i) + '/camera_info'), callback=self.create_info_callback(i), qos_profile=10, callback_group=info_grp)
            self.input.update({i: {
                'camera_matrix': [],
                'dist_matrix': [],
                'start': (),
                'R': [],
                'tf': dict(),
            }})
            self.output.append([])
        
        self.tf_sub = self.create_subscription(msg_type=TFMessage, topic=('/tf'), callback=self.tf_callback, qos_profile=10, callback_group=tf_grp)
        self.publisher = self.create_publisher(msg_type=MarkerArray, topic=('test'), qos_profile=10)
        
        # # # main loop
        self.guess = np.array([0., 0., 0.])
        self.loop_time = 0.03
        # self.loop_time = 0.10
        self.loop = self.create_timer(self.loop_time, self.loop_callback, callback_group=loop_grp)

    def loop_callback(self):
        start_time = time.time()

        id = 0
        markerarray = MarkerArray()
        # average_distance = 0
        # print(self.output)

        while (1):
            # Berechnung des durch. Abstands des ersten Schätzpunktes
            distance = self.calulate_average_distance(self.guess)

            # Skalierung der Schrittgröße
            scale = distance * 0.5

            # Idealer Richtungsvektor, um Abstand zu Geraden zu minimieren wird initialisiert
            move_vec = np.array([0., 0., 0.])
            
            # Punkt wird in alle 3 Richtungen verschoben
            for i in range(3):
                # temporärere Punkt wird erstellt
                temp_point = self.guess.copy()

                # verschieben des temporärere Punkt in eine Richtung verschoben um die Schrittgröße 
                temp_point[i] += scale 
                temp_point[i+1] += scale

                # Abstandswerte des neuen Punktes werden errechnet
                probe_distance = self.calulate_average_distance(temp_point)

                # Wenn die Änderung den Abstand verbessert, wird die Schätzung in diese Richtung verschoben
                # Wenn die Änderung den Abstand verschlechter, wird die Schätzung in andere Richtung verschoben
                # Je größer die Verbesserung, desto größer die Verschiebung
                move_vec[i] = (distance - probe_distance) 

            # neuer Schätzwert wird abgespeicher
            self.guess = np.array(vec.add_v3v3(self.guess, move_vec))

            marker = mrk.create_point(self.guess, 'isect', id, 'world', self.get_clock().now().to_msg())
            markerarray.markers.append(marker)
            id += 1
            # stop loop if running too long
            speed = (self.loop_time - (time.time() - start_time))
            if speed <= 0.1:
                break

        # print(scale)
        # marker = mrk.create_point(self.guess, 'isect', 100, 'world', self.get_clock().now().to_msg())
        self.publisher.publish(markerarray)

        # speed = (self.loop_time - (time.time() - start_time))
        # print(str(speed))
        # marker = mrk.create_point(self.guess, 'isect', 100, 'world', self.get_clock().now().to_msg())
        # markerarray.markers.append(marker)
        # marker = mrk.create_line(self.guess, isect_point, 'isect', id, 'world', self.get_clock().now().to_msg())
        # markerarray.markers.append(marker)
        # id += 1

    def create_tracks_callback(self, index):
        return lambda msg:self.tracks_callback(msg, index)
    def create_info_callback(self, index):
        return lambda msg:self.info_callback(msg, index)
    
    def tracks_callback(self, msg, index):
        input = self.input[index]
        if len(input['camera_matrix']) == 0:
            return
        if len(input['tf']) == 0:
            return

        self.output[index] = []
        # markerarray = MarkerArray()
        start = input['start']
        for object in msg.tracks:
            x = object.x
            y = object.y
            point = cv2.undistortPoints((x, y), cameraMatrix=input['camera_matrix'], distCoeffs=input['dist_matrix'], P=None).flatten()
            point = (point[0], point[1], 1)
            point = np.matmul(point, np.linalg.inv(input['R']))
            end = (point[0] + start[0], point[1] + start[1], point[2] + start[2])
            self.output[index].append((start, end))

        # visualization
            # marker = self.create_marker(start, end)
            # markerarray.markers.append(marker)
        # self.publisher.publish(markerarray)
    
    def info_callback(self, msg, index):
        k = msg.k
        d = msg.d
        self.input[index]['camera_matrix'] = np.matrix([[k[0], k[1], k[2]], [k[3], k[4], k[5]], [k[6], k[7], k[8]]])
        self.input[index]['dist_matrix'] = np.array([d[0], d[1], d[2], d[3], d[4]])

    def tf_callback(self, msg):
        t = msg.transforms[0]
        id = int(''.join(filter(str.isdigit, t.child_frame_id)))
        t = msg.transforms[0].transform
        self.input[id]['tf'].update({
            'x': t.translation.x,
            'y': t.translation.y,
            'z': t.translation.z,
            'ax': t.rotation.x,
            'ay': t.rotation.y,
            'az': t.rotation.z,
            'aw': t.rotation.w,
        })
        self.input[id]['start'] = (t.translation.x, t.translation.y, t.translation.z)
        self.input[id]['R'] = R.from_quat([t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w]).as_matrix()

    def calulate_average_distance(self, point):
        distances = []
        for cam in self.output:
            for line in cam:
                normal_vec = vec.sub_v3v3(line[0], line[1])
                isect_point = vec.isect_line_plane_v3(line[0], line[1], self.guess, normal_vec)
                distances.append(vec.len_between_points_v3(point, isect_point))
        # calculate average distance
        if distances != []:
            return (sum(distances) / len(distances))
        else:
            return 0


def main(args=None):
    rclpy.init(args=args)
    node = object_estimator()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

