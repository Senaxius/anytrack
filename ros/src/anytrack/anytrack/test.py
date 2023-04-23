import rclpy
from rclpy.node import Node

from scanner_interfaces.msg import Tracks

class test(Node):  
    def __init__(self):
        super().__init__("test")  
        
        cam0_points = [

        ]
        cam1_points = [

        ]
        self.xy0 = (0,0)
        self.xy1 = (1,1)

        self.listener_0 = self.create_subscription(msg_type=Tracks, topic=('/cam' + str("0") + '/tracks'), callback=self.track_0, qos_profile=10)
        self.listener_1 = self.create_subscription(msg_type=Tracks, topic=('/cam' + str("1") + '/tracks'), callback=self.track_1, qos_profile=10)
    
        self.loop = self.create_timer(0.1, callback=self.loop)

    def track_0(self, msg):
        if len(msg.tracks) > 0:
            self.xy0 = (msg.tracks[0].x, msg.tracks[0].y)
    def track_1(self, msg):
        if len(msg.tracks) > 1:
            print(msg.track)
            self.xy1 = (msg.tracks[0].x, msg.tracks[0].y)
    
    def loop(self):
        input()
        print(str(self.xy0) + "   " + str(self.xy1))



def main(args=None):
    rclpy.init(args=args)
    node = test() 
    rclpy.spin(node)
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()