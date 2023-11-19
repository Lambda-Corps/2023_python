import wpilib
from wpilib.interfaces import GenericHID
from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
from commands2.button import CommandXboxController, JoystickButton

import commands2
import commands2.button

import navx
import constants
from subsystems.drivetrain import DriveTrain
from subsystems.ledsubsystem import LEDSubsystem
from commands.turntoangle import TurnToAngle
from commands.autonomouscommand import AutonomousCommand


from typing import List

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The driver's controller
        # self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        # self.drivercontroller = wpilib.Joystick(constants.kDriverControllerPort)

        # The robot's subsystems
        # self.led = LEDSubsystem()
        # self.drive = DriveTrain()
        
        self.configureButtonBindings()

        # # Setup the default commands for subsystems
        # self.drive.setDefaultCommand(
        #     # A split-stick arcade command, with forward/backward controlled by the left
        #     # hand, and turning controlled by the right.
        #     RunCommand(
        #         lambda: self.drive.driveManually(
        #             self.drivercontroller.getRawAxis(0),
        #             self.drivercontroller.getRawAxis(1),
        #         ),
        #         self.drive,
        #     )
        # )

# #######################################################
# # Items to support the simulation    
#     # def getSpeeds(self) -> List[float]:
#     #     return [0.0, 0.0] if self.drive is None else self.drive.getSpeeds()

#     def update_sensor_odometry(self, left_pos: float, left_vel: float, right_pos: float, right_vel: float) -> None:
#         self.drive.update_dt_odometry(left_pos, left_vel, right_pos, right_vel)


    # def configureButtonBindings(self):
    #     """
    #     Use this method to define your button->command mappings. Buttons can be created by
    #     instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
    #     and then passing it to a JoystickButton.
    #     """

    #     ## Pulled from Gryo
    #     # Turn to 90 degrees when the 'X' button is pressed, with a 5 second timeout
    #     commands2.button.JoystickButton(
    #         # self.driverController, wpilib.PS4Controller.Button.kCross
    #         self.drivercontroller, 4).onTrue(TurnToAngle(90, self.drive).withTimeout(5))

        # # Turn to -90 degrees with a profile when the Circle button is pressed, with a 5 second timeout
        # commands2.button.JoystickButton(
        #     # self.driverController, wpilib.PS4Controller.Button.kCircle
        #     self.driverController, 5).onTrue(TurnToAngleProfiled( -90, self.drive).withTimeout(5)
        # )

    def getAutonomousCommand(self) -> commands2.Command:
        return AutonomousCommand (self.drive)
    
    
