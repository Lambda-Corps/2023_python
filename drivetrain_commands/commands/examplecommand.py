import wpilib
import commands2

from subsystems.examplesubsystem import ExampleSubsystem

#     Import all subsystem referenced in the this command
# from subsystems.drivetrain import DriveTrain

class ExampleCommand(commands2.CommandBase):
    """Example command:  A command that will turn the robot to the specified angle."""


    def __init__(self, targetAngleDegrees: float, exsubsystem: ExampleSubsystem) -> None:
        """
        This example command is used to control a subsystem
        In this case the examplesubsystem

        We are passing in two parameters: The first is an angle that can be
        used to turn a robot to a specific heading or move an arm 
        to a specific angle.

        :param: targetAngleDegrees: The angle to ...
        :param: subsystem: The subsystem to used by this command
        """
        super().__init__()
        self.exsubsystem = exsubsystem
        self.targetAngleDegrees = targetAngleDegrees
        self.addRequirements(exsubsystem)


    #  The initialization function is called once when the command is first called
    #  We can use this to reset sensors, start motors, or whatever needs to happen once
    #  as the command starts
    def initialize(self) -> None:
        # This print statement is just used to show the order the functions are called, can be removed
        print ("Command Initialization function, passed in angle: ", 
               self.targetAngleDegrees)
        # For example:  self.drivetrain.zeroHeading()
        pass  #  This command does nothing


    #  The execute function runs 50 times every second
    def execute(self) -> None:
        # For example:  self.drivetrain.driveManually(0.0, -self.speed)
        pass  #  The "pass" command does nothing.  Python requires at least one line of code in a function


    #  The isFinished function is used to check to see of we have completed the purpose 
    #  of the function.  We should check a sensor or a PID to determine if we are done.
    #  This function is called right after the execute function is called (50 times a second)
    def isFinished(self) -> bool:
        # For Example
        # angleSensor = subsystem.readAngleSensor()
        # if (angleSensor > self.targetAngleDegrees):
        #     return True   ##  We are Done!
        # else:
        #     return False  ## Keep going, Not done yet
        return True



    #  The end function is run one time once we decide our function has finshed.
    #  It can be used to stop drivetrain motors or arm motors or what ever
    def end(self, interrupted: bool) -> None:
        print("Command end function:  We are done with the command!")
        # For example:  self.drivetrain.driveManually(0.0, 0.0)    # Stop the robot
        pass
        

