class sensor:

    import os
    from os import getcwd;
    import time
    from time import sleep
    import RPi.GPIO as GPIO
    import null
    print.sys.path
    print(getcwd())

    def __init__(self):
        pass


    def set_name(self):
        self.__name = input("Please enter your sensor convention:")

    def get_name(self):
        return self.__name


    def set_GPIO_TRIGGER(self):
        self.__GPIO_TRIGGER = int(input("Please enter your sensor GPIO Trigger pin number:"))

    def get_GPIO_TRIGGER(self):
        return self.__GPIO_TRIGGER


    def set_GPIO_ECHO(self):
        self.__GPIO_ECHO = int(input("Please enter your sensor GPIO Echo pin number:"))

    def get_GPIO_ECHO(self):
        return self.__GPIO_ECHO


    def set_switch(self):
        self.__switch = bool(input("Please turn on your sensor:"))

    def get_switch(self):
        return self.__switch

    def set_trigger(self):
        self.__trigger = True

    def reset_trigger(self):
        self.__trigger = False

    def get_trigger(self):
        return self.__trigger
