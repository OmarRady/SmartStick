class stick_sensors:

    def __init__(self, name: str, switch: bool , SetGPIO_TRIGGER: int , SetGPIO_ECHO: int):

        self.name = name 
        self.switch = switch
        self.SetGPIO_TRIGGER = SetGPIO_TRIGGER
        self.SetGPIO_ECHO = SetGPIO_ECHO
        

class ultrasonics_sensor(stick_sensors):
        
    # setting up the sensor pins, signals, and coomunication
    def setup(self):
        super(ultrasonics_sensor, self).__init__(int (SetGPIO_TRIGGER) ,int (SetGPIO_ECHO))

        import RPi.GPIO as GPIO
        import time
        from time import sleep
        import os

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        #set GPIO Pins
        try:
            GPIO_TRIGGER = SetGPIO_TRIGGER #18
            GPIO_ECHO = SetGPIO_ECHO       #24
        except:
            print("Sensor instance misses the GPIO pins setup parameters")
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

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
              StartTime = time.time()
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
              StopTime = time.time()
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

    def detect(self):
        pass


    # starting the sensor loop / turning the sensor on  
    def run(self):
        super(ultrasonics_sensor, self).__init__(bool (switch))
        if switch:
            try:
                setup()
                while True:
                    distance = self.scan()
                    print ("Measured Distance = %.1f cm" % distance)
                    time.sleep(1)
                    if distance <= 100:
                        detect()
                    continue
                # Reset by pressing CTRL + C
            except KeyboardInterrupt:
                print("Measurement stopped by User")
        else:
             print("The Sensor's switch is off")
    
