import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

import math as m
import cv2
import numpy as np
from scipy.spatial.transform import Rotation   

class calibration(Node): 
    def __init__(self):
        super().__init__("calibration") 
        

        # # self.cam0_points = np.array([(42.0, 430.5), (331.1666564941406, 462.9166564941406), (638.8715209960938, 438.8064880371094), (638.8715209960938, 438.8064880371094), (550.0, 515.5), (630.1802978515625, 268.9013671875), (99.5, 270.5), (755.2792358398438, 229.7207794189453), (513.022705078125, 138.5454559326172)])
        # # self.cam1_points = np.array([(146.0, 432.5), (478.2234191894531, 462.3723449707031), (752.4038696289062, 438.9017028808594), (752.4038696289062, 438.9017028808594), (774.3980102539062, 515.7572631835938), (708.0988159179688, 268.906982421875), (176.5, 270.0), (882.6141967773438, 229.6929168701172), (729.7863159179688, 138.90977478027344)])

        # self.cam0_points = np.array([(253.58084106445312, 452.0838317871094), (1040.0546875, 427.2298889160156), (700.705810546875, 397.1164245605469), (477.51275634765625, 397.5780029296875), (834.758056640625, 370.0), (424.5, 243.0), (98.61164855957031, 146.20388793945312), (1085.0689697265625, 78.12068939208984)])
        # self.cam1_points = np.array([(390.63482666015625, 451.8146057128906), (1216.0, 425.5), (816.921630859375, 397.2686462402344), (606.642578125, 397.78997802734375), (912.859375, 370.0), (507.68182373046875, 243.31817626953125), (221.5, 146.5), (1182.0, 79.5)])

        # self.cam0_points = np.array([(229.24490356445312, 487.5728759765625), (948.8225708007812, 472.94085693359375), (700.705810546875, 397.1164245605469), (477.51275634765625, 397.5780029296875), (424.5, 243.0), (98.61164855957031, 146.20388793945312), (834.5, 108.0), (1124.0, 81.0)])
        # self.cam1_points = np.array([(419.5, 486.5), (1137.0, 473.5), (816.921630859375, 397.2686462402344), (606.642578125, 397.78997802734375), (507.68182373046875, 243.31817626953125), (221.5, 146.5), (912.7653198242188, 108.23469543457031), (1176.0, 81.0)])

        self.cam0_points = np.array([(233.88235473632812, 486.6764831542969), (842.0, 473.0), (702.4569091796875, 397.2131042480469), (480.1981201171875, 398.0), (425.9615478515625, 243.73077392578125), (101.76829528808594, 147.256103515625), (835.7127685546875, 108.2872314453125), (1125.0, 82.0)])

        self.cam1_points = np.array([(618.7017211914062, 461.6974182128906), (1103.0, 451.0), (895.5, 392.5), (723.5, 392.3125), (597.0, 255.0), (388.0, 176.0), (958.99560546875, 131.83628845214844), (1190.5, 98.5)])

        self.focal = 762.7249
        self.pp = (640.5, 360.5)

        self.R = np.zeros(shape=(3, 3))
        self.t = np.zeros(shape=(3, 3))

        E = np.zeros(shape=(3, 3))

        E, _ = cv2.findEssentialMat(
            self.cam0_points,
            self.cam1_points,
            self.focal,
            self.pp,
            cv2.RANSAC,
            0.999,
            1.0,
            None,
        )


        R1 = np.zeros(shape=(3, 3))
        R2 = np.zeros(shape=(3, 3))
        t = np.zeros(shape=(3))
        
        # cv2.decomposeEssentialMat(E, R1, R2, t)

        # print(E)

        _, self.R, self.t, _ = cv2.recoverPose(
            E,
            self.cam0_points,
            self.cam1_points,
            # self.R,
            # self.t,
            focal=self.focal,
            pp = self.pp,
            mask=None,
        )

        # print(self.t)
        print("translation: (" + str(round(self.t[2][0], 1)), end='')
        print(", " + str(round(self.t[0][0], 1)), end='')
        print(", " + str(round(self.t[1][0], 1)), end='')
        print(")")

        # print(self.R)
        r = Rotation.from_matrix(self.R)
        angles = r.as_euler("xyz", degrees=True)
        print("rotation (in degrees): (" + str(round(angles[1], 1)), end='')
        print(", " + str(round(angles[2], 1)), end='')
        print(", " + str(round(angles[0], 1)), end='')
        print(")")


def main(args=None):
    rclpy.init(args=args)
    node = calibration() 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
