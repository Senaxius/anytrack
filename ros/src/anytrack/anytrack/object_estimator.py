import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

# from scipy.spatial.transform import Rotation   
# import threading as th
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
import time 


from interfaces.msg import Tracks
from sensor_msgs.msg import CameraInfo
from tf2_msgs.msg import TFMessage

from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

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
        self.guess = (0, 0, 1)
        self.loop_time = 0.03
        self.loop = self.create_timer(self.loop_time, self.loop_callback, callback_group=loop_grp)

    def loop_callback(self):
        start_time = time.time()



        markerarray = MarkerArray()
        id = 0
        marker = self.create_point(self.guess, id)
        markerarray.markers.append(marker)
        self.publisher.publish(markerarray)

        

        speed = (self.loop_time - (time.time() - start_time))
        print(str(speed))

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


    def create_marker(self, start_p, end_p, id):
        marker = Marker()
        marker.header.frame_id = ('world')
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.id = id
        marker.ns = ('test')
        marker.action = marker.ADD
        marker.lifetime.sec = 1
        marker.lifetime.nanosec = 200000000
        
        marker.scale.x = 0.005
        marker.scale.y = 0.0
        marker.scale.z = 0.0

        marker.color.a = 0.3
        marker.color.r = 0.5
        marker.color.g = 0.3
        marker.color.b = 0.1
        start = Point()
        start.x = float(start_p[0])
        start.y = float(start_p[1])
        start.z = float(start_p[2])
        end = Point()
        end.x = float(end_p[0])  
        end.y = float(end_p[1])
        end.z = float(end_p[2])  
        marker.points = [start, end]
        return marker

    def create_point(self, point, id):
        marker = Marker()
        marker.header.frame_id = ('world')
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.id = id
        marker.ns = ('object_estimations')
        marker.action = marker.ADD
        marker.lifetime.sec = 1
        marker.lifetime.nanosec = 200000000
        marker.type = 2
        
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05

        marker.color.a = 1.0
        marker.color.r = float(30)
        marker.color.g = float(227)
        marker.color.b = float(105)
        pose = Point()
        pose.x = float(point[0])
        pose.y = float(point[1])
        pose.z = float(point[2])
        marker.pose.position = pose
        return marker
    # def quaternionMult(self, quaternionOne, quaternionTwo):
    #     w1, x1, y1, z1 = quaternionOne
    #     w2, x2, y2, z2 = quaternionTwo
    #     w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    #     x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    #     y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    #     z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    #     return w, x, y, z

    # def quaternionConjugate(self, quaternion):
    #     w, x, y, z = quaternion
    #     return (w, -x, -y, -z)

    # def quaternionvectorProduct(self, quaternion, vector):
    #     quaternion2 = (0.0,) + vector
    #     return self.quaternionMult(self.quaternionMult(quaternion, quaternion2), self.quaternionConjugate(quaternion))[1:]

def main(args=None):
    rclpy.init(args=args)
    node = object_estimator()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
