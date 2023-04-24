import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.node import Node

from scanner_interfaces.msg import Tracks

class test(Node):  
    def __init__(self):
        super().__init__("test")  
        
        self.cam0_points = [

        ]
        self.cam1_points = [

        ]
        # self.cam0_points = [(570.3306884765625, 357.27435302734375), (684.0728759765625, 358.3771667480469), (684.1583251953125, 169.79367065429688), (172.0, 169.0), (171.91378784179688, 407.5)]
        # self.cam1_points = [(397.274658203125, 356.5), (991.5, 357.5), (991.0, 73.5), (526.8737182617188, 193.2474822998047), (527.0, 400.79998779296875)]
        self.xy0 = (0,0)
        self.xy1 = (0,0)

        group_0 = MutuallyExclusiveCallbackGroup() 
        group_1 = MutuallyExclusiveCallbackGroup() 
        group_2 = MutuallyExclusiveCallbackGroup() 

        self.listener_0 = self.create_subscription(msg_type=Tracks, topic=('/cam' + str("0") + '/tracks'), callback=self.track_0, qos_profile=10, callback_group=group_0)
        self.listener_1 = self.create_subscription(msg_type=Tracks, topic=('/cam' + str("1") + '/tracks'), callback=self.track_1, qos_profile=10, callback_group=group_1)
    
        self.loop = self.create_timer(0.1, callback=self.loop, callback_group=group_2)

    def track_0(self, msg):
        if len(msg.tracks) > 0:
            buffer = []
            for object in msg.tracks:
                self.xy0 = (object.x, object.y)
                buffer.append(self.xy0)
            self.cam0_points = buffer
    def track_1(self, msg):
        if len(msg.tracks) > 0:
            # self.xy1 = (msg.tracks[0].x, msg.tracks[0].y)
            buffer = []
            for object in msg.tracks:
                self.xy1 = (object.x, object.y)
                buffer.append(self.xy1)
            self.cam1_points = buffer
    
    def loop(self):
        input()
        # print(str(self.xy0) + "   " + str(self.xy1))
        # self.cam0_points.append(self.xy0)
        # self.cam1_points.append(self.xy1)
        
        print("self.cam0_points = np.array(" + str(self.cam0_points) + ")")
        print()
        print("self.cam1_points = np.array(" + str(self.cam1_points) + ")")



def main(args=None):
    rclpy.init(args=args)
    node = test() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    executor.spin()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()