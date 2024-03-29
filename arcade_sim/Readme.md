# Introduction
This exercise aims to build a robot that can be controlled by a user with a Joystick in the WPILib simulator.  By the time a user follows all these steps they will have a python robot file that can be run with the simulator and will update the position of the robot on the simulated field.

## Pre-Requisites
For this step-by-step set of instructions to work, the user must have followed the setup steps described in the Readme.md of the root directory.  This means that the user has successfully:
* Installed Python on their host system
* Installed VS Code (or other IDE for development)
* This repository has been cloned (or copied) to the target system
* The extra Python libraries have been installed -- RobotPy, Robotpy[ctre], Robotpy[navx], and Robotpy[commands2]
    * Windows - py -3 -m pip install -U robotpy[ctre,navx,commands2]
    * Mac OS - python3 -m pip isntall -U robotpy[ctre,navx,commands2]

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
1. To control the robot in the simulator, you need to assign a Keyboard to one of the ***Joysticks*** slots. Within the Glass UI, you will see a small sub-window called **System Joysticks** and one called **Joysticks**. To assign the Joystick, click on the item and drag it to Keyboard slot 0.
    * On this system where the instructions were written, in the System Joysticks window there is a line that says ***16: Keyboard 0***, yours may be different.  Click on it with the mouse, drag it to the column titled ***Joystick[0]***.
    * After successfully completing this step, if you hold down W, A, S, or D keys on the keyboard, you should see the values next to the ***Axis[0]*** and ***Axis[1]*** change between -1 and 1.  The W represents pressing an Xbox style gamepad's left thumbstick forward, the S represents pressing the left thumbstick backward. The A represents pressing the right thumbstick to the left, and the D key represents pressing the thumbstick to the right.
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
1. Create a Python class called DriveTrain -- Note for classes we capitilize the first and middle letters. Also, to be a proper robot drivetrain we need to make sure the scheduler knows how to deal with the class we're defining so we're going to import some code from WPILib to make it work. For more information on inheritance and classes, see the W3 Schools entry on [Python Classes](https://www.w3schools.com/python/python_classes.asp) and [Python Inheritance](https://www.w3schools.com/python/python_inheritance.asp).
    1. Add the import statement to the top of the new file to include _wpilib_ and from the _commands2_ package: _SubsystemBase_.
        ```python
        import wpilib
        from commands2 import SubsystemBase
        ```
    1. Next in the file define a class called ***DriveTrain*** that inherits from ***Subsystembase***
        ```python
        import wpilib
        from commands2 import SubsystemBase

        class DriveTrain(SubsystemBase):
        ```
    1. To make this class useful, we need to create a constructor to build a DriveTrain instance. The code snippet below shows the python code that both declares the class definition, and the constructor method. Each line is preceded by a code comment (words enclosed between an opening and closing set of single quotes ''') that explains some more detail.  The actual code you write does not need to include the comment text to be functional, though including it will not affect the behavior either as comments are ignored at execution time.
        ```python
        '''The following line defines a class called DriveTrain, that will inherit the data and methods from it's parent class of Subsystembase. When being used, the Scheduler will call various periodic methods that it knows about based on the fact that our DriveTrain is an instance of a Subsystem.  Methods such as periodic() will be called in the scheduler loop every 20 ms (or 50Hz, or 50 times a second)'''
        class DriveTrain(SubsystemBase):
            '''The following line defines a constructor method called __init__ that is used to create the instance of the DriveTrain class. Every class method is defined with an argument of the instance, most of the time called 'self' (referring to _this_ DriveTrain specifically). This constructor receives no other arguments to be used to customize it's behavior.  The return value of __init__ is None (or null), by virtue of having the -> None before the end of the method declaration (the ':' character) '''
            def __init__(self) -> None:
        ```
    1. Inside the construtor method, call the Subsystembase constructor to fully initialize our DriveTrain. This is done by referencing the keyword ***super*** to refer to our _Parent_ class, not us.
        ```python
        import wpilib
        from commands2 import SubsystemBase

        class DriveTrain(SubsystemBase):
            def __init__(self) -> None:
                super().__init__()
        ```

    1. Import the ***CTRE*** library code at the top of the ***drivetrain.py*** file as well as the ***wpilib.drive*** library for future use.
        ```python
        import wpilib
        import wpilib.drive
        from commands2 import SubsystemBase
        import ctre
        ```
    1. Next instantiate two different motor controllers to control the wheens on the left and right sides of the robot respectively. This code simulates two motor controllers that are plugged into the CAN bus with IDs 1 and 2..
        ```python
        import wpilib
        import wpilib.drive
        from commands2 import SubsystemBase
        import ctre

        class DriveTrain(SubsystemBase):
            def __init__(self) -> None:
                super().__init__()

                self._left_leader = ctre.WPI_TalonFX(1)
                self._right_leader = ctre.WPI_TalonFX(2)
        ```


    1. For the simulator (and the real robot to work) we need to track the kinematics of our robot.  Kinematics is a fancy word that means the study of motion, but motion without accounting for physical factors like mass, gravity, etc. In this code, we want the simulator to draw on the screen where our robot _would_ be if we applied certain inputs to it. To make this happen, we are going to declare two variables that track the left and right speeds of our Differential Drive robot. Along with tracking these variables, we are going to then define two functions that make these variables accessible to the rest of our robot structure as well. These variables have nothing to do with _making_ the robot move.  Just tracking the variables _used_ to make the robot move.
        * Import the relavant motor controller code (i.e. import ctre library) 
        * Add two instance variables called ***lastLeftSet*** and ***lastRightSet*** to track the motor set speeds inside of the *init* method.
        * Add two methods called ***getLeftSpeed*** and ***getRightSpeed*** that return a type float (a decimal number) representing the output percentage applied to the motors on each side of the robot

        ```python
        import wpilib
        import wpilib.drive
        from commands2 import SubsystemBase
        import ctre

        class DriveTrain(SubsystemBase):
            def __init__(self) -> None:
                super().__init__()

                self._left_leader = ctre.WPI_TalonFX(1)
                self._right_leader = ctre.WPI_TalonFX(2)

                self._lastLeftSet = 0.0
                self._lastRightSet = 0.0

            
            def getLeftSpeed(self) -> float:
                return self._lastLeftSet


            def getRightSpeed(self) -> float:
                return self._lastRightSet
        ```
    1. Now we need to configure the motor controllers to do what we want.  The first step is to set the configuration back to the factory default.  This ensures the controllers are configured as we run them, and we're never running older configurations on the devices.
        ```python
        import wpilib
        import wpilib.drive
        from commands2 import SubsystemBase
        import ctre

        class DriveTrain(SubsystemBase):
            def __init__(self) -> None:
                super().__init__()

                self._left_leader = ctre.WPI_TalonFX(1)
                self._right_leader = ctre.WPI_TalonFX(2)

                # Factory default the motor controllers
                self._left_leader.configFactoryDefault()
                self._right_leader.configFactoryDefault()
                # Motor are mounted opposite of each other, so one needs to run "backward" to make the robot move
                # in the direction we want.
                self._right_leader.setInverted(ctre.TalonFXInvertType.Clockwise)
                self._left_leader.setInverted(ctre.TalonFXInvertType.CounterClockwise)

                self._lastLeftSet = 0.0
                self._lastRightSet = 0.0

            
            def getLeftSpeed(self) -> float:
                return self._lastLeftSet


            def getRightSpeed(self) -> float:
                return self._lastRightSet
        ```
    
    1. Next, we'll define a method that will but used by other parts of our robot code that will take two numbers and inputs from the joysticks, and make the robot move in the given direction based on those inputs. The method will be called ***driveManually*** and take two arguments, one argument to represent the percentage of motor output in the forward and backward directions, and one argument to represent the percentage of output for the robot rotation around the Z Axis. Think of viewing the robot from above, the rotation will have the robot spin in place either clockwise or counterclockwise depending on the sign of the number put in (either positive or negative number). The arguments will be of type _float_ which means it will be a number that can b represented as a decimal. The inputs for both forward and turning directions have the range of -1.0 <-> 1.0 (-100% to 100%). This will be done by calculating the robot kinematics of an arcadeDrive set of outputs based on those inputs. This means that given the two inputs representing the forward and turning speeds, calculate the output that would be applied to the left and right sides to make that move happen.
        ```python
        import wpilib
        import wpilib.drive
        from commands2 import SubsystemBase
        import ctre

        class DriveTrain(SubsystemBase):
            def __init__(self) -> None:
                super().__init__()

                self._left_leader = ctre.WPI_TalonFX(1)
                self._right_leader = ctre.WPI_TalonFX(2)

                # Factory default the motor controllers
                self._left_leader.configFactoryDefault()
                self._right_leader.configFactoryDefault()
                # Motor are mounted opposite of each other, so one needs to run "backward" to make the robot move
                # in the direction we want.
                self._right_leader.setInverted(ctre.TalonFXInvertType.Clockwise)
                self._left_leader.setInverted(ctre.TalonFXInvertType.CounterClockwise)

                self._lastLeftSet = 0.0
                self._lastRightSet = 0.0

            
            def getLeftSpeed(self) -> float:
                return self._lastLeftSet


            def getRightSpeed(self) -> float:
                return self._lastRightSet

            
            def driveManually(self, forward: float, turn: float):
                '''Use the member variable _diffdrive to set the left and right side motors based on the inputs. The third argument being passed in true represents whether or not we should allow the robot to turn in place or not'''
                wheelSpeeds = wpilib.drive.DifferentialDrive.arcadeDriveIK(forward, turn, True)
                
                self._left_leader.set(wheelSpeeds.left)
                self._right_leader.set(wheelSpeeds.right)

                self._lastLeftSet = wheelSpeeds.left
                self._lastRightSet = wheelSpeeds.right
        ```

    With the ***Drivetrain*** fully formed now, we can move on to the next steps which are: Creating the Operator Interface and Creating the *Commands* to drive our ***Drivetrain Subsystem***.

1. To create the ***Operator Interface*** for the robot, we're going to program the bot to be controlled by a gamepad. ***Operator Interface*** is a fancy way to say how the human will control the robot. This ***Operator Interface*** will use a gampepad that resembles the button layout common to the Xbox controllers.  This means the four main buttons will be A, B, X, Y configured in a diamond formation on the right hand side of the controller.  We are going to program the robot to drive in ***ArcadeDrive*** mode, which means that the forward/back translation movement will come from the thumbstick on the left side of the controller, and the side to side turn (or Yaw) will come from the thumbstick on the right hand side.
    1. The first step in the ***Operator Interface*** will be creating the controller object to be used. To do this, open the ***robot.py*** file in VS Code.  (Click on the file on the left in the Solution Explorer and it should open up)
    1. Add the import statement to include the ***CommandXboxController*** code from the commands v2 library
        ```python
        #!/usr/bin/env python3
        import wpilib
        from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
        from commands2.button import CommandXboxController
        ```
    1. Find the ***robotInit()*** method defined in the file, should be somewhere in the range of line 8. Find the commented line that references setting up the Operator Interface, and one line below that add the contructor call for the *CommandXboxController* object and assign it to a variable named ***_driver_controller***. See the following code example on how to perform this action.
        ```python
        #!/usr/bin/env python3
        import wpilib
        from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
        from commands2.button import CommandXboxController

        class MyRobot(TimedCommandRobot):
            ''' Class that defines the totality of our Robot'''

            def robotInit(self) -> None:
                '''
                This method must eventually exit in order to ever have the robot
                code light turn green in DriverStation. So, this will create an 
                instance of the Robot that contains all the subsystems,
                button bindings, and operator interface pieces like driver 
                dashboards
                '''
                
                # Setup the operator interface (typically CommandXboxController)
                self._driver_controller = CommandXboxController(0)

                # Instantiate any subystems
        ```
    1. Create an instance of our previously created ***Drivetrain*** class. First, import the ***drivetrain.py*** file we created earlier into your ***robot.py*** file. 
        ```python
        #!/usr/bin/env python3
        import wpilib
        from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
        from commands2.button import CommandXboxController

        import drivetrain
        ```
    1. Next, call the constructor (or __init__) method for the class and assign it to a variable damed ***_drivetrain***. This all happens in the ***robotInit*** method.
        ```python
        #!/usr/bin/env python3
        import wpilib
        from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
        from commands2.button import CommandXboxController

        import drivetrain

        class MyRobot(TimedCommandRobot):
            ''' Class that defines the totality of our Robot'''

            def robotInit(self) -> None:
                '''
                This method must eventually exit in order to ever have the robot
                code light turn green in DriverStation. So, this will create an 
                instance of the Robot that contains all the subsystems,
                button bindings, and operator interface pieces like driver 
                dashboards
                '''
                
                # Setup the operator interface (typically CommandXboxController)
                self._driver_controller = CommandXboxController(0)

                # Instantiate any subystems
                self._drivetrain = drivetrain.DriveTrain()

        ```
    1. Now that we have an instantiated ***DriveTrain*** object, we're going to assign it a default command that will try to drive the robot according to the input from the thumbsticks. To do that, we're going to assign a ***DefaultCommand*** to be run on the ***DriveTrain Subsystem***.  Copy the following code and add it to your ***robotInit()*** method:
        ```python
        #!/usr/bin/env python3
        import wpilib
        from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
        from commands2.button import CommandXboxController
        import navx

        import drivetrain
        class MyRobot(TimedCommandRobot):
        ''' Class that defines the totality of our Robot'''

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
                self._drivetrain.setDefaultCommand(
                    # A split-stick arcade command, with forward/backward controlled by the left
                    # hand, and turning controlled by the right.
                    RunCommand(
                        lambda: self._drivetrain.driveManually(
                            self._driver_controller.getRawAxis(0),
                            self._driver_controller.getRawAxis(1),
                        ),
                        [self._drivetrain],
                    )
                )
        ```

## Testing the Code
With the code now complete, you should be able to simulate running the code on the system and control the robot with the keyboard. To perform these steps, you'll simulate the robot code, enable the teleop control of the robot, and use the keyboard to control the robot driving.
1. Simulate the robot code for testing.
    * Mac OS 
        ```
        python3 robot.py sim
        ```
    * Windows
        ```
        py -3 robot.py sim
        ```
    * You should see the Glass UI open up as you saw before, and in your terminal output something related to the Robot Program successfully starting up.  If there are any error messages, read the error to find both the error type and which line in one of your files caused the error.
1. Verify the keyboard input has been assigned properly to the ***Joystick[0]*** slot in the **Joysticks** window.  When you push the W, A, S, or D keys, you should see axis values changing.
1. Enable the robot in ***Teleoperated*** mode. This will enable the robot to move around the 2-dimensional field that we setup in the earlier steps.
    * To enable the robot, click on the word ***Teleoperated*** in the **Robot State** window in the Glass UI.
1. Once enabled, use the W, A, S, and D keys on the keyboard to drive the robot around the field.  
    * W - Move the robot forward (to the right on the screen)
    * S - Move the robot backward (to the left of the screen)
    * A - Move the robot left (upwards of the screen)
    * D - Move the robot right (downwards of the screen)
    