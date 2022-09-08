#!/usr/bin/env python3

from math import atan, cos, exp, tan
import rospy
from geometry_msgs.msg import Twist

#parameters lf, lr in yaml
#inputs Velocity, time, angle in yaml


class TurtleBot:

    def __init__(self):
        
        rospy.init_node ('bicycle_controller', anonymous=True)
    
        self.velocity_publisher = rospy.Publisher ('/turtle1/cmd_vel', Twist, queue_size=10)

        self.rate = rospy.Rate(3)

    def move(self):
       
        vel_msg = Twist()

        #inputs
        lf = rospy.get_param("/length/lf")
        lr = rospy.get_param("/length/lr")
        self.pi = 22/7
        self.angle = rospy.get_param("/inputs/angle")
        self.delta = float(self.angle*(self.pi/180))
        self.B =atan(lr * tan(self.delta)/ (lr+lf) )
        self.time = rospy.get_param("/inputs/time")
        self.V = float(rospy.get_param("/inputs/velocity"))
        omega = (self.V * cos(self.B) * tan(self.delta))/ (lr+lf)

        #velocities
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = float(omega)

        vel_msg.linear.x = self.V
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        print(vel_msg.angular.z)
        print(vel_msg.linear.x)


        while not rospy.is_shutdown():
            
            #initializing timer
            t0 = rospy.Time.now().to_sec()
            current_time = 0

            while (current_time < self.time):
                
                self.velocity_publisher.publish(vel_msg)
                
                t1 = rospy.Time.now().to_sec()
                
                current_time = (t1-t0)
                
                #decay function (bonus)
                decay = float(-current_time/ self.time)
                vel_msg.angular.z = vel_msg.angular.z * exp(decay)
                
                #print(vel_msg.angular.z)
                
                self.rate.sleep()
            
            #stopping the turtle
            vel_msg.linear.x = 0
            vel_msg.angular.z= 0
            self.velocity_publisher.publish(vel_msg)    
        
if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move()
    except rospy.ROSInterruptException:
        pass 
