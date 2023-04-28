#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import random

from gazebo_msgs.srv import SetEntityState

class simulation_publisher(Node): 
    def __init__(self):
        super().__init__("simulation_publisher") 

        self.client = self.create_client(SetEntityState, "/simulation/set_entity_state")

        self.corners = [(0, 0, 0), (0, 6, 0), (4, 5, 0), (4, 1, 0), (0, 0, 3), (0, 6, 3), (4, 5, 3), (4, 1, 3)]
        # self.corners = [(0, 0, 0), (0, 3, 0), (3, 3, 0), (3, -3, 3), (1, -2, 3), (2, 1, 0.5)]
        self.iter = 100
        self.id = 0
        self.cor_id_now = 0
        self.cor_id_future = 1
        self.max = 7

        self.loop = self.create_timer(0.01, self.loop)

        self.get_logger().info("Starting publisher...")

        self.x = 6
        self.y = -2
        self.z = 0.3
        self.x_step = 0
        self.y_step = 0
        self.z_step = 0

    def loop(self):
        if self.id == 0:
            self.x_step = self.corners[self.cor_id_future][0] - self.corners[self.cor_id_now][0]
            self.y_step = self.corners[self.cor_id_future][1] - self.corners[self.cor_id_now][1]
            self.z_step = self.corners[self.cor_id_future][2] - self.corners[self.cor_id_now][2]
            self.x_step /= self.iter
            self.y_step /= self.iter
            self.z_step /= self.iter

        self.id += 1

        if self.id == self.iter:
            self.id = 0
            if self.cor_id_now == self.max:
                self.cor_id_now = 0
            else:
                self.cor_id_now += 1
            if self.cor_id_future == self.max:
                self.cor_id_future = 0
            else:
                self.cor_id_future += 1
        
        self.x = self.x + self.x_step
        self.y = self.y + self.y_step
        self.z = self.z + self.z_step


        print(self.id)




        # self.px = self.x
        # self.py = self.y
        # self.pz = self.z
        # self.x = 0
        # self.y = 0
        # self.z = 0

        # while(1):
        #     self.x = self.px + (random.random() - 0.5)
        #     if self.x <= 10 and self.x >= 4:
        #         break
        # while(1):
        #     self.y = self.py + ((random.random() - 0.5) * 2)
        #     if self.y <= 3 and self.y >= -3:
        #         break
        # while(1):
        #     self.z = self.pz + (random.random() - 0.5)
        #     if self.z <= 2 and self.z >= 0.3:
        #         break
        
        self.set_position(self.x, self.y, self.z)
        

    def set_position(self, x, y, z):
        request = SetEntityState.Request()
        request.state.name = 'ball'
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
