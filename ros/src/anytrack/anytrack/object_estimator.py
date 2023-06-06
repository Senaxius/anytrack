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
    # def update_object(self, object):
    #     self.object = 
    
class object:
    def __init__(self, count, id):
        self.id = id
        self.filter = 0.3
        self.points = []
        self.lines = []
        self.vecs = []
        for i in range(count):
            # self.lines.append(None)
            self.vecs.append((np.array([0,0,0]) , np.array([0,0,0])))
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
        loop2_grp = MutuallyExclusiveCallbackGroup()

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
        self.publisher = self.create_publisher(msg_type=MarkerArray, topic=('/anytrack_objects'), qos_profile=10)
        
        # # # main loop
        self.guess = np.array([0., 0., 0.])
        self.step = 0.02
        self.filter = 0.3
        self.colors = [
                (255, 255, 0, 255),
                (255, 0, 0, 255),
                (255, 0, 255, 0),
                (255, 25, 160, 13),
                (255, 25, 160, 13),
                (255, 25, 160, 13),
                (255, 25, 160, 13),
                (255, 25, 160, 13),
                ]
        self.objects = []
        self.lines = []

        self.loop_time = 0.03
        # self.loop = self.create_timer(self.loop_time, self.closest_distance_single, callback_group=loop_grp)
        # self.loop = self.create_timer(self.loop_time, self.closest_distance_multi, callback_group=loop_grp)
        self.loop = self.create_timer(self.loop_time, self.closest_distance_multi_v2, callback_group=loop_grp)

    def closest_distance_multi_v2(self): # with closestDistanceBetweenLines for multiple points
        buffer = self.output

        ### find new lines
        line_buffer = []
        for cam_index, cam in enumerate(buffer):
            for line_index, line in enumerate(cam):
                found = 0
                for existing_line in self.lines:
                    if existing_line.line_id == line_index and existing_line.cam_id == cam_index:
                        existing_line.line = line
                        line_buffer.append(existing_line)
                        found = 1
                        break
                if found == 0:
                    # print("found new line with cam_index: " + str(cam_index) + " and line_index: " + str(line_index))
                    new_line = vec(line, cam_index, line_index)
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
                pA, pB, dis = self.closestDistanceBetweenLines(a0,a1,b0,b1)
                mid = pA + (0.5 * (pB - pA))
                line.distances.append((line_2.cam_id, line_2.line_id, dis))


        ### add line to object, or create new one
        for line_index, line in enumerate([probe for probe in self.lines if probe.object_id == None]):
            found = 0
            print("wtf")
            # check if line can be appended to known objects
            # print(line)
            for ob_index, ob in enumerate(self.objects):
                for line_2 in ob.lines:
                    dis = [probe for probe in line.distances if probe[0] == line_2.cam_id and probe[1] == line_2.line_id]
                    print("line_index: " + str(line_index) + " ob_index: " + str(ob_index) + " dis: " + str(dis))
                    found = 1
                    # if len(dis) != 1:
                    #     print("WTF")
                    #     break
                    # print(dis[0][2])
                    # if len(dis) != 1:
                    #     print("WTF")
                    # dis = dis[0][2]
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

        ### remove objects, where only 1 or less lines are left
        for ob_index, ob in enumerate(self.objects):
            num_lines = len(ob.lines)
            for line in ob.lines:
                line = [probe for probe in self.lines if probe.line_id == line.line_id and probe.cam_id == line.cam_id]
                if len(line) == 0:
                    num_lines -= 1
            if num_lines <= 1:
                self.objects.pop(ob_index)

        # print(len(self.objects))
        # for i in self.objects:
        #     print(len(i.lines))





    def closest_distance_multi(self): # with closestDistanceBetweenLines for multiple points
        start_time = time.time()
        id = 0
        markerarray = MarkerArray()

        # move lines into buffer
        buffer = self.output

        # update known objects
        for i, ob in enumerate(self.objects):
            ob.points = []
            for index, line_number in enumerate(ob.lines):
                if line_number == None:
                    continue
                line = np.array([i for i in buffer[index] if i[2] == line_number], dtype=object)
                if len(line) == 0:
                    continue
                a0 = np.array(line[0][0])
                a1 = np.array(line[0][1])
                for index2, line_number2 in enumerate(ob.lines):
                    if index == index2:
                        continue
                    line2 = np.array([i for i in buffer[index2] if i[2] == line_number2], dtype=object)
                    if len(line2) == 0:
                        # print("line gone :(")
                        continue
                    b0 = np.array(line2[0][0])
                    b1 = np.array(line2[0][1])
                    pA, pB, dis = self.closestDistanceBetweenLines(a0,a1,b0,b1)
                    mid = pA + (0.5 * (pB - pA))
                    ob.add_point(mid)
                    ob.vecs[index] = (a0, a1)
                    ob.vecs[index2] = (b0, b1)
                    # marker = mrk.create_point(mid, 'debug', id, 'world', self.get_clock().now().to_msg(), self.colors[i], lifetime=(1, 30000000))
                    # id += 1
                    # markerarray.markers.append(marker)

            for index, line in enumerate(ob.lines):
                if line != None:
                    # update shit
                    buffer[index] = [i for i in buffer[index] if i[2] != line]


        # self.objects = []


        # check for new objects
        objects = []
        for index, cam in enumerate(buffer):
            if cam != []:
                for point in cam:
                    for index2, cam2 in enumerate(buffer):
                        if index2 != index and cam2 != []:
                            for point2 in cam2:
                                a0 = np.array(point[0])
                                a1 = np.array(point[1])
                                b0 = np.array(point2[0])
                                b1 = np.array(point2[1])
                                pA, pB, dis = self.closestDistanceBetweenLines(a0,a1,b0,b1)
                                mid = pA + (0.5 * (pB - pA))

                                if dis <= 0.08:
                                    if objects == []:
                                        temp = object(count=self.device_count)
                                        print("found new object")
                                        temp.add_point(mid)
                                        temp.vecs[index] = (a0, a1)
                                        temp.vecs[index2] = (b0, b1)
                                        temp.lines[index] = point[2]
                                        temp.lines[index2] = point2[2]
                                        objects.append(temp)
                                    else:
                                        found = 0
                                        for ob in objects:
                                            if self.distanceBetweenPoints(ob.average, mid) <= 0.1:
                                                ob.add_point(mid)
                                                ob.vecs[index] = (a0, a1)
                                                ob.vecs[index2] = (b0, b1)
                                                ob.lines[index] = point[2]
                                                ob.lines[index2] = point2[2]
                                                found = 1
                                                break
                                        if found == 0:
                                            temp = object(count=self.device_count)
                                            print("found new object")
                                            temp.add_point(mid)
                                            temp.vecs[index] = (a0, a1)
                                            temp.vecs[index2] = (b0, b1)
                                            temp.lines[index] = point[2]
                                            temp.lines[index2] = point2[2]
                                            objects.append(temp)
        number = 0
        for i in buffer:
            for a in i:
                number += 1
        number = int(round(number / int(self.device_count), 0))
        objects.sort(key=lambda key: len(key.points), reverse=True)
        for index in range(number):
            if len(objects) >= number:
                ob = objects[index]
                # print("found new object!")
                ob.guess = ob.average
                self.objects.append(ob)

        # print the points
        for index, ob in enumerate(self.objects):
            marker = mrk.create_point(ob.guess, 'debug', id, 'world', self.get_clock().now().to_msg(), self.colors[index], lifetime=(1, 30000000))
            id += 1
            markerarray.markers.append(marker)
            # for vec in ob.vecs:
            #     marker = mrk.create_line(vec[0], vec[0] + ((vec[1] - vec[0]) * 10), 'debug', id, 'world', self.get_clock().now().to_msg(), self.colors[index], lifetime=(1, 30000000))
            #     id += 1
            #     markerarray.markers.append(marker)
        self.publisher.publish(markerarray)

        speed = (self.loop_time - (time.time() - start_time))
        # print(speed)

    def closest_distance_single(self): # with closestDistanceBetweenLines for one point
        id = 0
        markerarray = MarkerArray()

        self.guesses = []
        self.distances = []

        for index, cam in enumerate(self.output):
            if cam != []:
                for index2, cam2 in enumerate(self.output):
                    if index2 != index:
                        if cam2 != []:
                            # print(cam2[0][0])
                            a0 = np.array(cam[0][0])
                            a1 = np.array(cam[0][1])
                            b0 = np.array(cam2[0][0])
                            b1 = np.array(cam2[0][1])
                            pA, pB, dis = self.closestDistanceBetweenLines(a0,a1,b0,b1)
                            mid = pA + (0.5 * (pB - pA))
                            self.distances.append(dis)
                            self.guesses.append(mid)

        if len(self.guesses) != 0:
            x, y, z = [], [], []
            for point in self.guesses:
                x.append(point[0])
                y.append(point[1])
                z.append(point[2])
            average = np.array([sum(x) / len(x), sum(y) / len(y), sum(z) / len(z)])

            self.guess = (1-self.filter) * self.guess + self.filter * average 

            marker = mrk.create_point(self.guess, 'closest_distance_single', 0, 'world', self.get_clock().now().to_msg(), color=(255, 3, 212, 11), lifetime=(1, 50000000))
            markerarray.markers.append(marker)

            self.publisher.publish(markerarray)

            # calculate quality 
            quality = sum(self.distances) / len(self.distances)
            # TODO: publish this in some sort of message for calibration feedback
            # TODO: design camera specific quality feedback

    def gradient_descent_v1(self): #  with guassien descent
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
                # temp_point[i+1] += scale

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

    def guassian_descent_v2(self): # shit idk what this is^^
        start_time = time.time()

        id = 0
        markerarray = MarkerArray()

        while (1):
            distance = self.calulate_average_distance(self.guess)
            # self.step = distance / 10
            move_vec = np.array([0., 0., 0.])

            for i in range(3):
                temp_point = self.guess.copy()
                temp_point[i] += self.step
                probe_distance = self.calulate_average_distance(temp_point)
                change = distance - probe_distance
                if change >= 0:
                    move_vec[i] = (distance - probe_distance) 
            for i in range(3):
                temp_point = self.guess.copy()
                temp_point[i] -= self.step
                probe_distance = self.calulate_average_distance(temp_point)
                change = distance - probe_distance
                if change >= 0:
                    move_vec[i] = -(distance - probe_distance) 

            # improvement = self.calulate_average_distance(self.guess + move_vec) * 1
            # improvement = 1
            # print(improvement)

            # marker = mrk.create_line(self.guess, (self.guess + move_vec), 'isect', id, 'world', self.get_clock().now().to_msg())
            self.guess = self.guess + move_vec

            # marker = mrk.create_line(self.guess, move_vec * 10, 'isect', id, 'world', self.get_clock().now().to_msg())

            speed = (self.loop_time - (time.time() - start_time))
            if speed <= 0.1:
                break

        marker = mrk.create_point(self.guess, 'isect', id, 'world', self.get_clock().now().to_msg())
        markerarray.markers.append(marker)
        self.publisher.publish(markerarray)


            # move_vec[i] = (distance - probe_distance) 

        # neuer Schätzwert wird abgespeicher
        # self.guess = np.array(vec.add_v3v3(self.guess, move_vec))

        # marker = mrk.create_line((0,0,0), move_vec * 100, 'isect', id, 'world', self.get_clock().now().to_msg())
        # self.publisher.publish(markerarray)

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

        self.output[index] = buffer

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
            # return (sum(distances) / len(distances))
            return sum(distances)
        else:
            return 0

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

    def distanceBetweenPoints(self, p0, p1):
        return m.sqrt(m.pow(p0[0] - p1[0], 2) + m.pow(p0[1] - p1[1], 2) + m.pow(p0[2] - p1[2], 2))



def main(args=None):
    rclpy.init(args=args)
    node = object_estimator()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

