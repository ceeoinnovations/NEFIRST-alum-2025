from TuftsMQTT.mqttconnect import *
from XRPLib.defaults import *
import time
import struct

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver
# Write your code Here

c = connect_mqtt()
c.ping()
board.led_on()
board.wait_for_button()

c.publish("XRPArcade", "0.5, 0.0")
drivetrain.arcade(1.0,0.0)

time.sleep(2)

c.publish("XRPArcade", "0.5, 0.5")
drivetrain.arcade(1.0, 1.0)

time.sleep(1)

c.publish("XRPArcade", "0.0, 0.0")
drivetrain.arcade(0.0,0.0)
