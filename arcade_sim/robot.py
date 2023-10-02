#!/usr/bin/env python3
import wpilib
from commands2 import TimedCommandRobot, CommandScheduler, Command, PrintCommand

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
        # Setup the operator interface (typically CommandXboxController)

        # Instantiate any subystems
        self._drivetrain = None

        # Map the button bindings for the driver

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