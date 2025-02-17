from XRPLib.defaults import *

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver
# Write your code Here
from XRPLib.defaults import *
from huskylensPythonLibrary import HuskyLensLibrary
import time
import uos
import machine
import random
                                        # oled display height
husky = HuskyLensLibrary("I2C") ## SERIAL OR I2C 

 
 
differentialDrive = DifferentialDrive.get_default_differential_drive()


Kp_heading = 0.003
Kp_dist = 0.01

setpoint_x, setpoint_y = 120, 110

# while not husky.object_tracking_mode():
#     husky.object_tracking_mode()

while True:
    state = husky.command_request_blocks()
    
    print(state)
    
    if len(state) > 0: 
        curr_state = state[0]
        
        curr_x = curr_state[0]
        curr_y = curr_state[1]
        
        heading_error = setpoint_x - curr_x
        dist_error = setpoint_y - curr_y
        
        dist_effort = Kp_dist * dist_error
        heading_effort = Kp_heading * heading_error
        
        print(heading_effort)
        
        differentialDrive.arcade(dist_effort, heading_effort)
    
    time.sleep(0.05)
    
# while not husky.face_recognition_mode():
#     husky.face_recognition_mode()

# while True:
#     print(husky.command_request_blocks())
#     time.sleep(1)