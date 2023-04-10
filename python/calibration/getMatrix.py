import cv2
import numpy as np

class MonoVideoOdometry(object):
    def __init__(self):
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
        self.focal = 655.59075
        self.pp = (654.93, 351.73)
        self.K = K
        self.lk_params = LUCAS_KANADE_PARAMS
        self.image_shape = (720,1280)
        self.fivepoint = True

        self.R = np.zeros(shape=(3, 3))
        self.t = np.zeros(shape=(3, 3))

        self.id = 0
        self.n_features = 0

        self.video = 0
        self.fps = 30
        self.width = self.image_shape[1]
        self.height = self.image_shape[0]

        self.cap = cv2.VideoCapture(self.video)

        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)

        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        ret, self.old_frame = self.cap.read()
        cv2.waitKey(1) 
        ret, self.current_frame = self.cap.read()
        cv2.waitKey(1) 

        cv2.imshow("old", self.old_frame)
        cv2.imshow("new", self.current_frame)

        self.process_frame()

    def hasNextFrame(self):
        """
        Determine whether there are remaining frames in the folder to process
        :return: Whether there are still frames in the folder to process
        """

        return self.id < len(os.listdir(self.file_path))

    def detect(self, img):
        """
        Detect features and parse into useable format
        :param img: Image for which to detect keypoints on
        :return: A sequence of points in (x, y) coordinate format denoting location of detected keypoint
        """

        p0 = self.detector.detect(img)

        return np.array([x.pt for x in p0], dtype=np.float32).reshape(-1, 1, 2)

    def visual_odometry(self):
        if self.n_features < 2000:
            self.p0 = self.detect(self.old_frame)

        # Calculate optical flow between frames, and track matched points from frame to frame
        self.p1, st, err = cv2.calcOpticalFlowPyrLK(
            self.old_frame, self.current_frame, self.p0, None, **self.lk_params
        )
        print(self.p1)

        # Save the good points from the optical flow
        self.previous_frame_points = self.p0[st == 1]
        self.current_frame_points = self.p1[st == 1]

        if self.id < 2:
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

            _, self.R, self.t, _ = cv2.recoverPose(
                E,
                self.previous_frame_points,
                self.current_frame_points,
                self.R.copy(),
                self.t,
                self.focal,
                self.pp,
                None,
            )
        else:
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
                self.R.copy(),
                self.t.copy(),
                self.focal,
                self.pp,
                None,
            )

            absolute_scale = self.get_absolute_scale()
            if absolute_scale > 0.1 and abs(t[2][0]) > abs(t[0][0]) and abs(t[2][0]) > abs(t[1][0]):
                self.t = self.t + absolute_scale * self.R.dot(t)
                self.R = R.dot(self.R)

        # Save the total number of good features
        self.n_features = self.current_frame_points.shape[0]

        print(self.R)

    def get_mono_coordinates(self):
        """
        Multiply by the diagonal matrix to fix our vector onto same coordinate axis as true values
        :return: Array in format [x, y, z]
        """

        diag = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
        adj_coord = np.matmul(diag, self.t)

        return adj_coord.flatten()

    def get_true_coordinates(self):
        """
        Returns true coordinates of vehicle
        :return: Array in format [x, y, z]
        """

        return self.true_coord.flatten()

    def get_absolute_scale(self):
        """
        Estimation of scale for multiplying translation vectors
        :return: Scalar multiplier
        """

        pose = self.pose[self.id - 1].strip().split()
        x_prev = float(pose[3])
        y_prev = float(pose[7])
        z_prev = float(pose[11])
        pose = self.pose[self.id].strip().split()
        x = float(pose[3])
        y = float(pose[7])
        z = float(pose[11])

        true_vect = np.array([[x], [y], [z]])
        self.true_coord = true_vect
        prev_vect = np.array([[x_prev], [y_prev], [z_prev]])

        return np.linalg.norm(true_vect - prev_vect)

    def process_frame(self):
        self.old_frame = self.current_frame
        ret, self.current_frame = self.cap.read()
        self.visual_odometry()
        self.id == 2

if __name__ == "__main__":
    calib = MonoVideoOdometry()

