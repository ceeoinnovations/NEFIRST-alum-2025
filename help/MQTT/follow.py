from TuftsMQTT.mqttconnect import *
from XRPLib.defaults import *
import struct
import time

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver
# Write your code Here

def handle_message(topic, msg):
    try:
        #print(topic)
        #print(msg)
        if msg == b'0.0':
            return
        speed, turn = (float(value.strip()) for value in msg.decode().split(","))
        #print(f"Received speed: {speed}, turn: {turn}")
        drivetrain.arcade(speed, turn)
    except:
        print("Exception parsing")

c = connect_mqtt()

c.set_callback(handle_message)
c.subscribe("XRPArcade")
board.led_on()
while True:
    try:
        c.wait_msg()
    except:
        print("exception")
        #c.connect()
    #time.sleep(.01)