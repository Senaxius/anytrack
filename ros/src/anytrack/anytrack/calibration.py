import rclpy
from rclpy.node import Node

import os
import time
import json
import math as m

from scanner_interfaces.msg import Tracks
from scanner_interfaces.msg import Object
from scanner_interfaces.msg import Location
from scanner_interfaces.msg import CameraLocations
from sensor_msgs.msg import CameraInfo

class calibration(Node):  
    def __init__(self):
        super().__init__("calibration")  

        self.width = 1280
        self.height = 720

        # TODO: add dynamic device detection
        self.devices = [0,1]

        print("Starting calibration...")

        self.publisher = self.create_publisher(msg_type=CameraLocations, topic="calibration", qos_profile=10)

        self.output = dict()
        self.input = dict()

        # create subscribers
        for i in range(len(self.devices)):
            self.create_subscription(msg_type=Tracks, topic=('/cam' + str(i) + '/tracks'), callback=self.create_tracks_callback(i), qos_profile=10)
            self.create_subscription(msg_type=CameraInfo, topic=('/cam' + str(i) + '/camera_info'), callback=self.create_info_callback(i), qos_profile=10)
            self.output.update({i: {
                'x': float(i*1.5),
                'y': 0.0,
                'z': 0.0,
                'ax': 0.0,
                'ay': 0.0,
                'az': 0.0,
            }})
            self.input.update({i: {
                'fx': 0.0,
                'fy': 0.0,
                'cx': 0.0,
                'cy': 0.0,
                'objects': [],
            }})
        
        # main loop
        self.loop = self.create_timer(0.1, self.loop_callback)

    def loop_callback(self):
        check = 0
        # check if input is good to calibrate
        # check = 0
        # for i in range(len(self.devices)):
        #     if len(self.input[i]['objects']) == 1:
        #         check += 1
        # if check == len(self.devices):
        #     vecs = dict()

        #     # create 3d vectors from camera matrix and tracking data
        #     for index in range(len(self.input)):
        #         cam = self.input[index]
        #         vecs.update({index: {
        #             'x': (float(cam['objects'][0].x) - cam['cx']) / cam['fx'],
        #             'y': (float(cam['objects'][0].y) - cam['cy']) / cam['fy'],
        #             'z': 1.0,
        #         }})
        #         vecs[index].update({'r': m.sqrt(pow(vecs[index]['x'], 2) + pow(vecs[index]['y'], 2) + 1)})
        #     print(vecs)
        # if len(self.input[0]['objects']) != 0:
        #     print(self.input[0]['objects'][0].x)
        # self.publish_calibration()
    
    def create_tracks_callback(self, index):
        return lambda msg:self.tracks_callback(msg, index)
    def create_info_callback(self, index):
        return lambda msg:self.info_callback(msg, index)
    
    def tracks_callback(self, msg, index):
        self.input[index]['objects'] = []
        for object in msg.tracks:
            self.input[index]['objects'].append(object)
    def info_callback(self, msg, index):
        self.input[index]['fx'] = (msg.p[0] * (self.width / msg.width))
        self.input[index]['fy'] = (msg.p[5] * (self.height / msg.height))
        self.input[index]['cx'] = (msg.p[2] * (self.width / msg.width))
        self.input[index]['cy'] = (msg.p[6] * (self.height / msg.height))
    
    def publish_calibration(self):
        msg = CameraLocations()
        for i in range(len(self.devices)):
            location = Location()
            location.id = i
            location.x = self.output[i]['x']
            location.y = self.output[i]['y']
            location.z = self.output[i]['z']
            location.ax = self.output[i]['ax']
            location.ay = self.output[i]['ay']
            location.az = self.output[i]['az']
            msg.locations.append(location)
        self.publisher.publish(msg)

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

def main(args=None):
    rclpy.init(args=args)
    node = calibration() 
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()