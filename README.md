# robt492_capstone_project_2
This repository is dedicated to the capstone project of Nazarbayev University students majoring in Robotics Engineering. The capstone topic is "Autonomous Wheelchair Navigation System Using SLAM and Vision-Based Control".

To control the robot from the control laptop, the "controller_ws" folder should be put on the PC from which you want to give commands to your robot. This PC should have Ubuntu 22.04 with ROS2 Humble.

The "JoyLocal_udp.py" file should be run on the Raspberry PI connected to the power wheelchair via CAN bus. Raspberry PI 3 is used for this project. Messages via CAN bus can be sent using github repository developed by redragonx. 

# Launch procedure:

## Step 1. 
Turn on the wheelchair.

## Step 2. 
Run "JoyLocal_udp.py" in the Terminal of the Raspberry PI. This file should be put in the same folder as the original JoyLocal files developed by **redragonx**. After you run it, the Raspberry PI should be waiting for messages from the control laptop.

## Step 3. 
Open the new terminal on the control laptop. Properly source it and build if necessary. Run "udp_twist_bridge".

## Step 4. 
Open the new terminal on the control laptop. Properly source it and build if necessary. Use the teleop command on ROS2. After launching it, keep it present in this Terminal. Now, you should be able to control the linear and angular velocities of the robot using simple predefined Twist messages. The process is similar to the control of TurtleBot.


