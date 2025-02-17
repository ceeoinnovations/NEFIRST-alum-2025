from XRPLib.defaults import *
from XRPLib.timeout import Timeout
from camera_test import HuskyLensLibrary

BLACK_THRESH = 0.85

# This code navigates to maze intersections using user inputs, searching for the color calibrated to the husky lens camera
# Calibrate Sensor Readings:
# while(True):
#     print(f"Left Sensor: {reflectance.get_left()}")
#     print(f"Right Sensor: {reflectance.get_right()}")
#     print("/n")

def drive_until_intersection(): #TODO expand this into also stopping before hitting a wall
    base_effort = 0.6
    KP = 0.6
    left_reflect  = reflectance.get_left()
    right_reflect = reflectance.get_right()
    error = left_reflect - right_reflect
    # print(f"Error: {error}, Left: {left_reflect}, Right: {right_reflect}")
    while(left_reflect < BLACK_THRESH or right_reflect < BLACK_THRESH):
        # You always want to take the difference of the sensors because the raw value isn't always consistent.
        # print(f"Error is {error}, left is {left_reflect}, right is {right_reflect}")
        drivetrain.set_effort(base_effort - error * KP, base_effort + error * KP)
        time.sleep(0.01)
        left_reflect  = reflectance.get_left()
        right_reflect = reflectance.get_right()
        error = left_reflect - right_reflect
    drivetrain.set_effort(0, 0)

def turn_right():
    drivetrain.set_effort(0.4, 0)
    time.sleep(0.7)
    while (reflectance.get_left() < BLACK_THRESH):
        time.sleep(0.01)
    drivetrain.stop()
    
def turn_left():
    drivetrain.set_effort(0, 0.4)
    time.sleep(0.7)
    while (reflectance.get_right() < BLACK_THRESH):
        time.sleep(0.01)
    drivetrain.stop()
    
def turn_around():
    drivetrain.set_effort(0.8, -0.8)
    time.sleep(1.0)
    drivetrain.stop()
    
def victory_spin():
    print("Found it!")
    drivetrain.set_effort(1, -1)
    time.sleep(10.0)
    drivetrain.stop()
    
#initialize husky lens, which is already calibrated for color we are looking for
camera = HuskyLensLibrary("I2C")
    
while (True):
    #Use user input to make choices at every intersection
    direction = input("Which way should I go? (r, l, f, b)")
    
    if direction == 'f':
        drive_until_intersection()
    elif direction == 'r':
        turn_right()
    elif direction == 'l':
        turn_left()
    elif direction == 'b':
        turn_around()
        
    #pan to look for goal (camera is seraching for specific color)
    print("Panning")
    drivetrain.set_effort(0.3, -0.3)
    timer = Timeout(3.0)
    print(time.time)
    while not timer.is_done():
        time.sleep(0.1)
        if(camera.command_request_blocks_by_id(1)):
                victory_spin()
                break
    drivetrain.stop()
    print("Starting second pan")
    time.sleep(0.5)
    drivetrain.set_effort(-0.3, 0.3)
    timer2 = Timeout(3)
    while not timer2.is_done():
        time.sleep(0.1)
        if(camera.command_request_blocks_by_id(1)):
            victory_spin()
            break  
    drivetrain.stop()  
    print("Pan complete")
    
    time.sleep(0.5)
    
    