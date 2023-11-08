#!/usr/bin/env python3
import wpilib
from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
from commands2.button import CommandXboxController
import navx
import drivetrain

from typing import Tuple, List
class MyRobot(TimedCommandRobot):
    ''' Class that defines the totality of our Robot'''

    def robotInit(self) -> None:
        '''
        This method must eventually exit in order to ever have the robot
        code light turn green in DriverStation. So, this will create an 
        instance of the Robot that contains all the subsystems,
        button bindings, and operator interface pieces like driver 
        dashboards
        '''
        self._gyro = navx.AHRS.create_spi()

        # Setup the operator interface (typically CommandXboxController)
        self._driver_controller = CommandXboxController(0)

        # Instantiate any subystems
        self._drivetrain = drivetrain.DriveTrain()

        # Setup the default commands for subsystems
        self._drivetrain.setDefaultCommand(
            # A split-stick arcade command, with forward/backward controlled by the left
            # hand, and turning controlled by the right.
            RunCommand(
                lambda: self._drivetrain.driveManually(
                    self._driver_controller.getRawAxis(0),
                    self._driver_controller.getRawAxis(1),
                ),
                self._drivetrain,
            )
        )

        self._auto_command = None

        # Keep track of the linear position of the simulation
        self._left_position_in_feet = 0
        self._right_position_in_feet = 0
    

    def getAutonomousCommand(self) -> Command:
        return PrintCommand("Default auto selected")


    def teleopInit(self) -> None:
        if self._auto_command is not None:
            self._auto_command.cancel()

    
    def testInit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
    

    def autonomousInit(self) -> None:
        self._auto_command = self.getAutonomousCommand()

        if( self._auto_command is not None):
            self._auto_command.schedule()


    def getSpeeds(self) -> List[float]:
        return [0.0, 0.0] if self._drivetrain is None else self._drivetrain.getSpeeds()
    

    def disabledPeriodic(self) -> None:
        pass


    def autonomousPeriodic(self) -> None:
        pass


    def testPeriodic(self) -> None:
        pass


    def teleopPeriodic(self) -> None:
        return super().teleopPeriodic()
    
    def update_sensor_odometry(self, left_pos: float, left_vel: float, right_pos: float, right_vel: float) -> None:
        self._drivetrain.update_dt_odometry(left_pos, left_vel, right_pos, right_vel)


if __name__ == "__main__":
    wpilib.run(MyRobot)