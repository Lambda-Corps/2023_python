import math
import wpilib
if wpilib.RobotBase.isSimulation():
    from pyfrc.physics.units import units
DT_TRACKWIDTH_METERS = .546
DT_WHEEL_DIAMETER = 6
DT_WHEEL_RADIUS_INCHES = DT_WHEEL_DIAMETER/2
# User interface 
kDriverControllerPort = 0


# LED Strip information
kLEDBuffer = 20           # number of LEDs in strip
kPWMInterfaceNumber = 9   # the physical PWM connector which the LED strip is connected

class DriveConstants:


    kGyroReversed = False

    kStabilizationP = 1
    kStabilizationI = 0.5
    kStabilizationD = 0

    kTurnP = 1
    kTurnI = 0
    kTurnD = 0

    kMaxTurnRateDegPerS = 100
    kMaxTurnAccelerationDegPerSSquared = 300

    kTurnToleranceDeg = 5
    kTurnRateToleranceDegPerS = 10  # degrees per second


# Robot Physical Characteristics with dimensional units

if wpilib.RobotBase.isSimulation():
    ROBOT_MASS = 110 * units.lbs
else:
    ROBOT_MASS = 110 * 1

DT_HIGH_GEAR_RATIO = 4.17
DT_LOW_GEAR_RATIO = 11.03
DT_GEAR_RATIO = DT_LOW_GEAR_RATIO # start with low gear as our sim
DT_MOTORS_PER_SIDE = 2

if wpilib.RobotBase.isSimulation():
    ROBOT_WHEELBASE = 22 * units.inch
    ROBOT_BUMPER_WIDTH = 3.25 * units.inch
    ROBOT_WIDTH = (23 * units.inch) + (ROBOT_BUMPER_WIDTH * 2)
    ROBOT_LENGTH = (32 * units.inch) + (ROBOT_BUMPER_WIDTH * 2)
    DT_WHEEL_DIAMETER = 6 * units.inch
else:
    ROBOT_WHEELBASE = 22 * 1
    ROBOT_BUMPER_WIDTH = 3.25 * 1
    ROBOT_WIDTH = (23 * 1) + (ROBOT_BUMPER_WIDTH * 2)
    ROBOT_LENGTH = (32 * 1) + (ROBOT_BUMPER_WIDTH * 2)
    DT_WHEEL_DIAMETER = 6 * 1

# CAN IDS
DT_LEFT_LEADER      = 2 #1  (Originally 1)
DT_RIGHT_LEADER     = 1 #2  (Orginially 2)
DT_LEFT_FOLLOWER    = 3 #3
DT_RIGHT_FOLLOWER   = 4 #4
#5
#6
#7
#8
#9
#10
#11
#12
#13
#14