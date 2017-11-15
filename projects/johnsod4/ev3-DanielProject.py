"""
Daniel Johnson
ev3 autonomous portion of the final project.  Tests to see if the beacon is in range and active, then drives towards and picks it up
If successful, it turns itself off.
"""

import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time
import math


def main():
    robot = robo.Snatch3r()
    ev3.Sound.speak("this isn't going to WORK, nope nope nooooooooooooooooooooooooooooopppppee")
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.mqtt_create(mqtt_client)
    robot.running = True
    beacon_seeker = ev3.BeaconSeeker(channel=1)
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    time.sleep(5)
    k = 0
    while True:
        # ev3.Sound.speak("beep")
        # time.sleep(2)
        beacon_seeker = ev3.BeaconSeeker(channel=1)

        #and math.fabs(beacon_seeker.heading) <= 10

        if beacon_seeker.distance > 0 and math.fabs(beacon_seeker.heading) <= 10:
            robot.stop()
            time.sleep(3)
            robot.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Sound.speak("mine")
            if robot.seek_beacon():
                ev3.Sound.play("/home/robot/csse120/assets/sounds/mine2.wav")
                robot.arm_up()
                time.sleep(1.5)
                ev3.Sound.play("/home/robot/csse120/assets/sounds/mine2.wav")
                time.sleep(7)
                robot.arm_down()
                ev3.Sound.speak("I'm done, good bye")
                robot.shutdown()
            robot.stop()
        elif beacon_seeker.distance < 0:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        elif beacon_seeker.distance > 5:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
        else:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        if not robot.running:
            break
        time.sleep(0.01)
        k = k + 1
        if k > 50:
            ev3.Sound.speak("beep")
            k = 0

main()