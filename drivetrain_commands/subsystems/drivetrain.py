import wpilib
import wpilib.drive
from commands2 import SubsystemBase
import ctre
import navx
import constants
import math
from typing import List

if wpilib.RobotBase.isSimulation():
    from pyfrc.physics.units import units

class DriveTrain(SubsystemBase):
    DT_TICKS_PER_MOTOR_REV = int(2048) # Falcons are 2048

    if wpilib.RobotBase.isSimulation():
        DT_TICKS_PER_INCH = (DT_TICKS_PER_MOTOR_REV * constants.DT_GEAR_RATIO) / ((2 * math.pi ) * constants.DT_WHEEL_DIAMETER.m_as(units.inch))
    else:
        DT_TICKS_PER_INCH = (DT_TICKS_PER_MOTOR_REV * constants.DT_GEAR_RATIO) / ((2 * math.pi ) * constants.DT_WHEEL_DIAMETER)

    def __init__(self) -> None:
        super().__init__()

        self._left_leader = ctre.WPI_TalonFX(constants.DT_LEFT_LEADER)
        self._left_follower = ctre.WPI_TalonFX(constants.DT_LEFT_FOLLOWER)
        self._right_leader = ctre.WPI_TalonFX(constants.DT_RIGHT_LEADER)
        self._right_follower = ctre.WPI_TalonFX(constants.DT_RIGHT_FOLLOWER)

        # Factory default the motor controllers
        self._left_leader.configFactoryDefault()
        self._left_follower.configFactoryDefault()
        self._right_leader.configFactoryDefault()
        self._right_follower.configFactoryDefault()

        # Motor are mounted opposite of each other, so one needs to run "backward" to make the robot move
        # in the direction we want.
        if wpilib.RobotBase.isReal():
            self._right_leader.setInverted(ctre.TalonFXInvertType.Clockwise)  # (original Clockwise)
            self._left_leader.setInverted(ctre.TalonFXInvertType.CounterClockwise) # (original CounterClockwise)
        else:
            self._right_leader.setInverted(ctre.TalonFXInvertType.CounterClockwise)  # (original Clockwise)
            self._left_leader.setInverted(ctre.TalonFXInvertType.Clockwise) # (original CounterClockwise)
        # Set the follower motors, and their inversions to match
        self._left_follower.follow(self._left_leader)
        self._left_follower.setInverted(ctre.TalonFXInvertType.FollowMaster)
        self._right_follower.follow(self._right_leader)
        self._right_follower.setInverted(ctre.TalonFXInvertType.FollowMaster)

        # Set the neutral mode to brake so the robot stops more responsively
        self._left_leader.setNeutralMode(ctre.NeutralMode.Brake)
        self._right_leader.setNeutralMode(ctre.NeutralMode.Brake)

        # Set the integrated encoder as the primary feedback sensor and force it's starting position to 0
        self._left_leader.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, 0)
        self._right_leader.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, 0)
        self._left_leader.setSelectedSensorPosition(0)
        self._right_leader.setSelectedSensorPosition(0)

        self._lastLeftSet = 0.0
        self._lastRightSet = 0.0

        self._left_motor_sim = None
        self._right_motor_sim = None

        if wpilib.RobotBase.isSimulation():
            self._left_motor_sim = self._left_leader.getSimCollection()
            self._right_motor_sim = self._right_leader.getSimCollection()

        self._gyro = navx.AHRS.create_spi()
        self.rangefinder = wpilib.AnalogInput(0)


    def update_dt_odometry(self, left_pos: float, left_vel: float, right_pos: float, right_vel: float) -> None:
        ''' Receive the positions and velocities from the simulation in feet
                Convert the units to encoder ticks, and set the simulation sensors 
        '''
        if self._left_motor_sim is not None:
            self._left_motor_sim.setIntegratedSensorRawPosition(self.feet_to_encoder_ticks(left_pos))
            self._left_motor_sim.setIntegratedSensorVelocity(self.velocity_to_talon_ticks(left_vel))

        if self._right_motor_sim is not None:
            self._right_motor_sim.setIntegratedSensorRawPosition(self.feet_to_encoder_ticks(right_pos))
            self._right_motor_sim.setIntegratedSensorVelocity(self.velocity_to_talon_ticks(right_vel))


    def getSpeeds(self) -> List[float]:
        return self._lastLeftSet, self._lastRightSet
    
    def driveManually(self, forward: float, turn: float):
        '''Use the member variable _diffdrive to set the left and right side motors based 
        on the inputs. The third argument being passed in true represents whether or 
        not we should allow the robot to turn in place or not'''

        SPEED_REDUCTION_PERCENT = 0.5    # reduce speed by xx% in manual drive
        forward = forward * SPEED_REDUCTION_PERCENT
        turn = turn * SPEED_REDUCTION_PERCENT

        if wpilib.RobotBase.isSimulation():
            wheelSpeeds = wpilib.drive.DifferentialDrive.arcadeDriveIK(forward, turn, True)
        else:
            wheelSpeeds = wpilib.drive.DifferentialDrive.arcadeDriveIK(-forward, -turn, True) 
            
        rangefinder_voltage = self.rangefinder.getAverageVoltage()
       # print("range: %5.2f  joystick: %5.2f" %(rangefinder_voltage, forward))
        # print (rangefinder_voltage,' ',forward)

        if (self.rangefinder.getAverageVoltage() < 1.0) and (forward < 0):
            forward = 0
            turn = 0
            
        self._left_leader.set(wheelSpeeds.left)
        self._right_leader.set(wheelSpeeds.right)

        self._lastLeftSet = wheelSpeeds.left
        self._lastRightSet = wheelSpeeds.right

        # print ("Encoder Value     Left:  %8.1f    Right:  %8.1f    Heading: %6.2f" % 
        #        (self._left_leader.getSelectedSensorPosition(), 
        #         self._right_leader.getSelectedSensorPosition(),
        #         self._gyro.getAngle()))
        
        # print (">>> Forward:  %5.2f    Turn:  %5.2f " % (forward, turn))
      
    def feet_to_encoder_ticks(self, distance_in_feet: float) -> int:
        return int((distance_in_feet * 12) * self.DT_TICKS_PER_INCH)
    

    def velocity_to_talon_ticks(self, velocity_in_feet: float) -> int:
        if wpilib.RobotBase.isSimulation():
            wheen_rotations_per_second = (velocity_in_feet * 12) / (2 * math.pi * constants.DT_WHEEL_DIAMETER.m_as(units.inch))
        else:
            wheen_rotations_per_second = (velocity_in_feet * 12) / (2 * math.pi * constants.DT_WHEEL_DIAMETER)

        wheel_rotations_per_100ms = (wheen_rotations_per_second * constants.DT_GEAR_RATIO) / 10
        motor_rotations_per_100ms = wheen_rotations_per_second * constants.DT_GEAR_RATIO
        return int(motor_rotations_per_100ms * self.DT_TICKS_PER_MOTOR_REV)
    
    def zeroHeading(self):
        """
        Zeroes the heading of the robot.
        """
        print ("Reset Gyro ")
        self._gyro.reset()

    def getHeading(self):
        """
        Returns the heading of the robot.

        :returns: the robot's heading in degrees, from 180 to 180
        """
        return math.remainder(self._gyro.getAngle(), 180) * (
            -1 if constants.DriveConstants.kGyroReversed else 1
        )

    def getTurnRate(self):
        """
        Returns the turn rate of the robot.

        :returns: The turn rate of the robot, in degrees per second
        """
        return self._gyro.getRate() * (
            -1 if constants.DriveConstants.kGyroReversed else 1
        )
