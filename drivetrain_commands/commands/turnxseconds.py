import commands2

# Import the subsystem
from subsystems.drivetrain import DriveTrain


class TurnXSeconds(commands2.CommandBase):
    def __init__(self, drivetrain:DriveTrain, seconds:float, speed:float) -> None:
        super().__init__()

        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.counter = 0
        self.seconds  = seconds
        self.speed = speed

    def initialize(self) -> None:
        print ("Init Turn x Seconds: ", self.seconds)
        self.drivetrain.zeroHeading()

    def execute(self) -> None:
        self.drivetrain.driveManually(0.0, -self.speed) # Positive is Clockwise, Negative is Counter Clockwise    
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

