#!/usr/bin/env python3
# The above line should always exist in a python node file.
# This command execute the file as a python script.

# import libraries
import rospy
from geometry_msgs.msg import Twist


# define a class later to control different movements of turtlesim
def turtle_circle(linear_vel, angular_vel):

    rospy.init_node('turtle_circle', anonymous=True)
    vel_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel_cmd = Twist()
    vel_cmd.linear.x = linear_vel
    vel_cmd.angular.z = angular_vel
    
    while not rospy.is_shutdown():
        vel_publisher.publish(vel_cmd)
        rate.sleep()


def get_input():
    print("input desired values for speed:")
    
    # getting input from user and processing with if statement
    while True:
        try:
            linear_vel = float(input("input a linear velocity between [-3,3]:"))
            if int(linear_vel) in range(-3, 3):
                # print("the input is not in [-3,3] interval")
                break
            else:
                print("the input is incorrect.try again.")
        except:
            print("the input should be a float. try a new input.")

    # getting input form user and processing with while loop
    while True:
        try:
            angular_vel = float(input("input a angular velocity between [-6,6]:"))
            while int(angular_vel) not in range(-6, 6):
                print("the input is incorrect. try new input")
                angular_vel = input("input a angular velocity between [-6,6]:")
            break
        except:
            print("the input should be a float. try a new input.")

    return linear_vel, angular_vel


if __name__ == '__main__':
    
    try:
            lin, ang = get_input()
            turtle_circle(lin, ang)

    except rospy.ROSInterruptException:
        pass
