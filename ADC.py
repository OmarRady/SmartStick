from spidev import SpiDev


class MCP3008:
    def __init__(self):
        self.spi = SpiDev()

    def get_channels_used(self):
        self.__channels_used = int(input("How many MCP3008 channels are your going to use? :"))  # 1
        self.__channels_used -= 1
    def set_channels_used(self):
        return self.__channels_used

    def get_SPI_bus(self):
        self.__bus = int(input("Please enter SPI bus number:")) # 0
    def set_SPI_bus(self):
        return self.__bus

    def get_SPI_device(self):
        self.__device = int(input("Please enter device/cs number:")) # 0
    def set_SPI_device(self):
        return self.__device

    def get_SPI_channel(self):
        for i in self.set_channels_used():
            self.__channel[i] = int(input("Please enter device/cs number:")) # 0
    def set_SPI_channel(self, i):
        return self.__channel[i]



    def open(self):
        self.spi.open(self.set_SPI_bus(), self.set_SPI_device())

    def read(self):
        for i in self.set_channels_used():
            adc = self.spi.xfer2([1, (8 + self.get_SPI_channel(i)) << 4, 0])
            data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()


# test
if __name__ == "__main__":
    with MCP3008(channel=0) as ch0:
        print
        ch0.read()