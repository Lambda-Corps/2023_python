#!/usr/bin/env python3
import wpilib
import commands2
from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
from commands2.button import CommandXboxController
import commands2.button

from subsystems.drivetrain import DriveTrain
from subsystems.ledsubsystem import LEDSubsystem
from commands.turntoangle import TurnToAngle
from commands.autonomouscommand import AutonomousCommand
from commands.driveforwardxseconds import DriveForwardXSeconds
# from robotcontainer import RobotContainer

from typing import Tuple, List


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
###################################
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """


        # self._gyro = navx.AHRS.create_spi()

        # Setup the operator interface (typically CommandXboxController)
        self.drivercontroller = CommandXboxController(0)

        # Instantiate any subystems
        self.drivetrain = DriveTrain()
        self.led = LEDSubsystem()


        # Setup the default commands for subsystems
        if wpilib.RobotBase.isReal():
            self.drivetrain.setDefaultCommand(
                # A split-stick arcade command, with forward/backward controlled by the left
                # hand, and turning controlled by the right.
                RunCommand(
                    lambda: self.drivetrain.driveManually(
                        self.drivercontroller.getRawAxis(3),  # Forward  (Was 0)
                        self.drivercontroller.getRawAxis(2),  # Turn   (was 1)
                    ),
                    self.drivetrain,
                )
            )
        else:
            self.drivetrain.setDefaultCommand(
                # A split-stick arcade command, with forward/backward controlled by the left
                # hand, and turning controlled by the right.
                RunCommand(
                    lambda: self.drivetrain.driveManually(
                        -self.drivercontroller.getRawAxis(1),  # Forward  (Was 0)
                        -self.drivercontroller.getRawAxis(0),  # Turn   (was 1)
                    ),
                    self.drivetrain,
                )
            )

        self._auto_command = None

        # Keep track of the linear position of the simulation
        self._left_position_in_feet = 0
        self._right_position_in_feet = 0

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        # self.container = RobotContainer()

        self.configureButtonBindings()

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """


        # Turn to 90 degrees when the 'X' button is pressed, with a 5 second timeout
        commands2.button.JoystickButton(
            # self.driverController, wpilib.PS4Controller.Button.kCross
            self.drivercontroller, 1).onTrue(TurnToAngle(90, self.drivetrain).withTimeout(5))

        self.drivercontroller.B().onTrue(DriveForwardXSeconds(self.drivetrain,2,1))

    def getAutonomousCommand(self) -> Command:
        return AutonomousCommand (self.drivetrain,self.led)

# #######################################################
# # Items to support the simulation    
    def getSpeeds(self) -> List[float]:
        return [0.0, 0.0] if self.drivetrain is None else self.drivetrain.getSpeeds()

    def update_sensor_odometry(self, left_pos: float, left_vel: float, right_pos: float, right_vel: float) -> None:
        self.drivetrain.update_dt_odometry(left_pos, left_vel, right_pos, right_vel)

########################################################
# Standard items to be placed in common robot.py file


    def teleopInit(self) -> None:
        if self._auto_command is not None:
            self._auto_command.cancel()

    def testInit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
    
    def autonomousInit(self) -> None:
        self._auto_command = self.getAutonomousCommand()

        if( self._auto_command is not None):
            self._auto_command.schedule()

    def disabledPeriodic(self) -> None:
        pass


    def autonomousPeriodic(self) -> None:
        pass


    def testPeriodic(self) -> None:
        pass


    def teleopPeriodic(self) -> None:
        return super().teleopPeriodic()
    
if __name__ == "__main__":
    wpilib.run(MyRobot)