import rclpy
from rclpy.node import Node
import time
import os
from launch import LaunchDescription, LaunchService
from launch_ros.actions import Node as Action

class scan_manager(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("scanner") # MODIFY NAME

        self.get_logger().info("Starting scan_manager...")

        self.get_logger().info("Searching for devices...")
        devices = self.search_devices()

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

        position_manager = Action(
            package="scanner",
            executable="position_manager",
            parameters=[
                {"devices": [0, 1, 2]}
                # {"devices": [
                #     {'device': 0},
                #     {'name': 1},
                #     {'position': 4}
                # ]}
            ]
        )
        ld.add_action(position_manager)

        for cam in devices:
            camX_tracker = Action(
                package="scanner",
                executable="tracker",
                namespace= ('cam' + str(cam)),
                name=('tracker'),
                parameters=[
                    {"index": cam},
                    {"track": 0}
                ]
            )
            camX_camera_info = Action(
                package="scanner",
                executable="camera_info",
                namespace= ('cam' + str(cam)),
                name=('camera_info'),
                parameters=[
                    {"index": cam}
                ]
            )

            # ld.add_action(camX_tracker)
            # ld.add_action(camX_camera_info)
        return ld

def main(args=None):
    rclpy.init(args=args)
    node = scan_manager() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()