import commands2
from commands2 import PrintCommand ,  CommandGroupBase, SequentialCommandGroup
from commands.driveforwardxseconds import DriveForwardXSeconds
from commands.turnxseconds import TurnXSeconds
from commands.waitxseconds import WaitXSeconds 

from subsystems.drivetrain import DriveTrain
from subsystems.ledsubsystem import LEDSubsystem

class AutonomousCommand(commands2.SequentialCommandGroup):
    def __init__(self,  drivetrainsubsystem : DriveTrain,led:LEDSubsystem  ) -> None:
        super().__init__()
        print ("Within Autonomous SequentialCommand Group")
        self.led = led
        self.drivetrainsubsystem = drivetrainsubsystem
        # self.addCommands(setLEDgreen(self.led))
        # self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        # self.addCommands(setLEDred(self.led))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1))
        
        self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,3.0,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1.2,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,2))

        self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,2.0,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1.2,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))

        self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,3.0,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1.2,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))

        self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,2.0,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1.2,0.75))
        self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))

        # self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.67))
        # self.addCommands(WaitXSeconds(self.drivetrainsubsystem,1))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1,0.5))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.67))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1,0.5))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.6))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1,0.5))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.82))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1,0.5))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.6))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1,0.5))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.6))
        # self.addCommands(TurnXSeconds(self.drivetrainsubsystem,1,0.5))
        # self.addCommands(DriveForwardXSeconds(self.drivetrainsubsystem,5,0.6))
        self.addCommands(PrintCommand("Done"))
            
# References:
#  https://robotpy.readthedocs.io/projects/commands-v2/en/stable/commands2/SequentialCommandGroup.html

#
