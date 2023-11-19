
import commands2
import wpilib
import constants

##
##  This example is inspired by the "AddressableLED"
##  https://github.com/robotpy/examples
#
#   The command framework was guided by the following example:
#
## https://github.com/robotpy/examples/tree/main/commands-v2/hatchbot

class LEDSubsystem(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()      # Call the initialization routing of the parent Object

        # Instantiate the LED Object
        self.LED = wpilib.AddressableLED(constants.kPWMInterfaceNumber)

        # Create an array of data to hold the color of each LED
        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(constants.kLEDBuffer)]

        # Store what the last hue of the first pixel is
        self.rainbowFirstPixelHue = 0

        # Set the number of LEDs in the LED Array
        self.LED.setLength(constants.kLEDBuffer)

        # Push the array of LED color information into the physical LED strip
        self.LED.setData(self.ledData)
        self.LED.start()
        print (">>>> Robot Initialization complete in __init__ in LEDSubsystem.py")


    def rainbow(self):
        # Loop thru the array and load it with color.  In this case a changing rainbow
        for i in range(constants.kLEDBuffer):
            # Calculate the hue - hue is easier for rainbows because the color
            # shape is a circle so only one value needs to precess
            hue = (self.rainbowFirstPixelHue + (i * 180 / constants.kLEDBuffer)) % 180
            # Set the value
            self.ledData[i].setHSV(int(hue), 255, 128)
        # Increase by to make the rainbow "move"
        self.rainbowFirstPixelHue += 3
        # Check bounds
        self.rainbowFirstPixelHue %= 180

    def setColorGreen(self):
        # Loop thru the array and load it with color.  In this case a changing Green
        for i in range(constants.kLEDBuffer):
            hue = 240  #  120 is blue, 0 is red
            # Set the value
            self.ledData[i].setHSV(int(hue), 255, 128)

    def setColorBlue(self):
        # Loop thru the array and load it with color.  In this case a changing Green
        for i in range(constants.kLEDBuffer):
            hue = 120  #  120 is blue, 0 is red
            # Set the value
            self.ledData[i].setHSV(int(hue), 255, 128)

    def setColorRed(self):
        # Loop thru the array and load it with color.  In this case a changing red
        print ("printing red")
        for i in range(constants.kLEDBuffer):
            hue = 0  #  120 is blue, 0 is red
            # Set the value
            self.ledData[i].setHSV(int(hue), 255, 128)

    def displayRainbow(self):
        # Fill the buffer with a rainbow
        self.rainbow()
        # Set the LEDs
        self.LED.setData(self.ledData)
        # print (">>> Display Rainbow Function within the LEDSubsystem")

    def displayGreen(self):
        # Fill the buffer with a green color
        self.setColorGreen()
        # Set the LEDs
        self.LED.setData(self.ledData) 
        # print (">>> Display Green Function within the LEDSubsystem")

    def displayBlue(self):
        # Fill the buffer with a blue color
        self.setColorBlue()
        # Set the LEDs
        self.LED.setData(self.ledData)
        # print (">>> Display Blue Function within the LEDSubsystem")

    def displayRed(self):
        # Fill the buffer with a blue color
        self.setColorRed()
        # Set the LEDs
        self.LED.setData(self.ledData)
        # print (">>> Display Red Function within the LEDSubsystem")
