import tkinter as tk
from tkinter import ttk
from multiprocessing import Process

# root window
root = tk.Tk()
root.geometry('300x200')
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

def slider_changed(event):
    data = [int(h_value.get()), int(s_value.get()), int(v_value.get()), int(h_end.get()), int(s_end.get()), int(v_end.get())]
    print(data)

h_label = ttk.Label(
    root,
    text='Hue:'
)
h_label.grid(
    column=0,
    row=0,
    sticky='w'
)
s_label = ttk.Label(
    root,
    text='Saturation:'
)
s_label.grid(
    column=0,
    row=1,
    sticky='w'
)
v_label = ttk.Label(
    root,
    text='Value:'
)
v_label.grid(
    column=0,
    row=2,
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
root.mainloop()
print("test")