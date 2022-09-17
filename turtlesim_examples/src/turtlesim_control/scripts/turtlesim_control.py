#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

# define these variables as global variables, so we can use and chanege them 
# everywhere throughout the code.
x = 0
y= 0 
yaw = 0

def get_input():
    print("input desired values for speed: ")

    while True:
        try:
            x_vel = float(input("enter a velocity in range [-5,5] in x direction: "))
            direction = int(input("type a direction, forward=1 or backward=0 : "))
            goal_distance = float(input("input a goal distance: "))
            if int(x_vel) in range (-5,5) :
                print("the velocity is not in range [-5,5], try again: ")            
                break
        except:
            print("the velocity value is incorrect, try again: ")

    return x_vel, direction, goal_distance



def position_callback(pose_message):
    global x 
    global y,  yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def move_turtle(velocity, direction, goal_distance):
    velocity_message = Twist()
    global x,y
    x_initial = x
    y_initial = y

    if direction == 1:
        velocity_message.linear.x = abs(velocity)
    else:
        velocity_message.linear.x = -abs(velocity)

    distance_moved = 0.0
    rate = rospy.Rate(10)
    velocity_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(velocity_topic, Twist, queue_size=10)

    while True:
        rospy.loginfo("turtlesim mmoves forward")
        velocity_publisher.publish(velocity_message)
        rate.sleep()

        distance_moved = distance_moved + abs(0.5 * math.sqrt(((x - x_initial)**2) + (y - y_initial)**2))

        if not (distance_moved < goal_distance):
            rospy.loginfo("Goal distance rechead")
            break
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        velocity_topic = '/turtle1/cmd_vel'
        # the message type of the velocity topic is Twist
        velocity_publisher = rospy.Publisher(velocity_topic, Twist, queue_size = 1)

        position_topic = '/turtle1/pose'
        # read data from pose topic with the message type of Pose, and each time, execute
        # the position_callback function 
        pose_subscriber = rospy.Subscriber(position_topic, Pose, position_callback)

        x_vel, direction, goal_distance = get_input()
        move_turtle(x_vel, direction, goal_distance)

    except rospy.ROSInterruptException :
        pass