#Libraries
import RPi.GPIO as GPIO
import time
import os
import argparse
from os import getcwd ; print(getcwd())
from oauth2client.client import GoogleCredentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


 
def distance():
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
    
def capture():
    def remove_oldimg(self, file_path, img_name):
        file_path = '/home/pi/gcloud/'
        img_name = 'scene_image'
        global path = path + '/' + img_name
        
        os.remove(path + '/' + img_name)
        # check if file exists or not
        if os.path.exists(path + '/' + img_name) is false:
        # file did not exists
            return True
    camera.start_preview()
    sleep(5)
    camera.capture('path')
    camera.stop()
    #camera.stop_preview()
    
def localize_objects(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations
    #file = open('detection_output', "w")
    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        #file.write(str(a))
        print('Normalized bounding polygon vertices: ')
        #file.write(str(b))
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
            #file.write(str(c))
    #file.close()


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
