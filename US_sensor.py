from sensors import sensor

class us_sensor(sensor):

    objs = []  # registrar

    def inputs(self):
        self.set_name()
        self.set_GPIO_TRIGGER()
        self.set_GPIO_ECHO()
        self.set_switch()


    # setting up the sensor pins, signals, and communication

    def setup(self):
        # register the new class obj
        us_sensor.objs.append(self)  # register the new object with the class

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO Pins
        try:
            GPIO_TRIGGER = self.get_GPIO_TRIGGER()  # 18
            GPIO_ECHO = self.get_GPIO_ECHO()  # 24
        except:
            print("Ultrasonic Sensor misses the GPIO pins setup parameters")
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)


    # declare the scan loop setup
    def scan(self):

        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        # initial time
        StartTime = time.time()
        StopTime = time.time()

        #save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        #save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        #time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        #multiply with the sonic speed (34300 cm/s)
        #and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

    def detect(self):
        self.set_trigger()
        i = 0  # indicator
        for obj in us_sensor.objs:  # loop over the class objects
            if obj.get_trigger(self) == True:
                i += 1
        if i > 1:  # check if any other ultrasonic objects triggered
            # Alert.dual_ultrasonic()
            print("two sensor alert")
        else:
            # Alert.ultrasonic()
            print("One sensor alert")

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
                        self.detect()
                     continue
                 # Reset by pressing CTRL + C
             except KeyboardInterrupt:
                 print("Measurement stopped by User")
        else:
             print("The Sensor's switch is off")