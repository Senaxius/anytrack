import tkinter as tk
from tkinter import ttk
import  multiprocessing as m
import time
import cv2
import numpy as np

# root window
root = tk.Tk()
root.geometry('500x100')
root.resizable(False, False)
root.title('Slider Demo')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# slider current value
h_value = tk.DoubleVar()
s_value = tk.DoubleVar()
v_value = tk.DoubleVar()
h_end = tk.DoubleVar()
s_end = tk.DoubleVar()
v_end = tk.DoubleVar()

def slider_changed(event, ):
    data[0] = int(h_value.get())
    data[1] = int(s_value.get())
    data[2] = int(v_value.get())
    data[3] = int(h_end.get())
    data[4] = int(s_end.get())
    data[5] = int(v_end.get())

h_label = ttk.Label(
    root,
    text='Hue-start:'
)
h_label.grid(
    column=0,
    row=0,
    sticky='w'
)
s_label = ttk.Label(
    root,
    text='Saturation-start:'
)
s_label.grid(
    column=0,
    row=1,
    sticky='w'
)
v_label = ttk.Label(
    root,
    text='Value-start:'
)
v_label.grid(
    column=0,
    row=2,
    sticky='w'
)
# end labels
h_end_label = ttk.Label(
    root,
    text='Hue-end:'
)
h_end_label.grid(
    column=0,
    row=3,
    sticky='w'
)
s_end_label = ttk.Label(
    root,
    text='Saturation-end:'
)
s_end_label.grid(
    column=0,
    row=4,
    sticky='w'
)
v_end_label = ttk.Label(
    root,
    text='Value-end:'
)
v_end_label.grid(
    column=0,
    row=5,
    sticky='w'
)

#  slider
h = ttk.Scale(
    root,
    from_=0,
    to=180,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=h_value
)
h.grid(
    column=1,
    row=0,
    sticky='we'
)
s = ttk.Scale(
    root,
    from_=0,
    to=255,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=s_value
)
s.grid(
    column=1,
    row=1,
    sticky='we'
)
v = ttk.Scale(
    root,
    from_=0,
    to=255,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=v_value
)
v.grid(
    column=1,
    row=2,
    sticky='we'
)
h_end = ttk.Scale(
    root,
    from_=0,
    to=180,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=h_end
)
h_end.grid(
    column=1,
    row=3,
    sticky='we'
)
s_end = ttk.Scale(
    root,
    from_=0,
    to=255,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=s_end
)
s_end.grid(
    column=1,
    row=4,
    sticky='we'
)
v_end = ttk.Scale(
    root,
    from_=0,
    to=255,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=v_end
)
v_end.grid(
    column=1,
    row=5,
    sticky='we'
)

def run_slider():
    root.mainloop()
def showImg(data):
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(42, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    width = 1270
    height = 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    while(1):
        _, frame = cap.read()
        # frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        start_color = np.array([data[0], data[1], data[2]])
        end_color = np.array([data[3], data[4], data[5]])

        # start_color = np.array([5,0,0])
        # end_color = np.array([100, 255, 255])

        print(start_color, end_color)
        
        color_mask = cv2.inRange(hsv, start_color, end_color)
        white_mask = cv2.inRange(hsv, np.array([140, 0, 255]), np.array([255, 255, 255]))

        res = cv2.bitwise_and(frame, frame, mask= color_mask)
        white_bgr = cv2.bitwise_or(frame, frame, mask= white_mask)
        # res = cv2.add(res, white_bgr)

        # hsv2 = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

        # ball = cv2.inRange(hsv2, np.array([0, 0, 100]), np.array([255, 255, 255]))
        # ball = cv2.inRange(hsv2, start_colo, end_colo)
        
        cv2.imshow('frame',frame)
        # cv2.imshow('mask', mask)
        # cv2.imshow('white', white_mask)
        cv2.imshow('res',res)
        # cv2.imshow('ball',ball)
        
        cv2.waitKey(1) 

    cv2.destroyAllWindows()
    cap.release()

data = m.Array('i', 6)
slider_process = m.Process(target=run_slider)
slider_process.start()
img_process = m.Process(target=showImg, args=(data,))
img_process.start()
img_process.join()
