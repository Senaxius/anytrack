# import the necessary packages
import cv2
import time

from threading import Thread
import cv2

class VideoStream:
	def __init__(self, src=0, resolution=(640, 480), framerate=30, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		self.stream = cv2.VideoCapture(src)
        
		# setting the right codex to use
		fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
		self.stream.set(cv2.CAP_PROP_FOURCC, fourcc)
		
		self.stream.set(cv2.CAP_PROP_FPS, framerate)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

if __name__ == "__main__":
    cap = VideoStream(src=0, resolution=(1920, 1080), framerate=60).start()

    prev_frame_time=0

    # use this to limit the loop speed, otherwise might use too much cpu
    limit_rate = 60

    while True:
        start_time=time.time()

        frame = cap.read()

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # print fps
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        print(fps)

        time.sleep(max((1 / limit_rate) - (time.time() - start_time), 0))