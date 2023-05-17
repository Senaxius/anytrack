#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import time
import math as m
import numpy as np

from visualization_msgs.msg import Marker 

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

def quaternion_from_euler(ai, aj, ak):
    # siehe Skizze:
    # aj = b
    # ak = a

    # ai = 0
    ai /= 2.0
    # ai = 0
    aj /= 2.0
    ak /= 2.0
    ci = m.cos(ai)
    # ci = 1
    si = m.sin(ai)
    # si = 0
    cj = m.cos(aj)
    sj = m.sin(aj)
    ck = m.cos(ak)
    sk = m.sin(ak)
    cc = ci*ck
    # cc = ck
    cs = ci*sk
    # cs = sk
    sc = si*ck
    # sc = 0
    ss = si*sk
    # ss = 0

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    # q[0] = -sj*sk
    # q[0] = -sin(b)*sin(a)
    q[1] = cj*ss + sj*cc
    # q[1] = sj*ck
    # q[1] = sin(b)*cos(a)
    q[2] = cj*cs - sj*sc
    # q[2] = cj*sk 
    # q[2] = cos(b)*sin(a) 
    q[3] = cj*cc + sj*ss
    # q[3] = cj*ck 
    # q[3] = cos(b)*cos(a) 

    return q

def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, m.cos(theta),-m.sin(theta)],
                   [ 0, m.sin(theta), m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta), -m.sin(theta), 0 ],
                   [ m.sin(theta), m.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

class test(Node): 
    def __init__(self):
        super().__init__("test") 

        # self.x, self.y, self.z, self.ax, self.ay, self.az = 0, 0, 0, 0 ,0 ,0
        # self.x = 0.0
        # self.ax = m.pi/2
        # self.ay = m.pi/4
        # self.az = 0

        self.position_broadcaster = TransformBroadcaster(self)

        # # test
        # ax = m.pi/2
        # ay = m.pi/4
        # az = 0

        # # R = Rx(ax) * Ry(ay) * Rz(az)
        # R = Ry(ay) 
        # vec1 = np.array([[0],[0.1],[0]])
        # vec2 = R * vec1

        # a = 45
        # a = a/180 * m.pi
        # # a = m.pi/2
        # print(a)
        # vec = np.array([[m.cos(a)],[0],[m.sin(a)]])

        p = np.array([[0.1],[0.0],[0.1]])
        # polar koordinaten 2d

        # r = m.sqrt(p[0]**2 + p[2]**2)
        # a = m.acos(p[0]/r)
        # print(r)
        # print(a)

        # am = 50
        # am = am/180 * m.pi
        # a += am
        # vec = np.array([[r * m.cos(a)],[0.1],[r * m.sin(a)]])
        # # vec[0] = r * m.cos(a)
        # # vec[2] = r * m.sin(a)
        # print(vec)

        # polar koordinaten 3d
        r = m.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
        o = m.acos(p[2]/r)
        l = m.atan2(p[1], p[0])
        # print(r)
        # print(o / m.pi * 180)
        # print(l / m.pi * 180)

        o -= -25/180 * m.pi
        l -= 180/180 * m.pi

        vec = np.array([[r*m.sin(o)*m.cos(l)], [r*m.sin(o)*m.sin(l)], [r*m.cos(o)]])
        print(vec)

        while(1):
            # self.publish_position("", "fef", self.x, self.y, self.z, self.ax, self.ay, self.az)
            self.publish_position_euler("", "test", 0.1, 0, 0, 0, 0, 0)
            self.publish_position("test", "lol", vec[0], vec[1], vec[2], 0, 0, 0, 0)
            # self.publish_position("", "lol", 0, 0, 0, (m.sqrt(2)/2), 0, 0, (m.sqrt(2)/2))
            # self.publish_position_euler("lol", "test", 0.1, 0, 0, 0, 0, 0)
            # self.publish_position("", "ooh", vec2[0], vec2[1], vec2[2], 0, 0, 0)
            time.sleep(0.5)
            print("hello")

        # self.publisher_ = self.create_publisher(msg_type=Marker, topic="marker", qos_profile=10)
        # self.get_logger().info("Starting publisher...")

        # while (1):
            # self.get_logger().info("Sending...")
            # self.publish_topic()
            # time.sleep(1)
    def publish_position(self, origin, child, x, y, z, w, i, j, k):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = origin
        t.child_frame_id = child

        t.transform.translation.x = float(x)
        t.transform.translation.y = float(y)
        t.transform.translation.z = float(z)

        t.transform.rotation.x = float(i)
        t.transform.rotation.y = float(j)
        t.transform.rotation.z = float(k)
        t.transform.rotation.w = float(w)

        self.position_broadcaster.sendTransform(t)

    def publish_position_euler(self, origin, child, x, y, z, ax, ay, az):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = origin
        t.child_frame_id = child

        t.transform.translation.x = float(x)
        t.transform.translation.y = float(y)
        t.transform.translation.z = float(z)

        q = quaternion_from_euler(float(ax), float(ay), float(az))
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the transformation
        self.position_broadcaster.sendTransform(t)

    def publish_topic(self):
        msg = Marker()
        # msg.header.frame_id = "test"

        msg.id = 0
        msg.type = Marker.ARROW
        msg.action = Marker.ADD

        q = quaternion_from_euler(0, 0, 0)
        
        msg.pose.position.x = 0.
        msg.pose.position.y = 0.
        msg.pose.position.z = 0.
        msg.pose.orientation.x = q[0]
        msg.pose.orientation.y = q[1]
        msg.pose.orientation.z = q[2]
        msg.pose.orientation.w = q[3]
        msg.scale.x = 1.
        msg.scale.y = 0.005
        msg.scale.z = 0.005
        msg.color.a = 1.
        msg.color.r = 0.8
        msg.color.g = 0.5
        msg.color.b = 0.3

        self.publisher_.publish(msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = test() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
