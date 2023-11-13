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

## Command Composition
There are two ways to define comamnds to be used by **Subsystems**: In-line, or class definition.  Defining Commands inline means that in the ***Subsystem*** file, you'll make a function that returns a CommandBase object. Defining commands in a class file means that you'll create a class definition with all the appropriate lifecycle methods.

Before you start working on the lesson, [read through BoVLB's FRC command tips](https://bovlb.github.io/frc-tips/commands). That site shows you all the lifecycle methods, explains how the ***Scheduler*** works, as well as more complex topics like ***Command Groups***.

### Class file definitions
To define your command class, you will need follow the following steps:
* Create a new file called ***drivetrain_default.py***
* Define the class by giving it a name, and inheriting from the **CommandBase** class.
* Implement the constructor, ensuring that you add the **Subsystem** requirements for the scheduler.
* Define and implement the lifecycle methods: initialize, execute, isFinished, and end.
* Assign the default command 

For the exercise, we're going to define a command to be assigned as the ***Default Command*** for the drivetrain. This command is going to take input from the controller joysticks, and apply that to the motor from -100% to 100% (e.g. -1.0 to 1.0). Because this is the default command, we don't want it to ever end, we want it to be running at all times when ***no other commands are scheduled to run***.

1. Create the new file ***drivetrain_default.py*** either by right-clicking on solution explorer and choosing "New File" or click File->New File and in the window that appears at the top choose "Python File".
1. At the top of the file, import the two WPILib classes that we're going to use: *CommandBase* and *CommandXboxController*, as well as the DriveTrain class
    ```python
    from commands2 import CommandBase
    from commands2.button import CommandXboxController

    from drivetrain import DriveTrain
    ```
1. Now define the class we're creating
    ```python
    from commands2 import CommandBase
    from commands2.button import CommandXboxController

    from drivetrain import DriveTrain

    class DefaultDrivetrainCommand(CommandBase):
    ```
1. Next define the constructor method that will initialize the instance of the DefaultDriveTrain command.
    ```python
    from commands2 import CommandBase
    from commands2.button import CommandXboxController

    from drivetrain import DriveTrain

    class DefaultDrivetrainCommand(CommandBase):
        def __init__(self, dt: DriveTrain, driver_controller: CommandXboxController):
            # To make sure our child class is fully intitialized, we make sure to call the 
            # parent class constructor first.  Then we initialize our own object to be used 
            # later on.
            super().__init__()

            # We received a Drivetrain and a CommandXboxController as arguments to the constructor
            # so we want to make sure we store those objects as our own for future use.
            self._dt = dt
            self._driver_controller = driver_controller

            # Tell the scheduler that this command requires exclusive access to the Drivetrain
            # subsystem that was passed in
            self.addRequirements(self._dt)
    ```
1. Finish the class by implementing all the lifecycle methods the **Scheduler** needs to call to make our command function on the robot.
    ```python
    from commands2 import CommandBase
    from commands2.button import CommandXboxComtroller

    from drivetrain import DriveTrain

    class DefaultDrivetrainCommand(CommandBase):
        def __init__(self, dt: DriveTrain, driver_controller: CommandXboxController):
            # To make sure our child class is fully intitialized, we make sure to call the 
            # parent class constructor first.  Then we initialize our own object to be used 
            # later on.
            super().__init__()

            # We received a Drivetrain and a CommandXboxController as arguments to the constructor
            # so we want to make sure we store those objects as our own for future use.
            self._dt = dt
            self._driver_controller = driver_controller

            # Tell the scheduler that this command requires exclusive access to the Drivetrain
            # subsystem that was passed in
            self.addRequirements(self._dt)

        
        def initialize(self) -> None:
            # There isn't anything we need to do to when this command gets scheduled.
            # This command will only respond to the joysticks and set the motors accordingly
            pass # Python way of doing 'nothing'
    

        def execute(self) -> None:
            # Collect the joystick inputs and apply them to the motors.  Motors are counter-clockwise positive
            # so invert the joystick values to make sure that left goes left, right goes right.
            forward_speed = -self._driver_controller.getRawAxis(1)
            turn_speed = -self._driver_controller.getRawAxis(0)

            # Tell the Drivetrain to drive the motors
            self._dt.driveManually(forward_speed, turn_speed)
        

        def isFinished(self) -> bool:
            # We don't want this command to end, so we'll always return False when the 
            # scheduler asks us if we're done
            return False
        

        def end(self, interrupted: bool) -> None:
            # If for some reason we end, at least stop the motors from driving the robot
            self._dt.driveManually(0,0)
    ```
1. Save the file, make sure the file is named ***default_drivetrain.py***.

1. Open the ***robot.py*** file by clicking on it in the Solution Explorer on the left-hand side.

1. Import the newly created class in the top of the file by adding the line
    ```python
    from default_drivetrain import DefaultDrivetrainCommand
    ```

1. Locate the following lines of code (near line 28):
    ```python
        # Setup the default commands for subsystems
        self._drivetrain.setDefaultCommand(
            # A split-stick arcade command, with forward/backward controlled by the left
            # hand, and turning controlled by the right.
            RunCommand(
                lambda: self._drivetrain.driveManually(
                    self._driver_controller.getRawAxis(0),
                    self._driver_controller.getRawAxis(1),
                ),
                self._drivetrain,
            )
        )
    ```
1. Replace those lines with the following code that will use our new class
    ```python
        # Setup the default commands for subsystems
        self._drivetrain.setDefaultCommand(DefaultDrivetrainCommand(self._drivetrain, self._driver_controller))
    ```

## Timed Driving Commands
In this section we'll learn both ways of constructing simple commands through inline methods or class definitions. To start, we'll make a class definition of a new command who's purpose will be to drive for an amount of timme and then stop the robot from moving.  To do this we'll perform the following steps:
* Create a new class called DriveForSeconds
* Bind that newly defined command to a trigger such that when a button is pressed the robot will drive in a certain direction for a specified amount of time

1. Create the new file ***drivetrain_commands.py*** either by right-clicking on solution explorer and choosing "New File" or click File->New File and in the window that appears at the top choose "Python File".

1. Now put in the import statements for code we need to use for this **Command** and create the class definition
    ```python
    from commands2 import CommandBase
    from wpilib import Timer
    from drivetrain import DriveTrain

    class DriveForSeconds(CommandBase):
    ```
1. Implement the constructor for our **Command**.  This constructor needs to receive a ***DriveTrain*** object, the forward speed (movement on the x axis) and the turning speed (the rotation around the Z axis). Make sure your constructor, calls the parent constructor to ensure the system is stable. Then assign the values passed into the constructor for later use. Next, instantiate a Timer object to track how long we'll be running. Lastly, inform the scheduler that we need exclusive access to the ***DriveTrain*** while we're running.
    ```python
    from commands2 import CommandBase
    from wpilib import Timer
    from drivetrain import DriveTrain

    class DriveForSeconds(CommandBase):
        def __init__(self, dt: DriveTrain,runtime: float, forward_speed: float, turn_speed: float):
            super().__init__()
            
            # Store our runtime and speed to be used for each time the command runs
            self._runtime = runtime
            self._forward_speed = forward_speed
            self._turn_speed = turn_speed
            self._dt = dt

            # Instantiate a timer object to limit our runtime
            self._timer = Timer()
            self._timer.reset()

            # Tell the scheduler that this command requires exclusive access to the Drivetrain
            # subsystem that was passed in to the constructor
            self.addRequirements(self._dt)
    ```
1. To finish defining the class, implement the **Command** lifecycle methods. In the ***initialize()*** method, reset and start the timer counting. In the ***execute()*** method, set the robot to drive according to the stored forward/turn speeds. In the ***end()*** method, turn off the motors.
    ```python
        def initialize(self) -> None:
        # When we schedule the command to run, make sure the timer gets reset to 0 and then start it to initiate timekeeping
        self._timer.reset()
        self._timer.start()
    

        def execute(self) -> None:
            self._dt.driveManually(self._forward_speed, self._turn_speed)
        

        def isFinished(self) -> bool:
            return self._timer.hasElapsed(self._runtime)
        

        def end(self, interrupted: bool) -> None:
            if interrupted:
                print("Command Interrupted") 
            
            # When we've completed our run, no matter the reason, stop the motors.
            self._dt.driveManually(0,0)
    ```

1. With the ***DriveForSeconds*** comman now defined, open the ***robot.py*** file to actually use it.  At the top of the ***robot.py*** file, import the ***DriveForSeconds*** class
    ```python
    from drivetrain_commands import DriveForSeconds
    ```
1. Find the bottom of the ***robotInit()*** method to make the button bindings and add the following bindings:
    ```python
        # Setup the button bindings
        # When the driver presses the A() button, drive the robot forward in a straight line at half speed for 3 seconds.
        self._driver_controller.A().onTrue(DriveForSeconds(self._drivetrain, 3, .5, 0))
        # When the driver pressexs the B() button, drive the robot backward in a straight line at half speed for 3 seconds.
        self._driver_controller.B().onTrue(DriveForSeconds(self._drivetrain, 3, -.5, 0))
    ```

Once completed you should have a robot.py file with a ***robotInit()*** method that looks like the below file and is able to be run in the simulator by typing
```
python3 robot.py sim
```

```python
def robotInit(self) -> None:
        '''
        This method must eventually exit in order to ever have the robot
        code light turn green in DriverStation. So, this will create an 
        instance of the Robot that contains all the subsystems,
        button bindings, and operator interface pieces like driver 
        dashboards
        '''
        self._gyro = navx.AHRS.create_spi()

        # Setup the operator interface (typically CommandXboxController)
        self._driver_controller = CommandXboxController(0)

        # Instantiate any subystems
        self._drivetrain = drivetrain.DriveTrain()


        # Setup the default commands for subsystems
        self._drivetrain.setDefaultCommand(DefaultDrivetrainCommand(self._drivetrain, self._driver_controller))
        self._auto_command = None

        # Setup the button bindings
        # When the driver presses the A() button, drive the robot forward in a straight line at half speed for 3 seconds.
        self._driver_controller.A().onTrue(DriveForSeconds(self._drivetrain, 3, .5, 0))
        # When the driver pressexs the B() button, drive the robot backward in a straight line at half speed for 3 seconds.
        self._driver_controller.B().onTrue(DriveForSeconds(self._drivetrain, 3, -.5, 0))
```