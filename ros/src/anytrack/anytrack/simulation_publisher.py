#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import random
import threading as th

from gazebo_msgs.srv import SetEntityState

class ball_0:
    corners = [(2.5, 0, 0.3), (1.5, 4, -0.4), (3.5, 3, -0.6), (0, 2, 1.7), (5, -3, 2), (2, -1.5, 0.3), (5, 0, 2),]
    iter = 100
    id = 0
    cor_id_now = 0
    cor_id_future = 1
    max = len(corners) - 1
    x = 6
    y = -2
    z = 0.3
    x_step = 0
    y_step = 0
    z_step = 0

class ball_1:
    # corners = [(2.5, 0, 0.3), (1.5, 4, -0.4), (3.5, 3, -0.6), (0, 2, 1.7), (5, -3, 2), (2, -1.5, 0.3), (5, 0, 2),]
    corners = [(1.5, 4, -0.4), (3.5, 3, -0.6), (0, 2, 1.7), (5, -3, 2), (2, -1.5, 0.3), (5, 0, 2), (2.5, 0, 0.3),]
    iter = 200
    id = 0
    cor_id_now = 0
    cor_id_future = 1
    max = len(corners) - 1
    x = 6+2.5
    y = -2+0
    z = 0.3+0.3
    x_step = 0
    y_step = 0
    z_step = 0

class simulation_publisher(Node): 
    def __init__(self):
        super().__init__("simulation_publisher") 

        self.declare_parameter("ball_count", 1)
        self.ball_count = self.get_parameter("ball_count").value

        self.client = self.create_client(SetEntityState, "/simulation/set_entity_state")

        self.loop = self.create_timer(0.02, self.loop)

        self.get_logger().info("Starting publisher...")

        # self.key = 0
        # th.Thread(target=self.key_capture, args=(), name='key_capture_thread', daemon=True).start()

    def key_capture(self):
        while(1):
            input()
            # self.key += 1
            if ball_0.id == 0:
                ball_0.x_step = ball_0.corners[ball_0.cor_id_future][0] - ball_0.corners[ball_0.cor_id_now][0]
                ball_0.y_step = ball_0.corners[ball_0.cor_id_future][1] - ball_0.corners[ball_0.cor_id_now][1]
                ball_0.z_step = ball_0.corners[ball_0.cor_id_future][2] - ball_0.corners[ball_0.cor_id_now][2]
                ball_0.x_step /= ball_0.iter
                ball_0.y_step /= ball_0.iter
                ball_0.z_step /= ball_0.iter

            ball_0.id += 1
            # ball_0.id = self.key


            if ball_0.id == ball_0.iter:
                ball_0.id = 0
                if ball_0.cor_id_now == ball_0.max:
                    ball_0.cor_id_now = 0
                else:
                    ball_0.cor_id_now += 1
                if ball_0.cor_id_future == ball_0.max:
                    ball_0.cor_id_future = 0
                else:
                    ball_0.cor_id_future += 1
            
            ball_0.x = ball_0.x + ball_0.x_step
            ball_0.y = ball_0.y + ball_0.y_step
            ball_0.z = ball_0.z + ball_0.z_step

            self.set_position('ball_0', ball_0.x, ball_0.y, ball_0.z)

            if self.ball_count == 2:
                if ball_1.id == 0:
                    ball_1.x_step = ball_1.corners[ball_1.cor_id_future][0] - ball_1.corners[ball_1.cor_id_now][0]
                    ball_1.y_step = ball_1.corners[ball_1.cor_id_future][1] - ball_1.corners[ball_1.cor_id_now][1]
                    ball_1.z_step = ball_1.corners[ball_1.cor_id_future][2] - ball_1.corners[ball_1.cor_id_now][2]
                    ball_1.x_step /= ball_1.iter
                    ball_1.y_step /= ball_1.iter
                    ball_1.z_step /= ball_1.iter

                ball_1.id += 1
                # ball_1.id = self.key

                if ball_1.id == ball_1.iter:
                    ball_1.id = 0
                    if ball_1.cor_id_now == ball_1.max:
                        ball_1.cor_id_now = 0
                    else:
                        ball_1.cor_id_now += 1
                    if ball_1.cor_id_future == ball_1.max:
                        ball_1.cor_id_future = 0
                    else:
                        ball_1.cor_id_future += 1
                
                ball_1.x = ball_1.x + ball_1.x_step
                ball_1.y = ball_1.y + ball_1.y_step
                ball_1.z = ball_1.z + ball_1.z_step

                self.set_position('ball_1', ball_1.x, ball_1.y, ball_1.z)


    def loop(self):
        if ball_0.id == 0:
            ball_0.x_step = ball_0.corners[ball_0.cor_id_future][0] - ball_0.corners[ball_0.cor_id_now][0]
            ball_0.y_step = ball_0.corners[ball_0.cor_id_future][1] - ball_0.corners[ball_0.cor_id_now][1]
            ball_0.z_step = ball_0.corners[ball_0.cor_id_future][2] - ball_0.corners[ball_0.cor_id_now][2]
            ball_0.x_step /= ball_0.iter
            ball_0.y_step /= ball_0.iter
            ball_0.z_step /= ball_0.iter

        ball_0.id += 1
        # ball_0.id = self.key


        if ball_0.id == ball_0.iter:
            ball_0.id = 0
            if ball_0.cor_id_now == ball_0.max:
                ball_0.cor_id_now = 0
            else:
                ball_0.cor_id_now += 1
            if ball_0.cor_id_future == ball_0.max:
                ball_0.cor_id_future = 0
            else:
                ball_0.cor_id_future += 1
        
        ball_0.x = ball_0.x + ball_0.x_step
        ball_0.y = ball_0.y + ball_0.y_step
        ball_0.z = ball_0.z + ball_0.z_step

        self.set_position('ball_0', ball_0.x, ball_0.y, ball_0.z)

        if self.ball_count == 2:
            if ball_1.id == 0:
                ball_1.x_step = ball_1.corners[ball_1.cor_id_future][0] - ball_1.corners[ball_1.cor_id_now][0]
                ball_1.y_step = ball_1.corners[ball_1.cor_id_future][1] - ball_1.corners[ball_1.cor_id_now][1]
                ball_1.z_step = ball_1.corners[ball_1.cor_id_future][2] - ball_1.corners[ball_1.cor_id_now][2]
                ball_1.x_step /= ball_1.iter
                ball_1.y_step /= ball_1.iter
                ball_1.z_step /= ball_1.iter

            ball_1.id += 1
            # ball_1.id = self.key

            if ball_1.id == ball_1.iter:
                ball_1.id = 0
                if ball_1.cor_id_now == ball_1.max:
                    ball_1.cor_id_now = 0
                else:
                    ball_1.cor_id_now += 1
                if ball_1.cor_id_future == ball_1.max:
                    ball_1.cor_id_future = 0
                else:
                    ball_1.cor_id_future += 1
            
            ball_1.x = ball_1.x + ball_1.x_step
            ball_1.y = ball_1.y + ball_1.y_step
            ball_1.z = ball_1.z + ball_1.z_step

            self.set_position('ball_1', ball_1.x, ball_1.y, ball_1.z)
        
    def set_position(self, name, x, y, z):
        request = SetEntityState.Request()
        request.state.name = name
        request.state.pose.position.x = float(x)
        request.state.pose.position.y = float(y)
        request.state.pose.position.z = float(z)
        self.client.call_async(request)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = simulation_publisher()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
