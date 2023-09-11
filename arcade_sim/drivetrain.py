import wpilib
from commands2 import SubsystemBase
import wpilib.drive

class DriveTrain(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self._leftMotor = wpilib.PWMSparkMax(1)
        self._rightMotor = wpilib.PWMSparkMax(2)

        self._lastLeftSet = 0.0
        self._lastRightSet = 0.0

    
    def driveManually(self, forward: float, turn: float):
        '''Use the member variable _diffdrive to set the left and right side motors based on the inputs. The third argument being passed in true represents whether or not we should allow the robot to turn in place or not'''
        wheelSpeeds = wpilib.drive.DifferentialDrive.arcadeDriveIK(forward, turn, True)
        
        self._leftMotor.set(wheelSpeeds.left)
        self._rightMotor.set(wheelSpeeds.right)

        self._lastLeftSet = wheelSpeeds.left
        self._lastRightSet = wheelSpeeds.right