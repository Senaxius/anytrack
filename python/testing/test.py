# import keyboard

# while True:
#     if keyboard.read_key() == "q":
#         print("ohohoh")

import keyboard
while True:
    if keyboard.is_pressed("a"):
        print("You pressed 'a'.")
        break
