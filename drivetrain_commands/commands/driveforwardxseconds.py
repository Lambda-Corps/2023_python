import commands2
import wpilib
# Import the subsystem
from subsystems.drivetrain import DriveTrain


class DriveForwardXSeconds(commands2.CommandBase):
    def __init__(self, drivetrain:DriveTrain, seconds:float, speed:float) -> None:
        super().__init__()

        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.counter = 0
        self.seconds  = seconds
         
        if wpilib.RobotBase.isSimulation():
            self.speed = speed
        else:
            self.speed = -speed
        # print ("__init__ Drive x Seconds: ", self.seconds)


    def initialize(self) -> None:
        print ("Init Drive x Seconds: ", self.seconds)
        self.drivetrain.zeroHeading()
        self.counter = 0

    def execute(self) -> None:
        # Fill the buffer with a Green
        self.drivetrain.driveManually(self.speed, 0.0)    # Move the robot forward
        self.counter = self.counter + 1

 
    def end(self, interrupted: bool) -> None:
        self.drivetrain.driveManually(0.0, 0.0)    # Stop the robot
        

    def isFinished(self) -> bool:
        # This command should be triggered while a button is held
        # so we don't want it to finish on it's own.  So always return
        # false to keep the command running until the button is released.

        if self.counter >  (self.seconds * 50):
            return True
        else:
            return False

