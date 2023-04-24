import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from scanner_interfaces.msg import Tracks
 
class template(Node): 
    def __init__(self):
        super().__init__("template") 

        clb_group = ReentrantCallbackGroup() 
        
        # publisher
        self.publisher = self.create_publisher(msg_type=Tracks, topic="", qos_profile=10)

        # listener
        self.subscriber = self.create_subscription(msg_type=Tracks, topic=('/cam' + str(self.index) + '/tracks'), callback=self.listener_callback, qos_profile=10, callback_group=clb_group)
 
        # loop
        self.loop = self.create_timer(0.00001, self.loop_callback)
    
    def listener_callback(self, msg):
        pass
    
    def loop_callback(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = template() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
