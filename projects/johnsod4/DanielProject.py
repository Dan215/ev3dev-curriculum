"""
Manually controlled to move around, uses a rosegraphics window to plot its position, with the center of the window being
its starting position.  When a beacon is detected, the robot ignores manual controls and drives and picks up the beacon.
"""

import time
import tkinter
from tkinter import ttk
import rosegraphics as rg
import mqtt_remote_method_calls as com


def main():
    global turtleState
    turtleState = "stop"
    print('Project Testing')
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    window = rg.TurtleWindow()
    rob = rg.SimpleTurtle('turtle')
    rob.pen = rg.Pen('midnight blue', 2)

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    """
    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)
    """
    speed_label = ttk.Label(main_frame, text="Speed")
    speed_label.grid(row=0, column=1)
    speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    speed_entry.insert(0, "600")
    speed_entry.grid(row=1, column=1)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: go_forward(mqtt_client, speed_entry, window, rob)
    root.bind('<Up>', lambda event: go_forward(mqtt_client, speed_entry, window, rob))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: go_left(mqtt_client, speed_entry, window, rob)
    root.bind('<Left>', lambda event: go_left(mqtt_client, speed_entry, window, rob))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: go_right(mqtt_client, speed_entry, window, rob)
    root.bind('<Right>', lambda event: go_right(mqtt_client, speed_entry, window, rob))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: go_backward(mqtt_client, speed_entry, window, rob)
    root.bind('<Down>', lambda event: go_backward(mqtt_client, speed_entry, window, rob))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    if turtleState == "forward":
        rob.speed = int(speed_entry.get())
        rob.forward(1)
    elif turtleState == "backward":
        rob.speed = int(speed_entry.get())
        rob.backward(1)
    elif turtleState == "right":
        rob.speed = int(speed_entry.get())
        rob.right(1)
    elif turtleState == "left":
        rob.speed = int(speed_entry.get())
        rob.left(1)

    root.mainloop()


# callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def go_forward(mqtt_client, speed_entry, window, rob):
    print("forward")
    mqtt_client.send_message("forward", [int(speed_entry.get()), int(speed_entry.get())])
    turtleState = "forward"


def go_right(mqtt_client, speed_entry, window, rob):
    print("right")
    mqtt_client.send_message("right", [int(speed_entry.get()), int(speed_entry.get())])
    turtleState = "right"


def stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")
    turtleState = "stop"


def go_left(mqtt_client, speed_entry, window, rob):
    print("left")
    mqtt_client.send_message("left", [int(speed_entry.get()), int(speed_entry.get())])
    turtleState = "left"


def go_backward(mqtt_client, speed_entry, window, rob):
    print("back")
    mqtt_client.send_message("back", [int(speed_entry.get()), int(speed_entry.get())])
    turtleState = 'backward'


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()