from time import sleep

from sensors import sensor

class cmera(sensor):

    def inputs(self):
        self.set_name()
        self.set_switch()

    def setup(self):

        camera = PiCamera(resolution=(1280, 720), framerate=30)
        # Set ISO to the desired value
        camera.iso = 100
        # Wait for the automatic gain control to settle
        sleep(2)
        # Now fix the values
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g

    def capture(self):

        def remove_oldimg(self, file_path, img_name):
            file_path = '/home/pi/smartstick/'
            img_name = 'scene_image.jpg'
            os.remove(path + '/' + img_name)
            # check if file exists or not
            if os.path.exists(path + '/' + img_name) is false:
            # file did not exists
                return True

        camera.capture('/home/pi/smartstick/scene_image.jpg')
        camera.stop_preview()
        camera.close()
