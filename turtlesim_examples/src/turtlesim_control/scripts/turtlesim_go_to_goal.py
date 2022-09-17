#!/usr/bin/env python3
#!/usr/bin/env python3
# ^^^ its called shebang constructs 


import rospy
from geometry_msgs.msg import Twist
from math import pow, atan2, sqrt
from turtlesim.msg import Pose

class turtlesim_go_to_goal:

    def __init__(self):
        
        rospy.init_node('turtlesim_go_to_goal', anonymous=True)

        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist , queue_size = 10 )
        self.pos_subscriber = rospy.Subscriber('/turtle1/pose', Pose , self.position_callback )
        
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    
    def position_callback(self, pose_data):

        self.pose = pose_data
        self.pose.x = round(self.pose.x , 4)
        self.pose.y = round(self.pose.y , 4)


    
    def calculate_distance(self, goal_pose):
        
        euclidean_distance = sqrt(pow((goal_pose.x - self.pose.x), 4) + 
                                  pow((goal_pose.y - self.pose.y), 4))
        return euclidean_distance

    
    def linear_velocity(self, goal_pose, constant = 1.5): 
        
        linear_vel = constant * self.calculate_distance(goal_pose) 
        return linear_vel



    def steering_angle(self, goal_pose):
        
        tangent_line = atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) 
        return tangent_line


    def angular_velocity(self, goal_pose, constant = 6):
        
        angular_vel = constant * (self.steering_angle(goal_pose) - self.pose.theta)
        return angular_vel

    def go_to_goal(self):
        
        goal_pose = Pose()
        goal_pose.x = float(input("set goal x position: "))
        goal_pose.y = float(input("set goal y position: "))
        goal_tolerance = input("set goal tolerance: ")

        velocity_msg = Twist()

        while self.calculate_distance(goal_pose) >= goal_tolerance:

            # the turtlesim is considered to have non-holonomic kinematics, so 
            # it can only move in the x direction or rotate about z axis. 
            velocity_msg.linear.x = self.linear_velocity(goal_pose)
            velocity_msg.angular.z = self.angular_velocity(goal_pose)
            
            self.velocity_publisher.publish(velocity_msg)
            self.rate.sleep()

        # stop the robot when it reached the destination
        velocity_msg.linear.x = 0
        velocity_msg.angular.z = 0

        self.velocity_publisher.publish(velocity_msg)

            # to stop the turtlesim when user pressed ctrl + c
        rospy.spin()
    

if __name__ == '__main__' :
    try:
        turtlesim = turtlesim_go_to_goal()
        turtlesim.go_to_goal()

    except rospy.ROSInterruptException:
        pass


