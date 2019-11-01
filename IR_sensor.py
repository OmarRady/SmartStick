from sensors import sensor
from ADC import MCP3008
class ir_sensor(sensor , MCP3008):

    def inputs(self):
        self.set_name()
        self.set_GPIO_TRIGGER()
        self.set_GPIO_ECHO()
        self.set_switch()


    # setting up the sensor pins, signals, and communication

    def setup(self):

        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BOARD)

        #set GPIO Pins
        try:
            GPIO_TRIGGER = self.get_GPIO_TRIGGER()  # 18
            GPIO_ECHO = self.get_GPIO_ECHO()  # 24
        except:
            print("Infrared Sensor instance misses the GPIO pins setup parameters")
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        bus = smbus.SMBus(1)  # RPi revision 2 (0 for revision 1)
        i2c_address = 0x48
        # u = mx + b, x = 1/distance
        m = 19.8
        b = 0.228

    # declare the scan loop setup
    def scan(self):

        data = bus.read_byte_data(i2c_address, 0)  # use CH0
        u = data / 255 * 5
        distance = int(m / (u - b))
        time.sleep(0.1)

        return distance

    def detect(self):
        self.set_trigger()


        self.reset_trigger()

    # starting the sensor loop / turning the sensor on
    def run(self):
        self.inputs()
        self.setup()
        if self.get_switch():
             try:
                while True:
                     distance = self.scan()
                     print("Measured Distance = %.1f cm" % distance)
                     time.sleep(1)
                     if distance <= 100:

                         print("detected")
                         #self.trigger = True
                         #self.detect()
                     continue
                 # Reset by pressing CTRL + C
             except KeyboardInterrupt:
                 print("Measurement stopped by User")
        else:
             print("The Sensor's switch is off")