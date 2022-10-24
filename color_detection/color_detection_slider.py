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
    cap = cv2.VideoCapture(0)
    while(1):
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        start_color = np.array([data[0], data[1], data[2]])
        end_color = np.array([data[3], data[4], data[5]])

        print(start_color, end_color)
        
        mask = cv2.inRange(hsv, start_color, end_color)
        res = cv2.bitwise_and(frame,frame, mask= mask)

        # cv2.imshow('frame',frame)
        # cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        
        cv2.waitKey(1) 

    cv2.destroyAllWindows()
    cap.release()

data = m.Array('i', 6)
slider_process = m.Process(target=run_slider)
slider_process.start()
img_process = m.Process(target=showImg, args=(data,))
img_process.start()
img_process.join()