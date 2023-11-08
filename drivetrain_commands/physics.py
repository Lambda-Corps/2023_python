import wpilib.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import typing

import constants

if typing.TYPE_CHECKING:
    from robot import MyRobot


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """
    LEFT_SPEED_INDEX = 0
    RIGHT_SPEED_INDEX = 1
    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        self.physics_controller = physics_controller

        # Keep a reference to the robot passed in
        self._robot_instance = robot

        # Create a sim Gyro to be used for maintaining the heading
        # self._gyro = wpilib.simulation.AnalogGyroSim(robot._gyro)
        self._gyro = wpilib.simulation.SimDeviceSim("navX-Sensor[4]")
        self.navx_yaw = self._gyro.getDouble("Yaw")

        self.position = 0

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_FALCON_500,# motor configuration
            constants.ROBOT_MASS,           # robot mass
            constants.DT_GEAR_RATIO,        # drivetrain gear ratio
            2,                              # motors per side
            constants.ROBOT_WHEELBASE,      # robot wheelbase
            constants.ROBOT_WIDTH,          # robot width
            constants.ROBOT_LENGTH,         # robot length
            constants.DT_WHEEL_DIAMETER,    # wheel diameter
        )
        # fmt: on

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.
        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        speeds = self._robot_instance.getSpeeds()

        transform = self.drivetrain.calculate(speeds[self.LEFT_SPEED_INDEX], speeds[self.RIGHT_SPEED_INDEX], tm_diff)
        pose = self.physics_controller.move_robot(transform)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        self.navx_yaw.set(-pose.rotation().degrees())

        # Tell the robot the current linear position of the left and right side motors
        # This will be used to convert to encoder ticks for the motor controllers
        self._robot_instance.update_sensor_odometry(self.drivetrain.l_position, self.drivetrain.l_velocity, self.drivetrain.r_position, self.drivetrain.r_velocity)