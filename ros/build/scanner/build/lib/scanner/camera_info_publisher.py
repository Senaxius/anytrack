import rclpy
from rclpy.node import Node
import yaml

from sensor_msgs.msg import CameraInfo


def yaml_to_CameraInfo(yaml_fname):
    # Load data from file
    with open(yaml_fname, "r") as file_handle:
        calib_data = yaml.load(file_handle)
    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.width = calib_data["image_width"]
    camera_info_msg.height = calib_data["image_height"]
    camera_info_msg.K = calib_data["camera_matrix"]["data"]
    camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calib_data["rectification_matrix"]["data"]
    camera_info_msg.P = calib_data["projection_matrix"]["data"]
    camera_info_msg.distortion_model = calib_data["distortion_model"]
    return camera_info_msg


class camera_info_publisher(Node):
    def __init__(self):
        super().__init__("camera_info_publisher")  # MODIFY NAME

        self.get_logger().info("Initialize the camera_info_publisher...")
        self.publisher_ = self.create_publisher(
            msg_type=CameraInfo, topic="camera_info", qos_profile=10)
        self.get_logger().info("done!")

        self.get_logger().info("Reading yaml file and creating camera_info msg...")
        self.declare_parameter("file", "")
        if (self.get_parameter("file").get_parameter_value().string_value == ""):
            self.get_logger().warning("define a yaml file to use with '--ros-args -p file:=...")
            exit()
        else:
            filename = self.get_parameter(
                "file").get_parameter_value().string_value
            self.read_yaml(filename)
            self.convert_yaml_to_msg()
        self.get_logger().info("done!")

        self.get_logger().info("Publishing camera info on topic 'camera_info'")
        self.publisher_.publish(self.msg)
        self.get_logger().info("done!")

    def read_yaml(self, filename):
        with open(filename, "r") as file_handle:
            self.data = yaml.load(file_handle)

    def convert_yaml_to_msg(self):
        self.msg = CameraInfo()
        self.msg.width = 1920
        self.msg.height = 1080
        self.msg.distortion_model = "plumb_bob"
        self.msg.d = [0.131296, -0.316123, -0.001248, -0.005877, 0.000000]
        self.msg.k = [1530.73069,    0.,  940.42419,
                      0., 1528.93764,  546.71409,
                      0.,    0.,    1.]
        self.msg.p = [1532.60596,    0.,  926.34739,    0.,
                      0., 1553.67395,  545.35453,    0.,
                      0.,    0.,    1.,    0.]
        # self.msg.width = self.data["image_width"]
        # self.msg.height = self.data["image_height"]
        # self.msg.k = self.data["camera_matrix"]["data"]
        # self.msg.d = self.data["distortion_coefficients"]["data"]
        # self.msg.r = self.data["rectification_matrix"]["data"]
        # self.msg.p = self.data["projection_matrix"]["data"]
        # self.msg.distortion_model = self.data["distortion_model"]
        print(self.msg)


def main(args=None):
    rclpy.init(args=args)
    node = camera_info_publisher()  # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
    # # Get fname from command line (cmd line input required)
    # import argparse
    # arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument("filename", help="Path to yaml file containing " +\
    #                                          "camera calibration data")
    # args = arg_parser.parse_args()
    # filename = args.filename

    # # Parse yaml file
    # camera_info_msg = yaml_to_CameraInfo(filename)

    # # Initialize publisher node
    # rospy.init_node("camera_info_publisher", anonymous=True)
    # publisher = rospy.Publisher("camera_info", CameraInfo, queue_size=10)
    # rate = rospy.Rate(10)

    # # Run publisher
    # while not rospy.is_shutdown():
    #     publisher.publish
