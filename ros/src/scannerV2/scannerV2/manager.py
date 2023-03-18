import rclpy
from rclpy.node import Node
import time
import os
from launch import LaunchDescription, LaunchService
from launch_ros.actions import Node as Action

class manager(Node): 
    def __init__(self):
        super().__init__("manager") 
        self.get_logger().info("Starting manager...")

        self.get_logger().info("Searching for devices...")
        devices = self.search_devices()

        if not devices:
            self.get_logger().warning("No cameras were detected!")
            exit()
        self.get_logger().info("Found Number of Devices: " + str(len(devices)))

        ls = LaunchService()
        ls.include_launch_description(self.generate_launch_description(devices))
        ls.run()

    def search_devices(self):
        buffer = []
        stream = os.popen('ls /dev/ | grep video')
        output = stream.read()
        if (output == ''):
            self.devices = []
            return
        output = output.strip()
        output = output.replace("video", '')
        output = output.replace("\n", ',')

        untested_devices = output.split(',')

        for index in untested_devices:
            command = "v4l2-ctl -d /dev/video" + index + " -D | grep 'Video Pixel Formatter'"
            stream = os.popen(command)
            output = stream.read()
            if (output != ''):
                buffer.append(int(index))
        
        return buffer

    def generate_launch_description(self, devices):
        ld = LaunchDescription()

        count = 0
        length = len(devices)

        width = 1280
        height = 720

        for cam in devices:
            device = cam
            index = count
            count += 1

            camX_tracker2D = Action(
                package="scannerV2",
                executable="tracker2D",
                name=('tracker2D'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"device": device},
                    {"track": 1},
                    {"visualize": 1},
                    {"limit": 35},
                    {"debug": 0},
                    {"framerate": 60},
                    {"width": width},
                    {"height": height},
                ]
            )
            camX_camera_info = Action(
                package="scannerV2",
                executable="camera_info",
                name=('camera_info'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"device": device}
                ]
            )
            camX_vector= Action(
                package="scannerV2",
                executable="camera_vector",
                name=('vector'),
                namespace= ('cam' + str(index)),
                parameters=[
                    {"index": index},
                    {"device": device},
                    {"multiplier": 2},
                    {"width": width},
                    {"height": height},
                ]
            )

            ld.add_action(camX_tracker2D)
            ld.add_action(camX_camera_info)
            ld.add_action(camX_vector)

        position_manager = Action(
            package="scannerV2",
            executable="position_manager",
            name=('position_manager'),
            parameters=[
                {"device_count": length},
                {"config_path": '/home/ALEX/3dev/config/camera_positions.json'}
            ]
        )
        ld.add_action(position_manager)
        return ld

def main(args=None):
    rclpy.init(args=args)
    node = manager()
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()