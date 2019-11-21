#!/usr/bin/python
from spidev import SpiDev
import os
from threading import Thread
from os import getcwd
import time
from time import sleep
import RPi.GPIO as GPIO

class MCP3008:
  def __init__(self, channels_used, bus, device, channel):
    self.spi = SpiDev()
    #How many MCP3008 channels are your going to use? 1
    self.channels_used = channels_used - 1
    #SPI bus number 0
    self.bus = bus
    #device/cs number 0
    self.device = device
    #SPI channel number 0
    self.channel = channel

  def Open(self):
    self.spi.open(self.bus , self.device)

  def read(self):
      adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
      data = ((adc[1] & 3) << 8) + adc[2]
      return data

  def close(self):
    self.spi.close()

class sharp_2Y0A02(MCP3008):

  def __init__(self, name, channels_used, SPI_bus, SPI_device, SPI_channel, trigger = None):
    super().__init__(channels_used, SPI_bus, SPI_device, SPI_channel) 
    self.name = name
    self.channels_used = channels_used
    self.SPI_bus = SPI_bus
    self.SPI_device = SPI_device
    self.SPI_channel = SPI_channel
    self.trigger = trigger

  def clean_up(self):
    GPIO.cleanup()

  # setting up the sensor pins, signals, and communication
  @classmethod
  def user_inputs(cls):  
    name = str(input("Please enter your sensor convention:"))
    channels_used = int(input("How many channels will you be using?:"))
    SPI_bus = int(input("Which SPI bus will you be using?:"))
    SPI_device = int(input("Which SPI device will you be using?:"))
    SPI_channel = int(input("Which SPI channel will you be using?:"))
    
    return cls(name, channels_used, SPI_bus, SPI_device, SPI_channel)

  # declare the scan loop setup
  def scan(self):
    self.Open()
    data = float(self.read())# use CH0
    voltage = float((data / 1023.0) * 3.3)
    distance = float(16.2537 * voltage ** 4 - 129.893 * voltage ** 3 + 382.268 * voltage ** 2 - 512.611 * voltage + 301.439)
    time.sleep(0.1)

    return distance

  def detect(self):
    i = int(0)
    for obj in objs: #loop over the class objects
      if obj.trigger:
        i += 1
    if i >= 1: #check
      #if any other ultrasonic objects triggered
      pass
    else :
      print("IR Detection")
    self.trigger = 0

  # starting the sensor loop / turning the sensor on
  def run(self):
    try:
      while True:
        distance = self.scan()
        print("Measured Distance = %.1f cm" % distance)
        if distance <= 100:
          self.trigger = 1
          self.detect()
          continue# Reset by pressing CTRL + C
    except KeyboardInterrupt:
      print("Measurement stopped by User")
      self.close()
      
      
class HC_SRO4(object):
  global objs# registrar
  objs = []

  def __init__(self, name, GPIO_TRIGGER, GPIO_ECHO, trigger = None):
    self.name = name
    self.GPIO_TRIGGER = GPIO_TRIGGER
    self.GPIO_ECHO = GPIO_ECHO
    self.pins = (GPIO_TRIGGER, GPIO_ECHO)
    self.trigger = trigger
    
  def clean_up(self):
    GPIO.cleanup()

  # setting up the sensor pins, signals, and communication
  @classmethod
  def user_inputs(cls):

    name = str(raw_input("Please enter your sensor convention:"))
    
    GPIO_TRIGGER = int(raw_input("Please enter your sensor GPIO Trigger pin number:"))
    
    GPIO_ECHO = int(raw_input("Please enter your sensor GPIO Echo pin number:"))
    
    return cls(name, GPIO_TRIGGER, GPIO_ECHO)

  def setup(self):
    GPIO_TRIGGER = self.pins[0]
    GPIO_ECHO = self.pins[1]# GPIO Mode(BOARD / BCM)
    GPIO.setmode(GPIO.BCM)# set GPIO direction(IN / OUT)
    GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(self.GPIO_ECHO, GPIO.IN)# register the new class obj
    objs.append(HC_SRO4(self.name, self.GPIO_TRIGGER, self.GPIO_ECHO, self.trigger))# assign the pins setup as the function 's output
    print("Setup done")

  # declare the scan loop setup
  def scan(self):
    GPIO_TRIGGER = self.pins[0]
    GPIO_ECHO = self.pins[1]# set Trigger to HIGH
    GPIO.output(self.GPIO_TRIGGER, True)# set Trigger after 0.01 ms to LOW
    time.sleep(0.00001)
    GPIO.output(self.GPIO_TRIGGER, False)
    
    # initial time
    StartTime = time.time()
    StopTime = time.time()
    
    # save StartTime
    while GPIO.input(self.GPIO_ECHO) == 0:
      StartTime = time.time()
    
    # save time of arrival
    while GPIO.input(self.GPIO_ECHO) == 1:
      StopTime = time.time()
    
    # time difference between start and arrival
    TimeElapsed = float(StopTime - StartTime)
    
    # multiply with the sonic speed(34300 cm / s)# and divide by 2, because there and back
    distance = float((TimeElapsed * 34300) / 2)
    
    return distance

  def detect(self):
    i = int(0)# indicator
    for obj in objs: #loop over the class objects
      if obj.trigger:
        i += 1
    if i > 1: #check
      print('us dual detection')# speaker.dual_US_mss()
    else :
      print('us single detection')# speaker.single_US_mss()

    self.trigger = 0# starting the sensor loop / turning the sensor on
    
    
  def run(self):
      try:
        while True:
          distance = float(self.scan())
          print(self.name)
          print("Measured Distance = %.1f cm" % distance)
          time.sleep(1)
          if distance <= 100:
            self.trigger = 1
            self.detect()
            continue# Reset by pressing CTRL + C
      except KeyboardInterrupt:
        print("Measurement stopped by User")

if __name__ == "__main__":
  GPIO.cleanup()
  ''' 
  us1 = HC_SRO4.user_inputs()
  t1 = Thread(us1.run())
  t1.start()
  
  us2 = HC_SRO4.user_inputs()
  t2 = Thread(us2.run())
  t2.start()
  '''

  ir1 = sharp_2Y0A02.user_inputs()
  t3 = Thread(ir1.run())
  t3.start()
  
