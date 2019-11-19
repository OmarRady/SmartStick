import setup
from ADC import MCP3008
import speaker

class sharp_2Y0A02(setup.hardsetup, MCP3008):

    # setting up the sensor pins, signals, and communication
    def setup(self):
        self.set_name()
        name = str(self.get_name())
        self.set_switch()
        switch = bool(self.get_switch())
        self.get_channels_used()
        self.get_SPI_bus()
        self.get_SPI_device()
        self.get_SPI_channel()

    # declare the scan loop setup
    def scan(self):

        data = float(self.MCP3008.read()) # use CH0
        voltage = float((data/1023.0)*3.3)
        distance = float(16.2537 * voltage**4 - 129.893 * voltage**3 + 382.268 * voltage**2 - 512.611 * voltage + 301.439)
        time.sleep(0.1)

        return distance

    def detect(self, distance):
        self.set_trigger()
        trigger = bool(self.get_trigger())
        i = int(0)
        for obj in setup.objs:  # loop over the class objects
            if obj.trigger:
                i += 1
        if i >= 1:  # check if any other ultrasonic objects triggered
            pass
        else:
            speaker.IR_mss()
        self.reset_trigger()
        trigger = bool(self.get_trigger())

    # starting the sensor loop / turning the sensor on
    def run(self):
        self.inputs()
        self.setup()
        if self.get_switch():
             try:
                while True:
                     distance = self.scan()
                     print("Measured Distance = %.1f cm" % distance)
                     if distance <= 100:
                        self.detect(distance)
                     continue
                 # Reset by pressing CTRL + C
             except KeyboardInterrupt:
                 print("Measurement stopped by User")
        else:
             print("The Sensor's switch is off")
