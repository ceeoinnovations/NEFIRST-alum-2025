import qwiic_twist


print("\nInitializing Qwiic\n")
myTwist = qwiic_twist.QwiicTwist()

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
    
def throttle_relation(myTwist):
    myTwist.set_color(0, 255, 0)
    myTwist.set_connect_red(10)
    myTwist.set_connect_green(-10)
    #starts at green and can slowly transition to yellow to red.

def check_state(myTwist):
    i = 0
    if ((myTwist.get_red() == 0) and (myTwist.is_pressed())):
        i = 1
    if ((myTwist.get_red() > 0) and (myTwist.is_pressed())):
        i = 2
    return i
    #selects between states (blue and purple)
# Main Task: monitor buttons for functions
def main():
    reset_twist(myTwist)
    state_relation(myTwist)
    print("twist to select a state!")
    
    while True:
        if (check_state(myTwist) == 1):
            print("blue selected!")
		    
        if (check_state(myTwist) == 2):
            reset_twist(myTwist)
            throttle_relation(myTwist)
            print("purple selected!")
            print("throttle relation started!")
            for x in range(10):
                print("speed: ", myTwist.get_green()/2.55)
                time.sleep(1)
            print("back to selection!")
            reset_twist(myTwist)
            state_relation(myTwist)
        time.sleep(0.1)
# Run the Main Task
main()
