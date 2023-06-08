import enum
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

import cv2
import math as m
import numpy as np
from scipy.spatial.transform import Rotation as R
import time 
import sys
import copy

from interfaces.msg import Tracks
from sensor_msgs.msg import CameraInfo
from tf2_msgs.msg import TFMessage

from visualization_msgs.msg import MarkerArray

sys.path.append('/home/ALEX/anytrack/python/lib')
import vector as vec
import marker as mrk

class vec:
    def __init__(self, line, cam, id):
        self.cam_id = cam
        self.line_id = id
        self.line = line
        self.distances = []
        self.object_id = None
    def update_line(self, line):
        self.line = line 
    def add_distance(self, line):
        self.line = line 
    
class object:
    def __init__(self, count, id):
        self.id = id
        self.filter = 0.3
        self.points = []
        self.lines = []
        self.average = (0,0,0)
        self.guess = (0,0,0)
    def add_point(self, point):
        self.points.append(point)
        self.average=self.calculate_average()
        self.guess=self.run_filter()
    def add_line(self, line):
        self.lines.append(line)
    def calculate_average(self):
        return sum(self.points) / len(self.points)
    def run_filter(self):
        return ((1 - self.filter) * np.array(self.guess) + self.filter * np.array(self.average))

class object_estimator(Node): 
    def __init__(self):
        super().__init__("object_estimator") 
        # declare Parameters
        self.declare_parameter("device_count", 0)
        self.declare_parameter("debug", 0)
        # import parameters
        self.device_count = self.get_parameter("device_count").value 
        self.debug = self.get_parameter("debug").value 
        # debug only
        # self.device_count = 2
        self.debug = 1

        if self.device_count == 0:
            self.get_logger().error("Number of devices wasn't specified!")
            exit()

        self.get_logger().info("Starting object_estimator...")

        tf_grp = MutuallyExclusiveCallbackGroup()
        tracks_grp = ReentrantCallbackGroup()
        info_grp = ReentrantCallbackGroup()
        loop_grp = MutuallyExclusiveCallbackGroup()

        # create variables to store output and input for data gathering
        self.input = dict()
        self.output = []

        ### create subscribers for data_gathering
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
        self.publisher = self.create_publisher(msg_type=MarkerArray, topic=('/anytrack_objects'), qos_profile=10)

        # create variable to show when enough data was gathered
        self.ready = []
        for i in range(self.device_count):
            self.ready.append(0)
        
        self.colors = [
                (255, 55, 194, 251),
                (255, 50, 227, 120),
                (255, 186, 250, 67),
                (255, 255, 209, 56),
                (255, 255, 129, 56),
                ]
        self.objects = []
        self.lines = []

        ### main loop
        self.loop_time = 0.03
        self.loop = self.create_timer(self.loop_time, self.closest_distance_multi_v2, callback_group=loop_grp)


    def closest_distance_multi_v2(self): # with closestDistanceBetweenLines for multiple points
        id = 0
        markerarray = MarkerArray()
        # wait until enough data is gathered
        for i in self.ready:
            if i < 5:
                print("not enough data!")
                return
        buffer = self.output
        if self.debug == 1:
            # print("loop")
            print("")

        ### find new lines
        line_buffer = []
        for cam_index, cam in enumerate(buffer):
            for line_index, line in enumerate(cam):
                found = 0
                for existing_line in self.lines:
                    if existing_line.line_id == line[2] and existing_line.cam_id == cam_index:
                        existing_line.line = (line[0], line[1])
                        line_buffer.append(existing_line)
                        found = 1
                        break
                if found == 0:
                    if self.debug == 1:
                        print("Line (" + str(cam_index) + ", " + str(line[2]) + ") found")
                    new_line = vec((line[0], line[1]), cam_index, line[2])
                    line_buffer.append(new_line)
        self.lines = line_buffer

        ### calculate distances between every line
        for line_index, line in enumerate(self.lines):
            line.distances = []
            for line_index_2, line_2 in enumerate([probe for probe in self.lines if probe.cam_id != line.cam_id]):
                a0 = np.array(line.line[0])
                a1 = np.array(line.line[1])
                b0 = np.array(line_2.line[0])
                b1 = np.array(line_2.line[1])
                _, _, dis = self.closestDistanceBetweenLines(a0,a1,b0,b1)
                line.distances.append((line_2.cam_id, line_2.line_id, dis))

        ### update known objects
        length = len(self.objects)
        for i in range(len(self.objects)):
            move = length - len(self.objects)
            ob_index = i - move
            ob = self.objects[ob_index]
            # remove lines that disappeared
            length2 = len(ob.lines)
            for a in range(len(ob.lines)):
                move2 = length2 - len(ob.lines)
                line_index = a - move2
                line = ob.lines[line_index]
                test = [probe for probe in self.lines if probe.line_id == line.line_id and probe.cam_id == line.cam_id]
                if len(test) == 0:
                    if self.debug == 1:
                        print("Line (" + str(ob.id) + ", " + str(line.cam_id) + ", " + str(line.line_id) + ") removed (disappeared)")
                    ob.lines.pop(line_index)
            if len(ob.lines) <= 1:
                # ungroup leftover lines
                for line_index, line in enumerate(ob.lines):
                    line.object_id = None
                    if self.debug == 1:
                        print("Line (" + str(ob.id) + ", " + str(line.cam_id) + ", " + str(line.line_id) + ") ungrouped (Leftover)")
                # remove lost object
                if self.debug == 1:
                    print("Object (" + str(ob.id) + ") removed (disappeared)")
                self.objects.pop(ob_index)
                continue

            ### calculate points
            ob.points = []
            for line_index, line in enumerate(ob.lines):
                if line.object_id == None:
                    continue
                warnings = 0
                for line_index_2, line_2 in enumerate([probe for probe in ob.lines if probe.cam_id != line.cam_id]):
                    if line_2.object_id == None:
                        continue
                    a0 = np.array(line.line[0])
                    a1 = np.array(line.line[1])
                    b0 = np.array(line_2.line[0])
                    b1 = np.array(line_2.line[1])
                    pA, pB, dis = self.closestDistanceBetweenLines(a0,a1,b0,b1)
                    mid = pA + (0.5 * (pB - pA))
                    if dis > 0.1:
                        warnings += 1
                    else:
                        ob.add_point(mid)
                if warnings > 1:
                    line.object_id = None

            # ### remove Lines marked as faulty
            for a in range(len(ob.lines)):
                move2 = length2 - len(ob.lines)
                line_index = a - move2
                line = ob.lines[line_index]
                if line.object_id == None:
                    if self.debug == 1:
                        print("Line (" + str(ob.id) + ", " + str(line.cam_id) + ", " + str(line.line_id) + ") ungrouped (out of bound)")
                    ob.lines.pop(line_index)

        ### add line to object, or create new one
        for line_index, line in enumerate([probe for probe in self.lines if probe.object_id == None]):
            if self.debug == 1:
                print("Searching object for Line (" + str(line.cam_id) + ", " + str(line.line_id) + ")")
            found = 0
            # check if line can be appended to known objects
            min = [-1, -1]
            for ob_index, ob in enumerate(self.objects):
                if len(ob.lines) >= self.device_count:
                    continue
                # check if line with same cam_id is already present in object
                used = 0
                if len([probe for probe in ob.lines if probe.cam_id == line.cam_id]) > 0:
                    used = 1
                    continue
                distances = []
                for line_2 in ob.lines:
                    dis = [probe for probe in line.distances if probe[0] == line_2.cam_id and probe[1] == line_2.line_id]
                    if len(dis) == 0:
                        break
                    distances.append(dis[0][2])
                if len(distances) > 0:
                    average = sum(distances) / len(distances)
                    if self.debug == 1:
                        print("Average distance: " + str(average))
                    if average < min[1] or min[0] == -1:
                        # check if object already contains line from same camera
                        min = [ob_index, average]

            if min[1] < 0.50 and min[0] != -1:
                # ob.add_line(copy.deepcopy(line))
                ob = self.objects[min[0]]
                ob.add_line(line)
                line.object_id = ob.id
                found = 1
                if self.debug:
                    print("Added Line (" + str(line.cam_id) + ", " + str(line.line_id) + ") to Object " + str(ob.id))

            # if not, create new one
            if found == 0:
                id = 0
                for ob in self.objects:
                    if ob.id == id:
                        id += 1
                    else:
                        break
                new_object = object(self.device_count, id)
                line.object_id = id
                new_object.add_line(line)
                self.objects.append(new_object)
                if self.debug:
                    print("Created Object " + str(id) + " with Line (" + str(line.cam_id) + ", " + str(line.line_id) + ")")

        ### remove objects, where only 1 or less lines are left
        length = len(self.objects)
        for i in range(len(self.objects)):
            move = length - len(self.objects)
            ob_index = i - move
            ob = self.objects[ob_index]
            if len(ob.lines) <= 1:
                # ungroup leftover lines
                for line_index, line in enumerate(ob.lines):
                    line.object_id = None
                # remove lost object
                if self.debug:
                    print("Remove object " + str(ob.id) + " (too small)")
                self.objects.pop(ob_index)

        # publish lines
        # for line in self.lines:
        #     p0 = np.array(line.line[0])
        #     p1 = np.array(line.line[1])
        #     if line.object_id == None:
        #         marker = mrk.create_line(p0, p0 + ((p1 - p0) * 10), 'debug', id, 'world', self.get_clock().now().to_msg(), (255,255,255,255), lifetime=(0, 50000000))
        #     else:
        #         marker = mrk.create_line(p0, p0 + ((p1 - p0) * 10), 'debug', id, 'world', self.get_clock().now().to_msg(), self.colors[line.object_id], lifetime=(0, 50000000))
        #     id += 1
        #     markerarray.markers.append(marker)

        # publish points
        # for ob in self.objects:
        #     for point in ob.points:
        #         marker = mrk.create_point(point, 'anytrack', id, 'world', self.get_clock().now().to_msg(), self.colors[ob.id], lifetime=(0, 50000000))
        #         id += 1
        #         markerarray.markers.append(marker)
        # publish guess
        for ob in self.objects:
            marker = mrk.create_point(ob.guess, 'anytrack', id, 'world', self.get_clock().now().to_msg(), self.colors[ob.id], lifetime=(0, 50000000))
            id += 1
            markerarray.markers.append(marker)

        self.publisher.publish(markerarray)

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

        buffer = []
        # markerarray = MarkerArray()
        start = input['start']
        for object in msg.tracks:
            x = object.x
            y = object.y
            point = cv2.undistortPoints((x, y), cameraMatrix=input['camera_matrix'], distCoeffs=input['dist_matrix'], P=None).flatten()
            point = (point[0], point[1], 1)
            point = np.matmul(point, np.linalg.inv(input['R']))
            end = (point[0] + start[0], point[1] + start[1], point[2] + start[2])
            buffer.append((start, end, object.id))

        self.ready[index] += 1
        self.output[index] = buffer
    
    def info_callback(self, msg, index):
        self.ready[index] *= 5
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
    node = object_estimator()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

