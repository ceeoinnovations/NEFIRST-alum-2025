from XRPLib.defaults import *
from huskylensPythonLibrary import HuskyLensLibrary
import time
import uos
import machine
import random
                                        # oled display height
husky = HuskyLensLibrary("I2C") ## SERIAL OR I2C 

 
 
differentialDrive = DifferentialDrive.get_default_differential_drive()


base_speed = 0.35
Kp = 0.0015

while not husky.line_tracking_mode():
    husky.line_tracking_mode()

while True:
    state = husky.command_request_arrows()
    
    if (len(state) > 0): 
        
        state_vector = state[0]
    
        state_x = state_vector[0]
        setpoint_x = state_vector[2]
        
        error = setpoint_x - state_x
        effort = Kp * error 
        
        differentialDrive.set_effort(base_speed - effort, base_speed + effort)
        
        print(state)
        print(error)
    
    time.sleep(0.05)
    
# while not husky.face_recognition_mode():
#     husky.face_recognition_mode()

# while True:
#     print(husky.command_request_blocks())
#     time.sleep(1)