from XRPLib.board import Board
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.reflectance import Reflectance
import random
import time
import qwiic_twist

# Initialize board, drivetrain, and IMU
board = Board.get_default_board()
differentialDrive = DifferentialDrive.get_default_differential_drive()
reflectance = Reflectance.get_default_reflectance()
myTwist = qwiic_twist.QwiicTwist()


# Constants
motor_slow = 0.2
motor_medium = 0.3
motor_fast = 0.4
motor_stop = 0
num_steps_per_episode = 30
test_extra = 2
StateSpace = [-3, -2, -1, 0, 1, 2, 3, 4]
RewardSpace = [-25, -10, -2, 10, -2, -10, -25, -40]
ActionSpace = [
    [motor_slow, motor_slow], [motor_slow, motor_medium], [motor_slow, motor_fast],
    [motor_medium, motor_slow], [motor_medium, motor_medium], [motor_medium, motor_fast],
    [motor_fast, motor_slow], [motor_fast, motor_medium], [motor_fast, motor_fast],
    [motor_stop, motor_slow], [motor_slow, motor_stop],
    [motor_stop, motor_medium], [motor_medium, motor_stop],
    [motor_stop, motor_fast], [motor_fast, motor_stop]
]

# Learning parameters
gamma = 0.9
alpha = 0.1

if myTwist.connected == False:
    print("The Qwiic twist device isn't connected to the system. Please check your connection", \
	    file=sys.stderr)
	    
def reset_twist(myTwist):
    myTwist.begin()
    myTwist.set_color(0, 0, 0)
    myTwist.set_connect_red(0)
    myTwist.set_connect_blue(0)
    myTwist.set_connect_green(0)
    #LED Vals set to 0, twist relations set to none	

def state_relation(myTwist):
    myTwist.set_color(0, 0, 255)
    myTwist.set_connect_red(255)
    #seting the inital color to blue and if twisted it cycles to purple

def check_state(myTwist):
    i = 0
    if ((myTwist.get_red() == 0) and (myTwist.is_pressed())):
        i = 1
    if ((myTwist.get_red() > 0) and (myTwist.is_pressed())):
        i = 2
    return i
    #selects between states (blue and purple)

def initialize_q_table(num_states, num_actions):
    return [[0] * num_actions for _ in range(num_states)]

def get_line_state():
    left_sensor = reflectance.get_left()
    print("left sensor", left_sensor)
    right_sensor = reflectance.get_right()
    print("right sensor", right_sensor)
    current_diff = (10*(left_sensor - right_sensor))
    print ("current diff", current_diff)
    if current_diff < -4.5:
        return -3
      	#State: super far left
        
    elif current_diff < -4 and right_sensor > 0.3:
        return -2
      	#State: kinda far left
    elif current_diff < -3.5 and right_sensor > 0.2:
        return -1
      	#State: little left
    elif current_diff > 4.5:
        return 3
      	#State: super far right
    elif current_diff > 4 and right_sensor > 0.3:
        return 2
      	#State: kinda far right
    elif current_diff > 3.5 and left_sensor > 0.2:
        return 1
      	#State: litte right
      
    elif (abs(current_diff) > 0 and left_sensor > 0.5 and right_sensor > 0.5):
        return 0
      	#State: in the middle
      
    else:
        return 4
        #State: all white

def select_action(state, q_table, epsilon=0.0):
    k = random.random()
    if epsilon > k:
        return random.choice(ActionSpace)
    else:
        state_index = StateSpace.index(state)
        action_array = q_table[state_index]
        action_index = action_array.index(max(action_array))
        return ActionSpace[action_index]

def update_q(q_table, state, action, reward, next_state):
    qvalue = q_table[StateSpace.index(state)][ActionSpace.index(action)]
    new_q = (1 - alpha) * qvalue + alpha * (reward + gamma * max(q_table[StateSpace.index(next_state)]))
    q_table[StateSpace.index(state)][ActionSpace.index(action)] = new_q

def drive(action):
    right_velocity = action[0]
    left_velocity = action[1]
    differentialDrive.set_effort(left_velocity, right_velocity)

def train(q_table):
    myTwist.set_color(255, 0, 0)
    step = 0
    epsilon = 0.9
    while step < num_steps_per_episode:
        state = get_line_state()
        action = select_action(state, q_table, epsilon)
        drive(action)
        time.sleep(0.5)
        new_state = get_line_state()
        # issue
        reward = RewardSpace[StateSpace.index(new_state)]
        # issue
        update_q(q_table, state, action, reward, new_state)

        print("Train - Step:", step, "From state:", state, "To state:", new_state, "Reward:", reward)

        step += 1
        epsilon = max(0.4, epsilon - 0.008)
        left_sensor = reflectance.get_left()
        right_sensor = reflectance.get_right()
        current_diff = 10*(left_sensor - right_sensor)
        current_diff = get_line_state()
        if abs(current_diff > 8):
            print('Testing: Robot turned too much, halting sequence!')
            break

    differentialDrive.stop()

def test(q_table):
    myTwist.set_color(0, 255, 0)
    step = 0
    while step < num_steps_per_episode * test_extra:
        state = get_line_state()
        action = select_action(state, q_table, epsilon=0)
        drive(action)
        time.sleep(0.5)

        new_state = get_line_state()
        reward = RewardSpace[StateSpace.index(new_state)]

        print("Test - Step:", step, "From state:", state, "To state:", new_state, "Reward:", reward)

        step += 1

        left_sensor = reflectance.get_left()
        right_sensor = reflectance.get_right()
        current_diff = 10*(left_sensor - right_sensor)
        current_diff = get_line_state()
        if abs(current_diff > 8):
            print('Testing: Robot turned too much, halting sequence!')
            break

    differentialDrive.stop()

def main():
    reset_twist(myTwist)
    myTwist.set_color(0, 0, 255)
    print('Welcome RL Walker')
    print('- press the blue button to train')
    
    q_table = initialize_q_table(len(StateSpace), len(ActionSpace))
    episode = 0

    while True:
        while (episode < 2):
            if (check_state(myTwist) == 1):
                train(q_table)
                episode += 1
                reset_twist(myTwist)
                if (episode == 2):
                    print('- twist to blue, then press to train')
                    print('- twist to purple, then press to test')
                    state_relation(myTwist)
                else:
                    print('- click on the blue button to train')
                    myTwist.set_color(0, 0, 255)

        while (episode >= 2):
            if (check_state(myTwist) == 1):
                train(q_table)
                episode +=1
                reset_twist(myTwist)
                state_relation(myTwist)
                print('- twist to blue, then press to train')
                print('- twist to purple, then press to test')
                
            if (check_state(myTwist) == 2):
                test(q_table)
                reset_twist(myTwist)
        # Logic to choose test/train based on user input could be added here.
        # Simulate button press or condition to switch modes
        # To demonstrate, alternating between training and testing here

main()
