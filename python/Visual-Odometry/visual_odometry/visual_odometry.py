from .monovideoodometry import MonoVideoOdometry
from .parameters import *


def visual_odometry(
    image_path="./input/sequences/10/image_0/",
    pose_path="./input/poses/10.txt",
    fivepoint=False,
):

    vo = MonoVideoOdometry(image_path, pose_path, FOCAL, PP, K, LUCAS_KANADE_PARAMS, fivepoint)
    trajectory = np.zeros(shape=(800, 1200, 3))

    frame_count = 0
    while vo.hasNextFrame():
        frame_count += 1
        frame = vo.current_frame

        vo.process_frame()

        estimated_coordinates = vo.get_mono_coordinates()
        true_coordinates = vo.get_true_coordinates()
