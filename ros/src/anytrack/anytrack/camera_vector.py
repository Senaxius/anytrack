import rclpy
from rclpy.node import Node

from scanner_interfaces.msg import Tracks
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point
from sensor_msgs.msg import CameraInfo

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup,MutuallyExclusiveCallbackGroup

class camera_vector(Node):  
    def __init__(self):
        super().__init__("camera_vector")  

        # declare Parameters
        self.declare_parameter("index", -1)
        self.declare_parameter("device", -1)
        self.declare_parameter("multiplier", -1)
        self.declare_parameter("width", -1)
        self.declare_parameter("height", -1)

        # import parameters
        self.index = self.get_parameter("index").value
        self.device = self.get_parameter("device").value
        self.multiplier = self.get_parameter("multiplier").value
        self.width = self.get_parameter("width").value
        self.height = self.get_parameter("height").value

        # debug only
        # self.index = 0
        # self.device = 0
        # self.multiplier = 2
        # self.width = 1280
        # self.height = 720

        # check if Parameters is set
        if (self.device == -1 or self.index == -1):
            self.get_logger().warning("no index was set")
            exit()
        
        # colors for visualisation
        color_1 = (237, 255, 0)
        color_2 = (0, 255, 255)
        color_3 = (255, 0, 255)
        color_4 = (0, 255, 0)
        self.colors = [color_1, color_2, color_3, color_4]

        # so only once receive info
        self.info_received = 0
        
        # create callback groups
        tracks_group = MutuallyExclusiveCallbackGroup()
        info_group = MutuallyExclusiveCallbackGroup()
        
        # create subscriber and publisher
        self.info_subscriber = self.create_subscription(msg_type=CameraInfo, topic=('/cam' + str(self.index) + '/camera_info'), callback=self.info_callback, qos_profile=10, callback_group=info_group)
        self.tracks_subscriber = self.create_subscription(msg_type=Tracks, topic=('/cam' + str(self.index) + '/tracks'), callback=self.tracks_callback, qos_profile=10, callback_group=tracks_group)
        self.publisher = self.create_publisher(msg_type=MarkerArray, topic="vector", qos_profile=10)

        self.get_logger().info("Starting camera vector with index " + str(self.index))

    def tracks_callback(self, msg):
        markerarray = MarkerArray()
        for object in msg.tracks:
            marker = self.create_marker(object.x, object.y, object.id)
            markerarray.markers.append(marker)
        self.publisher.publish(markerarray)

    def info_callback(self, msg):
        if self.info_received != 1:
            self.fx = (msg.p[0] * (self.width / msg.width))
            self.fy = (msg.p[5] * (self.height / msg.height))
            self.cx = (msg.p[2] * (self.width / msg.width))
            self.cy = (msg.p[6] * (self.height / msg.height))
            self.info_received = 1
    
    def create_marker(self, x, y, id):
        x = (float(x) - self.cx) / self.fx
        y = (float(y) - self.cy) / self.fy
        marker = Marker()
        marker.header.frame_id = ('cam' + str(self.index) + '_position')
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.id = id
        marker.ns = ('cam' + str(self.index) + '/markers')
        marker.action = marker.ADD
        marker.lifetime.sec = 1
        marker.lifetime.nanosec = 200000000
        
        marker.scale.x = 0.01
        marker.scale.y = 0.0
        marker.scale.z = 0.0

        marker.color.a = 1.0
        if id < 4:
            marker.color.r = float(self.colors[id][2])
            marker.color.g = float(self.colors[id][1])
            marker.color.b = float(self.colors[id][0])
        start = Point()
        start.x = 0.0
        start.y = 0.0
        start.z = 0.0
        end = Point()
        end.x = x    * self.multiplier
        end.y = y  * self.multiplier
        end.z = 1.0  * self.multiplier
        marker.points = [start, end]
        return marker

def main(args=None):
    rclpy.init(args=args)
    node = camera_vector() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()