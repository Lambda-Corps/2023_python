# Introduction
This section of the Python tutorial will provide some basic interactions in the Command-Based system. 

Inside of this code you will see:
* There is a fully-functional robot code base that can be run in the simulator
* This codebase is designed as a Command-Based paradigm
* There is a ***Subsystem*** setup that will drive an LED Strip
* There are ***Commands*** that bind to certain triggers.
* There is a ***CommandXboxController*** that is used to bind a command to the ***A button*** as a trigger.

## Robot Execution Explanation
In the ***Command-Based*** robot, there are two different ways to have the robot perform the actions we want to control: Periodic Methods and Triggers.  

Periodic methods, are functions that are called in our robot code by the ***Robot Scheduler***. The Scheduler runs on a loop running at 50 Hertz, or 50 times per second. If you were to divide 1 second into 50 smaller chunks (1/50) you would get the result of .02.  That means that the robot scheduler loop runs every .02 seconds, or every 20 milliseconds (a millisecond is 1/1000 of a second). No matter what else is happening on the robot, meaning even if other Commands are running, the periodic methods are called. Our Robot has several layers of periodic functions: 
* Subsystem Periodic - This is a periodic method called in each subsystem.  The name of the method is not *SubsystemPeriodic*, rather the name of the function is ***periodic()***. In our code if our Subystem was named led_subsystem, then calling the periodic method would look like ***led_subsystem.periodic()***.
* Mode Specific Periodic - This is a periodic method called during a specific mode of operation. Our robot will generally have three modes of operation: ***Disabled*** (no robot movement), ***Teleop*** (human controlled) or ***Autonomous*** (no human controls).  The ***robot.py*** source file *may* define each of the respective functions, but doesn't have to, so you may or may not see a ***disabledPeriodic***, ***teleopPeriodic***, or ***autonomousPeriodic*** method.

Triggers are conditions that are either True, or False in the robot.  The easiest example to understand is a button pressed.  A button is either pressed, or it isn't. So if the button is pressed, we can say the trigger is True and if it is not pressed, it is False.  There is also a time in the middle where the trigger is true, but no *new events* have happened. The below diagram visualizes what the Trigger of a button press looks like:
```
           OnTrue                       OnFalse
             ______________________________
             |                             |
             |                             |
             |                             |
             |                             |
             |                             |
             |<------   WhileTrue   ------>|
             |        (button held)        |
             |                             |
             |                             |
             |                             |
_____________|                             |________________
             ^                             ^
             |                             |
             |                             |
        Button Pressed              Button Released          
```
If the diagram above is viewed with a wide enough view, the lines of the events on the button and their respective Trigger Events should all line up nicely.  Starting from the bottom of the diagram, there are three different events that happen.  The Button on a controller is pressed down, it is held down for some amount of time, and ultimately the button is released.  Imagine looking down at a controller (like an Xbox controller) and seeing the green A button.  We'll use that as a reference.  When I press the A Button on the controller, the Trigger signal is *raised*, and the condition ***onTrue*** becomes triggered. For as long as I hold the button down the Trigger signal remains *raised*, and the condition ***whileTrue*** remains triggered, however the ***onTrue*** signal is no longer triggered. When I release the button on the controller, the Trigger signal *falls*, and the condition ***onFalse*** becomes triggered and the ***whileTrue*** trigger ends. As long as nobody else touches the button, the trigger will remain in the ***False*** state an nothing will happen on the robot.