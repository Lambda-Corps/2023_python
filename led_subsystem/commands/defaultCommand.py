import commands2

# Import the subsystem
from subsystems.LEDsubsystem import LEDSubsystem

class DefaultCommand(commands2.CommandBase):
    def __init__(self, led: LEDSubsystem) -> None:
        super().__init__()

        self.led = led
        self.addRequirements(led)

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.led.displayRainbow()
 
    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False
