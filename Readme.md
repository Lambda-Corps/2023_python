# Introduction
This repository has instructions for several different robot tutorial levels. Each example is self-contained within it's own sub directory. 

These projects are intended to be run in the WPILib Robot Simulator, not on a real robot. 

To prepare the computer, simply follow the instructions on the Robot Python website:
https://robotpy.readthedocs.io/en/stable/install/computer.html

Writing code in an Integrated Development Environment is extremely helpful, especially for new programmers.  I would also recommend that you install Visual Studio Code for your particular computer from here: https://code.visualstudio.com/download

I would also recommend you install the Python Extension for VS Code as well from here: https://marketplace.visualstudio.com/items?itemName=ms-python.python



Once you have your environment setup, you're ready to start going through the various exercises.  The recommended order is:
1. Arcade Simulator -- located in arcade_sim directory
1. Command-Based -- located in commands_sim directory
1.
1.

Each of the exercises all contain a Readme.md file in their own directory that include the step by step directions to complete successfully.

# Next Steps
## Python Introduction
Once the instructions above have been installed, familiarize yourself with the basics of the Python Programming Language.  The Robot Python website documentation has a nicely formatted primer on programming in Python: https://robotpy.readthedocs.io/en/stable/guide/python.html

Some of the most important parts to understand are:
* Variables -- Variables are labels that get used to store information. A variable is **assigned** a value, and when you want to use that later on you reference it by name.  A variable can be of any type, it can be a number, a string, an object.  Only important to realize that variables should be given a name that tells you (and the other programmers around you) what that thing does.  For example, if you had a variable that represented a name of a person, the variable name could be something like _persons_name_.

* Comments -- This is a way to inject context and explanation of things into the program for a human to read, but don't affect _how_ the robot operates

* Indentation -- Python is a programming language that uses indentation for structure. Meaning, the indentation has to match so the code executes properly.

* Conditional Control Flow -- This is one of the most important aspects to understanding code.  Basically, you need to logically tell the program how to behave.  If this condition, then do this action; or If this condition isn't true, then do this; and so on.  Here's an example of an If/Else If/Else block.  Meaning, two conditions will be checked, and if neither are met, the code will take the default path.
```python
if number < 0:
    # The current variable is negative
    spin_motors_backward()
elif number > 0: 
    # The current variable is positive
    spin_motors_forward()
else:
    # If a number is neither negative, nor positive, then the number must be 0. In the case of 0, turn off the motors.
    turn_motors_off()
```
In the above example, using a robot as the base. This could be a set of conditions that one would use to drive the robot. If the joystick value is negative, drive backward. If the joystick value is positive, drive forward. If the joystick value is 0, then we don't want the robot to move.


## Simulator Introduction
Once you've gotten familiar with Python, take a look and read through the basics of the WPILib simulator interface. In there, you'll be able to view some state of the robot, assign your keyboard to simulate a connected joystick to control the robot, among other things: https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/simulation-gui.html

Some of the important parts to note in the Simulator introduction are the components of the GUI.  You will not necessarily understand what each of the functions are of the various things, but you should know what they are.  The most fundamental things you'll need to know are:
* Joysticks -- This is where you will use either the keyboard, or if you've connected a USB controller to the computer you can use it. You'll need to tell the simulator which joystick you're going to be using.
* Robot State -- This is how you are going to tell the robot to do certain things. In the beginning, the first thing that you're going to learn


## Robot Introduction
The most important piece of information you need to understand about the robot how how the sequence of operations work. The robot we use fundamentally works on a timing loop. The timing loop attempts to execute 50 times a second (or every 20 milliseconds). In software, the robot is typically divided into subsystems, each of which have their own periodic methods as well. So, a Robot is made up of a collection of subsystems. A subsystem is made up of the components that make the robot do something (like motors, solenoids, sensors, etc). Subsystems are generally told what to do via Commands. 

The Scheduler is the software that controls which commands are being run, and when the subsystem's periodic methods get called, etc.  The most imoprtant components to understand are: Subsystems, Commands, and the Scheduler.  Understanding those basic components is enough to write software to fully control the robot.

### Subsystems
The Subsystem is a collection of software components and robot hardware that operate together as a cohesive unit to perform an action.  Subsystems will vary from robot to robot, but basically every robot out there is going to need to drive.  So at a minimum, each robot will have a DriveTrain subsystem. The DriveTrain would be made up of motor controllers (the thing that actually tells the motors to spin), and any other sensors that may help driving (like a gyro, encoders, range finders, etc).

### Commands 
Commands represent actions that the robot can take. Commands only execute when the scheduler allows them to run. They will run forever, unless they are interrupted by another command, or the command ends through a natural condition. Examples of commands that are used by a robot may be DriveWithJoysticks, or Drive10Feet. In the case of a command named Drive10Feet, it should be obvious that the end condition of that command would be once we've measured the robot has traveled 10 feet it should stop.  DriveWithJoysticks however may be a command that you don't ever want to end necessarily, as we never want to lose control of the robot.  If our robot had these two commands, they would clearly be in conflict with each other. You wouldn't have the robot driving 10 feet autonomously (Drive10Feet command) and also allow the operator to use joysticks to control the bot.  

The Scheduler is the robot software that would manage the conflict between the DriveWithJoysticks and Drive10Feet.

### Scheduler
The Scheduler, also known as the CommandScheduler, is the software responsible for running the commands on the robot. The CommandScheduler operates in a loop, typically every 20 milliseconds, wherein it scans all the possible triggers (like button presses on a Joystick), and when a trigger is activated, it schedules the appropriate command to run.