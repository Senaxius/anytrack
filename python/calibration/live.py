import cv2
import numpy as np
import yaml

class Calibrator(object):
    def __init__(self):
        self.video = 0
        self.fps = 30
        self.width = 1280
        self.height = 720
        self.cap = cv2.VideoCapture(self.video)
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        K = np.array(
            [
                [655.59075, 0.0, 654.93],
                [0.0, 654.22866, 351.73],
                [0.0,0.0,1.0],
            ]
        )
        LUCAS_KANADE_PARAMS = dict(
            winSize=(21, 21),
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
        )
        self.detector = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)
        self.lk_params = LUCAS_KANADE_PARAMS
        self.focal = 655.59075
        self.pp = (654.93, 351.73)
        self.K = K

        ret, self.old_frame = self.cap.read()
        cv2.waitKey(1) 
        ret, self.current_frame = self.cap.read()
        cv2.waitKey(1) 

        self.setup()

        self.loop()
    
    def setup(self):
        self.R = np.zeros(shape=(3, 3))
        self.t = np.zeros(shape=(3, 3))

        self.id = 0
        self.n_features = 0
        
        self.process_frame()

    def loop(self):
        while (1):
            # get images
            self.old_frame = self.current_frame
            ret, self.current_frame = self.cap.read()
            if ret != True:
                print("Camera Error!")
                exit()
            self.visual_odometry()
            print(type(float(self.current_frame_points[0][0])))
            for i in self.current_frame_points:
                center = (int(i[0]), int(i[1]))
                image = cv2.circle(self.current_frame, center, 1, color=(255,0,255))
            cv2.imshow("image", image)
            cv2.waitKey(1)
            self.id += 1

    def process_frame(self):
        if self.id < 2:
            self.old_frame = self.current_frame
            ret, self.current_frame = self.cap.read()
            self.visual_odometry()
            self.id = 2
        else:
            self.old_frame = self.current_frame
            ret, self.current_frame = self.cap.read()
            self.visual_odometry()
            self.id += 1

    def detect(self, img):
        p0 = self.detector.detect(img)

        return np.array([x.pt for x in p0], dtype=np.float32).reshape(-1, 1, 2)

    def visual_odometry(self):
        if self.n_features < 2000:
            self.p0 = self.detect(self.old_frame)

        # Calculate optical flow between frames, and track matched points from frame to frame
        self.p1, st, err = cv2.calcOpticalFlowPyrLK(
            self.old_frame, self.current_frame, self.p0, None, **self.lk_params
        )

        # Save the good points from the optical flow
        self.previous_frame_points = self.p0[st == 1]
        self.current_frame_points = self.p1[st == 1]

        E, _ = cv2.findEssentialMat(
            self.current_frame_points,
            self.previous_frame_points,
            self.focal,
            self.pp,
            cv2.RANSAC,
            0.999,
            1.0,
            None,
        )
        _, R, t, _ = cv2.recoverPose(
            E,
            self.previous_frame_points,
            self.current_frame_points,
        )


            # absolute_scale = self.get_absolute_scale()
            # if absolute_scale > 0.1 and abs(t[2][0]) > abs(t[0][0]) and abs(t[2][0]) > abs(t[1][0]):
            #     self.t = self.t + absolute_scale * self.R.dot(t)
            #     self.R = R.dot(self.R)

        # Save the total number of good features
        self.n_features = self.current_frame_points.shape[0]

        # print(t)

if __name__ == "__main__":
    calib = Calibrator()