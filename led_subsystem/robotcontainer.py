import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button
import constants
from commands.defaultCommand import DefaultCommand
from commands.setLEDgreen import setLEDgreen
from commands.autononmousCommand import autoCommand

from subsystems.LEDsubsystem import LEDSubsystem

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The driver's controller
        self.driverController = commands2.button.CommandXboxController(constants.kDriverControllerPort)
        # The robot's subsystems
        self.led = LEDSubsystem()

        self.configureButtonBindings()

        # set up default drive command
        self.led.setDefaultCommand( DefaultCommand(self.led))
        print (">>>> Robot Initialization complete in __init__ in robotcontainer.py")

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        self.driverController.A().whileTrue(setLEDgreen(self.led))


    # This function defines what is run during autonomous
    def getAutonomousCommand(self) -> commands2.Command:
        print (">>>> Autonomous command defined")

        # assign the autoCommand passing in the LED Subsystem as a parameter
        return autoCommand(self.led)
