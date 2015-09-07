import smbus

address = 0x28
data_fetch = 0x80 | address

class Sensor:
    def __init__(self, i2c_bus):
        self._bus = smbus.SMBus(i2c_bus)
    
    def read(self):
        self._data = self._bus.read_i2c_block_data(address, data_fetch)
        self.rh = float((self._data[0] & 0x3f) * 256 + self._data[1]) / (1 << 14) * 100.
        self.tempC = float(self._data[2] * 64 + (self._data[4] & 0xfc) / 4) / (1 << 14) * 165. - 40.
        self.tempF = self.tempC * 9./5. + 32.
        return self.rh, self.tempF
