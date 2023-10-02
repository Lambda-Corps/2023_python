#!/usr/bin/env python3
import wpilib
from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand, RunCommand
from commands2.button import CommandXboxController
import navx

import drivetrain
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

        # Instantiate any subystems

        # Setup the default commands for subsystems

        self._auto_command = None
    

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


    def getLeftSpeed(self) -> float:
        return 0.0 if self._drivetrain is None else self._drivetrain.getLeftSpeed()
    

    def getRightSpeed(self) -> float:
        return 0.0 if self._drivetrain is None else self._drivetrain.getRightSpeed()
    

    def disabledPeriodic(self) -> None:
        pass


    def autonomousPeriodic(self) -> None:
        pass


    def testPeriodic(self) -> None:
        pass


    def teleopPeriodic(self) -> None:
        return super().teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)