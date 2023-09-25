These instructions for Robot Python installation require Internet access.

These Instructions will set your local computer up to be able to write code for the robot, and test it in the simulator before deploying it to the robot.
1. Install Python for your operations system.
   * https://www.python.org/downloads/mac-osx/
1. Install Robot Python
   * pip3 install robotpy
1. Install the WPILib Commands version 2 framework
   * pip3 install -U robotpy[commands2]
1. Install the CTRE framework for Falcon/Talon motor controllers
   * pip3 install -U robotpy[ctre]
1. Install the Navx Gyro framework
   * pip3 install -U robotpy[navx]
