import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

import math

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()

    frame1 = ttk.Frame(root,padding = 5)
    frame1.grid()

    speed_entry = ttk.Entry(frame1)
    speed_entry.grid(row=1,column=0)

    speed_label = ttk.Label(frame1,text = 'speed')
    speed_label.grid(row=2,column=0)

    scale_entry = ttk.Entry(frame1)
    scale_entry.grid(row=1,column=1)

    scale_label = ttk.Label(frame1,text = 'scale')
    scale_label.grid(row=2,column=1)

    path_button = ttk.Button(frame1,text = 'Pick Path')
    path_button.grid(row=1,column=2)
    path_button['command'] = lambda: pick_path(speed_entry,scale_entry,mqtt_client)

    root.mainloop()

def pick_path(speed_entry,scale_entry,mqtt_client):
    path_list = []
    speed = int(speed_entry.get())

    root2 = tkinter.Tk()

    frame2 = ttk.Frame(root2,padding = 5)
    frame2.grid()

    canvas = tkinter.Canvas(frame2, background="lightgray", width=1000, height=700)
    canvas.grid(columnspan=2)
    canvas.bind("<Button-1>", lambda event: left_mouse_click(event, mqtt_client,path_list))

    done_button = ttk.Button(frame2,text='Done')
    done_button.grid(row=3,column=1)
    done_button['command'] = lambda: drive_the_path(speed_entry, scale_entry,path_list,mqtt_client)

    clear_button = ttk.Button(frame2,text='clear')
    clear_button.grid(row=3,column=0)
    clear_button['command'] = lambda: clear_everything(canvas,path_list)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")


    root2.mainloop()


def left_mouse_click(event, mqtt_client,path_list):
    point = (event.x,event.y)
    path_list.append(point)
    if len(path_list) > 1:
        mqtt_client.send_message('make_line',[path_list])

def clear_everything(canvas,path_list):
    for k in range(len(path_list)):
        path_list.pop(-1)
    canvas.delete('all')

def drive_the_path(speed,scale,path,mqtt_client):
    print(speed.get(), scale.get(), path)
    speed = int(speed.get())
    scale = int(scale.get())
    for k in range(len(path)-2):
        p1 = path[k]
        p2 = path[k+1]
        distance = ((((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (1/2)) / 100) * scale
        if p2[0]-p1[0] < 0:
            angle_add = math.pi
        else:
            angle_add = 0
        angle = math.tan((p2[0]-p1[0]) / (p2[1]-p1[1])) + angle_add
        mqtt_client.send_message('turn_degrees',[angle,speed])
        mqtt_client.send_message('drive_inches',[distance,speed])


class MyDelegate(object):

    def __init__(self, canvas):
        self.canvas = canvas

    def make_line(self, list_of_points):
        x2 = list_of_points[len(list_of_points)-1][0]
        y2 = list_of_points[len(list_of_points)-1][1]
        x1 = list_of_points[len(list_of_points)-2][0]
        y1 = list_of_points[len(list_of_points)-2][1]

        self.canvas.create_line(x1, y1, x2, y2)

main()