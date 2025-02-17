from XRPLib.defaults import *
from XRPLib.pid import PID
from XRPLib.rangefinder import Rangefinder
from XRPLib.differential_drive import DifferentialDrive
from machine import Timer
import time

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver

class LowPassFilter:
    def __init__(self, alpha, init_value = 0):
        self.alpha = alpha
        self.prev_val = 0
    
    def new_measurement(self, val):
        old_val = self.prev_val
        self.prev_val = val
        return self.alpha * val + (1-self.alpha) * old_val

def distance_provider():
    lpf = LowPassFilter(alpha = 0.8, init_value = dist_sensor.distance())
    def get_distance():
        return lpf.new_measurement(dist_sensor.distance())
    return get_distance
        
        
controller = PID(0.055, 0, 0.0035, min_output = -1, max_output = 1, tolerance=0.01, tolerance_count=10)
dist_sensor = Rangefinder.get_default_rangefinder()
differentialDrive = DifferentialDrive.get_default_differential_drive()

# in cm

TARGETS = [10, 25, 50, 75]
i = 0
cycles = 0
frequency = 25
time_between_phases = 5

cycle_phase = frequency * time_between_phases

TARGET_DISTANCE = TARGETS[0]
get_distance = distance_provider()

def update_robot():
    # error = get_distance() - TARGETS[i]
    error = get_distance() - TARGETS[2]
    ping = controller.update(error)
    #print(dist_sensor.distance())
    differentialDrive.set_effort(ping, ping)
    
main_timer = Timer(-1)

while True:
    update_robot()
    time.sleep(1/frequency)
    cycles += 1
    if cycles > cycle_phase:
        cycles = 0
        i = (i + 1) % len(TARGETS)
        print(f"New target: {TARGETS[i]}")
# main_timer.init(mode=Timer.PERIODIC, freq=1000, callback = lambda t: update_robot())


    
    
    
