from XRPLib.defaults import DifferentialDrive, IMU
import math, time

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver
# Write your code Here

class MotionProfile:
    def __init__(self, target_distance, max_speed=1, max_accel=1):
        self.MAX_SPEED = max_speed
        self.MAX_ACCELERATION = max_accel
        self.current_speed = 0
        self.max_speed = 0
        self.target_distance = target_distance
        self.finished = False
        self.distance_traveled = 0
        self.t1 = 0
        self.t2 = 0
        self.tf = 0
        
        # Critical distance
        critical_distance = (self.MAX_SPEED**2)/self.MAX_ACCELERATION
        if (self.target_distance <= critical_distance):
            self.t1 = math.sqrt(abs(self.target_distance)/self.MAX_ACCELERATION)
            self.t2 = self.t1
            self.tf = 2 * self.t1
        else:
            self.t1 = self.MAX_SPEED/self.MAX_ACCELERATION
            self.t2 = (abs(self.target_distance)-self.MAX_SPEED*self.t1)/self.MAX_SPEED+self.t1;
            self.tf = self.t2+self.t1
        print(self.t1, self.t2, self.tf)
        
        
        
    def update(self, t):
        coefficient  = -1 if (self.target_distance < 0) else 1;
        v = 0;
        v_max = self.MAX_SPEED
        if t > self.tf:
            self.finished = True
            return 0
        
        if self.t1==self.t2:
            v_max = math.sqrt(abs(self.target_distance)*self.MAX_ACCELERATION); #Use kinematic without t
        if t <= self.t1:
            phase = "RAMPING UP"
            v=self.MAX_ACCELERATION*t;
        elif t <= self.t2:
            phase = "CRUISE"
            v = v_max;
        elif t <= self.tf:
            phase = "RAMPING DOWN"
            v = (v_max-self.MAX_ACCELERATION*(t-self.t2));
        print(phase, v, sep = "\t|\t")
        return v*coefficient;
        
        """
        updates the controller and returns the speed
        """
    
    def is_finished(self):
        return self.finished
        
drivetrain = DifferentialDrive.get_default_differential_drive()
imu = IMU.get_default_imu()

imu.acc_rate("1660Hz")


denom = 500
# for i in range(1,denom+1):
#     for j in range(50):
#         drivetrain.arcade(-0.5, (-0.1*(i ** 1.5/denom)))
mp = MotionProfile(-2, 0.6, 0.4)
start_time = time.ticks_ms()
initial_yaw = imu.get_yaw()
kP = 0.02


while not mp.is_finished():
    elapsed = (time.ticks_ms() - start_time) / 1000
    speed = -mp.update(elapsed)
    
    correction = -(imu.get_yaw() - initial_yaw) * kP
    drivetrain.set_effort(speed + correction, speed - correction)
