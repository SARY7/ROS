#!/usr/bin/env python
# The above line should always exist in a python node file.
# This command execute the file as a python script.

# import libraries
import rospy
from geometry_msgs.msg import Twist


# define a class later to control different movements of turtlesim
def turtle_circle(linear_vel, angular_vel):

    rospy.init_node('turtle_fig8', anonymous=True)
    vel_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel_cmd = Twist()
    vel_cmd.linear.x = linear_vel
    vel_cmd.angular.z = angular_vel
    
    while not rospy.is_shutdown():
        vel_publisher.publish(vel_cmd)
        # change = input("Do you want to change the velocity? press 'y':")
        rate.sleep()



def get_input():

    print("input desired values for speed:")
    while True:
        try:
            linear_vel = float(input("input a linear velocity between [-3,3]:"))
            while int(linear_vel) not in range(-3, 3):
                print("the input is not in [1,3] interval")
                linear_vel = input("input a linear velocity between [-3,3]:")
            break
        except:
            print("the input should be an int. try a new input.")

    while True:
        try:
            angular_vel = float(input("input a angular velocity between [-6,6]:"))
            while int(angular_vel) not in range(-6, 6):
                print("the input is incorrect. try new input")
                angular_vel = input("input a angular velocity between [-6,6]:")
            break
        except:
            print("the input should be an int. try a new input.")

    return linear_vel, angular_vel


    # while True:
        # while not 2 <= linear_vel <= 6:
            # print("the input is incorrect. try new input")
            # linear_vel = input("input a linear velocity between [2,6]:")

        # angular_vel = int(input("input an angular velocity between [1,3]:"))
        # while not 1 <= angular_vel <= 3:
        #     print("the input is incorrect. try new input")
        #     angular_vel = input("input an angular velocity between [1,3]:")
        # break



    # rospy.loginfo("Press CTRL+c to stop moving the Turtle")
    # rospy.on_shutdown(self.shutdown)
    # vel_cmd.linear.x = 1
    # vel_cmd.linear.y = 0
    # vel_cmd.linear.z = 0
    # vel_cmd.angular.x = 0
    # vel_cmd.angular.y = 0
    # vel_cmd.angular.z = 1


if __name__ == '__main__':
    
    try:
            lin, ang = get_input()
            turtle_circle(lin, ang)

    except rospy.ROSInterruptException:
        pass
