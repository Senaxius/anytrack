# import the necessary packages
import cv2
import time

if __name__ == "__main__":
    VIDEO_SOURCE = 0
    CAMERA_CAPTURE_FPS = 60
    CAMERA_CAPTURE_WIDTH = 1920
    CAMERA_CAPTURE_HEIGHT = 1080

    cap = cv2.VideoCapture(VIDEO_SOURCE)

    # setting the right codex to use
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    
    cap.set(cv2.CAP_PROP_FPS, CAMERA_CAPTURE_FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CAPTURE_HEIGHT)

    print()
    print("WIDTH: " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("HEIGHT: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("FPS: " + str(cap.get(cv2.CAP_PROP_FPS)))
    print("FOURCC: " + str(cap.get(cv2.CAP_PROP_FOURCC)))

    prev_frame_time=0

    while True:
        ret, frame = cap.read()

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # print fps
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        print(fps)

    cv2.destroyAllWindows()
    cap.release()