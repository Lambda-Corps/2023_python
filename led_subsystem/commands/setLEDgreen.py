import commands2

# Import the subsystem
from subsystems.LEDsubsystem import LEDSubsystem

class setLEDgreen(commands2.CommandBase):
    def __init__(self, led: LEDSubsystem) -> None:
        super().__init__()

        self.led = led
        self.addRequirements(led)
        print (">>>> Command Instantiation complete in __init__ in setLEDgreen.py")

    def initialize(self) -> None:
        print (">>>> Initialization complete in initialize in setLEDgreen.py")
        pass

    def execute(self) -> None:
        # Fill the buffer with a Green
        self.led.displayGreen()
 
    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        # This command should be triggered while a button is held
        # so we don't want it to finish on it's own.  So always return
        # false to keep the command running until the button is released.
        return False
