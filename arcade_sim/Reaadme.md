# Introduction
This exercise aims to build a robot that can be controlled by a user with a Joystick in the WPILib simulator.  By the time a user follows all these steps they will have a python robot file that can be run with the simulator and will update the position of the robot on the simulated field.

## Pre-Requisites
For this step-by-step set of instructions to work, the user must have followed the setup steps described in the Readme.md of the root directory.  This means that the user has successfully:
* Installed Python on their host system
* Installed VS Code (or other IDE for development)
* This repository has been cloned (or copied) to the target system

# Get Started 
The first step is to verify that the system setup is functional.  In this section you will get your IDE setup and open to the right location, verify the simulator properly executes.  If successful, upon executing the python script the WPILib Simulator User Interface (Glass) will open on the host system and the terminal window in VS Code will have output that shows some debugging information.  If it fails, there will be a Python traceback error with some information about what went wrong.
1. Open VS Code
1. Click File -> Open Folder
    * Navigate to the **arcade_sim** directory on the file system and click ***Open***.
1. In the VS Code menu bar at the top of the screen click Terminal -> New Terminal
1. Run the existing robot file in the simulator by clicking inside the new terminal window that appeared at the bottom of the VS Code windows and type:
    ```
    python3 robot.py sim
    ```
1. Verify the simulator windows is up and running by observing inside the Glass UI that the FPGA Time value under the **Timing** window is counting upward.
    * In the terminal window you should see a print statement indicating that the robot program has started.
    ```
    ********** Robot program startup complete **********
    ```
1. Add the simulator field to the Glass UI by clicking on the top menu bar NetworkTables -> Smartdashboard -> Field
    * You should see a black window with a an orange rectangle representing the boundaries of the field.
    * You should also see on the bottom left a red square with a yellow triangle inside representing a robot
1. Close the simulor by clicking on the ***X*** at the top of the window.
    * In the terminal output you should see a debug print statement indicating that the robot code exited cleanly.
    ```
    15:07:58:572 INFO    : robotpy             : Robot code exited
    ```

# Exercise Steps
Now that you have successfully run the existing robot code in the simulator you are ready to make this robot actually do something interesting. Success will be measured when the robot can be simulated successfully, taking input from a driver via a Joystick and driving correctly. We are going to aim for an arcade drive on a Differential Drive (Tank Drive) robot design. A Differential Drive, or sometimes called West Coast Drive, is a robot that have two sets of wheels driven independently by two motors. One down the left side, one down the right.

The simulation is going to show the robot driving in a two-dimensional grid (like a video game does). The X Axis is going to represent "forward" pointing to the right of the screen, and the rotation of the robot will be calculated on the Z Axis. The Z Axis as you look at the simulation will mean the rotation will turn the robot from a top-down view. As an example, it will be the equivalent of having a drone flying over a field or court, and watching the robot drive from the top down.

The high-level steps that you will take to make this happen are: 
* Create the DriveTrain -- This will create all the programming necessary to make a robot drive
* Create the Operator Interface -- This will create the programming necessary to take input from a user and give it to the robot.
* Schedule the Commands that will make the robot drive -- As previously shown in the pre-requisites, the robot software is managed by a piece of software called the _Scheduler_. This step will tell the scheduler to execute the commands that will make the robot drive with user input from the joysticks.
* Add the required information to inform the simulator of where the robot is in space, and have the simulator update the robots position on the screen.

## Create the Drive Train

1. Create a new file named _drivetrain.py_ in your project directory.  There are multiple ways to do this.
    *  Right click in the Solution Explorer view on the left (where you see the other files) and click _New File_ from the context menu
    * or  Click on File -> New File 
        * From the Dialog box that opens choose *Python File* 
        * Click on File -> Save and give the file the name _drivetrain.py_
1. Create a Python class called DriveTrain -- Note for classes we capitilize the first and middle letters